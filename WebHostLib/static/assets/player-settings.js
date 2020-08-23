window.addEventListener('load', () => {
    const gameSettings = document.getElementById('game-settings');
    new Promise((resolve, reject) => {
        const ajax = new XMLHttpRequest();
        ajax.onreadystatechange = () => {
            if (ajax.readyState !== 4) { return; }
            if (ajax.status !== 200) {
                reject("Unable to fetch source yaml file.");
                return;
            }
            resolve(ajax.responseText);
        };
        ajax.open('GET', `${window.location.origin}/static/static/playerSettings.yaml` ,true);
        ajax.send();
    }).then((results) => {
        // Load YAML into object
        const sourceData = jsyaml.load(results);

        // Update localStorage with three settings objects. Preserve original objects if present.
        for (let i=1; i<=3; i++) {
            const localSettings = JSON.parse(localStorage.getItem(`gameSettings${i}`));
            const updatedObj = localSettings ? Object.assign(sourceData, localSettings) : sourceData;
            localStorage.setItem(`gameSettings${i}`, JSON.stringify(updatedObj));
        }

        populateSettings();
        document.getElementById('preset-number').addEventListener('change', populateSettings);
        gameSettings.addEventListener('change', handleOptionChange);
        gameSettings.addEventListener('keyup', handleOptionChange);
    }).catch((error) => {
        gameSettings.innerHTML = `
        <h2>Something went wrong while loading your game settings page.</h2>
        <h2>${error}</h2>
        <h2><a href="${window.location.origin}">Click here to return to safety!</a></h2>
        `
    });
});

const handleOptionChange = (event) => {
    if(!event.target.matches('.setting')) { return; }
    const presetNumber = document.getElementById('preset-number').value;
    const settings = JSON.parse(localStorage.getItem(`gameSettings${presetNumber}`))
    const settingString = event.target.getAttribute('data-setting');
    document.getElementById(settingString).innerText = event.target.value;
    if(getSettingValue(settings, settingString) !== false){
        const keys = settingString.split('.');
        switch (keys.length) {
            case 1:
                settings[keys[0]] = event.target.value;
                break;
            case 2:
                settings[keys[0]][keys[1]] = event.target.value;
                break;
            case 3:
                settings[keys[0]][keys[1]][keys[2]] = event.target.value;
                break;
            default:
                console.warn(`Unknown setting string received: ${settingString}`)
                return;
        }

        // Save the updated settings object bask to localStorage
        localStorage.setItem(`gameSettings${presetNumber}`, JSON.stringify(settings));
    }else{
        console.warn(`Unknown setting string received: ${settingString}`)
    }
};

const populateSettings = () => {
    const presetNumber = document.getElementById('preset-number').value;
    const settings = JSON.parse(localStorage.getItem(`gameSettings${presetNumber}`))
    const settingsInputs = Array.from(document.querySelectorAll('.setting'));
    settingsInputs.forEach((input) => {
        const settingString = input.getAttribute('data-setting');
        const settingValue = getSettingValue(settings, settingString);
        console.info(`${settingString}: ${settingValue}`);
        if(settingValue !== false){
            input.value = settingValue;
            document.getElementById(settingString).innerText = settingValue;
        }
    });
};

/**
 * Returns the value of the settings object, or false if the settings object does not exist
 * @param settings
 * @param keyString
 * @returns {string} | bool
 */
const getSettingValue = (settings, keyString) => {
    const keys = keyString.split('.');
    let currentVal = settings;
    keys.forEach((key) => {
        if(typeof(key) === 'string' && currentVal.hasOwnProperty(key)){
            currentVal = currentVal[key];
        }else{
            return false;
        }
    });
    return currentVal;
};
