window.addEventListener('load', () => {
  // Generic change listener. Detecting unique qualities and acting on them here reduces initial JS initialisation time
  // and handles dynamically created elements
  document.addEventListener('change', (evt) => {
    // Handle clicks on world names
    if (evt.target.type === 'checkbox' && evt.target.classList.contains('world-collapse')) {
      // Collapse all option groups within the world if the checkbox was unchecked
      if (!evt.target.checked) {
        const worldName = evt.target.getAttribute('data-world-name');
        document.querySelectorAll(`input[type=checkbox].group-collapse`).forEach((checkbox) => {
          if (checkbox.hasAttribute('data-world-name') && checkbox.getAttribute('data-world-name') === worldName) {
            checkbox.checked = false;
          }
        });
      }
    }

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
      const [worldName, optionName] = evt.target.getAttribute('data-option').split('-');
      addRangeRow(worldName, optionName);
    }

    // Handle deleting range rows
    if (evt.target.classList.contains('range-option-delete')) {
      const targetRow = document.querySelector(`tr[data-row="${evt.target.getAttribute('data-target')}"]`);
      targetRow.parentElement.removeChild(targetRow);
    }
  });

  // Listen for enter presses on inputs intended to add range rows
  document.addEventListener('keydown', (evt) => {
    if (evt.key === 'Enter' && evt.target.classList.contains('range-option-value')) {
      const [worldName, optionName] = evt.target.getAttribute('data-option').split('-');
      addRangeRow(worldName, optionName);
    }
  });

  // Detect form submission
  document.getElementById('weighted-options-form').addEventListener('submit', (evt) => {
    // TODO: Save data to localStorage
    evt.preventDefault();
  });

  // TODO: Populate all settings from localStorage on page initialisation
});

const addRangeRow = (worldName, optionName) => {
  const inputTarget = document.querySelector(`input[type=number][data-option="${worldName}-${optionName}"].range-option-value`);
  const newValue = inputTarget.value;
  if (!/^\d+$/.test(newValue)) {
    alert('Range values must be a number!');
    return;
  }
  inputTarget.value = '';
  const tBody = document.querySelector(`table[data-option="${worldName}-${optionName}"].range-rows tbody`);
  const tr = document.createElement('tr');
  tr.setAttribute('data-row', `${worldName}-${optionName}-${newValue}-row`);
  const tdLeft = document.createElement('td');
  tdLeft.classList.add('td-left');
  const label = document.createElement('label');
  label.setAttribute('for', `${worldName}||${optionName}||${newValue}`);
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
  range.setAttribute('id', `${worldName}||${optionName}||${newValue}`);
  range.setAttribute('name', `${worldName}||${optionName}||${newValue}`);
  tdMiddle.appendChild(range);
  tr.appendChild(tdMiddle);
  const tdRight = document.createElement('td');
  tdRight.classList.add('td-right');
  const valueSpan = document.createElement('span');
  valueSpan.setAttribute('id', `${worldName}||${optionName}||${newValue}-value`);
  valueSpan.innerText = '0';
  tdRight.appendChild(valueSpan);
  tr.appendChild(tdRight);
  const tdDelete = document.createElement('td');
  const deleteSpan = document.createElement('span');
  deleteSpan.classList.add('range-option-delete');
  deleteSpan.classList.add('js-required');
  deleteSpan.setAttribute('data-target', `${worldName}-${optionName}-${newValue}-row`);
  deleteSpan.innerText = '❌';
  tdDelete.appendChild(deleteSpan);
  tr.appendChild(tdDelete);
  tBody.appendChild(tr);
};
