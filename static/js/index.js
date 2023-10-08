const switchCamSettings = document.getElementById('cameraSettings');
const switchPipeSettings = document.getElementById('pipelineSettings');
const switchSettings = document.getElementById('settings')
const settingsContainer = document.getElementById('settingsContainer');

let pageIndex;

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
            loadPipelineToggles()
            break;
        case 2:
            settingsContainer.innerHTML = '<p>Settings</p>';
            break;
    }
}

function loadPipelineToggles() {
    fetch('pageData.json')
        .then(response => response.json())
        .then(json => {
            setPipelineToggles(json["currentPipelineSettingsPage"]["toggles"])
        })
}
function setPipelineToggles(toggles) {
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
}
function saveChanges(pageData) {

}

switchCamSettings.addEventListener('click', function() {switchSettingsPage(0)});
switchPipeSettings.addEventListener('click', function() {switchSettingsPage(1)});
switchSettings.addEventListener('click', function() {switchSettingsPage(2)});