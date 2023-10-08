const switchCamSettings = document.getElementById('cameraSettings');
const switchPipeSettings = document.getElementById('pipelineSettings');
const switchSettings = document.getElementById('settings')
const settingsContainer = document.getElementById('settingsContainer');

function loadCurrentPage() {
    fetch('pageData.json')
        .then(response => response.json())
        .then(json => {
            switchSettingsPage(json["currentSettingsPage"])
        })  
}
function switchSettingsPage(index) {
    switch(index) {
        case 0: 
            settingsContainer.innerHTML = '<p>Camera Settings</p>';
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
}

// TO DO
function loadCameraSettings() {

}
function setCameraSettings() {

}
function updateCameraSettings() {

}

// loads the settings for the pipeline given the current camera, and sets the html to the correct values
function loadPipelineSettings() {
    fetch('pageData.json')
        .then(response => response.json())
        .then(json => {
            let currentCamera = json["currentCamera"];
            fetch('settings.json')
                .then(response => response.json())
                .then(json => {
                    let camera = "cam" + currentCamera.toString()
                    setPipelineSettings(json[camera]["pipelineSettings"]["toggles"]);
                })
        })
}
function setPipelineSettings(toggles) {
    console.log(toggles)
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

    apriltag2Toggle.addEventListener('click', function() {updatePipelineSettings()});
    apriltag3Toggle.addEventListener('click', function() {updatePipelineSettings()});
    gamePieceGeoToggle.addEventListener('click', function() {updatePipelineSettings()});
    gamePieceMLToggle.addEventListener('click', function() {updatePipelineSettings()});
    retroReflectiveToggle.addEventListener('click', function() {updatePipelineSettings()});
}
// TO DO
function updatePipelineSettings() {
    // checking toggles
    const apriltag2Toggle = document.getElementById("apriltag2Toggle");
    const apriltag3Toggle = document.getElementById("apriltag3Toggle");
    const gamePieceGeoToggle = document.getElementById("gamePieceGeoToggle");
    const gamePieceMLToggle = document.getElementById("gamePieceMLToggle");
    const retroReflectiveToggle = document.getElementById("gamePieceMLToggle");

    settingsJSON = getSettingsJSON()

    settingsJSON

}

// TO DO
function loadSettings() {

}
function setSettings() {

}
function updateSettings() {

}

function getPageDataJSON() {

}
function updatePageDataJSON() {
    
}

function getSettingsJSON() {
    fetch('settings.json')
        .then(response => response.json())
        .then(json => { return json })
}
function updateSettingsJSON() {

}

loadCurrentPage()

switchCamSettings.addEventListener('click', function() {switchSettingsPage(0)});
switchPipeSettings.addEventListener('click', function() {switchSettingsPage(1)});
switchSettings.addEventListener('click', function() {switchSettingsPage(2)});