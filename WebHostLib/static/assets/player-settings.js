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
  }).catch(() => {
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
    label.setAttribute('for', setting);
    label.setAttribute('data-tooltip', settings[setting].description);
    label.innerText = `${settings[setting].displayName}:`;
    tdl.appendChild(label);
    tr.appendChild(tdl);

    // td Right
    const tdr = document.createElement('td');
    let element = null;

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
        select.addEventListener('change', (event) => updateGameSetting(event));
        element.appendChild(select);
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
        const settingMax = settings[setting].max;
        const specialMax = settings[setting].specialMax;
        range.addEventListener('change', (event) => {
          const v = event.target.value;
          // if at max and have specialMax, use that, else use value
          const text = ((v === settingMax) && specialMax) || v;
          document.getElementById(`${setting}-value`).innerText = text;
          updateGameSetting(event);
        });
        element.appendChild(range);

        let rangeVal = document.createElement('span');
        rangeVal.classList.add('range-value');
        rangeVal.setAttribute('id', `${setting}-value`);
        rangeVal.innerText = currentSettings[gameName][setting] ?? settings[setting].defaultValue;
        element.appendChild(rangeVal);
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

const updateBaseSetting = (event) => {
  const options = JSON.parse(localStorage.getItem(gameName));
  options[event.target.getAttribute('data-key')] = isNaN(event.target.value) ?
    event.target.value : parseInt(event.target.value);
  localStorage.setItem(gameName, JSON.stringify(options));
};

const updateGameSetting = (event) => {
  const options = JSON.parse(localStorage.getItem(gameName));
  options[gameName][event.target.getAttribute('data-key')] = isNaN(event.target.value) ?
      event.target.value : parseInt(event.target.value, 10);
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
