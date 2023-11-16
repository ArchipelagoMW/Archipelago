let gameName = null;

window.addEventListener('load', () => {
  gameName = document.getElementById('player-options').getAttribute('data-game');

  // Update game name on page
  document.getElementById('game-name').innerText = gameName;

  fetchOptionData().then((results) => {
    let optionHash = localStorage.getItem(`${gameName}-hash`);
    if (!optionHash) {
      // If no hash data has been set before, set it now
      optionHash = md5(JSON.stringify(results));
      localStorage.setItem(`${gameName}-hash`, optionHash);
      localStorage.removeItem(gameName);
    }

    if (optionHash !== md5(JSON.stringify(results))) {
      showUserMessage(
          'Your options are out of date! Click here to update them! Be aware this will reset them all to default.'
      );
      document.getElementById('user-message').addEventListener('click', resetOptions);
    }

    // Page setup
    createDefaultOptions(results);
    buildUI(results);
    adjustHeaderWidth();

    // Event listeners
    document.getElementById('export-options').addEventListener('click', () => exportOptions());
    document.getElementById('generate-race').addEventListener('click', () => generateGame(true));
    document.getElementById('generate-game').addEventListener('click', () => generateGame());

    // Name input field
    const playerOptions = JSON.parse(localStorage.getItem(gameName));
    const nameInput = document.getElementById('player-name');
    nameInput.addEventListener('keyup', (event) => updateBaseOption(event));
    nameInput.value = playerOptions.name;

    // Presets
    const presetSelect = document.getElementById('game-options-preset');
    presetSelect.addEventListener('change', (event) => setPresets(results, event.target.value));
    for (const preset in results['presetOptions']) {
      const presetOption = document.createElement('option');
      presetOption.innerText = preset;
      presetSelect.appendChild(presetOption);
    }
    presetSelect.value = localStorage.getItem(`${gameName}-preset`);
    results['presetOptions']['__default'] = {};
  }).catch((e) => {
    console.error(e);
    const url = new URL(window.location.href);
    window.location.replace(`${url.protocol}//${url.hostname}/page-not-found`);
  })
});

const resetOptions = () => {
  localStorage.removeItem(gameName);
  localStorage.removeItem(`${gameName}-hash`);
  localStorage.removeItem(`${gameName}-preset`);
  window.location.reload();
};

const fetchOptionData = () => new Promise((resolve, reject) => {
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
  ajax.open('GET', `${window.location.origin}/static/generated/player-options/${gameName}.json`, true);
  ajax.send();
});

const createDefaultOptions = (optionData) => {
  if (!localStorage.getItem(gameName)) {
    const newOptions = {
      [gameName]: {},
    };
    for (let baseOption of Object.keys(optionData.baseOptions)){
      newOptions[baseOption] = optionData.baseOptions[baseOption];
    }
    for (let gameOption of Object.keys(optionData.gameOptions)){
      newOptions[gameName][gameOption] = optionData.gameOptions[gameOption].defaultValue;
    }
    localStorage.setItem(gameName, JSON.stringify(newOptions));
  }

  if (!localStorage.getItem(`${gameName}-preset`)) {
    localStorage.setItem(`${gameName}-preset`, '__default');
  }
};

const buildUI = (optionData) => {
  // Game Options
  const leftGameOpts = {};
  const rightGameOpts = {};
  Object.keys(optionData.gameOptions).forEach((key, index) => {
    if (index < Object.keys(optionData.gameOptions).length / 2) {
      leftGameOpts[key] = optionData.gameOptions[key];
    } else {
      rightGameOpts[key] = optionData.gameOptions[key];
    }
  });
  document.getElementById('game-options-left').appendChild(buildOptionsTable(leftGameOpts));
  document.getElementById('game-options-right').appendChild(buildOptionsTable(rightGameOpts));
};

const buildOptionsTable = (options, romOpts = false) => {
  const currentOptions = JSON.parse(localStorage.getItem(gameName));
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

          if ((isNaN(currentOptions[gameName][option]) &&
            (parseInt(opt.value, 10) === parseInt(currentOptions[gameName][option]))) ||
            (opt.value === currentOptions[gameName][option]))
          {
            optionElement.selected = true;
          }
          select.appendChild(optionElement);
        });
        select.addEventListener('change', (event) => updateGameOption(event.target));
        element.appendChild(select);

        // Randomize button
        randomButton.innerText = '🎲';
        randomButton.classList.add('randomize-button');
        randomButton.setAttribute('data-key', option);
        randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
        randomButton.addEventListener('click', (event) => toggleRandomize(event, select));
        if (currentOptions[gameName][option] === 'random') {
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
        range.value = currentOptions[gameName][option];
        range.addEventListener('change', (event) => {
          document.getElementById(`${option}-value`).innerText = event.target.value;
          updateGameOption(event.target);
        });
        element.appendChild(range);

        let rangeVal = document.createElement('span');
        rangeVal.classList.add('range-value');
        rangeVal.setAttribute('id', `${option}-value`);
        rangeVal.innerText = currentOptions[gameName][option] !== 'random' ?
          currentOptions[gameName][option] : options[option].defaultValue;
        element.appendChild(rangeVal);

        // Randomize button
        randomButton.innerText = '🎲';
        randomButton.classList.add('randomize-button');
        randomButton.setAttribute('data-key', option);
        randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
        randomButton.addEventListener('click', (event) => toggleRandomize(event, range));
        if (currentOptions[gameName][option] === 'random') {
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
        specialRangeSelect.setAttribute('data-key', option);
        Object.keys(options[option].value_names).forEach((presetName) => {
          let presetOption = document.createElement('option');
          presetOption.innerText = presetName;
          presetOption.value = options[option].value_names[presetName];
          const words = presetOption.innerText.split('_');
          for (let i = 0; i < words.length; i++) {
            words[i] = words[i][0].toUpperCase() + words[i].substring(1);
          }
          presetOption.innerText = words.join(' ');
          specialRangeSelect.appendChild(presetOption);
        });
        let customOption = document.createElement('option');
        customOption.innerText = 'Custom';
        customOption.value = 'custom';
        customOption.selected = true;
        specialRangeSelect.appendChild(customOption);
        if (Object.values(options[option].value_names).includes(Number(currentOptions[gameName][option]))) {
          specialRangeSelect.value = Number(currentOptions[gameName][option]);
        }

        // Build range element
        let specialRangeWrapper = document.createElement('div');
        specialRangeWrapper.classList.add('special-range-wrapper');
        let specialRange = document.createElement('input');
        specialRange.setAttribute('type', 'range');
        specialRange.setAttribute('data-key', option);
        specialRange.setAttribute('min', options[option].min);
        specialRange.setAttribute('max', options[option].max);
        specialRange.value = currentOptions[gameName][option];

        // Build rage value element
        let specialRangeVal = document.createElement('span');
        specialRangeVal.classList.add('range-value');
        specialRangeVal.setAttribute('id', `${option}-value`);
        specialRangeVal.innerText = currentOptions[gameName][option] !== 'random' ?
          currentOptions[gameName][option] : options[option].defaultValue;

        // Configure select event listener
        specialRangeSelect.addEventListener('change', (event) => {
          if (event.target.value === 'custom') { return; }

          // Update range slider
          specialRange.value = event.target.value;
          document.getElementById(`${option}-value`).innerText = event.target.value;
          updateGameOption(event.target);
        });

        // Configure range event handler
        specialRange.addEventListener('change', (event) => {
          // Update select element
          specialRangeSelect.value =
            (Object.values(options[option].value_names).includes(parseInt(event.target.value))) ?
            parseInt(event.target.value) : 'custom';
          document.getElementById(`${option}-value`).innerText = event.target.value;
          updateGameOption(event.target);
        });

        element.appendChild(specialRangeSelect);
        specialRangeWrapper.appendChild(specialRange);
        specialRangeWrapper.appendChild(specialRangeVal);
        element.appendChild(specialRangeWrapper);

        // Randomize button
        randomButton.innerText = '🎲';
        randomButton.classList.add('randomize-button');
        randomButton.setAttribute('data-key', option);
        randomButton.setAttribute('data-tooltip', 'Toggle randomization for this option!');
        randomButton.addEventListener('click', (event) => toggleRandomize(
            event, specialRange, specialRangeSelect)
        );
        if (currentOptions[gameName][option] === 'random') {
          randomButton.classList.add('active');
          specialRange.disabled = true;
          specialRangeSelect.disabled = true;
        }

        specialRangeWrapper.appendChild(randomButton);
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
};

const setPresets = (optionsData, presetName) => {
  const defaults = optionsData['gameOptions'];
  const preset = optionsData['presetOptions'][presetName];

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
      updateGameOption(randomElement, false);
    } else {
      optionElement.value = presetValue;
      randomElement.classList.remove('active');
      optionElement.disabled = undefined;
      updateGameOption(optionElement, false);
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

      case 'special_range': {
        const selectElement = document.querySelector(`select[data-key='${option}']`);
        const rangeElement = document.querySelector(`input[data-key='${option}']`);
        const randomElement = document.querySelector(`.randomize-button[data-key='${option}']`);

        if (presetValue === 'random') {
          randomElement.classList.add('active');
          selectElement.disabled = true;
          rangeElement.disabled = true;
          updateGameOption(randomElement, false);
        } else {
          rangeElement.value = presetValue;
          selectElement.value = Object.values(defaults[option]['value_names']).includes(parseInt(presetValue)) ?
              parseInt(presetValue) : 'custom';
          document.getElementById(`${option}-value`).innerText = presetValue;

          randomElement.classList.remove('active');
          selectElement.disabled = undefined;
          rangeElement.disabled = undefined;
          updateGameOption(rangeElement, false);
        }
        break;
      }

      default:
        console.warn(`Ignoring preset value for unknown option type: ${defaults[option].type} with name ${option}`);
        break;
    }
  }
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
    updateGameOption(active ? inputElement : randomButton);
};

const updateBaseOption = (event) => {
  const options = JSON.parse(localStorage.getItem(gameName));
  options[event.target.getAttribute('data-key')] = isNaN(event.target.value) ?
    event.target.value : parseInt(event.target.value);
  localStorage.setItem(gameName, JSON.stringify(options));
};

const updateGameOption = (optionElement, toggleCustomPreset = true) => {
  const options = JSON.parse(localStorage.getItem(gameName));

  if (toggleCustomPreset) {
    localStorage.setItem(`${gameName}-preset`, '__custom');
    const presetElement = document.getElementById('game-options-preset');
    presetElement.value = '__custom';
  }

  if (optionElement.classList.contains('randomize-button')) {
    // If the event passed in is the randomize button, then we know what we must do.
    options[gameName][optionElement.getAttribute('data-key')] = 'random';
  } else {
    options[gameName][optionElement.getAttribute('data-key')] = isNaN(optionElement.value) ?
      optionElement.value : parseInt(optionElement.value, 10);
  }

  localStorage.setItem(gameName, JSON.stringify(options));
};

const exportOptions = () => {
  const options = JSON.parse(localStorage.getItem(gameName));
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

  if (!options.name || options.name.trim().length === 0) {
    return showUserMessage('You must enter a player name!');
  }
  const yamlText = jsyaml.safeDump(options, { noCompatMode: true }).replaceAll(/'(\d+)':/g, (x, y) => `${y}:`);
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
  const options = JSON.parse(localStorage.getItem(gameName));
  if (!options.name || options.name.toLowerCase() === 'player' || options.name.trim().length === 0) {
    return showUserMessage('You must enter a player name!');
  }

  axios.post('/api/generate', {
    weights: { player: options },
    presetData: { player: options },
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
