let presets = {};

window.addEventListener('load', async () => {
  // Load settings from localStorage, if available
  loadSettings();

  // Fetch presets if available
  await fetchPresets();

  // Handle changes to range inputs
  document.querySelectorAll('input[type=range]').forEach((range) => {
    const optionName = range.getAttribute('id');
    range.addEventListener('change', () => {
      document.getElementById(`${optionName}-value`).innerText = range.value;

      // Handle updating named range selects to "custom" if appropriate
      const select = document.querySelector(`select[data-option-name=${optionName}]`);
      if (select) {
        let updated = false;
        select?.childNodes.forEach((option) => {
          if (option.value === range.value) {
            select.value = range.value;
            updated = true;
          }
        });
        if (!updated) {
          select.value = 'custom';
        }
      }
    });
  });

  // Handle changes to named range selects
  document.querySelectorAll('.named-range-container select').forEach((select) => {
    const optionName = select.getAttribute('data-option-name');
    select.addEventListener('change', (evt) => {
      document.getElementById(optionName).value = evt.target.value;
      document.getElementById(`${optionName}-value`).innerText = evt.target.value;
    });
  });

  // Handle changes to randomize checkboxes
  document.querySelectorAll('.randomize-checkbox').forEach((checkbox) => {
    const optionName = checkbox.getAttribute('data-option-name');
    checkbox.addEventListener('change', () => {
      const optionInput = document.getElementById(optionName);
      const namedRangeSelect = document.querySelector(`select[data-option-name=${optionName}]`);
      const customInput = document.getElementById(`${optionName}-custom`);
      if (checkbox.checked) {
        optionInput.setAttribute('disabled', '1');
        namedRangeSelect?.setAttribute('disabled', '1');
        if (customInput) {
          customInput.setAttribute('disabled', '1');
        }
      } else {
        optionInput.removeAttribute('disabled');
        namedRangeSelect?.removeAttribute('disabled');
        if (customInput) {
          customInput.removeAttribute('disabled');
        }
      }
    });
  });

  // Handle changes to TextChoice input[type=text]
  document.querySelectorAll('.text-choice-container input[type=text]').forEach((input) => {
    const optionName = input.getAttribute('data-option-name');
    input.addEventListener('input', () => {
      const select = document.getElementById(optionName);
      const optionValues = [];
      select.childNodes.forEach((option) => optionValues.push(option.value));
      select.value = (optionValues.includes(input.value)) ? input.value : 'custom';
    });
  });

  // Handle changes to TextChoice select
  document.querySelectorAll('.text-choice-container select').forEach((select) => {
    const optionName = select.getAttribute('id');
    select.addEventListener('change', () => {
      document.getElementById(`${optionName}-custom`).value = '';
    });
  });

  // Update the "Option Preset" select to read "custom" when changes are made to relevant inputs
  const presetSelect = document.getElementById('game-options-preset');
  document.querySelectorAll('input, select').forEach((input) => {
    if ( // Ignore inputs which have no effect on yaml generation
      (input.id === 'player-name') ||
      (input.id === 'game-options-preset') ||
      (input.classList.contains('group-toggle')) ||
      (input.type === 'submit')
    ) {
      return;
    }
    input.addEventListener('change', () => {
      presetSelect.value = 'custom';
    });
  });

  // Handle changes to presets select
  document.getElementById('game-options-preset').addEventListener('change', choosePreset);

  // Save settings to localStorage when form is submitted
  document.getElementById('options-form').addEventListener('submit', (evt) => {
    const playerName = document.getElementById('player-name');
    if (!playerName.value.trim()) {
      evt.preventDefault();
      window.scrollTo(0, 0);
      showUserMessage('You must enter a player name!');
    }

    saveSettings();
  });
});

// Save all settings to localStorage
const saveSettings = () => {
  const options = {
    inputs: {},
    checkboxes: {},
  };
  document.querySelectorAll('input, select').forEach((input) => {
    if (input.type === 'submit') {
      // Ignore submit inputs
    }
    else if (input.type === 'checkbox') {
      options.checkboxes[input.id] = input.checked;
    }
    else {
      options.inputs[input.id] = input.value
    }
  });
  const game = document.getElementById('player-options').getAttribute('data-game');
  localStorage.setItem(game, JSON.stringify(options));
};

// Load all options from localStorage
const loadSettings = () => {
  const game = document.getElementById('player-options').getAttribute('data-game');

  const options = JSON.parse(localStorage.getItem(game));
  if (options) {
    if (!options.inputs || !options.checkboxes) {
      localStorage.removeItem(game);
      return;
    }

    // Restore value-based inputs and selects
    Object.keys(options.inputs).forEach((key) => {
      try{
        document.getElementById(key).value = options.inputs[key];
        const rangeValue = document.getElementById(`${key}-value`);
        if (rangeValue) {
          rangeValue.innerText = options.inputs[key];
        }
      } catch (err) {
        console.error(`Unable to restore value to input with id ${key}`);
      }
    });

    // Restore checkboxes
    Object.keys(options.checkboxes).forEach((key) => {
      try{
        if (options.checkboxes[key]) {
          document.getElementById(key).setAttribute('checked', '1');
        }
      } catch (err) {
        console.error(`Unable to restore value to input with id ${key}`);
      }
    });
  }

  // Ensure any input for which the randomize checkbox is checked by default, the relevant inputs are disabled
  document.querySelectorAll('.randomize-checkbox').forEach((checkbox) => {
    const optionName = checkbox.getAttribute('data-option-name');
    if (checkbox.checked) {
      const input = document.getElementById(optionName);
      if (input) {
        input.setAttribute('disabled', '1');
      }
      const customInput = document.getElementById(`${optionName}-custom`);
      if (customInput) {
        customInput.setAttribute('disabled', '1');
      }
    }
  });
};

/**
 * Fetch the preset data for this game and apply the presets if localStorage indicates one was previously chosen
 * @returns {Promise<void>}
 */
const fetchPresets = async () => {
  const response = await fetch('option-presets');
  presets = await response.json();
  const presetSelect = document.getElementById('game-options-preset');
  presetSelect.removeAttribute('disabled');

  const game = document.getElementById('player-options').getAttribute('data-game');
  const presetToApply = localStorage.getItem(`${game}-preset`);
  const playerName = localStorage.getItem(`${game}-player`);
  if (presetToApply) {
    localStorage.removeItem(`${game}-preset`);
    presetSelect.value = presetToApply;
    applyPresets(presetToApply);
  }

  if (playerName) {
    document.getElementById('player-name').value = playerName;
    localStorage.removeItem(`${game}-player`);
  }
};

/**
 * Clear the localStorage for this game and set a preset to be loaded upon page reload
 * @param evt
 */
const choosePreset = (evt) => {
  if (evt.target.value === 'custom') { return; }

  const game = document.getElementById('player-options').getAttribute('data-game');
  localStorage.removeItem(game);

  localStorage.setItem(`${game}-player`, document.getElementById('player-name').value);
  if (evt.target.value !== 'default') {
    localStorage.setItem(`${game}-preset`, evt.target.value);
  }

  document.querySelectorAll('#options-form input, #options-form select').forEach((input) => {
    if (input.id === 'player-name') { return; }
    input.removeAttribute('value');
  });

  window.location.replace(window.location.href);
};

const applyPresets = (presetName) => {
  // Ignore the "default" preset, because it gets set automatically by Jinja
  if (presetName === 'default') {
    saveSettings();
    return;
  }

  if (!presets[presetName]) {
    console.error(`Unknown preset ${presetName} chosen`);
    return;
  }

  const preset = presets[presetName];
  Object.keys(preset).forEach((optionName) => {
    const optionValue = preset[optionName];

    // Handle List and Set options
    if (Array.isArray(optionValue)) {
      document.querySelectorAll(`input[type=checkbox][name=${optionName}]`).forEach((checkbox) => {
        if (optionValue.includes(checkbox.value)) {
          checkbox.setAttribute('checked', '1');
        } else {
          checkbox.removeAttribute('checked');
        }
      });
      return;
    }

    // Handle Dict options
    if (typeof(optionValue) === 'object' && optionValue !== null) {
      const itemNames = Object.keys(optionValue);
      document.querySelectorAll(`input[type=number][data-option-name=${optionName}]`).forEach((input) => {
        const itemName = input.getAttribute('data-item-name');
        input.value = (itemNames.includes(itemName)) ? optionValue[itemName] : 0
      });
      return;
    }

    // Identify all possible elements
    const normalInput = document.getElementById(optionName);
    const customInput = document.getElementById(`${optionName}-custom`);
    const rangeValue = document.getElementById(`${optionName}-value`);
    const randomizeInput = document.getElementById(`random-${optionName}`);
    const namedRangeSelect = document.getElementById(`${optionName}-select`);

    // It is possible for named ranges to use name of a value rather than the value itself. This is accounted for here
    let trueValue = optionValue;
    if (namedRangeSelect) {
      namedRangeSelect.querySelectorAll('option').forEach((opt) => {
        if (opt.innerText.startsWith(optionValue)) {
          trueValue = opt.value;
        }
      });
      namedRangeSelect.value = trueValue;
      // It is also possible for a preset to use an unnamed value. If this happens, set the dropdown to "Custom"
      if (namedRangeSelect.selectedIndex == -1)
      {
        namedRangeSelect.value = "custom";
      }
    }

    // Handle options whose presets are "random"
    if (optionValue === 'random') {
      normalInput.setAttribute('disabled', '1');
      randomizeInput.setAttribute('checked', '1');
      if (customInput) {
        customInput.setAttribute('disabled', '1');
      }
      if (rangeValue) {
        rangeValue.innerText = normalInput.value;
      }
      if (namedRangeSelect) {
        namedRangeSelect.setAttribute('disabled', '1');
      }
      return;
    }

    // Handle normal (text, number, select, etc.) and custom inputs (custom inputs exist with TextChoice only)
    normalInput.value = trueValue;
    normalInput.removeAttribute('disabled');
    randomizeInput.removeAttribute('checked');
    if (customInput) {
      document.getElementById(`${optionName}-custom`).removeAttribute('disabled');
    }
    if (rangeValue) {
      rangeValue.innerText = trueValue;
    }
  });

  saveSettings();
};

const showUserMessage = (text) => {
  const userMessage = document.getElementById('user-message');
  userMessage.innerText = text;
  userMessage.addEventListener('click', hideUserMessage);
  userMessage.style.display = 'block';
};

const hideUserMessage = () => {
  const userMessage = document.getElementById('user-message');
  userMessage.removeEventListener('click', hideUserMessage);
  userMessage.style.display = 'none';
};
