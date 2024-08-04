import subprocess


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


def create_instance(name, loader, version, modpack):
    print("New pack name:", name)
    print("New pack loader:", loader)
    print("New pack version:", version)
    print("New pack download url:", modpack)

    new_dir_cmd = f""

    return None
