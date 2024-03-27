import {loadOptions, BaseGameOptions} from './options.js';

window.addEventListener('load', async () => {
  const data = await loadOptions('/static/generated/weighted-options.json', 'weighted-settings');

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

const fetchOptionData = () => fetch(new Request(`${window.location.origin}/static/generated/weighted-options.json`))
      .then(response => response.json());

// The weighted settings across all games.
class WeightedSettings {
  // The data from the server describing the types of settings available for
  // each game, as a JSON-safe blob.
  data;

  current;

  // A record mapping game names to the associated GameOptions.
  games;

  constructor(data) {
    this.data = data;
    this.current = JSON.parse(localStorage.getItem('weighted-settings'));
    this.games = Object.keys(this.data.games).map((game) => new GameOptions(this, game));
    if (this.current) { return; }

    // Transfer base options directly
    this.current = {...this.data.baseOptions};

    // Set options per game
    for (let game of Object.keys(this.data.games)) {
      // Initialize game object
      this.current[game] = {};

      // Transfer game settings
      for (let gameSetting of Object.keys(this.data.games[game].gameOptions)){
        this.current[game][gameSetting] = {};

        const setting = this.data.games[game].gameOptions[gameSetting];
        switch(setting.type){
          case 'select':
            setting.options.forEach((option) => {
              this.current[game][gameSetting][option.value] =
                (setting.hasOwnProperty('defaultValue') && setting.defaultValue === option.value) ? 25 : 0;
            });
            break;
          case 'range':
          case 'named_range':
            this.current[game][gameSetting]['random'] = 0;
            this.current[game][gameSetting]['random-low'] = 0;
            this.current[game][gameSetting]['random-middle'] = 0;
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
    if (
      !settings.name ||
      settings.name.toString().trim().length === 0 ||
      settings.name.toString().toLowerCase().trim() === 'player'
    ) {
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

// Weighted options for an individual game.
class GameOptions extends BaseGameOptions {
  // The WeightedSettings that contains this game's settings. Used to save
  // settings after editing.
  #allSettings;

  get data() {
    return this.#allSettings.data.games[this.name];
  }

  get current() {
    return this.#allSettings.current[this.name];
  }

  constructor(allSettings, name) {
    super(name);
    this.#allSettings = allSettings;
  }

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
    this.buildBaseUI(weightedSettingsDiv);
    gameDiv.appendChild(weightedSettingsDiv);

    collapseButton.addEventListener('click', () => {
      collapseButton.classList.add('invisible');
      weightedSettingsDiv.classList.add('invisible');
      expandButton.classList.remove('invisible');
    });

    expandButton.addEventListener('click', () => {
      collapseButton.classList.remove('invisible');
      weightedSettingsDiv.classList.remove('invisible');
      expandButton.classList.add('invisible');
    });

    return gameDiv;
  }

  #buildWeightedSettingsDiv() {
    const settingsWrapper = document.createElement('div');
    settingsWrapper.classList.add('settings-wrapper');

    Object.keys(this.data.gameOptions).forEach((settingName) => {
      const setting = this.data.gameOptions[settingName];
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
        case 'named_range':
          const rangeTable = document.createElement('table');
          const rangeTbody = document.createElement('tbody');

          const hintText = document.createElement('p');
          hintText.classList.add('hint-text');
          hintText.innerHTML = 'This is a range option. You may enter a valid numerical value in the text box ' +
            `below, then press the "Add" button to add a weight for it.<br /><br />Accepted values:<br />` +
            `Normal range: ${setting.min} - ${setting.max}`;

          const acceptedValuesOutsideRange = [];
          if (setting.hasOwnProperty('value_names')) {
            Object.keys(setting.value_names).forEach((specialName) => {
              if (
                (setting.value_names[specialName] < setting.min) ||
                (setting.value_names[specialName] > setting.max)
              ) {
                hintText.innerHTML += `<br />${specialName}: ${setting.value_names[specialName]}`;
                acceptedValuesOutsideRange.push(setting.value_names[specialName]);
              }
            });

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
          let placeholderText = `${setting.min} - ${setting.max}`;
          acceptedValuesOutsideRange.forEach((aVal) => placeholderText += `, ${aVal}`);
          optionInput.setAttribute('placeholder', placeholderText);
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

            let optionAcceptable = false;
            if ((option >= setting.min) && (option <= setting.max)) {
              optionAcceptable = true;
            }
            if (setting.hasOwnProperty('value_names') && Object.values(setting.value_names).includes(option)){
              optionAcceptable = true;
            }
            if (!optionAcceptable) { return; }

            optionInput.value = '';
            if (document.getElementById(`${this.name}-${settingName}-${option}-range`)) { return; }

            const tr = document.createElement('tr');
            const tdLeft = document.createElement('td');
            tdLeft.classList.add('td-left');
            tdLeft.innerText = option;
            if (
              setting.hasOwnProperty('value_names') &&
              Object.values(setting.value_names).includes(parseInt(option, 10))
            ) {
              const optionName = Object.keys(setting.value_names).find(
                (key) => setting.value_names[key] === parseInt(option, 10)
              );
              tdLeft.innerText += ` [${optionName}]`;
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
            if (['random', 'random-low', 'random-middle', 'random-high'].includes(option)) { return; }

            const tr = document.createElement('tr');
            const tdLeft = document.createElement('td');
            tdLeft.classList.add('td-left');
            tdLeft.innerText = option;
            if (
              setting.hasOwnProperty('value_names') &&
              Object.values(setting.value_names).includes(parseInt(option, 10))
            ) {
              const optionName = Object.keys(setting.value_names).find(
                (key) => setting.value_names[key] === parseInt(option, 10)
              );
              tdLeft.innerText += ` [${optionName}]`;
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

          ['random', 'random-low', 'random-middle', 'random-high'].forEach((option) => {
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
                case 'random-middle':
                  tdLeft.innerText = 'Random (Middle)';
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
          const itemsList = this.buildItemsDiv(settingName);
          settingWrapper.appendChild(itemsList);
          break;

        case 'locations-list':
          const locationsList = this.buildLocationsDiv(settingName);
          settingWrapper.appendChild(locationsList);
          break;

        case 'custom-list':
          const customList = this.buildListDiv(settingName, this.data.gameOptions[settingName].options);
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
