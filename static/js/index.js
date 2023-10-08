const switchCamSettings = document.getElementById('cameraSettings');
const switchPipeSettings = document.getElementById('pipelineSettings');
const switchSettings = document.getElementById('settings')
const settingsContainer = document.getElementById('settingsContainer');

// Setup upon Loading
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

// Camera Settings
async function loadCameraSettings() {
    let pageDataJSON = await getPageDataJSON()
    let settingsJSON = await getSettingsJSON()
    let currentCamera = pageDataJSON["currentCamera"];
    let cam = "cam" + currentCamera.toString();
    setCameraSettings(settingsJSON[cam]["cameraSettings"]);
}
function setCameraSettings(values) {
    const connectVerbose = document.getElementById("connectVerbose");
    const brightness = document.getElementById("brightness");
    const contrast = document.getElementById("contrast");
    const saturation = document.getElementById("saturation");
    const hue = document.getElementById("hue");
    const gamma = document.getElementById("gamma");
    const sharpness = document.getElementById("sharpness");
    const autoExposure = document.getElementById("autoExposure");

    connectVerbose.value = values["connectVerbose"]
    brightness.value = values["brightness"]
    contrast.value = values["contrast"]
    saturation.value = values["saturation"]
    hue.value = values["hue"]
    gamma.value = values["gamma"]
    sharpness.value = values["sharpness"]
    autoExposure.checked = values["autoExposure"]

    const connectVerboseVal = document.getElementById("connectVerboseVal");
    const brightnessVal = document.getElementById("brightnessVal");
    const contrastVal = document.getElementById("contrastVal");
    const saturationVal = document.getElementById("saturationVal");
    const hueVal = document.getElementById("hueVal");
    const gammaVal = document.getElementById("gammaVal");
    const sharpnessVal = document.getElementById("sharpnessVal");

    connectVerboseVal.innerHTML = connectVerbose.value
    brightnessVal.innerHTML = brightness.value
    contrastVal.innerHTML = contrast.value
    saturationVal.innerHTML = saturation.value
    hueVal.innerHTML = hue.value
    gammaVal.innerHTML = gamma.value
    sharpnessVal.innerHTML = sharpness.value

    connectVerbose.addEventListener('click', async function() {await updateCameraSettings()})
    brightness.addEventListener('click', async function() {await updateCameraSettings()})
    contrast.addEventListener('click', async function() {await updateCameraSettings()})
    saturation.addEventListener('click', async function() {await updateCameraSettings()})
    hue.addEventListener('click', async function() {await updateCameraSettings()})
    gamma.addEventListener('click', async function() {await updateCameraSettings()})
    sharpness.addEventListener('click', async function() {await updateCameraSettings()})
    autoExposure.addEventListener('click', async function() {await updateCameraSettings()})
}
async function updateCameraSettings() {
    const connectVerbose = document.getElementById("connectVerbose");
    const brightness = document.getElementById("brightness");
    const contrast = document.getElementById("contrast");
    const saturation = document.getElementById("saturation");
    const hue = document.getElementById("hue");
    const gamma = document.getElementById("gamma");
    const sharpness = document.getElementById("sharpness");
    const autoExposure = document.getElementById("autoExposure");

    let pageDataJSON = await getPageDataJSON()
    let settingsJSON = await getSettingsJSON()

    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["cameraSettings"]["connectVerbose"] = connectVerbose.value
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["cameraSettings"]["brightness"] = brightness.value
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["cameraSettings"]["contrast"] = contrast.value
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["cameraSettings"]["saturation"] = saturation.value
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["cameraSettings"]["hue"] = hue.value
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["cameraSettings"]["gamma"] = gamma.value
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["cameraSettings"]["sharpness"] = sharpness.value
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["cameraSettings"]["autoExposure"] = autoExposure.checked

    const connectVerboseVal = document.getElementById("connectVerboseVal");
    const brightnessVal = document.getElementById("brightnessVal");
    const contrastVal = document.getElementById("contrastVal");
    const saturationVal = document.getElementById("saturationVal");
    const hueVal = document.getElementById("hueVal");
    const gammaVal = document.getElementById("gammaVal");
    const sharpnessVal = document.getElementById("sharpnessVal");

    connectVerboseVal.innerHTML = connectVerbose.value
    brightnessVal.innerHTML = brightness.value
    contrastVal.innerHTML = contrast.value
    saturationVal.innerHTML = saturation.value
    hueVal.innerHTML = hue.value
    gammaVal.innerHTML = gamma.value
    sharpnessVal.innerHTML = sharpness.value

    updateSettingsJSON(settingsJSON)
}

// Pipeline Settings
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
    const retroReflectiveToggle = document.getElementById("retroReflectiveToggle");

    apriltag2Toggle.checked = toggles[0]
    apriltag3Toggle.checked = toggles[1]
    gamePieceGeoToggle.checked = toggles[2]
    gamePieceMLToggle.checked = toggles[3]
    retroReflectiveToggle.checked = toggles[4]

    const apriltag2DropToggle = document.getElementById("apriltag2DropToggle");
    const apriltag3DropToggle = document.getElementById("apriltag3DropToggle");
    const gamePieceGeoDropToggle = document.getElementById("gamePieceGeoDropToggle");
    const gamePieceMLDropToggle = document.getElementById("gamePieceMLDropToggle");
    const retroReflectiveDropToggle = document.getElementById("retroReflectiveDropToggle");
    
    apriltag2DropToggle.addEventListener('click', async function() {await loadApriltag2Settings()})
    apriltag3DropToggle.addEventListener('click', async function() {await loadApriltag3Settings()})
    gamePieceGeoDropToggle.addEventListener('click', async function() {await loadGamePieceGeoSettings()})
    gamePieceMLDropToggle.addEventListener('click', async function() {await loadGamePieceMLSettings()})
    retroReflectiveDropToggle.addEventListener('click', async function() {await loadRetroReflectiveSettings()})

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
    const retroReflectiveToggle = document.getElementById("retroReflectiveToggle");

    let pageDataJSON = await getPageDataJSON()
    let settingsJSON = await getSettingsJSON()

    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][0] = apriltag2Toggle.checked;
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][1] = apriltag3Toggle.checked;
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][2] = gamePieceGeoToggle.checked;
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][3] = gamePieceMLToggle.checked;
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["toggles"][4] = retroReflectiveToggle.checked;
    
    updateSettingsJSON(settingsJSON);
}

// Apriltag 2D Settings
async function loadApriltag2Settings() {
    const apriltag2Content = document.getElementById("apriltag2Content");

    let data = await fetch("apriltag2Settings.json")
    let dataJSON = await data.json()
    let dataHTML = await dataJSON["data"]

    if (apriltag2Content.innerHTML == "") {
        apriltag2Content.innerHTML = dataHTML;
    }
    else {
        apriltag2Content.innerHTML = "";
    }
}
function setApriltag2Settings(values) {

}
async function updateApriltag2Settings() {

}

// Apriltag 3D Settings
async function loadApriltag3Settings() {
    const apriltag3Content = document.getElementById("apriltag3Content");

    let data = await fetch("apriltag3Settings.json")
    let dataJSON = await data.json()
    let dataHTML = await dataJSON["data"]

    if (apriltag3Content.innerHTML == "") {
        apriltag3Content.innerHTML = dataHTML;
    }
    else {
        apriltag3Content.innerHTML = "";
    }
}
function setApriltag3Settings(values) {

}
async function updateApriltag3Settings() {
    
}

// Game Piece Geometry Settings
async function loadGamePieceGeoSettings() {
    const gamePieceGeoContent = document.getElementById("gamePieceGeoContent");

    let data = await fetch("gamePieceGeoSettings.json")
    let dataJSON = await data.json()
    let dataHTML = await dataJSON["data"]

    if (gamePieceGeoContent.innerHTML == "") {
        gamePieceGeoContent.innerHTML = dataHTML;
    }
    else {
        gamePieceGeoContent.innerHTML = "";
    }
}
function setGamePieceGeoSettings(values) {

}
async function updateGamePieceGeoSettings() {
    
}

// Game Piece Machine Learning Settings
async function loadGamePieceMLSettings() {
    const gamePieceMLContent = document.getElementById("gamePieceMLContent");

    let data = await fetch("gamePieceMLSettings.json")
    let dataJSON = await data.json()
    let dataHTML = await dataJSON["data"]

    if (gamePieceMLContent.innerHTML == "") {
        gamePieceMLContent.innerHTML = dataHTML;
    }
    else {
        gamePieceMLContent.innerHTML = "";
    }
}
function setGamePieceMLSettings(values) {

}
async function updateGamePieceMLSettings() {
    
}

// RetroReflective Settings
async function loadRetroReflectiveSettings() {
    const retroReflectiveContent = document.getElementById("retroReflectiveContent");

    let data = await fetch("retroReflectiveSettings.json")
    let dataJSON = await data.json()
    let dataHTML = await dataJSON["data"]


    if (retroReflectiveContent.innerHTML == "") {
        retroReflectiveContent.innerHTML = dataHTML;
    }
    else {
        retroReflectiveContent.innerHTML = "";
    }
}
function setRetroReflectiveSettings(values) {

}
async function updateRetroReflectiveSettings() {
    
}

// TO DO | General Configuration Settings
function loadSettings() {

}
function setSettings() {

}
function updateSettings() {

}

// get and post requests to flask server
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
async function getSettingsJSON() {
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