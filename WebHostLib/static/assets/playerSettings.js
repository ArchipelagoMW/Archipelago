window.addEventListener('load', () => {
  fetchSettingData().then((settingData) => {
    createDefaultSettings(settingData);
    buildUI(settingData);
    populateSettings();
  });
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
  ajax.open('GET', `${window.location.origin}/static/static/playerSettings.json` ,true);
  ajax.send();
});

const createDefaultSettings = (settingData) => {
  if (!localStorage.getItem('playerSettings')) {
    const newSettings = {};
    for (let roSetting of Object.keys(settingData.readOnly)){
      newSettings[roSetting] = settingData.readOnly[roSetting];
    }
    for (let gameOption of Object.keys(settingData.gameOptions)){
      newSettings[gameOption] = settingData.gameOptions[gameOption].defaultValue;
    }
    for (let romOption of Object.keys(settingData.romOptions)){
      newSettings[romOption] = settingData.romOptions[romOption].defaultValue;
    }
    localStorage.setItem('playerSettings', JSON.stringify(newSettings));
  }
};

const buildUI = (settingData) => {
  // Game Options
  const leftGameOpts = {};
  const rightGameOpts = {};
  Object.keys(settingData.gameOptions).forEach((key, index) => {
    if (index % 2 === 0) { leftGameOpts[key] = settingData.gameOptions[key]; }
    else { rightGameOpts[key] = settingData.gameOptions[key]; }
  });
  document.getElementById('game-options-left').appendChild(buildOptionsTable(leftGameOpts));
  document.getElementById('game-options-right').appendChild(buildOptionsTable(rightGameOpts));

  // ROM Options
  const leftRomOpts = {};
  const rightRomOpts = {};
  Object.keys(settingData.romOptions).forEach((key, index) => {
    if (index % 2 === 0) { leftRomOpts[key] = settingData.romOptions[key]; }
    else { rightRomOpts[key] = settingData.romOptions[key]; }
  });
  document.getElementById('rom-options-left').appendChild(buildOptionsTable(leftRomOpts));
  document.getElementById('rom-options-right').appendChild(buildOptionsTable(rightRomOpts));
};

const buildOptionsTable = (settings) => {
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
    settings[setting].options.forEach((opt) => {
      const option = document.createElement('option');
      option.setAttribute('value', opt.value);
      option.innerText = opt.name;
      select.appendChild(option);
    });
    tdr.appendChild(select);
    tr.appendChild(tdr);
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  return table;
};

const populateSettings = () => {
  // TODO
};

const updateSetting = (key, setting) => {
  const options = JSON.parse(localStorage.getItem('playerSettings'));
  options[key] = setting;
  localStorage.setItem('playerSettings', JSON.stringify(options));
};
