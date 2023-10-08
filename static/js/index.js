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

function updateCurrentPage() {
    
}

function switchSettingsPage(index) {
    switch(index) {
        case 0:
            settingsContainer.innerHTML = '<p>Camera Settings</p>';
            break;
        case 1:
            settingsContainer.innerHTML = '<p>Pipeline Settings</p>';
            break;
        case 2:
            settingsContainer.innerHTML = '<p>Settings</p>';
            break;
    }
}

function switchCameraSettingsPage(index) {
    
}

function switchPipelinePage(index) {

}

loadCurrentPage()

switchCamSettings.addEventListener('click', function() {switchSettingsPage(0)});
switchPipeSettings.addEventListener('click', function() {switchSettingsPage(1)});
switchSettings.addEventListener('click', function() {switchSettingsPage(2)});