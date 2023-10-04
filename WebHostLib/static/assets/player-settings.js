let gameName = null;

window.addEventListener('load', () => {
  gameName = document.getElementById('player-settings').getAttribute('data-game');

  // Update game name on page
  document.getElementById('game-name').innerText = gameName;

  fetchSettingData().then((results) => {
    let settingHash = localStorage.getItem(`${gameName}-hash`);
    if (!settingHash) {
      // If no hash data has been set before, set it now
      settingHash = md5(JSON.stringify(results));
      localStorage.setItem(`${gameName}-hash`, settingHash);
      localStorage.removeItem(gameName);
    }

    if (settingHash !== md5(JSON.stringify(results))) {
      showUserMessage("Your settings are out of date! Click here to update them! Be aware this will reset " +
        "them all to default.");
      document.getElementById('user-message').addEventListener('click', resetSettings);
    }

    // Page setup
    createDefaultSettings(results);
    buildUI(results);
    adjustHeaderWidth();

    // Event listeners
    document.getElementById('export-settings').addEventListener('click', () => exportSettings());
    document.getElementById('generate-race').addEventListener('click', () => generateGame(true));
    document.getElementById('generate-game').addEventListener('click', () => generateGame());

    // Name input field
    const playerSettings = JSON.parse(localStorage.getItem(gameName));
    const nameInput = document.getElementById('player-name');
    nameInput.addEventListener('keyup', (event) => updateBaseSetting(event));
    nameInput.value = playerSettings.name;
  }).catch((e) => {
    console.error(e);
    const url = new URL(window.location.href);
    window.location.replace(`${url.protocol}//${url.hostname}/page-not-found`);
  })
});

const resetSettings = () => {
  localStorage.removeItem(gameName);
  localStorage.removeItem(`${gameName}-hash`)
  window.location.reload();
};

const fetchSettingData = () => new Promise((resolve, reject) => {
  const ajax = new XMLHttpRequest();
  ajax.onreadystatechange = () => {
    if (ajax.readyState !== 4) { return; }
    if (ajax.status !== 200) {
      reject(ajax.responseText);
      return;
    }
    try{ resolve(JSON.parse(ajax.responseText)); }
    catch(error){ reject(error); }
  };
  ajax.open('GET', `${window.location.origin}/static/generated/player-settings/${gameName}.json`, true);
  ajax.send();
});

const createDefaultSettings = (settingData) => {
  if (!localStorage.getItem(gameName)) {
    const newSettings = {
      [gameName]: {},
    };
    for (let baseOption of Object.keys(settingData.baseOptions)){
      newSettings[baseOption] = settingData.baseOptions[baseOption];
    }
    for (let gameOption of Object.keys(settingData.gameOptions)){
      newSettings[gameName][gameOption] = settingData.gameOptions[gameOption].defaultValue;
    }
    localStorage.setItem(gameName, JSON.stringify(newSettings));
  }
};

const buildUI = (settingData) => {
  // Game Options
  const leftGameOpts = {};
  const rightGameOpts = {};
  Object.keys(settingData.gameOptions).forEach((key, index) => {
    if (index < Object.keys(settingData.gameOptions).length / 2) { leftGameOpts[key] = settingData.gameOptions[key]; }
    else { rightGameOpts[key] = settingData.gameOptions[key]; }
  });
  document.getElementById('game-options-left').appendChild(buildOptionsTable(leftGameOpts));
  document.getElementById('game-options-right').appendChild(buildOptionsTable(rightGameOpts));
};

const buildOptionsTable = (settings, romOpts = false) => {
  const currentSettings = JSON.parse(localStorage.getItem(gameName));
  const table = document.createElement('table');
  const tbody = document.createElement('tbody');

  Object.keys(settings).forEach((setting) => {
    const tr = document.createElement('tr');

    // td Left
    const tdl = document.createElement('td');
    const label = document.createElement('label');
    label.textContent = `${settings[setting].displayName}: `;
    label.setAttribute('for', setting);

    const questionSpan = document.createElement('span');
    questionSpan.classList.add('interactive');
    questionSpan.setAttribute('data-tooltip', settings[setting].description);
    questionSpan.innerText = '(?)';

    label.appendChild(questionSpan);
    tdl.appendChild(label);
    tr.appendChild(tdl);

    // td Right
    const tdr = document.createElement('td');
    let element = null;

    const randomButton = document.createElement('button');

    switch(settings[setting].type){
      case 'select':
        element = document.createElement('div');
        element.classList.add('select-container');
        let select = document.createElement('select');
        select.setAttribute('id', setting);
        select.setAttribute('data-key', setting);
        if (romOpts) { select.setAttribute('data-romOpt', '1'); }
        settings[setting].options.forEach((opt) => {
          const option = document.createElement('option');
          option.setAttribute('value', opt.value);
          option.innerText = opt.name;
          if ((isNaN(currentSettings[gameName][setting]) &&
            (parseInt(opt.value, 10) === parseInt(currentSettings[gameName][setting]))) ||
            (opt.value === currentSettings[gameName][setting]))
          {
            option.selected = true;
          }
          select.appendChild(option);
        });
        select.addEventListener('change', (event) => updateGameSetting(event.target));
        element.appendChild(select);

        // Randomize button
        randomButton.innerText = '🎲';
        randomButton.classList.add('randomize-button');
        randomButton.setAttribute('data-key', setting);
        randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
        randomButton.addEventListener('click', (event) => toggleRandomize(event, select));
        if (currentSettings[gameName][setting] === 'random') {
          randomButton.classList.add('active');
          select.disabled = true;
        }

        element.appendChild(randomButton);
        break;

      case 'range':
        element = document.createElement('div');
        element.classList.add('range-container');

        let range = document.createElement('input');
        range.setAttribute('type', 'range');
        range.setAttribute('data-key', setting);
        range.setAttribute('min', settings[setting].min);
        range.setAttribute('max', settings[setting].max);
        range.value = currentSettings[gameName][setting];
        range.addEventListener('change', (event) => {
          document.getElementById(`${setting}-value`).innerText = event.target.value;
          updateGameSetting(event.target);
        });
        element.appendChild(range);

        let rangeVal = document.createElement('span');
        rangeVal.classList.add('range-value');
        rangeVal.setAttribute('id', `${setting}-value`);
        rangeVal.innerText = currentSettings[gameName][setting] !== 'random' ?
          currentSettings[gameName][setting] : settings[setting].defaultValue;
        element.appendChild(rangeVal);

        // Randomize button
        randomButton.innerText = '🎲';
        randomButton.classList.add('randomize-button');
        randomButton.setAttribute('data-key', setting);
        randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
        randomButton.addEventListener('click', (event) => toggleRandomize(event, range));
        if (currentSettings[gameName][setting] === 'random') {
          randomButton.classList.add('active');
          range.disabled = true;
        }

        element.appendChild(randomButton);
        break;

      case 'special_range':
        element = document.createElement('div');
        element.classList.add('special-range-container');

        // Build the select element
        let specialRangeSelect = document.createElement('select');
        specialRangeSelect.setAttribute('data-key', setting);
        Object.keys(settings[setting].value_names).forEach((presetName) => {
          let presetOption = document.createElement('option');
          presetOption.innerText = presetName;
          presetOption.value = settings[setting].value_names[presetName];
          const words = presetOption.innerText.split("_");
          for (let i = 0; i < words.length; i++) {
            words[i] = words[i][0].toUpperCase() + words[i].substring(1);
          }
          presetOption.innerText = words.join(" ");
          specialRangeSelect.appendChild(presetOption);
        });
        let customOption = document.createElement('option');
        customOption.innerText = 'Custom';
        customOption.value = 'custom';
        customOption.selected = true;
        specialRangeSelect.appendChild(customOption);
        if (Object.values(settings[setting].value_names).includes(Number(currentSettings[gameName][setting]))) {
          specialRangeSelect.value = Number(currentSettings[gameName][setting]);
        }

        // Build range element
        let specialRangeWrapper = document.createElement('div');
        specialRangeWrapper.classList.add('special-range-wrapper');
        let specialRange = document.createElement('input');
        specialRange.setAttribute('type', 'range');
        specialRange.setAttribute('data-key', setting);
        specialRange.setAttribute('min', settings[setting].min);
        specialRange.setAttribute('max', settings[setting].max);
        specialRange.value = currentSettings[gameName][setting];

        // Build rage value element
        let specialRangeVal = document.createElement('span');
        specialRangeVal.classList.add('range-value');
        specialRangeVal.setAttribute('id', `${setting}-value`);
        specialRangeVal.innerText = currentSettings[gameName][setting] !== 'random' ?
          currentSettings[gameName][setting] : settings[setting].defaultValue;

        // Configure select event listener
        specialRangeSelect.addEventListener('change', (event) => {
          if (event.target.value === 'custom') { return; }

          // Update range slider
          specialRange.value = event.target.value;
          document.getElementById(`${setting}-value`).innerText = event.target.value;
          updateGameSetting(event.target);
        });

        // Configure range event handler
        specialRange.addEventListener('change', (event) => {
          // Update select element
          specialRangeSelect.value =
            (Object.values(settings[setting].value_names).includes(parseInt(event.target.value))) ?
            parseInt(event.target.value) : 'custom';
          document.getElementById(`${setting}-value`).innerText = event.target.value;
          updateGameSetting(event.target);
        });

        element.appendChild(specialRangeSelect);
        specialRangeWrapper.appendChild(specialRange);
        specialRangeWrapper.appendChild(specialRangeVal);
        element.appendChild(specialRangeWrapper);

        // Randomize button
        randomButton.innerText = '🎲';
        randomButton.classList.add('randomize-button');
        randomButton.setAttribute('data-key', setting);
        randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
        randomButton.addEventListener('click', (event) => toggleRandomize(
            event, specialRange, specialRangeSelect)
        );
        if (currentSettings[gameName][setting] === 'random') {
          randomButton.classList.add('active');
          specialRange.disabled = true;
          specialRangeSelect.disabled = true;
        }

        specialRangeWrapper.appendChild(randomButton);
        break;

      default:
        console.error(`Ignoring unknown setting type: ${settings[setting].type} with name ${setting}`);
        return;
    }

    tdr.appendChild(element);
    tr.appendChild(tdr);
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  return table;
};

const toggleRandomize = (event, inputElement, optionalSelectElement = null) => {
  const active = event.target.classList.contains('active');
  const randomButton = event.target;

  if (active) {
    randomButton.classList.remove('active');
    inputElement.disabled = undefined;
    if (optionalSelectElement) {
      optionalSelectElement.disabled = undefined;
    }
  } else {
    randomButton.classList.add('active');
    inputElement.disabled = true;
    if (optionalSelectElement) {
      optionalSelectElement.disabled = true;
    }
  }
  updateGameSetting(active ? inputElement : randomButton);
};

const updateBaseSetting = (event) => {
  const options = JSON.parse(localStorage.getItem(gameName));
  options[event.target.getAttribute('data-key')] = isNaN(event.target.value) ?
    event.target.value : parseInt(event.target.value);
  localStorage.setItem(gameName, JSON.stringify(options));
};

const updateGameSetting = (settingElement) => {
  const options = JSON.parse(localStorage.getItem(gameName));
  if (settingElement.classList.contains('randomize-button')) {
    // If the event passed in is the randomize button, then we know what we must do.
    options[gameName][settingElement.getAttribute('data-key')] = 'random';
  } else {
    options[gameName][settingElement.getAttribute('data-key')] = isNaN(settingElement.value) ?
      settingElement.value : parseInt(settingElement.value, 10);
  }

  localStorage.setItem(gameName, JSON.stringify(options));
};

const exportSettings = () => {
  const settings = JSON.parse(localStorage.getItem(gameName));
  if (!settings.name || settings.name.toLowerCase() === 'player' || settings.name.trim().length === 0) {
    return showUserMessage('You must enter a player name!');
  }
  const yamlText = jsyaml.safeDump(settings, { noCompatMode: true }).replaceAll(/'(\d+)':/g, (x, y) => `${y}:`);
  download(`${document.getElementById('player-name').value}.yaml`, yamlText);
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

const generateGame = (raceMode = false) => {
  const settings = JSON.parse(localStorage.getItem(gameName));
  if (!settings.name || settings.name.toLowerCase() === 'player' || settings.name.trim().length === 0) {
    return showUserMessage('You must enter a player name!');
  }

  axios.post('/api/generate', {
    weights: { player: settings },
    presetData: { player: settings },
    playerCount: 1,
    spoiler: 3,
    race: raceMode ? '1' : '0',
  }).then((response) => {
    window.location.href = response.data.url;
  }).catch((error) => {
    let userMessage = 'Something went wrong and your game could not be generated.';
    if (error.response.data.text) {
      userMessage += ' ' + error.response.data.text;
    }
    showUserMessage(userMessage);
    console.error(error);
  });
};

const showUserMessage = (message) => {
  const userMessage = document.getElementById('user-message');
    userMessage.innerText = message;
    userMessage.classList.add('visible');
    window.scrollTo(0, 0);
    userMessage.addEventListener('click', () => {
      userMessage.classList.remove('visible');
      userMessage.addEventListener('click', hideUserMessage);
    });
};

const hideUserMessage = () => {
  const userMessage = document.getElementById('user-message');
  userMessage.classList.remove('visible');
  userMessage.removeEventListener('click', hideUserMessage);
};
