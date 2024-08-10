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
            .then(response => response.json())
            .then(data => {
                let remainingMods = data["remaining_mods"]
                if (remainingMods) {
                    const failDiv = failedDownloadList(remainingMods);
                    const container = modalDoc.getElementById("container");
                    container.insertBefore(failDiv, container.lastChild);
                }
            })
    });
}

function failedDownloadList(failList) {
    const modList = document.createElement("div");
    modList.id = "mod-list";
    failList.forEach(mod => {
        console.log(mod);
        const modName = mod[0]
        const modLink = mod[1]
        const modDiv = document.createElement("div");
        modDiv.className = "failed-mod"
        modDiv.innerHTML = modName + " - <a href=\"" + modLink + "\">" + modLink + "</a>";
    });
    return modList;
}

