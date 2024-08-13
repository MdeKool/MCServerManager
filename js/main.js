$(".instances").on("click", ".instance-btn", async event => {
    const action = event.target.classList[1];
    const instanceDiv = event.target.closest(".instance");
    const instanceName = $(instanceDiv).find(".instance-name");
    let instance = instanceName.text().replace(/ .*/, '')

    if ($(event.target).hasClass("instance-btn on") && instanceDiv.getAttribute("data-port")) {
        alert("Server is already on");
        return;
    }

    fetch("/servers/"+action,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                instance: instance
            })
        })
        .then(async response => await response.json())
        .then(data => {
            let instanceStatus = data["status"]
            switch (instanceStatus) {
                case "on":
                    instanceDiv.setAttribute("data-port", data["port"]);
                    $(instanceDiv).find(".status").text("Online");
                    instanceName.text(instance + " - port: " + data["port"]);
                    break;
                case "off":
                    // instanceDiv.setAttribute("data-port", "")
                    instanceDiv.setAttribute("data-port", "");
                    $(instanceDiv).find(".status").text("Offline");
                    instanceName.text(instance.replace(/:.*/, ''));
                    break;
                default:
                    alert("Something went wrong!")
            }
        });
});


$("#show-popup-btn").click(event => {
    showNewInstanceModal();
});

function showNewInstanceModal() {
    let blur = blurBackground();
    fetch("/modals/new_instance",
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(dict => {
            const modalDoc = parseModalText(dict["modal"]);
            const modal = modalDoc.getElementById("container");
            const loaderSelect = modalDoc.getElementById("modloader");
            const loaders = dict["loaders"];

            addLoaders(loaderSelect, loaders);

            const versionSelect = modalDoc.getElementById("version");
            const defaultLoader = loaders["fabric"];
            addLoaderVersions(loaderSelect, versionSelect, defaultLoader);

            addClickCloseListener(blur, modal);
            addButtonListeners(modalDoc, blur);
            addLoaderChangeListener(loaderSelect, versionSelect, loaders);

            blur.appendChild(modal);
        });
}

function blurBackground() {
    const blur = document.createElement("div");
    blur.id = "blur";
    blur.className = "blur";
    document.body.appendChild(blur);
    blur.offsetHeight;
    blur.classList.add("visible");

    return blur;
}

function parseModalText(htmlText) {
    const parser = new DOMParser();
    return parser.parseFromString(htmlText, "text/html");
}

function addClickCloseListener(blur, ignore=undefined) {
    blur.addEventListener("click", event => {
        if (ignore.contains(event.target)) {
            return;
        }
        blur.classList.remove("visible");
        blur.addEventListener("transitionend", () => blur.remove());
    });
}

function addLoaders(loaderSelect, loaders) {
    const loaderNames = {
        "fabric": "Fabric",
        "forge": "Forge",
        "neo": "NeoForged"
    }
    Object.keys(loaders).forEach(loader => {
        loaderSelect.add(new Option(loaderNames[loader], loader));
    })
}

function addLoaderVersions(loaderSelect, versionSelect, loader) {
    loader.forEach(version => {
        let opt = new Option(version, version);
        versionSelect.add(opt);
    })
}

function addLoaderChangeListener(loaderSelect, versionSelect, loaders) {
    loaderSelect.addEventListener("change", event => {
        let loader = loaders[event.target.value];
        versionSelect.innerHTML = null;

        addLoaderVersions(loaderSelect, versionSelect, loader);
    })
}

function addButtonListeners(modalDoc, blur) {
    const cancelBtn = modalDoc.getElementById("new-instance-cancel");
    cancelBtn.addEventListener("click", () => {
        blur.classList.remove("visible");
        blur.addEventListener("transitionend", () => blur.remove());
    });

    const createBtn = modalDoc.getElementById("new-instance-create");
    createBtn.addEventListener("click", () => {
        const instanceName = document.getElementById("instance-name").value;
        const modpackId = document.getElementById("modpack-id").value;
        const modloader = document.getElementById("modloader").value;
        const version = document.getElementById("version").value;

        const container = document.getElementById("container");
        const btns = document.getElementsByClassName("new-instance-btns")[0];
        const loader = createLoader();
        container.insertBefore(loader, btns);

        fetch("/servers/new",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: instanceName,
                    loader: modloader,
                    version: version,
                    modpack_id: modpackId
                })
            })
            .then(response => {
                loader.remove();
                return response.json();
            })
            .then(data => {
                let remainingMods = data["remaining_mods"]
                if (remainingMods) {
                    const failDiv = failedDownloadList(remainingMods);
                    const upload = uploadBox();
                    container.insertBefore(failDiv, btns);
                    container.insertBefore(upload, btns);
                }
            })
    });
}

function failedDownloadList(failList) {
    let modList;
    if (modList = document.getElementById("mod-list")) {  // If mod-list already exists use it, otherwise create new div.
        modList.innerHTML = '';
    } else {
        modList = document.createElement("div");
        modList.id = "mod-list";
    }
    modList.innerHTML = "Missing mods<br>";
    failList.forEach(mod => {
        const modName = mod[0]
        const modLink = mod[1]
        const modDiv = document.createElement("div");
        modDiv.className = "failed-mod"
        modDiv.innerHTML = modName + " - <a href=\"" + modLink + "\" target='_blank'>Link</a>";
        modList.appendChild(modDiv);
    });
    return modList;
}

function uploadBox() {
    const uploadDiv = document.createElement("div");
    uploadDiv.id = "file-upload-div";
    uploadDiv.innerHTML = "<p>Please upload a <span style='font-family: \"JetBrains Mono\", monospace'>missing.zip</span> with the missing mods</p>";
    const uploadForm = document.createElement("form");
    const uploadInput = document.createElement("input");
    uploadInput.type = "file";
    uploadInput.id = "file-upload"
    uploadInput.accept = ".zip"
    uploadForm.appendChild(uploadInput);
    uploadDiv.appendChild(uploadForm);
    uploadInput.addEventListener("change", event => {
        const file = new FormData();
        file.append('file', uploadInput.files[0])
        uploadFile(new FormData(uploadForm));
    });
    return uploadDiv;
}

function uploadFile(file) {
    for (const pair of file.entries()) {
        console.log(`${pair[0]}: ${pair[1]}`);
    }
    fetch("/upload/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/zip"
            },
            body: file,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => console.log("Uploaded form successfully"))
        .catch(error => {
            console.error(`Error: ${error}`);
        });
}

function createLoader() {
    const loader = document.createElement("div");
    loader.className = "loader";
    return loader;
}
