window.addEventListener('load', () => {
  fetchSettingData().then((data) => {
    let settingHash = localStorage.getItem('weighted-settings-hash');
    if (!settingHash) {
      // If no hash data has been set before, set it now
      settingHash = md5(JSON.stringify(data));
      localStorage.setItem('weighted-settings-hash', settingHash);
      localStorage.removeItem('weighted-settings');
    }

    if (settingHash !== md5(JSON.stringify(data))) {
      const userMessage = document.getElementById('user-message');
      userMessage.innerText = "Your settings are out of date! Click here to update them! Be aware this will reset " +
        "them all to default.";
      userMessage.classList.add('visible');
      userMessage.addEventListener('click', resetSettings);
    }

    // Page setup
    const settings = new WeightedSettings(data);
    settings.buildUI();
    settings.updateVisibleGames();
    adjustHeaderWidth();

    // Event listeners
    document.getElementById('export-options').addEventListener('click', () => settings.export());
    document.getElementById('generate-race').addEventListener('click', () => settings.generateGame(true));
    document.getElementById('generate-game').addEventListener('click', () => settings.generateGame());

    // Name input field
    const nameInput = document.getElementById('player-name');
    nameInput.setAttribute('data-type', 'data');
    nameInput.setAttribute('data-setting', 'name');
    nameInput.addEventListener('keyup', (evt) => settings.updateBaseSetting(evt));
    nameInput.value = settings.current.name;
  });
});

const resetSettings = () => {
  localStorage.removeItem('weighted-settings');
  localStorage.removeItem('weighted-settings-hash')
  window.location.reload();
};

const fetchSettingData = () => new Promise((resolve, reject) => {
  fetch(new Request(`${window.location.origin}/static/generated/weighted-settings.json`)).then((response) => {
    try{ response.json().then((jsonObj) => resolve(jsonObj)); }
    catch(error){ reject(error); }
  });
});

/// The weighted settings across all games.
class WeightedSettings {
  // The data from the server describing the types of settings available for
  // each game, as a JSON-safe blob.
  data;

  // The settings chosen by the user as they'd appear in the YAML file, stored
  // to and retrieved from local storage.
  current;

  // A record mapping game names to the associated GameSettings.
  games;

  constructor(data) {
    this.data = data;
    this.current = JSON.parse(localStorage.getItem('weighted-settings'));
    this.games = Object.keys(this.data.games).map((game) => new GameSettings(this, game));
    if (this.current) { return; }

    this.current = {};

    // Transfer base options directly
    for (let baseOption of Object.keys(this.data.baseOptions)){
      this.current[baseOption] = this.data.baseOptions[baseOption];
    }

    // Set options per game
    for (let game of Object.keys(this.data.games)) {
      // Initialize game object
      this.current[game] = {};

      // Transfer game settings
      for (let gameSetting of Object.keys(this.data.games[game].gameSettings)){
        this.current[game][gameSetting] = {};

        const setting = this.data.games[game].gameSettings[gameSetting];
        switch(setting.type){
          case 'select':
            setting.options.forEach((option) => {
              this.current[game][gameSetting][option.value] =
                (setting.hasOwnProperty('defaultValue') && setting.defaultValue === option.value) ? 25 : 0;
            });
            break;
          case 'range':
          case 'special_range':
            this.current[game][gameSetting]['random'] = 0;
            this.current[game][gameSetting]['random-low'] = 0;
            this.current[game][gameSetting]['random-high'] = 0;
            if (setting.hasOwnProperty('defaultValue')) {
              this.current[game][gameSetting][setting.defaultValue] = 25;
            } else {
              this.current[game][gameSetting][setting.min] = 25;
            }
            break;

          case 'items-list':
          case 'locations-list':
          case 'custom-list':
            this.current[game][gameSetting] = setting.defaultValue;
            break;

          default:
            console.error(`Unknown setting type for ${game} setting ${gameSetting}: ${setting.type}`);
        }
      }

      this.current[game].start_inventory = {};
      this.current[game].exclude_locations = [];
      this.current[game].priority_locations = [];
      this.current[game].local_items = [];
      this.current[game].non_local_items = [];
      this.current[game].start_hints = [];
      this.current[game].start_location_hints = [];
    }

    this.save();
  }

  // Saves the current settings to local storage.
  save() {
    localStorage.setItem('weighted-settings', JSON.stringify(this.current));
  }

  buildUI() {
    // Build the game-choice div
    this.#buildGameChoice();

    const gamesWrapper = document.getElementById('games-wrapper');
    this.games.forEach((game) => {
      gamesWrapper.appendChild(game.buildUI());
    });
  }

  #buildGameChoice() {
    const gameChoiceDiv = document.getElementById('game-choice');
    const h2 = document.createElement('h2');
    h2.innerText = 'Game Select';
    gameChoiceDiv.appendChild(h2);

    const gameSelectDescription = document.createElement('p');
    gameSelectDescription.classList.add('setting-description');
    gameSelectDescription.innerText = 'Choose which games you might be required to play.';
    gameChoiceDiv.appendChild(gameSelectDescription);

    const hintText = document.createElement('p');
    hintText.classList.add('hint-text');
    hintText.innerText = 'If a game\'s value is greater than zero, you can click it\'s name to jump ' +
      'to that section.'
    gameChoiceDiv.appendChild(hintText);

    // Build the game choice table
    const table = document.createElement('table');
    const tbody = document.createElement('tbody');

    Object.keys(this.data.games).forEach((game) => {
      const tr = document.createElement('tr');
      const tdLeft = document.createElement('td');
      tdLeft.classList.add('td-left');
      const span = document.createElement('span');
      span.innerText = game;
      span.setAttribute('id', `${game}-game-option`)
      tdLeft.appendChild(span);
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
      range.value = this.current.game[game];
      range.addEventListener('change', (evt) => {
        this.updateBaseSetting(evt);
        this.updateVisibleGames(); // Show or hide games based on the new settings
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
  }

  // Verifies that `this.settings` meets all the requirements for world
  // generation, normalizes it for serialization, and returns the result.
  #validateSettings() {
    const settings = structuredClone(this.current);
    const userMessage = document.getElementById('user-message');
    let errorMessage = null;

    // User must choose a name for their file
    if (!settings.name || settings.name.trim().length === 0 || settings.name.toLowerCase().trim() === 'player') {
      userMessage.innerText = 'You forgot to set your player name at the top of the page!';
      userMessage.classList.add('visible');
      userMessage.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
      return;
    }

    // Clean up the settings output
    Object.keys(settings.game).forEach((game) => {
      // Remove any disabled games
      if (settings.game[game] === 0) {
        delete settings.game[game];
        delete settings[game];
        return;
      }

      Object.keys(settings[game]).forEach((setting) => {
        // Remove any disabled options
        Object.keys(settings[game][setting]).forEach((option) => {
          if (settings[game][setting][option] === 0) {
            delete settings[game][setting][option];
          }
        });

        if (
          Object.keys(settings[game][setting]).length === 0 &&
          !Array.isArray(settings[game][setting]) &&
          setting !== 'start_inventory'
        ) {
          errorMessage = `${game} // ${setting} has no values above zero!`;
        }

        // Remove weights from options with only one possibility
        if (
          Object.keys(settings[game][setting]).length === 1 &&
          !Array.isArray(settings[game][setting]) &&
          setting !== 'start_inventory'
        ) {
          settings[game][setting] = Object.keys(settings[game][setting])[0];
        }

        // Remove empty arrays
        else if (
          ['exclude_locations', 'priority_locations', 'local_items', 
          'non_local_items', 'start_hints', 'start_location_hints'].includes(setting) &&
          settings[game][setting].length === 0
        ) {
          delete settings[game][setting];
        }

        // Remove empty start inventory
        else if (
          setting === 'start_inventory' &&
          Object.keys(settings[game]['start_inventory']).length === 0
        ) {
          delete settings[game]['start_inventory'];
        }
      });
    });

    if (Object.keys(settings.game).length === 0) {
      errorMessage = 'You have not chosen a game to play!';
    }

    // Remove weights if there is only one game
    else if (Object.keys(settings.game).length === 1) {
      settings.game = Object.keys(settings.game)[0];
    }

    // If an error occurred, alert the user and do not export the file
    if (errorMessage) {
      userMessage.innerText = errorMessage;
      userMessage.classList.add('visible');
      userMessage.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
      return;
    }

    // If no error occurred, hide the user message if it is visible
    userMessage.classList.remove('visible');
    return settings;
  }

  updateVisibleGames() {
    Object.entries(this.current.game).forEach(([game, weight]) => {
      const gameDiv = document.getElementById(`${game}-div`);
      const gameOption = document.getElementById(`${game}-game-option`);
      if (parseInt(weight, 10) > 0) {
        gameDiv.classList.remove('invisible');
        gameOption.classList.add('jump-link');
        gameOption.addEventListener('click', () => {
          const gameDiv = document.getElementById(`${game}-div`);
          if (gameDiv.classList.contains('invisible')) { return; }
          gameDiv.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
          });
        });
      } else {
        gameDiv.classList.add('invisible');
        gameOption.classList.remove('jump-link');
      }
    });
  }

  updateBaseSetting(event) {
    const setting = event.target.getAttribute('data-setting');
    const option = event.target.getAttribute('data-option');
    const type = event.target.getAttribute('data-type');

    switch(type){
      case 'weight':
        this.current[setting][option] = isNaN(event.target.value) ? event.target.value : parseInt(event.target.value, 10);
        document.getElementById(`${setting}-${option}`).innerText = event.target.value;
        break;
      case 'data':
        this.current[setting] = isNaN(event.target.value) ? event.target.value : parseInt(event.target.value, 10);
        break;
    }

    this.save();
  }

  export() {
    const settings = this.#validateSettings();
    if (!settings) { return; }

    const yamlText = jsyaml.safeDump(settings, { noCompatMode: true }).replaceAll(/'(\d+)':/g, (x, y) => `${y}:`);
    download(`${document.getElementById('player-name').value}.yaml`, yamlText);
  }

  generateGame(raceMode = false) {
    const settings = this.#validateSettings();
    if (!settings) { return; }

    axios.post('/api/generate', {
      weights: { player: JSON.stringify(settings) },
      presetData: { player: JSON.stringify(settings) },
      playerCount: 1,
      spoiler: 3,
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
      userMessage.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
      console.error(error);
    });
  }
}

// Settings for an individual game.
class GameSettings {
  // The WeightedSettings that contains this game's settings. Used to save
  // settings after editing.
  #allSettings;

  // The name of this game.
  name;

  // The data from the server describing the types of settings available for
  // this game, as a JSON-safe blob.
  get data() {
    return this.#allSettings.data.games[this.name];
  }

  // The settings chosen by the user as they'd appear in the YAML file, stored
  // to and retrieved from local storage.
  get current() {
    return this.#allSettings.current[this.name];
  }

  constructor(allSettings, name) {
    this.#allSettings = allSettings;
    this.name = name;
  }

  // Builds and returns the settings UI for this game.
  buildUI() {
    // Create game div, invisible by default
    const gameDiv = document.createElement('div');
    gameDiv.setAttribute('id', `${this.name}-div`);
    gameDiv.classList.add('game-div');
    gameDiv.classList.add('invisible');

    const gameHeader = document.createElement('h2');
    gameHeader.innerText = this.name;
    gameDiv.appendChild(gameHeader);

    const collapseButton = document.createElement('a');
    collapseButton.innerText = '(Collapse)';
    gameDiv.appendChild(collapseButton);

    const expandButton = document.createElement('a');
    expandButton.innerText = '(Expand)';
    expandButton.classList.add('invisible');
    gameDiv.appendChild(expandButton);

    // Sort items and locations alphabetically.
    this.data.gameItems.sort();
    this.data.gameLocations.sort();

    const weightedSettingsDiv = this.#buildWeightedSettingsDiv();
    gameDiv.appendChild(weightedSettingsDiv);

    const itemPoolDiv = this.#buildItemsDiv();
    gameDiv.appendChild(itemPoolDiv);

    const hintsDiv = this.#buildHintsDiv();
    gameDiv.appendChild(hintsDiv);

    const locationsDiv = this.#buildLocationsDiv();
    gameDiv.appendChild(locationsDiv);

    collapseButton.addEventListener('click', () => {
      collapseButton.classList.add('invisible');
      weightedSettingsDiv.classList.add('invisible');
      itemPoolDiv.classList.add('invisible');
      hintsDiv.classList.add('invisible');
      locationsDiv.classList.add('invisible');
      expandButton.classList.remove('invisible');
    });

    expandButton.addEventListener('click', () => {
      collapseButton.classList.remove('invisible');
      weightedSettingsDiv.classList.remove('invisible');
      itemPoolDiv.classList.remove('invisible');
      hintsDiv.classList.remove('invisible');
      locationsDiv.classList.remove('invisible');
      expandButton.classList.add('invisible');
    });

    return gameDiv;
  }

  #buildWeightedSettingsDiv() {
    const settingsWrapper = document.createElement('div');
    settingsWrapper.classList.add('settings-wrapper');

    Object.keys(this.data.gameSettings).forEach((settingName) => {
      const setting = this.data.gameSettings[settingName];
      const settingWrapper = document.createElement('div');
      settingWrapper.classList.add('setting-wrapper');

      const settingNameHeader = document.createElement('h4');
      settingNameHeader.innerText = setting.displayName;
      settingWrapper.appendChild(settingNameHeader);

      const settingDescription = document.createElement('p');
      settingDescription.classList.add('setting-description');
      settingDescription.innerText = setting.description.replace(/(\n)/g, ' ');
      settingWrapper.appendChild(settingDescription);

      switch(setting.type){
        case 'select':
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
            range.setAttribute('data-game', this.name);
            range.setAttribute('data-setting', settingName);
            range.setAttribute('data-option', option.value);
            range.setAttribute('data-type', setting.type);
            range.setAttribute('min', 0);
            range.setAttribute('max', 50);
            range.addEventListener('change', (evt) => this.#updateRangeSetting(evt));
            range.value = this.current[settingName][option.value];
            tdMiddle.appendChild(range);
            tr.appendChild(tdMiddle);

            const tdRight = document.createElement('td');
            tdRight.setAttribute('id', `${this.name}-${settingName}-${option.value}`);
            tdRight.classList.add('td-right');
            tdRight.innerText = range.value;
            tr.appendChild(tdRight);

            tbody.appendChild(tr);
          });

          optionTable.appendChild(tbody);
          settingWrapper.appendChild(optionTable);
          break;

        case 'range':
        case 'special_range':
          const rangeTable = document.createElement('table');
          const rangeTbody = document.createElement('tbody');

          if (((setting.max - setting.min) + 1) < 11) {
            for (let i=setting.min; i <= setting.max; ++i) {
              const tr = document.createElement('tr');
              const tdLeft = document.createElement('td');
              tdLeft.classList.add('td-left');
              tdLeft.innerText = i;
              tr.appendChild(tdLeft);

              const tdMiddle = document.createElement('td');
              tdMiddle.classList.add('td-middle');
              const range = document.createElement('input');
              range.setAttribute('type', 'range');
              range.setAttribute('id', `${this.name}-${settingName}-${i}-range`);
              range.setAttribute('data-game', this.name);
              range.setAttribute('data-setting', settingName);
              range.setAttribute('data-option', i);
              range.setAttribute('min', 0);
              range.setAttribute('max', 50);
              range.addEventListener('change', (evt) => this.#updateRangeSetting(evt));
              range.value = this.current[settingName][i] || 0;
              tdMiddle.appendChild(range);
              tr.appendChild(tdMiddle);

              const tdRight = document.createElement('td');
              tdRight.setAttribute('id', `${this.name}-${settingName}-${i}`)
              tdRight.classList.add('td-right');
              tdRight.innerText = range.value;
              tr.appendChild(tdRight);

              rangeTbody.appendChild(tr);
            }
          } else {
            const hintText = document.createElement('p');
            hintText.classList.add('hint-text');
            hintText.innerHTML = 'This is a range option. You may enter a valid numerical value in the text box ' +
              `below, then press the "Add" button to add a weight for it.<br />Minimum value: ${setting.min}<br />` +
              `Maximum value: ${setting.max}`;

            if (setting.hasOwnProperty('value_names')) {
              hintText.innerHTML += '<br /><br />Certain values have special meaning:';
              Object.keys(setting.value_names).forEach((specialName) => {
                hintText.innerHTML += `<br />${specialName}: ${setting.value_names[specialName]}`;
              });
            }

            settingWrapper.appendChild(hintText);

            const addOptionDiv = document.createElement('div');
            addOptionDiv.classList.add('add-option-div');
            const optionInput = document.createElement('input');
            optionInput.setAttribute('id', `${this.name}-${settingName}-option`);
            optionInput.setAttribute('placeholder', `${setting.min} - ${setting.max}`);
            addOptionDiv.appendChild(optionInput);
            const addOptionButton = document.createElement('button');
            addOptionButton.innerText = 'Add';
            addOptionDiv.appendChild(addOptionButton);
            settingWrapper.appendChild(addOptionDiv);
            optionInput.addEventListener('keydown', (evt) => {
              if (evt.key === 'Enter') { addOptionButton.dispatchEvent(new Event('click')); }
            });

            addOptionButton.addEventListener('click', () => {
              const optionInput = document.getElementById(`${this.name}-${settingName}-option`);
              let option = optionInput.value;
              if (!option || !option.trim()) { return; }
              option = parseInt(option, 10);
              if ((option < setting.min) || (option > setting.max)) { return; }
              optionInput.value = '';
              if (document.getElementById(`${this.name}-${settingName}-${option}-range`)) { return; }

              const tr = document.createElement('tr');
              const tdLeft = document.createElement('td');
              tdLeft.classList.add('td-left');
              tdLeft.innerText = option;
              tr.appendChild(tdLeft);

              const tdMiddle = document.createElement('td');
              tdMiddle.classList.add('td-middle');
              const range = document.createElement('input');
              range.setAttribute('type', 'range');
              range.setAttribute('id', `${this.name}-${settingName}-${option}-range`);
              range.setAttribute('data-game', this.name);
              range.setAttribute('data-setting', settingName);
              range.setAttribute('data-option', option);
              range.setAttribute('min', 0);
              range.setAttribute('max', 50);
              range.addEventListener('change', (evt) => this.#updateRangeSetting(evt));
              range.value = this.current[settingName][parseInt(option, 10)];
              tdMiddle.appendChild(range);
              tr.appendChild(tdMiddle);

              const tdRight = document.createElement('td');
              tdRight.setAttribute('id', `${this.name}-${settingName}-${option}`)
              tdRight.classList.add('td-right');
              tdRight.innerText = range.value;
              tr.appendChild(tdRight);

              const tdDelete = document.createElement('td');
              tdDelete.classList.add('td-delete');
              const deleteButton = document.createElement('span');
              deleteButton.classList.add('range-option-delete');
              deleteButton.innerText = '❌';
              deleteButton.addEventListener('click', () => {
                range.value = 0;
                range.dispatchEvent(new Event('change'));
                rangeTbody.removeChild(tr);
              });
              tdDelete.appendChild(deleteButton);
              tr.appendChild(tdDelete);

              rangeTbody.appendChild(tr);

              // Save new option to settings
              range.dispatchEvent(new Event('change'));
            });

            Object.keys(this.current[settingName]).forEach((option) => {
              // These options are statically generated below, and should always appear even if they are deleted
              // from localStorage
              if (['random-low', 'random', 'random-high'].includes(option)) { return; }

              const tr = document.createElement('tr');
                const tdLeft = document.createElement('td');
                tdLeft.classList.add('td-left');
                tdLeft.innerText = option;
                tr.appendChild(tdLeft);

                const tdMiddle = document.createElement('td');
                tdMiddle.classList.add('td-middle');
                const range = document.createElement('input');
                range.setAttribute('type', 'range');
                range.setAttribute('id', `${this.name}-${settingName}-${option}-range`);
                range.setAttribute('data-game', this.name);
                range.setAttribute('data-setting', settingName);
                range.setAttribute('data-option', option);
                range.setAttribute('min', 0);
                range.setAttribute('max', 50);
                range.addEventListener('change', (evt) => this.#updateRangeSetting(evt));
                range.value = this.current[settingName][parseInt(option, 10)];
                tdMiddle.appendChild(range);
                tr.appendChild(tdMiddle);

                const tdRight = document.createElement('td');
                tdRight.setAttribute('id', `${this.name}-${settingName}-${option}`)
                tdRight.classList.add('td-right');
                tdRight.innerText = range.value;
                tr.appendChild(tdRight);

                const tdDelete = document.createElement('td');
                tdDelete.classList.add('td-delete');
                const deleteButton = document.createElement('span');
                deleteButton.classList.add('range-option-delete');
                deleteButton.innerText = '❌';
                deleteButton.addEventListener('click', () => {
                  range.value = 0;
                  const changeEvent = new Event('change');
                  changeEvent.action = 'rangeDelete';
                  range.dispatchEvent(changeEvent);
                  rangeTbody.removeChild(tr);
                });
                tdDelete.appendChild(deleteButton);
                tr.appendChild(tdDelete);

                rangeTbody.appendChild(tr);
            });
          }

          ['random', 'random-low', 'random-high'].forEach((option) => {
            const tr = document.createElement('tr');
              const tdLeft = document.createElement('td');
              tdLeft.classList.add('td-left');
              switch(option){
                case 'random':
                  tdLeft.innerText = 'Random';
                  break;
                case 'random-low':
                  tdLeft.innerText = "Random (Low)";
                  break;
                case 'random-high':
                  tdLeft.innerText = "Random (High)";
                  break;
              }
              tr.appendChild(tdLeft);

              const tdMiddle = document.createElement('td');
              tdMiddle.classList.add('td-middle');
              const range = document.createElement('input');
              range.setAttribute('type', 'range');
              range.setAttribute('id', `${this.name}-${settingName}-${option}-range`);
              range.setAttribute('data-game', this.name);
              range.setAttribute('data-setting', settingName);
              range.setAttribute('data-option', option);
              range.setAttribute('min', 0);
              range.setAttribute('max', 50);
              range.addEventListener('change', (evt) => this.#updateRangeSetting(evt));
              range.value = this.current[settingName][option];
              tdMiddle.appendChild(range);
              tr.appendChild(tdMiddle);

              const tdRight = document.createElement('td');
              tdRight.setAttribute('id', `${this.name}-${settingName}-${option}`)
              tdRight.classList.add('td-right');
              tdRight.innerText = range.value;
              tr.appendChild(tdRight);
              rangeTbody.appendChild(tr);
          });

          rangeTable.appendChild(rangeTbody);
          settingWrapper.appendChild(rangeTable);
          break;

        case 'items-list':
          const itemsList = document.createElement('div');
          itemsList.classList.add('simple-list');

          Object.values(this.data.gameItems).forEach((item) => {
            const itemRow = document.createElement('div');
            itemRow.classList.add('list-row');

            const itemLabel = document.createElement('label');
            itemLabel.setAttribute('for', `${this.name}-${settingName}-${item}`)

            const itemCheckbox = document.createElement('input');
            itemCheckbox.setAttribute('id', `${this.name}-${settingName}-${item}`);
            itemCheckbox.setAttribute('type', 'checkbox');
            itemCheckbox.setAttribute('data-game', this.name);
            itemCheckbox.setAttribute('data-setting', settingName);
            itemCheckbox.setAttribute('data-option', item.toString());
            itemCheckbox.addEventListener('change', (evt) => this.#updateListSetting(evt));
            if (this.current[settingName].includes(item)) {
              itemCheckbox.setAttribute('checked', '1');
            }

            const itemName = document.createElement('span');
            itemName.innerText = item.toString();

            itemLabel.appendChild(itemCheckbox);
            itemLabel.appendChild(itemName);

            itemRow.appendChild(itemLabel);
            itemsList.appendChild((itemRow));
          });

          settingWrapper.appendChild(itemsList);
          break;

        case 'locations-list':
          const locationsList = document.createElement('div');
          locationsList.classList.add('simple-list');

          Object.values(this.data.gameLocations).forEach((location) => {
            const locationRow = document.createElement('div');
            locationRow.classList.add('list-row');

            const locationLabel = document.createElement('label');
            locationLabel.setAttribute('for', `${this.name}-${settingName}-${location}`)

            const locationCheckbox = document.createElement('input');
            locationCheckbox.setAttribute('id', `${this.name}-${settingName}-${location}`);
            locationCheckbox.setAttribute('type', 'checkbox');
            locationCheckbox.setAttribute('data-game', this.name);
            locationCheckbox.setAttribute('data-setting', settingName);
            locationCheckbox.setAttribute('data-option', location.toString());
            locationCheckbox.addEventListener('change', (evt) => this.#updateListSetting(evt));
            if (this.current[settingName].includes(location)) {
              locationCheckbox.setAttribute('checked', '1');
            }

            const locationName = document.createElement('span');
            locationName.innerText = location.toString();

            locationLabel.appendChild(locationCheckbox);
            locationLabel.appendChild(locationName);

            locationRow.appendChild(locationLabel);
            locationsList.appendChild((locationRow));
          });

          settingWrapper.appendChild(locationsList);
          break;

        case 'custom-list':
          const customList = document.createElement('div');
          customList.classList.add('simple-list');

          Object.values(this.data.gameSettings[settingName].options).forEach((listItem) => {
            const customListRow = document.createElement('div');
            customListRow.classList.add('list-row');

            const customItemLabel = document.createElement('label');
            customItemLabel.setAttribute('for', `${this.name}-${settingName}-${listItem}`)

            const customItemCheckbox = document.createElement('input');
            customItemCheckbox.setAttribute('id', `${this.name}-${settingName}-${listItem}`);
            customItemCheckbox.setAttribute('type', 'checkbox');
            customItemCheckbox.setAttribute('data-game', this.name);
            customItemCheckbox.setAttribute('data-setting', settingName);
            customItemCheckbox.setAttribute('data-option', listItem.toString());
            customItemCheckbox.addEventListener('change', (evt) => this.#updateListSetting(evt));
            if (this.current[settingName].includes(listItem)) {
              customItemCheckbox.setAttribute('checked', '1');
            }

            const customItemName = document.createElement('span');
            customItemName.innerText = listItem.toString();

            customItemLabel.appendChild(customItemCheckbox);
            customItemLabel.appendChild(customItemName);

            customListRow.appendChild(customItemLabel);
            customList.appendChild((customListRow));
          });

          settingWrapper.appendChild(customList);
          break;

        default:
          console.error(`Unknown setting type for ${this.name} setting ${settingName}: ${setting.type}`);
          return;
      }

      settingsWrapper.appendChild(settingWrapper);
    });

    return settingsWrapper;
  }

  #buildItemsDiv() {
    const itemsDiv = document.createElement('div');
    itemsDiv.classList.add('items-div');

    const itemsDivHeader = document.createElement('h3');
    itemsDivHeader.innerText = 'Item Pool';
    itemsDiv.appendChild(itemsDivHeader);

    const itemsDescription = document.createElement('p');
    itemsDescription.classList.add('setting-description');
    itemsDescription.innerText = 'Choose if you would like to start with items, or control if they are placed in ' +
      'your seed or someone else\'s.';
    itemsDiv.appendChild(itemsDescription);

    const itemsHint = document.createElement('p');
    itemsHint.classList.add('hint-text');
    itemsHint.innerText = 'Drag and drop items from one box to another.';
    itemsDiv.appendChild(itemsHint);

    const itemsWrapper = document.createElement('div');
    itemsWrapper.classList.add('items-wrapper');

    const itemDragoverHandler = (evt) => evt.preventDefault();
    const itemDropHandler = (evt) => this.#itemDropHandler(evt);

    // Create container divs for each category
    const availableItemsWrapper = document.createElement('div');
    availableItemsWrapper.classList.add('item-set-wrapper');
    availableItemsWrapper.innerText = 'Available Items';
    const availableItems = document.createElement('div');
    availableItems.classList.add('item-container');
    availableItems.setAttribute('id', `${this.name}-available_items`);
    availableItems.addEventListener('dragover', itemDragoverHandler);
    availableItems.addEventListener('drop', itemDropHandler);

    const startInventoryWrapper = document.createElement('div');
    startInventoryWrapper.classList.add('item-set-wrapper');
    startInventoryWrapper.innerText = 'Start Inventory';
    const startInventory = document.createElement('div');
    startInventory.classList.add('item-container');
    startInventory.setAttribute('id', `${this.name}-start_inventory`);
    startInventory.setAttribute('data-setting', 'start_inventory');
    startInventory.addEventListener('dragover', itemDragoverHandler);
    startInventory.addEventListener('drop', itemDropHandler);

    const localItemsWrapper = document.createElement('div');
    localItemsWrapper.classList.add('item-set-wrapper');
    localItemsWrapper.innerText = 'Local Items';
    const localItems = document.createElement('div');
    localItems.classList.add('item-container');
    localItems.setAttribute('id', `${this.name}-local_items`);
    localItems.setAttribute('data-setting', 'local_items')
    localItems.addEventListener('dragover', itemDragoverHandler);
    localItems.addEventListener('drop', itemDropHandler);

    const nonLocalItemsWrapper = document.createElement('div');
    nonLocalItemsWrapper.classList.add('item-set-wrapper');
    nonLocalItemsWrapper.innerText = 'Non-Local Items';
    const nonLocalItems = document.createElement('div');
    nonLocalItems.classList.add('item-container');
    nonLocalItems.setAttribute('id', `${this.name}-non_local_items`);
    nonLocalItems.setAttribute('data-setting', 'non_local_items');
    nonLocalItems.addEventListener('dragover', itemDragoverHandler);
    nonLocalItems.addEventListener('drop', itemDropHandler);

    // Populate the divs
    this.data.gameItems.forEach((item) => {
      if (Object.keys(this.current.start_inventory).includes(item)){
        const itemDiv = this.#buildItemQtyDiv(item);
        itemDiv.setAttribute('data-setting', 'start_inventory');
        startInventory.appendChild(itemDiv);
      } else if (this.current.local_items.includes(item)) {
        const itemDiv = this.#buildItemDiv(item);
        itemDiv.setAttribute('data-setting', 'local_items');
        localItems.appendChild(itemDiv);
      } else if (this.current.non_local_items.includes(item)) {
        const itemDiv = this.#buildItemDiv(item);
        itemDiv.setAttribute('data-setting', 'non_local_items');
        nonLocalItems.appendChild(itemDiv);
      } else {
        const itemDiv = this.#buildItemDiv(item);
        availableItems.appendChild(itemDiv);
      }
    });

    availableItemsWrapper.appendChild(availableItems);
    startInventoryWrapper.appendChild(startInventory);
    localItemsWrapper.appendChild(localItems);
    nonLocalItemsWrapper.appendChild(nonLocalItems);
    itemsWrapper.appendChild(availableItemsWrapper);
    itemsWrapper.appendChild(startInventoryWrapper);
    itemsWrapper.appendChild(localItemsWrapper);
    itemsWrapper.appendChild(nonLocalItemsWrapper);
    itemsDiv.appendChild(itemsWrapper);
    return itemsDiv;
  }

  #buildItemDiv(item) {
    const itemDiv = document.createElement('div');
    itemDiv.classList.add('item-div');
    itemDiv.setAttribute('id', `${this.name}-${item}`);
    itemDiv.setAttribute('data-game', this.name);
    itemDiv.setAttribute('data-item', item);
    itemDiv.setAttribute('draggable', 'true');
    itemDiv.innerText = item;
    itemDiv.addEventListener('dragstart', (evt) => {
      evt.dataTransfer.setData('text/plain', itemDiv.getAttribute('id'));
    });
    return itemDiv;
  }

  #buildItemQtyDiv(item) {
    const itemQtyDiv = document.createElement('div');
    itemQtyDiv.classList.add('item-qty-div');
    itemQtyDiv.setAttribute('id', `${this.name}-${item}`);
    itemQtyDiv.setAttribute('data-game', this.name);
    itemQtyDiv.setAttribute('data-item', item);
    itemQtyDiv.setAttribute('draggable', 'true');
    itemQtyDiv.innerText = item;

    const inputWrapper = document.createElement('div');
    inputWrapper.classList.add('item-qty-input-wrapper')

    const itemQty = document.createElement('input');
    itemQty.setAttribute('value', this.current.start_inventory.hasOwnProperty(item) ?
      this.current.start_inventory[item] : '1');
    itemQty.setAttribute('data-game', this.name);
    itemQty.setAttribute('data-setting', 'start_inventory');
    itemQty.setAttribute('data-option', item);
    itemQty.setAttribute('maxlength', '3');
    itemQty.addEventListener('keyup', (evt) => {
      evt.target.value = isNaN(parseInt(evt.target.value)) ? 0 : parseInt(evt.target.value);
      this.#updateItemSetting(evt);
    });
    inputWrapper.appendChild(itemQty);
    itemQtyDiv.appendChild(inputWrapper);

    itemQtyDiv.addEventListener('dragstart', (evt) => {
      evt.dataTransfer.setData('text/plain', itemQtyDiv.getAttribute('id'));
    });
    return itemQtyDiv;
  }

  #itemDropHandler(evt) {
    evt.preventDefault();
    const sourceId = evt.dataTransfer.getData('text/plain');
    const sourceDiv = document.getElementById(sourceId);

    const item = sourceDiv.getAttribute('data-item');

    const oldSetting = sourceDiv.hasAttribute('data-setting') ? sourceDiv.getAttribute('data-setting') : null;
    const newSetting = evt.target.hasAttribute('data-setting') ? evt.target.getAttribute('data-setting') : null;

    const itemDiv = newSetting === 'start_inventory' ? this.#buildItemQtyDiv(item) : this.#buildItemDiv(item);

    if (oldSetting) {
      if (oldSetting === 'start_inventory') {
        if (this.current[oldSetting].hasOwnProperty(item)) {
          delete this.current[oldSetting][item];
        }
      } else {
        if (this.current[oldSetting].includes(item)) {
          this.current[oldSetting].splice(this.current[oldSetting].indexOf(item), 1);
        }
      }
    }

    if (newSetting) {
      itemDiv.setAttribute('data-setting', newSetting);
      document.getElementById(`${this.name}-${newSetting}`).appendChild(itemDiv);
      if (newSetting === 'start_inventory') {
        this.current[newSetting][item] = 1;
      } else {
        if (!this.current[newSetting].includes(item)){
          this.current[newSetting].push(item);
        }
      }
    } else {
      // No setting was assigned, this item has been removed from the settings
      document.getElementById(`${this.name}-available_items`).appendChild(itemDiv);
    }

    // Remove the source drag object
    sourceDiv.parentElement.removeChild(sourceDiv);

    // Save the updated settings
    this.save();
  }

  #buildHintsDiv() {
    const hintsDiv = document.createElement('div');
    hintsDiv.classList.add('hints-div');
    const hintsHeader = document.createElement('h3');
    hintsHeader.innerText = 'Item & Location Hints';
    hintsDiv.appendChild(hintsHeader);
    const hintsDescription = document.createElement('p');
    hintsDescription.classList.add('setting-description');
    hintsDescription.innerText = 'Choose any items or locations to begin the game with the knowledge of where those ' +
      ' items are, or what those locations contain.';
    hintsDiv.appendChild(hintsDescription);

    const itemHintsContainer = document.createElement('div');
    itemHintsContainer.classList.add('hints-container');

    // Item Hints
    const itemHintsWrapper = document.createElement('div');
    itemHintsWrapper.classList.add('hints-wrapper');
    itemHintsWrapper.innerText = 'Starting Item Hints';

    const itemHintsDiv = document.createElement('div');
    itemHintsDiv.classList.add('simple-list');
    this.data.gameItems.forEach((item) => {
      const itemRow = document.createElement('div');
      itemRow.classList.add('list-row');

      const itemLabel = document.createElement('label');
      itemLabel.setAttribute('for', `${this.name}-start_hints-${item}`);

      const itemCheckbox = document.createElement('input');
      itemCheckbox.setAttribute('type', 'checkbox');
      itemCheckbox.setAttribute('id', `${this.name}-start_hints-${item}`);
      itemCheckbox.setAttribute('data-game', this.name);
      itemCheckbox.setAttribute('data-setting', 'start_hints');
      itemCheckbox.setAttribute('data-option', item);
      if (this.current.start_hints.includes(item)) {
        itemCheckbox.setAttribute('checked', 'true');
      }
      itemCheckbox.addEventListener('change', (evt) => this.#updateListSetting(evt));
      itemLabel.appendChild(itemCheckbox);

      const itemName = document.createElement('span');
      itemName.innerText = item;
      itemLabel.appendChild(itemName);

      itemRow.appendChild(itemLabel);
      itemHintsDiv.appendChild(itemRow);
    });

    itemHintsWrapper.appendChild(itemHintsDiv);
    itemHintsContainer.appendChild(itemHintsWrapper);

    // Starting Location Hints
    const locationHintsWrapper = document.createElement('div');
    locationHintsWrapper.classList.add('hints-wrapper');
    locationHintsWrapper.innerText = 'Starting Location Hints';

    const locationHintsDiv = document.createElement('div');
    locationHintsDiv.classList.add('simple-list');
    this.data.gameLocations.forEach((location) => {
      const locationRow = document.createElement('div');
      locationRow.classList.add('list-row');

      const locationLabel = document.createElement('label');
      locationLabel.setAttribute('for', `${this.name}-start_location_hints-${location}`);

      const locationCheckbox = document.createElement('input');
      locationCheckbox.setAttribute('type', 'checkbox');
      locationCheckbox.setAttribute('id', `${this.name}-start_location_hints-${location}`);
      locationCheckbox.setAttribute('data-game', this.name);
      locationCheckbox.setAttribute('data-setting', 'start_location_hints');
      locationCheckbox.setAttribute('data-option', location);
      if (this.current.start_location_hints.includes(location)) {
        locationCheckbox.setAttribute('checked', '1');
      }
      locationCheckbox.addEventListener('change', (evt) => this.#updateListSetting(evt));
      locationLabel.appendChild(locationCheckbox);

      const locationName = document.createElement('span');
      locationName.innerText = location;
      locationLabel.appendChild(locationName);

      locationRow.appendChild(locationLabel);
      locationHintsDiv.appendChild(locationRow);
    });

    locationHintsWrapper.appendChild(locationHintsDiv);
    itemHintsContainer.appendChild(locationHintsWrapper);

    hintsDiv.appendChild(itemHintsContainer);
    return hintsDiv;
  }

  #buildLocationsDiv() {
    const locationsDiv = document.createElement('div');
    locationsDiv.classList.add('locations-div');
    const locationsHeader = document.createElement('h3');
    locationsHeader.innerText = 'Priority & Exclusion Locations';
    locationsDiv.appendChild(locationsHeader);
    const locationsDescription = document.createElement('p');
    locationsDescription.classList.add('setting-description');
    locationsDescription.innerText = 'Priority locations guarantee a progression item will be placed there while ' +
      'excluded locations will not contain progression or useful items.';
    locationsDiv.appendChild(locationsDescription);

    const locationsContainer = document.createElement('div');
    locationsContainer.classList.add('locations-container');

    // Priority Locations
    const priorityLocationsWrapper = document.createElement('div');
    priorityLocationsWrapper.classList.add('locations-wrapper');
    priorityLocationsWrapper.innerText = 'Priority Locations';

    const priorityLocationsDiv = document.createElement('div');
    priorityLocationsDiv.classList.add('simple-list');
    this.data.gameLocations.forEach((location) => {
      const locationRow = document.createElement('div');
      locationRow.classList.add('list-row');

      const locationLabel = document.createElement('label');
      locationLabel.setAttribute('for', `${this.name}-priority_locations-${location}`);

      const locationCheckbox = document.createElement('input');
      locationCheckbox.setAttribute('type', 'checkbox');
      locationCheckbox.setAttribute('id', `${this.name}-priority_locations-${location}`);
      locationCheckbox.setAttribute('data-game', this.name);
      locationCheckbox.setAttribute('data-setting', 'priority_locations');
      locationCheckbox.setAttribute('data-option', location);
      if (this.current.priority_locations.includes(location)) {
        locationCheckbox.setAttribute('checked', '1');
      }
      locationCheckbox.addEventListener('change', (evt) => this.#updateListSetting(evt));
      locationLabel.appendChild(locationCheckbox);

      const locationName = document.createElement('span');
      locationName.innerText = location;
      locationLabel.appendChild(locationName);

      locationRow.appendChild(locationLabel);
      priorityLocationsDiv.appendChild(locationRow);
    });

    priorityLocationsWrapper.appendChild(priorityLocationsDiv);
    locationsContainer.appendChild(priorityLocationsWrapper);

    // Exclude Locations
    const excludeLocationsWrapper = document.createElement('div');
    excludeLocationsWrapper.classList.add('locations-wrapper');
    excludeLocationsWrapper.innerText = 'Exclude Locations';

    const excludeLocationsDiv = document.createElement('div');
    excludeLocationsDiv.classList.add('simple-list');
    this.data.gameLocations.forEach((location) => {
      const locationRow = document.createElement('div');
      locationRow.classList.add('list-row');

      const locationLabel = document.createElement('label');
      locationLabel.setAttribute('for', `${this.name}-exclude_locations-${location}`);

      const locationCheckbox = document.createElement('input');
      locationCheckbox.setAttribute('type', 'checkbox');
      locationCheckbox.setAttribute('id', `${this.name}-exclude_locations-${location}`);
      locationCheckbox.setAttribute('data-game', this.name);
      locationCheckbox.setAttribute('data-setting', 'exclude_locations');
      locationCheckbox.setAttribute('data-option', location);
      if (this.current.exclude_locations.includes(location)) {
        locationCheckbox.setAttribute('checked', '1');
      }
      locationCheckbox.addEventListener('change', (evt) => this.#updateListSetting(evt));
      locationLabel.appendChild(locationCheckbox);

      const locationName = document.createElement('span');
      locationName.innerText = location;
      locationLabel.appendChild(locationName);

      locationRow.appendChild(locationLabel);
      excludeLocationsDiv.appendChild(locationRow);
    });

    excludeLocationsWrapper.appendChild(excludeLocationsDiv);
    locationsContainer.appendChild(excludeLocationsWrapper);

    locationsDiv.appendChild(locationsContainer);
    return locationsDiv;
  }

  #updateRangeSetting(evt) {
    const setting = evt.target.getAttribute('data-setting');
    const option = evt.target.getAttribute('data-option');
    document.getElementById(`${this.name}-${setting}-${option}`).innerText = evt.target.value;
    if (evt.action && evt.action === 'rangeDelete') {
      delete this.current[setting][option];
    } else {
      this.current[setting][option] = parseInt(evt.target.value, 10);
    }
    this.save();
  }

  #updateListSetting(evt) {
    const setting = evt.target.getAttribute('data-setting');
    const option = evt.target.getAttribute('data-option');

    if (evt.target.checked) {
      // If the option is to be enabled and it is already enabled, do nothing
      if (this.current[setting].includes(option)) { return; }

      this.current[setting].push(option);
    } else {
      // If the option is to be disabled and it is already disabled, do nothing
      if (!this.current[setting].includes(option)) { return; }

      this.current[setting].splice(this.current[setting].indexOf(option), 1);
    }
    this.save();
  }

  #updateItemSetting(evt) {
    const setting = evt.target.getAttribute('data-setting');
    const option = evt.target.getAttribute('data-option');
    if (setting === 'start_inventory') {
      this.current[setting][option] = evt.target.value.trim() ? parseInt(evt.target.value) : 0;
    } else {
      this.current[setting][option] = isNaN(evt.target.value) ?
        evt.target.value : parseInt(evt.target.value, 10);
    }
    this.save();
  }

  // Saves the current settings to local storage.
  save() {
    this.#allSettings.save();
  }
}

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
