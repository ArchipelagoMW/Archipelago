window.addEventListener('load', () => {
  fetchSettingData().then((results) => {
    let settingHash = localStorage.getItem('weighted-settings-hash');
    if (!settingHash) {
      // If no hash data has been set before, set it now
      localStorage.setItem('weighted-settings-hash', md5(results));
      localStorage.removeItem('weighted-settings');
      settingHash = md5(results);
    }

    if (settingHash !== md5(results)) {
      const userMessage = document.getElementById('user-message');
      userMessage.innerText = "Your settings are out of date! Click here to update them! Be aware this will reset " +
        "them all to default.";
      userMessage.style.display = "block";
      userMessage.addEventListener('click', resetSettings);
    }

    // Page setup
    createDefaultSettings(results);
    buildUI(results);
    updateVisibleGames();
    adjustHeaderWidth();

    // Event listeners
    document.getElementById('export-settings').addEventListener('click', () => exportSettings());
    document.getElementById('generate-race').addEventListener('click', () => generateGame(true));
    document.getElementById('generate-game').addEventListener('click', () => generateGame());

    // Name input field
    const weightedSettings = JSON.parse(localStorage.getItem('weighted-settings'));
    const nameInput = document.getElementById('player-name');
    nameInput.setAttribute('data-type', 'data');
    nameInput.setAttribute('data-setting', 'name');
    nameInput.addEventListener('keyup', updateBaseSetting);
    nameInput.value = weightedSettings.name;
  });
});

const resetSettings = () => {
  localStorage.removeItem('weighted-settings');
  localStorage.removeItem('weighted-settings-hash')
  window.location.reload();
};

const fetchSettingData = () => new Promise((resolve, reject) => {
  fetch(new Request(`${window.location.origin}/static/generated/weighted-settings.json`)).then((response) => {
    try{ resolve(response.json()); }
    catch(error){ reject(error); }
  });
});

const createDefaultSettings = (settingData) => {
  if (!localStorage.getItem('weighted-settings')) {
    const newSettings = {};

    // Transfer base options directly
    for (let baseOption of Object.keys(settingData.baseOptions)){
      newSettings[baseOption] = settingData.baseOptions[baseOption];
    }

    // Set options per game
    for (let game of Object.keys(settingData.games)) {
      // Initialize game object
      newSettings[game] = {};

      // Transfer game settings
      for (let gameSetting of Object.keys(settingData.games[game].gameSettings)){
        newSettings[game][gameSetting] = {};

        const setting = settingData.games[game].gameSettings[gameSetting];
        switch(setting.type){
          case 'select':
            setting.options.forEach((option) => {
              newSettings[game][gameSetting][option.value] =
                (setting.hasOwnProperty('defaultValue') && setting.defaultValue === option.value) ? 25 : 0;
            });
            break;
          case 'range':
            for (let i = setting.min; i <= setting.max; ++i){
              newSettings[game][gameSetting][i] =
                (setting.hasOwnProperty('defaultValue') && setting.defaultValue === i) ? 25 : 0;
            }
            break;
          default:
            console.error(`Unknown setting type for ${game} setting ${gameSetting}: ${setting.type}`);
        }
      }

      newSettings[game].start_inventory = [];
      newSettings[game].exclude_locations = [];
      newSettings[game].local_items = [];
      newSettings[game].non_local_items = [];
      newSettings[game].start_hints = [];
    }

    localStorage.setItem('weighted-settings', JSON.stringify(newSettings));
  }
};

// TODO: Include item configs: start_inventory, local_items, non_local_items, start_hints
// TODO: Include location configs: exclude_locations
const buildUI = (settingData) => {
  // Build the game-choice div
  buildGameChoice(settingData.games);

  const gamesWrapper = document.getElementById('games-wrapper');
  Object.keys(settingData.games).forEach((game) => {
    // Create game div, invisible by default
    const gameDiv = document.createElement('div');
    gameDiv.setAttribute('id', `${game}-div`);
    gameDiv.classList.add('game-div');
    gameDiv.classList.add('invisible');

    const gameHeader = document.createElement('h2');
    gameHeader.innerText = game;
    gameDiv.appendChild(gameHeader);

    gameDiv.appendChild(buildOptionsDiv(game, settingData.games[game].gameSettings));
    gamesWrapper.appendChild(gameDiv);
  });
};

const buildGameChoice = (games) => {
  const settings = JSON.parse(localStorage.getItem('weighted-settings'));
  const gameChoiceDiv = document.getElementById('game-choice');
  const h2 = document.createElement('h2');
  h2.innerText = 'Game Select';
  gameChoiceDiv.appendChild(h2);

  const gameSelectDescription = document.createElement('p');
  gameSelectDescription.classList.add('setting-description');
  gameSelectDescription.innerText = 'Choose which games you might be required to play'
  gameChoiceDiv.appendChild(gameSelectDescription);

  // Build the game choice table
  const table = document.createElement('table');
  const tbody = document.createElement('tbody');

  Object.keys(games).forEach((game) => {
    const tr = document.createElement('tr');
    const tdLeft = document.createElement('td');
    tdLeft.classList.add('td-left');
    tdLeft.innerText = game;
    tr.appendChild(tdLeft);

    const tdMiddle = document.createElement('td');
    tdMiddle.classList.add('td-middle');
    const range = document.createElement('input');
    range.setAttribute('type', 'range');
    range.setAttribute('min', 0);
    range.setAttribute('max', 50);
    range.setAttribute('data-type', 'weight');
    range.setAttribute('data-setting', 'game');
    range.setAttribute('data-option', game);
    range.value = settings.game[game];
    range.addEventListener('change', (evt) => {
      updateBaseSetting(evt);
      updateVisibleGames(); // Show or hide games based on the new settings
    });
    tdMiddle.appendChild(range);
    tr.appendChild(tdMiddle);

    const tdRight = document.createElement('td');
    tdRight.setAttribute('id', `game-${game}`)
    tdRight.classList.add('td-right');
    tdRight.innerText = range.value;
    tr.appendChild(tdRight);
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  gameChoiceDiv.appendChild(table);
};

const buildOptionsDiv = (game, settings) => {
  const currentSettings = JSON.parse(localStorage.getItem('weighted-settings'));
  const optionsWrapper = document.createElement('div');
  optionsWrapper.classList.add('settings-wrapper');

  Object.keys(settings).forEach((settingName) => {
    const setting = settings[settingName];
    const settingWrapper = document.createElement('div');
    settingWrapper.classList.add('setting-wrapper');

    switch(setting.type){
      case 'select':
        const settingNameHeader = document.createElement('h4');
        settingNameHeader.innerText = setting.displayName;
        settingWrapper.appendChild(settingNameHeader);

        const settingDescription = document.createElement('p');
        settingDescription.classList.add('setting-description');
        settingDescription.innerText = setting.description.replace(/(\n)/g, ' ');
        settingWrapper.appendChild(settingDescription);

        const optionTable = document.createElement('table');
        const tbody = document.createElement('tbody');

        // Add a weight range for each option
        setting.options.forEach((option) => {
          const tr = document.createElement('tr');
          const tdLeft = document.createElement('td');
          tdLeft.classList.add('td-left');
          tdLeft.innerText = option.name;
          tr.appendChild(tdLeft);

          const tdMiddle = document.createElement('td');
          tdMiddle.classList.add('td-middle');
          const range = document.createElement('input');
          range.setAttribute('type', 'range');
          range.setAttribute('data-game', game);
          range.setAttribute('data-setting', settingName);
          range.setAttribute('data-option', option.value);
          range.setAttribute('data-type', setting.type);
          range.setAttribute('min', 0);
          range.setAttribute('max', 50);
          range.addEventListener('change', updateGameSetting);
          range.value = currentSettings[game][settingName][option.value];
          tdMiddle.appendChild(range);
          tr.appendChild(tdMiddle);

          const tdRight = document.createElement('td');
          tdRight.setAttribute('id', `${game}-${settingName}-${option.value}`)
          tdRight.classList.add('td-right');
          tdRight.innerText = range.value;
          tr.appendChild(tdRight);

          tbody.appendChild(tr);
        });

        optionTable.appendChild(tbody);
        settingWrapper.appendChild(optionTable);
        optionsWrapper.appendChild(settingWrapper);
        break;

      case 'range':
        // TODO: Include range settings
        break;

      default:
        console.error(`Unknown setting type for ${game} setting ${setting}: ${settings[setting].type}`);
        return;
    }
  });

  return optionsWrapper;
};

const updateVisibleGames = () => {
  const settings = JSON.parse(localStorage.getItem('weighted-settings'));
  Object.keys(settings.game).forEach((game) => {
    const gameDiv = document.getElementById(`${game}-div`);
    (parseInt(settings.game[game], 10) > 0) ?
      gameDiv.classList.remove('invisible') :
      gameDiv.classList.add('invisible')
  });
};

const updateBaseSetting = (event) => {
  const settings = JSON.parse(localStorage.getItem('weighted-settings'));
  const setting = event.target.getAttribute('data-setting');
  const option = event.target.getAttribute('data-option');
  const type = event.target.getAttribute('data-type');

  switch(type){
    case 'weight':
      settings[setting][option] = isNaN(event.target.value) ? event.target.value : parseInt(event.target.value, 10);
      document.getElementById(`${setting}-${option}`).innerText = event.target.value;
      break;
    case 'data':
      settings[setting] = isNaN(event.target.value) ? event.target.value : parseInt(event.target.value, 10);
      break;
  }

  localStorage.setItem('weighted-settings', JSON.stringify(settings));
};

const updateGameSetting = (event) => {
  const options = JSON.parse(localStorage.getItem('weighted-settings'));
  const game = event.target.getAttribute('data-game');
  const setting = event.target.getAttribute('data-setting');
  const option = event.target.getAttribute('data-option');
  const type = event.target.getAttribute('data-type');
  switch (type){
    case 'select':
      console.log(`${game}-${setting}-${option}`);
      document.getElementById(`${game}-${setting}-${option}`).innerText = event.target.value;
      break;
    case 'range':
      break;
  }
  options[game][setting][option] = isNaN(event.target.value) ?
      event.target.value : parseInt(event.target.value, 10);
  localStorage.setItem('weighted-settings', JSON.stringify(options));
};

const exportSettings = () => {
  const settings = JSON.parse(localStorage.getItem('weighted-settings'));
  if (!settings.name || settings.name.trim().length === 0 || settings.name.toLowerCase().trim() === 'player') {
    const userMessage = document.getElementById('user-message');
    userMessage.innerText = 'You forgot to set your player name at the top of the page!';
    userMessage.classList.add('visible');
    window.scrollTo(0, 0);
    return;
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
  axios.post('/api/generate', {
    weights: { player: localStorage.getItem('weighted-settings') },
    presetData: { player: localStorage.getItem('weighted-settings') },
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
