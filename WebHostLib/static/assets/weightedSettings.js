let spriteData = null;

window.addEventListener('load', () => {
  const gameSettings = document.getElementById('weighted-settings');
  Promise.all([fetchPlayerSettingsYaml(), fetchPlayerSettingsJson(), fetchSpriteData()]).then((results) => {
    // Load YAML into object
    const sourceData = jsyaml.safeLoad(results[0], { json: true });

    // Update localStorage with three settings objects. Preserve original objects if present.
    for (let i=1; i<=3; i++) {
      const localSettings = JSON.parse(localStorage.getItem(`weightedSettings${i}`));
      const updatedObj = localSettings ? Object.assign(sourceData, localSettings) : sourceData;
      localStorage.setItem(`weightedSettings${i}`, JSON.stringify(updatedObj));
    }

    // Parse spriteData into useful sets
    spriteData = JSON.parse(results[2]);

    // Build the entire UI
    buildUI(JSON.parse(results[1]));

    // Populate the UI and add event listeners
    populateSettings();
    document.getElementById('preset-number').addEventListener('change', populateSettings);
    gameSettings.addEventListener('change', handleOptionChange);
    gameSettings.addEventListener('keyup', handleOptionChange);

    document.getElementById('export-button').addEventListener('click', exportSettings);
    document.getElementById('reset-to-default').addEventListener('click', resetToDefaults);
    adjustHeaderWidth();
  }).catch((error) => {
    gameSettings.innerHTML = `
            <h2>Something went wrong while loading your game settings page.</h2>
            <h2>${error}</h2>
            <h2><a href="${window.location.origin}">Click here to return to safety!</a></h2>
            `
  });
});

const fetchPlayerSettingsYaml = () => new Promise((resolve, reject) => {
  const ajax = new XMLHttpRequest();
  ajax.onreadystatechange = () => {
    if (ajax.readyState !== 4) { return; }
    if (ajax.status !== 200) {
      reject("Unable to fetch source yaml file.");
      return;
    }
    resolve(ajax.responseText);
  };
  ajax.open('GET', `${window.location.origin}/static/static/weightedSettings.yaml` ,true);
  ajax.send();
});

const fetchPlayerSettingsJson = () => new Promise((resolve, reject) => {
  const ajax = new XMLHttpRequest();
  ajax.onreadystatechange = () => {
    if (ajax.readyState !== 4) { return; }
    if (ajax.status !== 200) {
      reject('Unable to fetch JSON schema file');
      return;
    }
    resolve(ajax.responseText);
  };
  ajax.open('GET', `${window.location.origin}/static/static/weightedSettings.json`, true);
  ajax.send();
});

const fetchSpriteData = () => new Promise((resolve, reject) => {
  const ajax = new XMLHttpRequest();
  ajax.onreadystatechange = () => {
    if (ajax.readyState !== 4) { return; }
    if (ajax.status !== 200) {
      reject('Unable to fetch sprite data.');
      return;
    }
    resolve(ajax.responseText);
  };
  ajax.open('GET', `${window.location.origin}/static/static/spriteData.json`, true);
  ajax.send();
});

const handleOptionChange = (event) => {
  if(!event.target.matches('.setting')) { return; }
  const presetNumber = document.getElementById('preset-number').value;
  const settings = JSON.parse(localStorage.getItem(`weightedSettings${presetNumber}`))
  const settingString = event.target.getAttribute('data-setting');
  document.getElementById(settingString).innerText = event.target.value;
  if(getSettingValue(settings, settingString) !== false){
    const keys = settingString.split('.');
    switch (keys.length) {
      case 1:
        settings[keys[0]] = isNaN(event.target.value) ?
          event.target.value : parseInt(event.target.value, 10);
        break;
      case 2:
        settings[keys[0]][keys[1]] = isNaN(event.target.value) ?
          event.target.value : parseInt(event.target.value, 10);
        break;
      case 3:
        settings[keys[0]][keys[1]][keys[2]] = isNaN(event.target.value) ?
          event.target.value : parseInt(event.target.value, 10);
        break;
      default:
        console.warn(`Unknown setting string received: ${settingString}`)
        return;
    }

    // Save the updated settings object bask to localStorage
    localStorage.setItem(`weightedSettings${presetNumber}`, JSON.stringify(settings));
  }else{
    console.warn(`Unknown setting string received: ${settingString}`)
  }
};

const populateSettings = () => {
  const presetNumber = document.getElementById('preset-number').value;
  const settings = JSON.parse(localStorage.getItem(`weightedSettings${presetNumber}`))
  const settingsInputs = Array.from(document.querySelectorAll('.setting'));
  settingsInputs.forEach((input) => {
    const settingString = input.getAttribute('data-setting');
    const settingValue = getSettingValue(settings, settingString);
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
      currentVal = false;
    }
  });
  return currentVal;
};

const exportSettings = () => {
  const presetNumber = document.getElementById('preset-number').value;
  const settings = JSON.parse(localStorage.getItem(`weightedSettings${presetNumber}`));
  const yamlText = jsyaml.safeDump(settings, { noCompatMode: true }).replaceAll(/'(\d+)':/g, (x, y) => `${y}:`);
  download(`${settings.description}.yaml`, yamlText);
};

const resetToDefaults = () => {
  [1, 2, 3].forEach((presetNumber) => localStorage.removeItem(`weightedSettings${presetNumber}`));
  location.reload();
};

/** Create an anchor and trigger a download of a text file. */
const download = (filename, text) => {
  const downloadLink = document.createElement('a');
  downloadLink.setAttribute('href','data:text/yaml;charset=utf-8,'+ encodeURIComponent(text))
  downloadLink.setAttribute('download', filename);
  downloadLink.style.display = 'none';
  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
};

const buildUI = (settings) => {
  const settingsWrapper = document.getElementById('settings-wrapper');
  const settingTypes = {
    gameOptions: 'Game Options',
    romOptions: 'ROM Options',
  }

  Object.keys(settingTypes).forEach((settingTypeKey) => {
    const sectionHeader = document.createElement('h2');
    sectionHeader.innerText = settingTypes[settingTypeKey];
    settingsWrapper.appendChild(sectionHeader);

    Object.values(settings[settingTypeKey]).forEach((setting) => {
      if (typeof(setting.inputType) === 'undefined' || !setting.inputType){
        console.error(setting);
        throw new Error('Setting with no inputType specified.');
      }

      switch(setting.inputType){
        case 'text':
          // Currently, all text input is handled manually because there is very little of it
          return;
        case 'range':
          buildRangeSettings(settingsWrapper, setting);
          return;
        default:
          console.error(setting);
          throw new Error('Unhandled inputType specified.');
      }
    });
  });

  // Build sprite options
  const spriteOptionsHeader = document.createElement('h2');
  spriteOptionsHeader.innerText = 'Sprite Options';
  settingsWrapper.appendChild(spriteOptionsHeader);

  const spriteOptionsWrapper = document.createElement('div');
  spriteOptionsWrapper.className = 'setting-wrapper';

  const spriteOptionsTitle = document.createElement('span');
  spriteOptionsTitle.className = 'title-span';
  spriteOptionsTitle.innerText = 'Alternate Sprites';
  spriteOptionsWrapper.appendChild(spriteOptionsTitle);

  const spriteOptionsDescription = document.createElement('span');
  spriteOptionsDescription.className = 'description-span';
  spriteOptionsDescription.innerText = "Choose an alternate sprite to play the game with.";
  spriteOptionsWrapper.appendChild(spriteOptionsDescription);

  const spriteOptionsTable = document.createElement('table');
  spriteOptionsTable.setAttribute('id', 'sprite-options-table');
  spriteOptionsTable.className = 'option-set';
  const tbody = document.createElement('tbody');
  tbody.setAttribute('id', 'sprites-tbody');

  const currentPreset = document.getElementById('preset-number').value;
  const playerSettings = JSON.parse(localStorage.getItem(`weightedSettings${currentPreset}`));

  // Manually add a row for random sprites
  addSpriteRow(tbody, playerSettings, 'random');

  // Add a row for each sprite currently present in the player's settings
  Object.keys(playerSettings.rom.sprite).forEach((spriteName) => {
    if(['random'].indexOf(spriteName) > -1) return;
    addSpriteRow(tbody, playerSettings, spriteName)
  });

  spriteOptionsTable.appendChild(tbody);
  spriteOptionsWrapper.appendChild(spriteOptionsTable);

  settingsWrapper.appendChild(spriteOptionsWrapper);

  // Append sprite picker
  settingsWrapper.appendChild(buildSpritePicker());
};

const buildRangeSettings = (parentElement, settings) => {
  // Ensure we are operating on a range-specific setting
  if(typeof(settings.inputType) === 'undefined' || settings.inputType !== 'range'){
    throw new Error('Invalid input type provided to buildRangeSettings func.');
  }

  const settingWrapper = document.createElement('div');
  settingWrapper.className = 'setting-wrapper';

  if(typeof(settings.friendlyName) !== 'undefined' && settings.friendlyName){
    const sectionTitle = document.createElement('span');
    sectionTitle.className = 'title-span';
    sectionTitle.innerText = settings.friendlyName;
    settingWrapper.appendChild(sectionTitle);
  }

  if(settings.description){
    const description = document.createElement('span');
    description.className = 'description-span';
    description.innerText = settings.description;
    settingWrapper.appendChild(description);
  }

  // Create table
  const optionSetTable = document.createElement('table');
  optionSetTable.className = 'option-set';

  // Create table body
  const tbody = document.createElement('tbody');
  Object.keys(settings.subOptions).forEach((setting) => {
    // Overwrite setting key name with real object
    setting = settings.subOptions[setting];
    const settingId = (Math.random() * 1000000).toString();

    // Create rows for each option
    const optionRow = document.createElement('tr');

    // Option name td
    const optionName = document.createElement('td');
    optionName.className = 'option-name';
    const optionLabel = document.createElement('label');
    optionLabel.setAttribute('for', settingId);
    optionLabel.setAttribute('data-tooltip', setting.description);
    optionLabel.innerText = setting.friendlyName;
    optionName.appendChild(optionLabel);
    optionRow.appendChild(optionName);

    // Option value td
    const optionValue = document.createElement('td');
    optionValue.className = 'option-value';
    const input = document.createElement('input');
    input.className = 'setting';
    input.setAttribute('id', settingId);
    input.setAttribute('type', 'range');
    input.setAttribute('min', '0');
    input.setAttribute('max', '100');
    input.setAttribute('data-setting', setting.keyString);
    input.value = setting.defaultValue;
    optionValue.appendChild(input);
    const valueDisplay = document.createElement('span');
    valueDisplay.setAttribute('id', setting.keyString);
    valueDisplay.innerText = setting.defaultValue;
    optionValue.appendChild(valueDisplay);
    optionRow.appendChild(optionValue);
    tbody.appendChild(optionRow);
  });

  optionSetTable.appendChild(tbody);
  settingWrapper.appendChild(optionSetTable);
  parentElement.appendChild(settingWrapper);
};

const addSpriteRow = (tbody, playerSettings, spriteName) => {
  const rowId = (Math.random() * 1000000).toString();
  const optionId = (Math.random() * 1000000).toString();
  const tr = document.createElement('tr');
  tr.setAttribute('id', rowId);

  // Option Name
  const optionName = document.createElement('td');
  optionName.className = 'option-name';
  const label = document.createElement('label');
  label.htmlFor = optionId;
  label.innerText = spriteName;
  optionName.appendChild(label);

  if(['random', 'random_sprite_on_event'].indexOf(spriteName) === -1) {
    const deleteButton = document.createElement('span');
    deleteButton.setAttribute('data-sprite', spriteName);
    deleteButton.setAttribute('data-row-id', rowId);
    deleteButton.innerText = ' (❌)';
    deleteButton.className = 'delete-button';
    optionName.appendChild(deleteButton);
    deleteButton.addEventListener('click', removeSpriteOption);
  }

  tr.appendChild(optionName);

  // Option Value
  const optionValue = document.createElement('td');
  optionValue.className = 'option-value';
  const input = document.createElement('input');
  input.className = 'setting';
  input.setAttribute('id', optionId);
  input.setAttribute('type', 'range');
  input.setAttribute('min', '0');
  input.setAttribute('max', '100');
  input.setAttribute('data-setting', `rom.sprite.${spriteName}`);
  input.value = "50";
  optionValue.appendChild(input);

  // Value display
  const valueDisplay = document.createElement('span');
  valueDisplay.setAttribute('id', `rom.sprite.${spriteName}`);
  valueDisplay.innerText = playerSettings.rom.sprite.hasOwnProperty(spriteName) ?
    playerSettings.rom.sprite[spriteName] : '0';
  optionValue.appendChild(valueDisplay);

  tr.appendChild(optionValue);
  tbody.appendChild(tr);
};

const addSpriteOption = (event) => {
  const presetNumber = document.getElementById('preset-number').value;
  const playerSettings = JSON.parse(localStorage.getItem(`weightedSettings${presetNumber}`));
  const spriteName = event.target.getAttribute('data-sprite');
  console.log(event.target);
  console.log(spriteName);

  if (Object.keys(playerSettings.rom.sprite).indexOf(spriteName) !== -1) {
    // Do not add the same sprite twice
    return;
  }

  // Add option to playerSettings object
  playerSettings.rom.sprite[event.target.getAttribute('data-sprite')] = 50;
  localStorage.setItem(`weightedSettings${presetNumber}`, JSON.stringify(playerSettings));

  // Add <tr> to #sprite-options-table
  const tbody = document.getElementById('sprites-tbody');
  addSpriteRow(tbody, playerSettings, spriteName);
};

const removeSpriteOption = (event) => {
  const presetNumber = document.getElementById('preset-number').value;
  const playerSettings = JSON.parse(localStorage.getItem(`weightedSettings${presetNumber}`));
  const spriteName = event.target.getAttribute('data-sprite');

  // Remove option from playerSettings object
  delete playerSettings.rom.sprite[spriteName];
  localStorage.setItem(`weightedSettings${presetNumber}`, JSON.stringify(playerSettings));

  // Remove <tr> from #sprite-options-table
  const tr = document.getElementById(event.target.getAttribute('data-row-id'));
  tr.parentNode.removeChild(tr);
};

const buildSpritePicker = () => {
  const spritePicker = document.createElement('div');
  spritePicker.setAttribute('id', 'sprite-picker');

  // Build description
  const description = document.createElement('span');
  description.innerText = 'To add a sprite to your playable list, click the one you want below.';
  spritePicker.appendChild(description);

  const sprites = document.createElement('div');
  sprites.setAttribute('id', 'sprite-picker-sprites');
  Object.keys(spriteData).forEach((spriteName) => {
    const spriteImg = document.createElement('img');
    spriteImg.setAttribute('src', `static/static/sprites/${spriteName}.gif`);
    spriteImg.setAttribute('data-sprite', spriteName);
    spriteImg.setAttribute('alt', spriteName);

    // Wrap the image in a span to allow for tooltip presence
    const imgWrapper = document.createElement('span');
    imgWrapper.className = 'sprite-img-wrapper';
    imgWrapper.setAttribute('data-tooltip', spriteName);
    imgWrapper.appendChild(spriteImg);
    imgWrapper.setAttribute('data-sprite', spriteName);
    sprites.appendChild(imgWrapper);
    imgWrapper.addEventListener('click', addSpriteOption);
  });

  spritePicker.appendChild(sprites);
  return spritePicker;
};
