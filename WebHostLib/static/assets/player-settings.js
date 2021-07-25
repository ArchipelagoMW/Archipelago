let gameName = null;

window.addEventListener('load', () => {
  const urlMatches = window.location.href.match(/^.*\/(.*)\/player-settings/);
  gameName = decodeURIComponent(urlMatches[1]);

  // Update game name on page
  document.getElementById('game-name').innerHTML = gameName;

  Promise.all([fetchSettingData()]).then((results) => {
    // Page setup
    createDefaultSettings(results[0]);
    buildUI(results[0]);
    adjustHeaderWidth();

    // Event listeners
    document.getElementById('export-settings').addEventListener('click', () => exportSettings());
    document.getElementById('generate-race').addEventListener('click', () => generateGame(true))
    document.getElementById('generate-game').addEventListener('click', () => generateGame());

    // Name input field
    const playerSettings = JSON.parse(localStorage.getItem(gameName));
    const nameInput = document.getElementById('player-name');
    nameInput.addEventListener('keyup', (event) => updateBaseSetting(event));
    nameInput.value = playerSettings.name;
  }).catch((error) => {
    console.error(error);
  })
});

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
  ajax.open('GET', `${window.location.origin}/static/generated/${gameName}.json`, true);
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
    label.innerText = `${settings[setting].friendlyName}:`;
    tdl.appendChild(label);
    tr.appendChild(tdl);

    // td Right
    const tdr = document.createElement('td');
    const select = document.createElement('select');
    select.setAttribute('id', setting);
    select.setAttribute('data-key', setting);
    if (romOpts) { select.setAttribute('data-romOpt', '1'); }
    settings[setting].options.forEach((opt) => {
      const option = document.createElement('option');
      option.setAttribute('value', opt.value);
      option.innerText = opt.name;
      if ((isNaN(currentSettings[setting]) && (parseInt(opt.value, 10) === parseInt(currentSettings[setting]))) ||
        (opt.value === currentSettings[setting])) {
        option.selected = true;
      }
      select.appendChild(option);
    });
    select.addEventListener('change', (event) => updateGameSetting(event));
    tdr.appendChild(select);
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
  if (!settings.name || settings.name.trim().length === 0) { settings.name = "noname"; }
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
  axios.post('/api/generate', {
    weights: { player: localStorage.getItem(gameName) },
    presetData: { player: localStorage.getItem(gameName) },
    playerCount: 1,
    race: raceMode ? '1' : '0',
  }).then((response) => {
    window.location.href = response.data.url;
  }).catch((error) => {
    const userMessage = document.getElementById('user-message');
    userMessage.innerText = 'Something went wrong and your game could not be generated.';
    if (error.response.data.text) {
      userMessage.innerText += ' ' + error.response.data.text;
    }
    userMessage.classList.add('visible');
    window.scrollTo(0, 0);
    console.error(error);
  });
};
