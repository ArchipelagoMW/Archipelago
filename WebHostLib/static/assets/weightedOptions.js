let deletedOptions = {};

window.addEventListener('load', () => {
  const worldName = document.querySelector('#weighted-options').getAttribute('data-game');

  // Generic change listener. Detecting unique qualities and acting on them here reduces initial JS initialisation time
  // and handles dynamically created elements
  document.addEventListener('change', (evt) => {
    // Handle updates to range inputs
    if (evt.target.type === 'range') {
      // Update span containing range value. All ranges have a corresponding `{rangeId}-value` span
      document.getElementById(`${evt.target.id}-value`).innerText = evt.target.value;

      // If the changed option was the name of a game, determine whether to show or hide that game's div
      if (evt.target.id.startsWith('game||')) {
        const gameName = evt.target.id.split('||')[1];
        const gameDiv = document.getElementById(`${gameName}-container`);
        if (evt.target.value > 0) {
          gameDiv.classList.remove('hidden');
        } else {
          gameDiv.classList.add('hidden');
        }
      }
    }
  });

  // Generic click listener
  document.addEventListener('click', (evt) => {
    // Handle creating new rows for Range options
    if (evt.target.classList.contains('add-range-option-button')) {
      const optionName = evt.target.getAttribute('data-option');
      addRangeRow(optionName);
    }

    // Handle deleting range rows
    if (evt.target.classList.contains('range-option-delete')) {
      const targetRow = document.querySelector(`tr[data-row="${evt.target.getAttribute('data-target')}"]`);
      setDeletedOption(
        targetRow.getAttribute('data-option-name'),
        targetRow.getAttribute('data-value'),
      );
      targetRow.parentElement.removeChild(targetRow);
    }
  });

  // Listen for enter presses on inputs intended to add range rows
  document.addEventListener('keydown', (evt) => {
    if (evt.key === 'Enter') {
      evt.preventDefault();
    }

    if (evt.key === 'Enter' && evt.target.classList.contains('range-option-value')) {
      const optionName = evt.target.getAttribute('data-option');
      addRangeRow(optionName);
    }
  });

  // Detect form submission
  document.getElementById('weighted-options-form').addEventListener('submit', (evt) => {
    // Save data to localStorage
    const weightedOptions = {};
    document.querySelectorAll('input[name]').forEach((input) => {
      const keys = input.getAttribute('name').split('||');

      // Determine keys
      const optionName = keys[0] ?? null;
      const subOption = keys[1] ?? null;

      // Ensure keys exist
      if (!weightedOptions[optionName]) { weightedOptions[optionName] = {}; }
      if (subOption && !weightedOptions[optionName][subOption]) {
        weightedOptions[optionName][subOption] = null;
      }

      if (subOption) { return weightedOptions[optionName][subOption] = determineValue(input); }
      if (optionName) { return weightedOptions[optionName] = determineValue(input); }
    });

    localStorage.setItem(`${worldName}-weights`, JSON.stringify(weightedOptions));
    localStorage.setItem(`${worldName}-deletedOptions`, JSON.stringify(deletedOptions));
  });

  // Remove all deleted values as specified by localStorage
  deletedOptions = JSON.parse(localStorage.getItem(`${worldName}-deletedOptions`) || '{}');
  Object.keys(deletedOptions).forEach((optionName) => {
    deletedOptions[optionName].forEach((value) => {
      const targetRow = document.querySelector(`tr[data-row="${value}-row"]`);
      targetRow.parentElement.removeChild(targetRow);
    });
  });

  // Populate all settings from localStorage on page initialisation
  const previousSettingsJson = localStorage.getItem(`${worldName}-weights`);
  if (previousSettingsJson) {
    const previousSettings = JSON.parse(previousSettingsJson);
    Object.keys(previousSettings).forEach((option) => {
      if (typeof previousSettings[option] === 'string') {
        return document.querySelector(`input[name="${option}"]`).value = previousSettings[option];
      }

      Object.keys(previousSettings[option]).forEach((value) => {
        const input = document.querySelector(`input[name="${option}||${value}"]`);
        if (!input?.type) {
          return console.error(`Unable to populate option with name ${option}||${value}.`);
        }

        switch (input.type) {
          case 'checkbox':
            input.checked = (parseInt(previousSettings[option][value], 10) === 1);
            break;
          case 'range':
            input.value = parseInt(previousSettings[option][value], 10);
            break;
          case 'number':
            input.value = previousSettings[option][value].toString();
            break;
          default:
            console.error(`Found unsupported input type: ${input.type}`);
        }
      });
    });
  }
});

const addRangeRow = (optionName) => {
  const inputQuery = `input[type=number][data-option="${optionName}"].range-option-value`;
  const inputTarget = document.querySelector(inputQuery);
  const newValue = inputTarget.value;
  if (!/^-?\d+$/.test(newValue)) {
    alert('Range values must be a positive or negative integer!');
    return;
  }
  inputTarget.value = '';
  const tBody = document.querySelector(`table[data-option="${optionName}"].range-rows tbody`);
  const tr = document.createElement('tr');
  tr.setAttribute('data-row', `${optionName}-${newValue}-row`);
  tr.setAttribute('data-option-name', optionName);
  tr.setAttribute('data-value', newValue);
  const tdLeft = document.createElement('td');
  tdLeft.classList.add('td-left');
  const label = document.createElement('label');
  label.setAttribute('for', `${optionName}||${newValue}`);
  label.innerText = newValue.toString();
  tdLeft.appendChild(label);
  tr.appendChild(tdLeft);
  const tdMiddle = document.createElement('td');
  tdMiddle.classList.add('td-middle');
  const range = document.createElement('input');
  range.setAttribute('type', 'range');
  range.setAttribute('min', '0');
  range.setAttribute('max', '50');
  range.setAttribute('value', '0');
  range.setAttribute('id', `${optionName}||${newValue}`);
  range.setAttribute('name', `${optionName}||${newValue}`);
  tdMiddle.appendChild(range);
  tr.appendChild(tdMiddle);
  const tdRight = document.createElement('td');
  tdRight.classList.add('td-right');
  const valueSpan = document.createElement('span');
  valueSpan.setAttribute('id', `${optionName}||${newValue}-value`);
  valueSpan.innerText = '0';
  tdRight.appendChild(valueSpan);
  tr.appendChild(tdRight);
  const tdDelete = document.createElement('td');
  const deleteSpan = document.createElement('span');
  deleteSpan.classList.add('range-option-delete');
  deleteSpan.classList.add('js-required');
  deleteSpan.setAttribute('data-target', `${optionName}-${newValue}-row`);
  deleteSpan.innerText = '❌';
  tdDelete.appendChild(deleteSpan);
  tr.appendChild(tdDelete);
  tBody.appendChild(tr);

  // Remove this option from the set of deleted options if it exists
  unsetDeletedOption(optionName, newValue);
};

/**
 * Determines the value of an input element, or returns a 1 or 0 if the element is a checkbox
 *
 * @param {object} input - The input element.
 * @returns {number} The value of the input element.
 */
const determineValue = (input) => {
  switch (input.type) {
    case 'checkbox':
      return (input.checked ? 1 : 0);
    case 'range':
      return parseInt(input.value, 10);
    default:
      return input.value;
  }
};

/**
 * Sets the deleted option value for a given world and option name.
 * If the world or option does not exist, it creates the necessary entries.
 *
 * @param {string} optionName - The name of the option.
 * @param {*} value - The value to be set for the deleted option.
 * @returns {void}
 */
const setDeletedOption = (optionName, value) => {
  deletedOptions[optionName] = deletedOptions[optionName] || [];
  deletedOptions[optionName].push(`${optionName}-${value}`);
};

/**
 * Removes a specific value from the deletedOptions object.
 *
 * @param {string} optionName - The name of the option.
 * @param {*} value - The value to be removed
 * @returns {void}
 */
const unsetDeletedOption = (optionName, value) => {
  if (!deletedOptions.hasOwnProperty(optionName)) { return; }
  if (deletedOptions[optionName].includes(`${optionName}-${value}`)) {
    deletedOptions[optionName].splice(deletedOptions[optionName].indexOf(`${optionName}-${value}`), 1);
  }
  if (deletedOptions[optionName].length === 0) {
    delete deletedOptions[optionName];
  }
};
