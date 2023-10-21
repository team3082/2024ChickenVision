const switchCamSettings = document.getElementById('cameraSettings');
const switchPipeSettings = document.getElementById('pipelineSettings');
const switchSettings = document.getElementById('settings')
const settingsContainer = document.getElementById('settingsContainer');
const currentCameraLabel = document.getElementById("currentCameraLabel")

// Setup upon Loading
async function loadCurrentPage() {
    let pageDataJSON = await getPageDataJSON()
    let pageIndex = pageDataJSON["currentSettingsPage"]
    const currentCameraLabel = document.getElementById("currentCameraLabel");
    currentCameraLabel.innerHTML = "cam" + pageDataJSON["currentCamera"].toString()
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

async function loadCurrentCamera() {
    console.log("loadCurrentCameras")
    const cameraSelectorDropdown = document.getElementById("cameraSelectorDropdown")

    if (cameraSelectorDropdown.innerHTML == "") {
        let pageDataJSON = await getPageDataJSON()
        let dataArray = await pageDataJSON["availableCams"];
        console.log(dataArray)
        let dropdownHTML = "";
        for (let index in dataArray) {
            console.log(dataArray[index])
            let id = "cam" + dataArray[index.toString()];
            let html = '<button id="' + id + '">' + id + '</button>'
            console.log(html)
            dropdownHTML += html;
        }
        console.log(dropdownHTML)
        cameraSelectorDropdown.innerHTML = dropdownHTML;
        console.log(cameraSelectorDropdown.innerHTML)
        setCurrentCamera(dataArray)
    }
    else {
        console.log("yo")
        cameraSelectorDropdown.innerHTML = "";
    }
}
function setCurrentCamera(availableCams) {
    for (let camIndex in availableCams) {
        const cameraHTML = document.getElementById("cam" + availableCams[camIndex].toString());
        cameraHTML.addEventListener('click', async function() {await updateCurrentCamera(availableCams[camIndex])});
    }
}
async function updateCurrentCamera(camIndex) {
    const currentCameraLabel = document.getElementById("currentCameraLabel");
    currentCameraLabel.innerHTML = "cam" + camIndex.toString()
    let pageData = await getPageDataJSON()
    pageData["currentCamera"] = camIndex;
    updatePageDataJSON(pageData);
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
    console.log("loadApriltag2D")
    const apriltag2Content = document.getElementById("apriltag2Content");

    if (apriltag2Content.innerHTML == "") {
        let data = await fetch("apriltag2Settings.json");
        let dataJSON = await data.json();
        let dataHTML = await dataJSON["data"];
        apriltag2Content.innerHTML = await dataHTML;

        let pageDataJSON = await getPageDataJSON();
        let settingsJSON = await getSettingsJSON();
        let currentCamera = pageDataJSON["currentCamera"];
        let cam = "cam" + currentCamera.toString();
        setApriltag2Settings(settingsJSON[cam]["pipelineSettings"]["apriltag2D"]);
    }
    else {
        apriltag2Content.innerHTML = "";
    }   
}
function setApriltag2Settings(values) {
    console.log("setApriltag2D")
    const apriltag2Family = document.getElementById("apriltag2Family");
    const apriltag2Nthreads = document.getElementById("apriltag2Nthreads");
    const apriltag2QuadDecimate = document.getElementById("apriltag2QuadDecimate");
    const apriltag2QuadBlur = document.getElementById("apriltag2QuadBlur");
    const apriltag2RefineEdges = document.getElementById("apriltag2RefineEdges");
    const apriltag2RefineDecode = document.getElementById("apriltag2RefineDecode");
    const apriltag2RefinePose = document.getElementById("apriltag2RefinePose");
    const apriltag2QuadContours = document.getElementById("apriltag2QuadContours");
    const apriltag2DecisionMargin = document.getElementById("apriltag2DecisionMargin");
    
    apriltag2Family.value = values["family"];
    apriltag2Nthreads.value = values["nthreads"];
    apriltag2QuadDecimate.value = values["quadDecimate"] * 10;
    apriltag2QuadBlur.value = values["quadBlur"] * 10;
    apriltag2RefineEdges.checked = values["refineEdges"];
    apriltag2RefineDecode.checked = values["refineDecode"];
    apriltag2RefinePose.checked = values["refinePose"];
    apriltag2QuadContours.checked = values["quadContours"];
    apriltag2DecisionMargin.value = values["decisionMargin"];

    const apriltag2FamilyVal = document.getElementById("apriltag2FamilyVal");
    const apriltag2NthreadsVal = document.getElementById("apriltag2NthreadsVal");
    const apriltag2QuadDecimateVal = document.getElementById("apriltag2QuadDecimateVal");
    const apriltag2QuadBlurVal = document.getElementById("apriltag2QuadBlurVal");
    const apriltag2DecisionMarginVal = document.getElementById("apriltag2DecisionMarginVal");
    
    apriltag2FamilyVal.innerHTML = apriltag2Family.value;
    apriltag2NthreadsVal.innerHTML = apriltag2Nthreads.value;
    apriltag2QuadDecimateVal.innerHTML = apriltag2QuadDecimate.value / 10;
    apriltag2QuadBlurVal.innerHTML = apriltag2QuadBlur.value / 10;
    apriltag2DecisionMarginVal.innerHTML = apriltag2DecisionMargin.value;  

    apriltag2Family.addEventListener('click', async function() {await updateApriltag2Settings()});
    apriltag2Nthreads.addEventListener('click', async function() {await updateApriltag2Settings()});
    apriltag2QuadDecimate.addEventListener('click', async function() {await updateApriltag2Settings()});
    apriltag2QuadBlur.addEventListener('click', async function() {await updateApriltag2Settings()});
    apriltag2RefineEdges.addEventListener('click', async function() {await updateApriltag2Settings()});
    apriltag2RefineDecode.addEventListener('click', async function() {await updateApriltag2Settings()});
    apriltag2RefinePose.addEventListener('click', async function() {await updateApriltag2Settings()});
    apriltag2QuadContours.addEventListener('click', async function() {await updateApriltag2Settings()});
    apriltag2DecisionMargin.addEventListener('click', async function() {await updateApriltag2Settings()});
}
async function updateApriltag2Settings() {
    console.log("updateApriltag2D")
    const apriltag2Family = document.getElementById("apriltag2Family");
    const apriltag2Nthreads = document.getElementById("apriltag2Nthreads");
    const apriltag2QuadDecimate = document.getElementById("apriltag2QuadDecimate");
    const apriltag2QuadBlur = document.getElementById("apriltag2QuadBlur");
    const apriltag2RefineEdges = document.getElementById("apriltag2RefineEdges");
    const apriltag2RefineDecode = document.getElementById("apriltag2RefineDecode");
    const apriltag2RefinePose = document.getElementById("apriltag2RefinePose");
    const apriltag2QuadContours = document.getElementById("apriltag2QuadContours");
    const apriltag2DecisionMargin = document.getElementById("apriltag2DecisionMargin");

    let pageDataJSON = await getPageDataJSON();
    let settingsJSON = await getSettingsJSON();
    let apriltag2Settings = settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["apriltag2D"];

    apriltag2Settings["family"] = apriltag2Family.value;
    apriltag2Settings["nthreads"] = apriltag2Nthreads.value;
    apriltag2Settings["quadDecimate"] = apriltag2QuadDecimate.value / 10;
    apriltag2Settings["quadBlur"] = apriltag2QuadBlur.value / 10;
    apriltag2Settings["refineEdges"] = apriltag2RefineEdges.checked;
    apriltag2Settings["refineDecode"] = apriltag2RefineDecode.checked;
    apriltag2Settings["refinePose"] = apriltag2RefinePose.checked;
    apriltag2Settings["quadContours"] = apriltag2QuadContours.checked;
    apriltag2Settings["decisionMargin"] = apriltag2DecisionMargin.value;

    const apriltag2FamilyVal = document.getElementById("apriltag2FamilyVal");
    const apriltag2NthreadsVal = document.getElementById("apriltag2NthreadsVal");
    const apriltag2QuadDecimateVal = document.getElementById("apriltag2QuadDecimateVal");
    const apriltag2QuadBlurVal = document.getElementById("apriltag2QuadBlurVal");
    const apriltag2DecisionMarginVal = document.getElementById("apriltag2DecisionMarginVal");
    
    apriltag2FamilyVal.innerHTML = apriltag2Family.value;
    apriltag2NthreadsVal.innerHTML = apriltag2Nthreads.value;
    apriltag2QuadDecimateVal.innerHTML = apriltag2QuadDecimate.value / 10;
    apriltag2QuadBlurVal.innerHTML = apriltag2QuadBlur.value / 10;
    apriltag2DecisionMarginVal.innerHTML = apriltag2DecisionMargin.value;    

    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["apriltag2D"] = apriltag2Settings;
    updateSettingsJSON(settingsJSON);
}

// Apriltag 3D Settings
async function loadApriltag3Settings() {
    const apriltag3Content = document.getElementById("apriltag3Content");

    if (apriltag3Content.innerHTML == "") {
        let data = await fetch("apriltag3Settings.json")
        let dataJSON = await data.json();
        let dataHTML = await dataJSON["data"];
        apriltag3Content.innerHTML = dataHTML;

        let pageDataJSON = await getPageDataJSON();
        let settingsJSON = await getSettingsJSON();
        let currentCamera = pageDataJSON["currentCamera"];
        let cam = "cam" + currentCamera.toString();
        setApriltag3Settings(settingsJSON[cam]["pipelineSettings"]["apriltag3D"]);
    }
    else {
        apriltag3Content.innerHTML = "";
    }
}
function setApriltag3Settings(values) {
    console.log("setApriltag3D")
    const apriltag3Family = document.getElementById("apriltag3Family");
    const apriltag3Nthreads = document.getElementById("apriltag3Nthreads");
    const apriltag3QuadDecimate = document.getElementById("apriltag3QuadDecimate");
    const apriltag3QuadBlur = document.getElementById("apriltag3QuadBlur");
    const apriltag3RefineEdges = document.getElementById("apriltag3RefineEdges");
    const apriltag3RefineDecode = document.getElementById("apriltag3RefineDecode");
    const apriltag3RefinePose = document.getElementById("apriltag3RefinePose");
    const apriltag3QuadContours = document.getElementById("apriltag3QuadContours");
    const apriltag3DecisionMargin = document.getElementById("apriltag3DecisionMargin");
    const apriltag3Fov = document.getElementById("apriltag3Fov");
    
    apriltag3Family.value = values["family"];
    apriltag3Nthreads.value = values["nthreads"];
    apriltag3QuadDecimate.value = values["quadDecimate"] * 10;
    apriltag3QuadBlur.value = values["quadBlur"] * 10;
    apriltag3RefineEdges.checked = values["refineEdges"];
    apriltag3RefineDecode.checked = values["refineDecode"];
    apriltag3RefinePose.checked = values["refinePose"];
    apriltag3QuadContours.checked = values["quadContours"];
    apriltag3DecisionMargin.value = values["decisionMargin"];
    apriltag3Fov.value = values["fov"];

    const apriltag3FamilyVal = document.getElementById("apriltag3FamilyVal");
    const apriltag3NthreadsVal = document.getElementById("apriltag3NthreadsVal");
    const apriltag3QuadDecimateVal = document.getElementById("apriltag3QuadDecimateVal");
    const apriltag3QuadBlurVal = document.getElementById("apriltag3QuadBlurVal");
    const apriltag3DecisionMarginVal = document.getElementById("apriltag3DecisionMarginVal");
    const apriltag3FovVal = document.getElementById("apriltag3FovVal");
    
    apriltag3FamilyVal.innerHTML = apriltag3Family.value;
    apriltag3NthreadsVal.innerHTML = apriltag3Nthreads.value;
    apriltag3QuadDecimateVal.innerHTML = apriltag3QuadDecimate.value / 10;
    apriltag3QuadBlurVal.innerHTML = apriltag3QuadBlur.value / 10;
    apriltag3DecisionMarginVal.innerHTML = apriltag3DecisionMargin.value;  
    apriltag3FovVal.innerHTML = apriltag3Fov.value;

    apriltag3Family.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3Nthreads.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3QuadDecimate.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3QuadBlur.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3RefineEdges.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3RefineDecode.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3RefinePose.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3QuadContours.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3DecisionMargin.addEventListener('click', async function() {await updateApriltag3Settings()});
    apriltag3Fov.addEventListener('click', async function() {await updateApriltag3Settings()});
}
async function updateApriltag3Settings() {
    console.log("updateApriltag3D")
    const apriltag3Family = document.getElementById("apriltag3Family");
    const apriltag3Nthreads = document.getElementById("apriltag3Nthreads");
    const apriltag3QuadDecimate = document.getElementById("apriltag3QuadDecimate");
    const apriltag3QuadBlur = document.getElementById("apriltag3QuadBlur");
    const apriltag3RefineEdges = document.getElementById("apriltag3RefineEdges");
    const apriltag3RefineDecode = document.getElementById("apriltag3RefineDecode");
    const apriltag3RefinePose = document.getElementById("apriltag3RefinePose");
    const apriltag3QuadContours = document.getElementById("apriltag3QuadContours");
    const apriltag3DecisionMargin = document.getElementById("apriltag3DecisionMargin");
    const apriltag3Fov = document.getElementById("apriltag3Fov");

    let pageDataJSON = await getPageDataJSON();
    let settingsJSON = await getSettingsJSON();
    let apriltag3Settings = settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["apriltag3D"];

    apriltag3Settings["family"] = apriltag3Family.value;
    apriltag3Settings["nthreads"] = apriltag3Nthreads.value;
    apriltag3Settings["quadDecimate"] = apriltag3QuadDecimate.value / 10;
    apriltag3Settings["quadBlur"] = apriltag3QuadBlur.value / 10;
    apriltag3Settings["refineEdges"] = apriltag3RefineEdges.checked;
    apriltag3Settings["refineDecode"] = apriltag3RefineDecode.checked;
    apriltag3Settings["refinePose"] = apriltag3RefinePose.checked;
    apriltag3Settings["quadContours"] = apriltag3QuadContours.checked;
    apriltag3Settings["decisionMargin"] = apriltag3DecisionMargin.value;
    apriltag3Settings["fov"] = apriltag3Fov.value;

    const apriltag3FamilyVal = document.getElementById("apriltag3FamilyVal");
    const apriltag3NthreadsVal = document.getElementById("apriltag3NthreadsVal");
    const apriltag3QuadDecimateVal = document.getElementById("apriltag3QuadDecimateVal");
    const apriltag3QuadBlurVal = document.getElementById("apriltag3QuadBlurVal");
    const apriltag3DecisionMarginVal = document.getElementById("apriltag3DecisionMarginVal");
    const apriltag3FovVal = document.getElementById("apriltag3FovVal");
    
    apriltag3FamilyVal.innerHTML = apriltag3Family.value;
    apriltag3NthreadsVal.innerHTML = apriltag3Nthreads.value;
    apriltag3QuadDecimateVal.innerHTML = apriltag3QuadDecimate.value / 10;
    apriltag3QuadBlurVal.innerHTML = apriltag3QuadBlur.value / 10;
    apriltag3DecisionMarginVal.innerHTML = apriltag3DecisionMargin.value;  
    apriltag3FovVal.innerHTML = apriltag3Fov.value;

    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["apriltag3D"] = apriltag3Settings;
    updateSettingsJSON(settingsJSON);
}

// Game Piece Geometry Settings
async function loadGamePieceGeoSettings() {
    const gamePieceGeoContent = document.getElementById("gamePieceGeoContent");

    if (gamePieceGeoContent.innerHTML == "") {
        let data = await fetch("gamePieceGeoSettings.json")
        let dataJSON = await data.json();
        let dataHTML = await dataJSON["data"];
        gamePieceGeoContent.innerHTML = dataHTML;

        let pageDataJSON = await getPageDataJSON();
        let settingsJSON = await getSettingsJSON();
        let currentCamera = pageDataJSON["currentCamera"];
        let cam = "cam" + currentCamera.toString();
        setGamePieceGeoSettings(settingsJSON[cam]["pipelineSettings"]["gamePieceGeo"]);
    }
    else {
        gamePieceGeoContent.innerHTML = "";
    }
}
function setGamePieceGeoSettings(values) {
    console.log("setGamePieceGeometry")
    const lowerPurpleH = document.getElementById("lowerPurpleH");
    const lowerPurpleS = document.getElementById("lowerPurpleS");
    const lowerPurpleV = document.getElementById("lowerPurpleV");
    const upperPurpleH = document.getElementById("upperPurpleH");
    const upperPurpleS = document.getElementById("upperPurpleS");
    const upperPurpleV = document.getElementById("upperPurpleV");
    const arbituaryValueCube = document.getElementById("arbituaryValueCube");
    const lowerYellowH = document.getElementById("lowerYellowH");
    const lowerYellowS = document.getElementById("lowerYellowS");
    const lowerYellowV = document.getElementById("lowerYellowV");
    const upperYellowH = document.getElementById("upperYellowH");
    const upperYellowS = document.getElementById("upperYellowS");
    const upperYellowV = document.getElementById("upperYellowV");
    const arbituaryValueCone = document.getElementById("arbituaryValueCone");

    lowerPurpleH.value = values["lowerPurple"][0];
    lowerPurpleS.value = values["lowerPurple"][1];
    lowerPurpleV.value = values["lowerPurple"][2];
    upperPurpleH.value = values["upperPurple"][0];
    upperPurpleS.value = values["upperPurple"][1];
    upperPurpleV.value = values["upperPurple"][2];
    arbituaryValueCube.value = values["arbituaryValueCube"];
    lowerYellowH.value = values["lowerYellow"][0];
    lowerYellowS.value = values["lowerYellow"][1];
    lowerYellowV.value = values["lowerYellow"][2];
    upperYellowH.value = values["upperYellow"][0];
    upperYellowS.value = values["upperYellow"][1];
    upperYellowV.value = values["upperYellow"][2];
    arbituaryValueCone.value = values["arbituaryValueCone"];

    const lowerPurpleHVal = document.getElementById("lowerPurpleHVal");
    const lowerPurpleSVal = document.getElementById("lowerPurpleSVal");
    const lowerPurpleVVal = document.getElementById("lowerPurpleVVal");
    const upperPurpleHVal = document.getElementById("upperPurpleHVal");
    const upperPurpleSVal = document.getElementById("upperPurpleSVal");
    const upperPurpleVVal = document.getElementById("upperPurpleVVal");
    const arbituaryValueCubeVal = document.getElementById("arbituaryValueCubeVal");
    const lowerYellowHVal = document.getElementById("lowerYellowHVal");
    const lowerYellowSVal = document.getElementById("lowerYellowSVal");
    const lowerYellowVVal = document.getElementById("lowerYellowVVal");
    const upperYellowHVal = document.getElementById("upperYellowHVal");
    const upperYellowSVal = document.getElementById("upperYellowSVal");
    const upperYellowVVal = document.getElementById("upperYellowVVal");
    const arbituaryValueConeVal = document.getElementById("arbituaryValueConeVal");

    lowerPurpleHVal.innerHTML = lowerPurpleH.value;
    lowerPurpleSVal.innerHTML = lowerPurpleS.value;
    lowerPurpleVVal.innerHTML = lowerPurpleV.value;
    upperPurpleHVal.innerHTML = upperPurpleH.value;
    upperPurpleSVal.innerHTML = upperPurpleS.value;
    upperPurpleVVal.innerHTML = upperPurpleV.value;
    arbituaryValueCubeVal.innerHTML = arbituaryValueCube.value / 100;
    lowerYellowHVal.innerHTML = lowerYellowH.value;
    lowerYellowSVal.innerHTML = lowerYellowS.value;
    lowerYellowVVal.innerHTML = lowerYellowV.value;
    upperYellowHVal.innerHTML = upperYellowH.value;
    upperYellowSVal.innerHTML = upperYellowS.value;
    upperYellowVVal.innerHTML = upperYellowV.value;
    arbituaryValueConeVal.innerHTML = arbituaryValueCone.value / 100;

    lowerPurpleH.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    lowerPurpleS.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    lowerPurpleV.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    upperPurpleH.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    upperPurpleS.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    upperPurpleV.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    arbituaryValueCube.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    lowerYellowH.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    lowerYellowS.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    lowerYellowV.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    upperYellowH.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    upperYellowS.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    upperYellowV.addEventListener('click', async function() {await updateGamePieceGeoSettings()});
    arbituaryValueCone.addEventListener('click', async function() {await updateGamePieceGeoSettings()});

}
async function updateGamePieceGeoSettings() {
    console.log("updateGamePieceGeometry")
    const lowerPurpleH = document.getElementById("lowerPurpleH");
    const lowerPurpleS = document.getElementById("lowerPurpleS");
    const lowerPurpleV = document.getElementById("lowerPurpleV");
    const upperPurpleH = document.getElementById("upperPurpleH");
    const upperPurpleS = document.getElementById("upperPurpleS");
    const upperPurpleV = document.getElementById("upperPurpleV");
    const arbituaryValueCube = document.getElementById("arbituaryValueCube");
    const lowerYellowH = document.getElementById("lowerYellowH");
    const lowerYellowS = document.getElementById("lowerYellowS");
    const lowerYellowV = document.getElementById("lowerYellowV");
    const upperYellowH = document.getElementById("upperYellowH");
    const upperYellowS = document.getElementById("upperYellowS");
    const upperYellowV = document.getElementById("upperYellowV");
    const arbituaryValueCone = document.getElementById("arbituaryValueCone");

    let pageDataJSON = await getPageDataJSON();
    let settingsJSON = await getSettingsJSON();
    let gamePieceGeoSettings = settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["gamePieceGeo"];

    let lowerPurple = [lowerPurpleH.value, lowerPurpleS.value, lowerPurpleV.value];
    let upperPurple = [upperPurpleH.value, upperPurpleS.value, upperPurpleV.value];
    let lowerYellow = [lowerYellowH.value, lowerYellowS.value, lowerYellowV.value];
    let upperYellow = [upperYellowH.value, upperYellowS.value, upperYellowV.value];

    gamePieceGeoSettings["lowerPurple"] = lowerPurple;
    gamePieceGeoSettings["upperPurple"] = upperPurple;
    gamePieceGeoSettings["arbituaryValueCube"] = arbituaryValueCube.value;
    gamePieceGeoSettings["lowerYellow"] = lowerYellow;
    gamePieceGeoSettings["upperYellow"] = upperYellow;
    gamePieceGeoSettings["arbituaryValueCone"] = arbituaryValueCone.value;

    const lowerPurpleHVal = document.getElementById("lowerPurpleHVal");
    const lowerPurpleSVal = document.getElementById("lowerPurpleSVal");
    const lowerPurpleVVal = document.getElementById("lowerPurpleVVal");
    const upperPurpleHVal = document.getElementById("upperPurpleHVal");
    const upperPurpleSVal = document.getElementById("upperPurpleSVal");
    const upperPurpleVVal = document.getElementById("upperPurpleVVal");
    const arbituaryValueCubeVal = document.getElementById("arbituaryValueCubeVal");
    const lowerYellowHVal = document.getElementById("lowerYellowHVal");
    const lowerYellowSVal = document.getElementById("lowerYellowSVal");
    const lowerYellowVVal = document.getElementById("lowerYellowVVal");
    const upperYellowHVal = document.getElementById("upperYellowHVal");
    const upperYellowSVal = document.getElementById("upperYellowSVal");
    const upperYellowVVal = document.getElementById("upperYellowVVal");
    const arbituaryValueConeVal = document.getElementById("arbituaryValueConeVal");

    lowerPurpleHVal.innerHTML = lowerPurpleH.value;
    lowerPurpleSVal.innerHTML = lowerPurpleS.value;
    lowerPurpleVVal.innerHTML = lowerPurpleV.value;
    upperPurpleHVal.innerHTML = upperPurpleH.value;
    upperPurpleSVal.innerHTML = upperPurpleS.value;
    upperPurpleVVal.innerHTML = upperPurpleV.value;
    arbituaryValueCubeVal.innerHTML = arbituaryValueCube.value / 100;
    lowerYellowHVal.innerHTML = lowerYellowH.value;
    lowerYellowSVal.innerHTML = lowerYellowS.value;
    lowerYellowVVal.innerHTML = lowerYellowV.value;
    upperYellowHVal.innerHTML = upperYellowH.value;
    upperYellowSVal.innerHTML = upperYellowS.value;
    upperYellowVVal.innerHTML = upperYellowV.value;
    arbituaryValueConeVal.innerHTML = arbituaryValueCone.value / 100;
    
    settingsJSON["cam" + pageDataJSON["currentCamera"].toString()]["pipelineSettings"]["gamePieceGeo"] = gamePieceGeoSettings;
    updateSettingsJSON(settingsJSON);
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

currentCameraLabel.addEventListener('click', async function() {await loadCurrentCamera()})
switchCamSettings.addEventListener('click', function() {switchSettingsPage(0)});
switchPipeSettings.addEventListener('click', function() {switchSettingsPage(1)});
switchSettings.addEventListener('click', function() {switchSettingsPage(2)});