import json
import os
import subprocess
from dotenv import load_dotenv

import httpx

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_instances():
    command = "for DIR in $(find /home/*/Instances -mindepth 1 -maxdepth 1 -type d); do echo $(basename $DIR); done"
    instances = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip().split("\n")
    return instances


def get_live_instances():
    command = "ls -laR /var/run/screen | grep MC-"
    live_server_processes = subprocess.run(command, shell=True, capture_output=True, text=True).stdout
    filtered_split_processes = list(filter(None, live_server_processes.split("\n")))
    screens = [p[p.index("MC-")+3:len(p)] for p in filtered_split_processes]
    live_servers = []
    for s in screens:
        instance_details = s.split(":")
        instance_name = instance_details[0]
        instance_port = instance_details[1]
        live_servers.append((instance_name, instance_port))
    return live_servers


def start_instance(instance):
    location_command = f"find /home/*/Instances -type d -name {instance}"
    location = subprocess.run(location_command, shell=True, capture_output=True, text=True).stdout.split("\n")[0]
    launch_command = f"{location}/run.sh"
    result = subprocess.run(launch_command, shell=True, capture_output=True, text=True)
    exit_code = result.returncode
    port = int(result.stdout)
    return {"status": "on" if exit_code == 0 else "off", "port": port}


def stop_instance(instance):
    stop_command = f'screen -S MC-{instance} -p 0 -X stuff "stop^m"'
    kill_screen_command = f"screen -XS MC-{instance} quit"
    stop_instance_command = stop_command + " && sleep 4 && " + kill_screen_command
    result = subprocess.run(stop_instance_command, shell=True, capture_output=True, text=True)
    return {"status": "off"}


def get_loaders():
    return {
        "fabric": [
            "1.21",
            "1.20.6",
            "1.20.5",
            "1.20.4",
            "1.20.3",
            "1.20.2",
            "1.20.1",
            "1.20",
            "1.18.2",
            "1.16.5",
            "1.12.2",
            "1.7.10"
        ],
        "forge": [
            "1.21",
            "1.20.2",
            "1.20.1"
        ],
        "neo": [
            "1.21",
            "1.20.6",
            "1.20.5",
            "1.20.4",
            "1.20.3",
            "1.20.2",
            "1.20.1",
            "1.20",
            "1.12.2"
        ]
    }


def create_instance(name, loader, version, modpack_id):
    class CustomAuth(httpx.Auth):
        def __init__(self, token):
            self.token = token

        def auth_flow(self, request: httpx.Request):
            request.headers['x-api-key'] = self.token
            yield request

    def download_main_file(pack_id):
        client = httpx.Client(auth=auth)

        response = client.get(base_url + f"/v1/mods/{pack_id}").json()
        pack_latest_release_id = response["data"]["mainFileId"]
        pack_latest_release_url = client.get(base_url + f"/v1/mods/{pack_id}/files/{pack_latest_release_id}/download-url").json()["data"]
        download_cmd = f"mkdir ~/.temp && cd ~/.temp && wget --header=x-api-key: {auth.token} {pack_latest_release_url}"
        subprocess.run(download_cmd, shell=True)
        subprocess.run("cd ~/.temp && unzip *.zip && rm *.zip", shell=True)

    def get_mods_from_manifest():
        f_manifest_path = os.path.expanduser("~/.temp/manifest.json")
        with open(f_manifest_path, 'r') as f_manifest:
            manifest = json.load(f_manifest)
        mods = []
        for file in manifest["files"]:
            mods.append((file["projectID"], file["fileID"]))
        return mods

    def download_mods(mods):
        client = httpx.Client(auth=auth)
        fails = []
        for (mod_project_id, mod_file_id) in mods:
            mod_dl_link_get = client.get(base_url + f"/v1/mods/{mod_project_id}/files/{mod_file_id}/download-url")
            if mod_dl_link_get.status_code != 200:
                fail = client.get(base_url + f"/v1/mods/{mod_project_id}").json()["data"]
                mod_name = fail["name"]
                mod_link = fail["links"]["websiteUrl"]
                print(f"Failed to download: {mod_name} - {mod_link}")
                fails.append((mod_name, mod_link))

        return fails

    print("New pack name:", name)
    print("New pack loader:", loader)
    print("New pack version:", version)
    print("New pack ID:", modpack_id)

    # API access
    base_url = "https://api.curseforge.com"
    auth = CustomAuth(API_KEY)

    download_main_file(modpack_id)
    mod_ids = get_mods_from_manifest()
    failed_downloads = download_mods(mod_ids)
    return failed_downloads
