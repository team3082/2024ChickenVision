const switchCamSettings = document.getElementById('cameraSettings');
const switchPipeSettings = document.getElementById('pipelineSettings');
const switchSettings = document.getElementById('settings')
const settingsContainer = document.getElementById('settingsContainer');

async function loadCurrentPage() {
    let pageDataJSON = await getPageDataJSON()
    let pageIndex = pageDataJSON["currentSettingsPage"]
    switchSettingsPage(pageIndex)
}
async function switchSettingsPage(index) {
    switch(index) {
        case 0: 
            fetch('cameraSettings.json')
                .then(response => response.json())
                .then(json => {
                settingsContainer.innerHTML = json["data"];
            });
            loadCameraSettings()
            break;
        case 1:
            fetch('pipelineSettings.json')
                .then(response => response.json())
                .then(json => {
                settingsContainer.innerHTML = json["data"];
            });
            loadPipelineSettings()
            break;
        case 2:
            settingsContainer.innerHTML = '<p>Settings</p>';
            break;
    }
    let pageDataJSON = await getPageDataJSON();
    if (pageDataJSON["currentSettingsPage"] != index) {
        pageDataJSON["currentSettingsPage"] = index;
        updatePageDataJSON(pageDataJSON)
    }
}

// TO DO
function loadCameraSettings() {

}
function setCameraSettings() {

}
function updateCameraSettings() {

}

// loads the settings for the pipeline given the current camera, and sets the html to the correct values
async function loadPipelineSettings() {
    let pageDataJSON = await getPageDataJSON();
    let settingsJSON = await getSettingsJSON();
    let currentCamera = pageDataJSON["currentCamera"];
    let cam = "cam" + currentCamera.toString();
    setPipelineSettings(settingsJSON[cam]["pipelineSettings"]["toggles"]);
}
function setPipelineSettings(toggles) {
    const apriltag2Toggle = document.getElementById("apriltag2Toggle");
    const apriltag3Toggle = document.getElementById("apriltag3Toggle");
    const gamePieceGeoToggle = document.getElementById("gamePieceGeoToggle");
    const gamePieceMLToggle = document.getElementById("gamePieceMLToggle");
    const retroReflectiveToggle = document.getElementById("gamePieceMLToggle");

    apriltag2Toggle.checked = toggles[0]
    apriltag3Toggle.checked = toggles[1]
    gamePieceGeoToggle.checked = toggles[2]
    gamePieceMLToggle.checked = toggles[3]
    retroReflectiveToggle.checked = toggles[4]

    apriltag2Toggle.addEventListener('click', async function() {await updatePipelineSettings()});
    apriltag3Toggle.addEventListener('click', async function() {await updatePipelineSettings()});
    gamePieceGeoToggle.addEventListener('click', async function() {await updatePipelineSettings()});
    gamePieceMLToggle.addEventListener('click', async function() {await updatePipelineSettings()});
    retroReflectiveToggle.addEventListener('click', async function() {await updatePipelineSettings()});
}
async function updatePipelineSettings() {
    console.log("updating")

    const apriltag2Toggle = document.getElementById("apriltag2Toggle");
    const apriltag3Toggle = document.getElementById("apriltag3Toggle");
    const gamePieceGeoToggle = document.getElementById("gamePieceGeoToggle");
    const gamePieceMLToggle = document.getElementById("gamePieceMLToggle");
    const retroReflectiveToggle = document.getElementById("gamePieceMLToggle");

    let pageDataJSON = await getPageDataJSON()
    let settingsJSON = await getSettingsJSON()

    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][0] = apriltag2Toggle.checked;
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][1] = apriltag3Toggle.checked;
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][2] = gamePieceGeoToggle.checked;
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][3] = gamePieceMLToggle.checked;
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][4] = retroReflectiveToggle.checked;
    
    updateSettingsJSON(settingsJSON);
}

// TO DO
function loadSettings() {

}
function setSettings() {

}
function updateSettings() {

}

async function getPageDataJSON() {
    let response = await fetch('pageData.json')
    let json = await response.json()
    return json
}
async function updatePageDataJSON(pageDataJSON) {
    let response = await fetch('pageData.json', {
        method: "POST", 
        body: JSON.stringify(pageDataJSON), 
        headers: {
        "Content-Type": "application/json"
        }
    })
}

async function getSettingsJSON(settingsJSON) {
    let response = await fetch('settings.json')
    let json = await response.json()
    return json
}
async function updateSettingsJSON(settingsJSON) {
    let response = await fetch('settings.json', {
        method: "POST", 
        body: JSON.stringify(settingsJSON),
        headers: {
            "Content-Type": "application/json"
        }
    })
}

loadCurrentPage()

switchCamSettings.addEventListener('click', function() {switchSettingsPage(0)});
switchPipeSettings.addEventListener('click', function() {switchSettingsPage(1)});
switchSettings.addEventListener('click', function() {switchSettingsPage(2)});