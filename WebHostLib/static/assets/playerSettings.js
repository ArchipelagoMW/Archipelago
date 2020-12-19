window.addEventListener('load', () => {
  Promise.all([fetchSettingData(), fetchSpriteData()]).then((results) => {
    // Page setup
    createDefaultSettings(results[0]);
    buildUI(results[0]);
    adjustHeaderWidth();

    // Event listeners
    document.getElementById('export-settings').addEventListener('click', () => exportSettings());
    document.getElementById('generate-race').addEventListener('click', () => generateGame(true))
    document.getElementById('generate-game').addEventListener('click', () => generateGame());

    // Name input field
    const playerSettings = JSON.parse(localStorage.getItem('playerSettings'));
    const nameInput = document.getElementById('player-name');
    nameInput.addEventListener('keyup', (event) => updateSetting(event));
    nameInput.value = playerSettings.name;

    // Sprite options
    const spriteData = JSON.parse(results[1]);
    const spriteSelect = document.getElementById('sprite');
    spriteData.sprites.forEach((sprite) => {
      if (sprite.name.trim().length === 0) { return; }
      const option = document.createElement('option');
      option.setAttribute('value', sprite.name.trim());
      if (playerSettings.rom.sprite === sprite.name.trim()) { option.selected = true; }
      option.innerText = sprite.name;
      spriteSelect.appendChild(option);
    });
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
  ajax.open('GET', `${window.location.origin}/static/static/playerSettings.json`, true);
  ajax.send();
});

const createDefaultSettings = (settingData) => {
  if (!localStorage.getItem('playerSettings')) {
    const newSettings = {};
    for (let roSetting of Object.keys(settingData.readOnly)){
      newSettings[roSetting] = settingData.readOnly[roSetting];
    }
    for (let generalOption of Object.keys(settingData.generalOptions)){
      newSettings[generalOption] = settingData.generalOptions[generalOption];
    }
    for (let gameOption of Object.keys(settingData.gameOptions)){
      newSettings[gameOption] = settingData.gameOptions[gameOption].defaultValue;
    }
    newSettings.rom = {};
    for (let romOption of Object.keys(settingData.romOptions)){
      newSettings.rom[romOption] = settingData.romOptions[romOption].defaultValue;
    }
    localStorage.setItem('playerSettings', JSON.stringify(newSettings));
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

  // ROM Options
  const leftRomOpts = {};
  const rightRomOpts = {};
  Object.keys(settingData.romOptions).forEach((key, index) => {
    if (index < Object.keys(settingData.romOptions).length / 2) { leftRomOpts[key] = settingData.romOptions[key]; }
    else { rightRomOpts[key] = settingData.romOptions[key]; }
  });
  document.getElementById('rom-options-left').appendChild(buildOptionsTable(leftRomOpts, true));
  document.getElementById('rom-options-right').appendChild(buildOptionsTable(rightRomOpts, true));
};

const buildOptionsTable = (settings, romOpts = false) => {
  const currentSettings = JSON.parse(localStorage.getItem('playerSettings'));
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
    select.addEventListener('change', (event) => updateSetting(event));
    tdr.appendChild(select);
    tr.appendChild(tdr);
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  return table;
};

const updateSetting = (event) => {
  const options = JSON.parse(localStorage.getItem('playerSettings'));
  if (event.target.getAttribute('data-romOpt')) {
    options.rom[event.target.getAttribute('data-key')] = isNaN(event.target.value) ?
      event.target.value : parseInt(event.target.value, 10);
  } else {
    options[event.target.getAttribute('data-key')] = isNaN(event.target.value) ?
      event.target.value : parseInt(event.target.value, 10);
  }
  localStorage.setItem('playerSettings', JSON.stringify(options));
};

const exportSettings = () => {
  const settings = JSON.parse(localStorage.getItem('playerSettings'));
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
    weights: { player: localStorage.getItem('playerSettings') },
    presetData: { player: localStorage.getItem('playerSettings') },
    playerCount: 1,
    race: raceMode ? '1' : '0',
  }).then((response) => {
    window.location.href = response.data.url;
  });
};

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
