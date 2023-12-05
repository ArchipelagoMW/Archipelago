import {download, loadOptions, showUserMessage, BaseGameOptions} from './options.js';

let gameName = null;

window.addEventListener('load', async () => {
  gameName = document.getElementById('player-options').getAttribute('data-game');

  // Update game name on page
  document.getElementById('game-name').innerText = gameName;

  try {
    const data = await loadOptions(`/static/generated/player-options/${gameName}.json`, gameName);

    // Page setup
    const options = new GameOptions(data, gameName);
    options.buildUI();
    adjustHeaderWidth();

    // Event listeners
    document.getElementById('export-options').addEventListener('click', () => options.export());
    document.getElementById('generate-race')
        .addEventListener('click', () => options.generateGame(true));
    document.getElementById('generate-game')
        .addEventListener('click', () => options.generateGame());

    // Name input field
    const nameInput = document.getElementById('player-name');
    nameInput.addEventListener('keyup', (event) => options.updateBaseOption(event));
    nameInput.value = options.playerName;

    // Presets
    if (!localStorage.getItem(`${gameName}-preset`)) {
      localStorage.setItem(`${gameName}-preset`, '__default');
    }

    const presetSelect = document.getElementById('game-options-preset');
    presetSelect.addEventListener('change', (event) => options.setPresets(event.target.value));
    for (const preset in data['presetOptions']) {
      const presetOption = document.createElement('option');
      presetOption.innerText = preset;
      presetSelect.appendChild(presetOption);
    }
    presetSelect.value = localStorage.getItem(`${gameName}-preset`);
    data['presetOptions']['__default'] = {};
  } catch (e) {
    console.error(e);
    const url = new URL(window.location.href);
    window.location.replace(`${window.origin}/page-not-found`);
  }
});

// Non-weighted options for the sole game displayed on the page.
class GameOptions extends BaseGameOptions {
  // The data from the server describing the types of settings available for
  // this game, as a JSON-safe blob.
  #data;

  // The settings chosen by the user as they'd appear in the YAML file, stored
  // to and retrieved from local storage.
  #current;

  get data() {
    return this.#data;
  }

  get current() {
    return this.#current[this.name];
  }

  // The name of the player for this game.
  get playerName() {
    return this.#current.name;
  }

  constructor(data, name) {
    super(name);
    this.#data = data;
    this.#current = JSON.parse(localStorage.getItem(name)) ?? {
      [name]: Object.fromEntries(
        Object.entries(data.gameOptions)
            .map(([name, option]) => [name, option.defaultValue])
      ),
      ...data.baseOptions,
    };
  }

  buildUI() {
    // Game Options
    // Divide options that can be rendered small into two columns
    const entries = Object.entries(this.data.gameOptions);
    const leftOptions = Object.fromEntries(entries.slice(0, Math.floor(entries.length / 2)));
    const rightOptions = Object.fromEntries(entries.slice(Math.floor(entries.length / 2) + 1));
    document.getElementById('game-options-left').appendChild(this.#buildSmallOptions(leftOptions));
    document.getElementById('game-options-right')
        .appendChild(this.#buildSmallOptions(rightOptions));

    this.buildBaseUI(document.getElementById('game-options-center'));
  }

  save() {
    localStorage.setItem(this.name, JSON.stringify(this.#current));
  }

  #buildSmallOptions(options, romOpts = false) {
    const table = document.createElement('table');
    const tbody = document.createElement('tbody');

    Object.keys(options).forEach((option) => {
      const tr = document.createElement('tr');

      // td Left
      const tdl = document.createElement('td');
      const label = document.createElement('label');
      label.textContent = `${options[option].displayName}: `;
      label.setAttribute('for', option);

      const questionSpan = document.createElement('span');
      questionSpan.classList.add('interactive');
      questionSpan.setAttribute('data-tooltip', options[option].description);
      questionSpan.innerText = '(?)';

      label.appendChild(questionSpan);
      tdl.appendChild(label);
      tr.appendChild(tdl);

      // td Right
      const tdr = document.createElement('td');
      let element = null;

      const randomButton = document.createElement('button');

      switch(options[option].type) {
        case 'select':
          element = document.createElement('div');
          element.classList.add('select-container');
          let select = document.createElement('select');
          select.setAttribute('id', option);
          select.setAttribute('data-key', option);
          if (romOpts) { select.setAttribute('data-romOpt', '1'); }
          options[option].options.forEach((opt) => {
            const optionElement = document.createElement('option');
            optionElement.setAttribute('value', opt.value);
            optionElement.innerText = opt.name;

            if ((isNaN(this.current[option]) &&
              (parseInt(opt.value, 10) === parseInt(this.current[option]))) ||
              (opt.value === this.current[option]))
            {
              optionElement.selected = true;
            }
            select.appendChild(optionElement);
          });
          select.addEventListener('change', (event) => this.#updateGameOption(event.target));
          element.appendChild(select);

          // Randomize button
          randomButton.innerText = '🎲';
          randomButton.classList.add('randomize-button');
          randomButton.setAttribute('data-key', option);
          randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
          randomButton.addEventListener('click', (event) => toggleRandomize(event, select));
          if (this.current[option] === 'random') {
            randomButton.classList.add('active');
            select.disabled = true;
          }

          element.appendChild(randomButton);
          break;

        case 'range':
          element = document.createElement('div');
          element.classList.add('range-container');

          let range = document.createElement('input');
          range.setAttribute('id', option);
          range.setAttribute('type', 'range');
          range.setAttribute('data-key', option);
          range.setAttribute('min', options[option].min);
          range.setAttribute('max', options[option].max);
          range.value = this.current[option];
          range.addEventListener('change', (event) => {
            document.getElementById(`${option}-value`).innerText = event.target.value;
            this.#updateGameOption(event.target);
          });
          element.appendChild(range);

          let rangeVal = document.createElement('span');
          rangeVal.classList.add('range-value');
          rangeVal.setAttribute('id', `${option}-value`);
          rangeVal.innerText = this.current[option] !== 'random' ?
            this.current[option] : options[option].defaultValue;
          element.appendChild(rangeVal);

          // Randomize button
          randomButton.innerText = '🎲';
          randomButton.classList.add('randomize-button');
          randomButton.setAttribute('data-key', option);
          randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
          randomButton.addEventListener('click', (event) => toggleRandomize(event, range));
          if (this.current[option] === 'random') {
            randomButton.classList.add('active');
            range.disabled = true;
          }

          element.appendChild(randomButton);
          break;

        case 'named_range':
          element = document.createElement('div');
          element.classList.add('named-range-container');

          // Build the select element
          let namedRangeSelect = document.createElement('select');
          namedRangeSelect.setAttribute('data-key', option);
          Object.keys(options[option].value_names).forEach((presetName) => {
            let presetOption = document.createElement('option');
            presetOption.innerText = presetName;
            presetOption.value = options[option].value_names[presetName];
            const words = presetOption.innerText.split('_');
            for (let i = 0; i < words.length; i++) {
              words[i] = words[i][0].toUpperCase() + words[i].substring(1);
            }
            presetOption.innerText = words.join(' ');
            namedRangeSelect.appendChild(presetOption);
          });
          let customOption = document.createElement('option');
          customOption.innerText = 'Custom';
          customOption.value = 'custom';
          customOption.selected = true;
          namedRangeSelect.appendChild(customOption);
          if (Object.values(options[option].value_names).includes(Number(this.current[option]))) {
            namedRangeSelect.value = Number(this.current[option]);
          }

          // Build range element
          let namedRangeWrapper = document.createElement('div');
          namedRangeWrapper.classList.add('named-range-wrapper');
          let namedRange = document.createElement('input');
          namedRange.setAttribute('type', 'range');
          namedRange.setAttribute('data-key', option);
          namedRange.setAttribute('min', options[option].min);
          namedRange.setAttribute('max', options[option].max);
          namedRange.value = this.current[option];

          // Build rage value element
          let namedRangeVal = document.createElement('span');
          namedRangeVal.classList.add('range-value');
          namedRangeVal.setAttribute('id', `${option}-value`);
          namedRangeVal.innerText = this.current[option] !== 'random' ?
            this.current[option] : options[option].defaultValue;

          // Configure select event listener
          namedRangeSelect.addEventListener('change', (event) => {
            if (event.target.value === 'custom') { return; }

            // Update range slider
            namedRange.value = event.target.value;
            document.getElementById(`${option}-value`).innerText = event.target.value;
            this.#updateGameOption(event.target);
          });

          // Configure range event handler
          namedRange.addEventListener('change', (event) => {
            // Update select element
            namedRangeSelect.value =
              (Object.values(options[option].value_names).includes(parseInt(event.target.value))) ?
              parseInt(event.target.value) : 'custom';
            document.getElementById(`${option}-value`).innerText = event.target.value;
            this.#updateGameOption(event.target);
          });

          element.appendChild(namedRangeSelect);
          namedRangeWrapper.appendChild(namedRange);
          namedRangeWrapper.appendChild(namedRangeVal);
          element.appendChild(namedRangeWrapper);

          // Randomize button
          randomButton.innerText = '🎲';
          randomButton.classList.add('randomize-button');
          randomButton.setAttribute('data-key', option);
          randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
          randomButton.addEventListener('click', (event) => toggleRandomize(
              event, namedRange, namedRangeSelect)
          );
          if (this.current[option] === 'random') {
            randomButton.classList.add('active');
            namedRange.disabled = true;
            namedRangeSelect.disabled = true;
          }

          namedRangeWrapper.appendChild(randomButton);
          break;

        case 'items-list':
          element = this.buildItemsDiv(option);
          break;

        case 'locations-list':
          element = this.buildLocationsDiv(option);
          break;

        case 'custom-list':
          element = this.buildListDiv(option, options[option].options);
          break;

        default:
          console.error(`Ignoring unknown option type: ${options[option].type} with name ${option}`);
          return;
      }

      tdr.appendChild(element);
      tr.appendChild(tdr);
      tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    return table;
  }

  #toggleRandomize(event, inputElement, optionalSelectElement = null) {
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
    this.#updateGameOption(active ? inputElement : randomButton);
  }

  setPresets(presetName) {
    const defaults = this.data.gameOptions;
    const preset = this.data.presetOptions[presetName];

    localStorage.setItem(`${gameName}-preset`, presetName);

    if (!preset) {
      console.error(`No presets defined for preset name: '${presetName}'`);
      return;
    }

    const updateOptionElement = (option, presetValue) => {
      const optionElement = document.querySelector(`#${option}[data-key='${option}']`);
      const randomElement = document.querySelector(`.randomize-button[data-key='${option}']`);

      if (presetValue === 'random') {
        randomElement.classList.add('active');
        optionElement.disabled = true;
        this.#updateGameOption(randomElement, false);
      } else {
        optionElement.value = presetValue;
        randomElement.classList.remove('active');
        optionElement.disabled = undefined;
        this.#updateGameOption(optionElement, false);
      }
    };

    for (const option in defaults) {
      let presetValue = preset[option];
      if (presetValue === undefined) {
        // Using the default value if not set in presets.
        presetValue = defaults[option]['defaultValue'];
      }

      switch (defaults[option].type) {
        case 'range':
          const numberElement = document.querySelector(`#${option}-value`);
          if (presetValue === 'random') {
            numberElement.innerText = defaults[option]['defaultValue'] === 'random'
                ? defaults[option]['min'] // A fallback so we don't print 'random' in the UI.
                : defaults[option]['defaultValue'];
          } else {
            numberElement.innerText = presetValue;
          }

          updateOptionElement(option, presetValue);
          break;

        case 'select': {
          updateOptionElement(option, presetValue);
          break;
        }

        case 'named_range': {
          const selectElement = document.querySelector(`select[data-key='${option}']`);
          const rangeElement = document.querySelector(`input[data-key='${option}']`);
          const randomElement = document.querySelector(`.randomize-button[data-key='${option}']`);

          if (presetValue === 'random') {
            randomElement.classList.add('active');
            selectElement.disabled = true;
            rangeElement.disabled = true;
            this.#updateGameOption(randomElement, false);
          } else {
            rangeElement.value = presetValue;
            selectElement.value = Object.values(defaults[option]['value_names']).includes(parseInt(presetValue)) ?
                parseInt(presetValue) : 'custom';
            document.getElementById(`${option}-value`).innerText = presetValue;

            randomElement.classList.remove('active');
            selectElement.disabled = undefined;
            rangeElement.disabled = undefined;
            this.#updateGameOption(rangeElement, false);
          }
          break;
        }

        default:
          console.warn(`Ignoring preset value for unknown option type: ${defaults[option].type} with name ${option}`);
          break;
      }
    }
  }

  updateBaseOption(event) {
    this.#current[event.target.getAttribute('data-key')] =
        isNaN(event.target.value) ? event.target.value : parseInt(event.target.value);
    this.save();
  }

  #updateGameOption(optionElement, toggleCustomPreset = true) {
    if (toggleCustomPreset) {
      localStorage.setItem(`${gameName}-preset`, '__custom');
      const presetElement = document.getElementById('game-options-preset');
      presetElement.value = '__custom';
    }

    if (optionElement.classList.contains('randomize-button')) {
      // If the event passed in is the randomize button, then we know what we must do.
      this.current[optionElement.getAttribute('data-key')] = 'random';
    } else {
      this.current[optionElement.getAttribute('data-key')] =
          isNaN(optionElement.value) ? optionElement.value : parseInt(optionElement.value, 10);
    }

    this.save();
  }

  export() {
    const options = {...this.#current};
    const preset = localStorage.getItem(`${gameName}-preset`);
    switch (preset) {
      case '__default':
        options['description'] = `Generated by https://archipelago.gg with the default preset.`;
        break;

      case '__custom':
        options['description'] = `Generated by https://archipelago.gg.`;
        break;

      default:
        options['description'] = `Generated by https://archipelago.gg with the ${preset} preset.`;
    }

    if (!options.name || options.name.toString().trim().length === 0) {
      showUserMessage('You must enter a player name!');
      return;
    }

    const yamlText = jsyaml.safeDump(options, { noCompatMode: true }).replaceAll(/'(\d+)':/g, (x, y) => `${y}:`);
    download(`${document.getElementById('player-name').value}.yaml`, yamlText);
  };

  async generateGame(raceMode = false) {
    if (!this.#current.name ||
        this.#current.name.toLowerCase() === 'player' ||
        this.#current.name.trim().length === 0) {
      return showUserMessage('You must enter a player name!');
    }

    try {
      window.location.href = await axios.post('/api/generate', {
        weights: { player: this.#current },
        presetData: { player: this.#current },
        playerCount: 1,
        spoiler: 3,
        race: raceMode ? '1' : '0',
      }).data.url;
    } catch (error) {
      let userMessage = 'Something went wrong and your game could not be generated.';
      if (error.response.data.text) {
        userMessage += ' ' + error.response.data.text;
      }
      showUserMessage(userMessage);
      console.error(error);
    }
  }
}
