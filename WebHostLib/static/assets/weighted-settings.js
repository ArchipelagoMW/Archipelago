window.addEventListener('load', () => {
  fetchSettingData().then((results) => {
    let settingHash = localStorage.getItem('weighted-settings-hash');
    if (!settingHash) {
      // If no hash data has been set before, set it now
      settingHash = md5(JSON.stringify(results));
      localStorage.setItem('weighted-settings-hash', settingHash);
      localStorage.removeItem('weighted-settings');
    }

    if (settingHash !== md5(JSON.stringify(results))) {
      const userMessage = document.getElementById('user-message');
      userMessage.innerText = "Your settings are out of date! Click here to update them! Be aware this will reset " +
        "them all to default.";
      userMessage.classList.add('visible');
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
    try{ response.json().then((jsonObj) => resolve(jsonObj)); }
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
          case 'special_range':
            newSettings[game][gameSetting]['random'] = 0;
            newSettings[game][gameSetting]['random-low'] = 0;
            newSettings[game][gameSetting]['random-high'] = 0;
            if (setting.hasOwnProperty('defaultValue')) {
              newSettings[game][gameSetting][setting.defaultValue] = 25;
            } else {
              newSettings[game][gameSetting][setting.min] = 25;
            }
            break;

          case 'items-list':
          case 'locations-list':
          case 'custom-list':
            newSettings[game][gameSetting] = setting.defaultValue;
            break;

          default:
            console.error(`Unknown setting type for ${game} setting ${gameSetting}: ${setting.type}`);
        }
      }

      newSettings[game].start_inventory = {};
      newSettings[game].exclude_locations = [];
      newSettings[game].priority_locations = [];
      newSettings[game].local_items = [];
      newSettings[game].non_local_items = [];
      newSettings[game].start_hints = [];
      newSettings[game].start_location_hints = [];
    }

    localStorage.setItem('weighted-settings', JSON.stringify(newSettings));
  }
};

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

    const collapseButton = document.createElement('a');
    collapseButton.innerText = '(Collapse)';
    gameDiv.appendChild(collapseButton);

    const expandButton = document.createElement('a');
    expandButton.innerText = '(Expand)';
    expandButton.classList.add('invisible');
    gameDiv.appendChild(expandButton);

    settingData.games[game].gameItems.sort((a, b) => (a > b ? 1 : (a < b ? -1 : 0)));
    settingData.games[game].gameLocations.sort((a, b) => (a > b ? 1 : (a < b ? -1 : 0)));

    const weightedSettingsDiv = buildWeightedSettingsDiv(game, settingData.games[game].gameSettings,
      settingData.games[game].gameItems, settingData.games[game].gameLocations);
    gameDiv.appendChild(weightedSettingsDiv);

    const itemPoolDiv = buildItemsDiv(game, settingData.games[game].gameItems);
    gameDiv.appendChild(itemPoolDiv);

    const hintsDiv = buildHintsDiv(game, settingData.games[game].gameItems, settingData.games[game].gameLocations);
    gameDiv.appendChild(hintsDiv);

    const locationsDiv = buildLocationsDiv(game, settingData.games[game].gameLocations);
    gameDiv.appendChild(locationsDiv);

    gamesWrapper.appendChild(gameDiv);

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

  Object.keys(games).forEach((game) => {
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

const buildWeightedSettingsDiv = (game, settings, gameItems, gameLocations) => {
  const currentSettings = JSON.parse(localStorage.getItem('weighted-settings'));
  const settingsWrapper = document.createElement('div');
  settingsWrapper.classList.add('settings-wrapper');

  Object.keys(settings).forEach((settingName) => {
    const setting = settings[settingName];
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
          range.setAttribute('data-game', game);
          range.setAttribute('data-setting', settingName);
          range.setAttribute('data-option', option.value);
          range.setAttribute('data-type', setting.type);
          range.setAttribute('min', 0);
          range.setAttribute('max', 50);
          range.addEventListener('change', updateRangeSetting);
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
            range.setAttribute('id', `${game}-${settingName}-${i}-range`);
            range.setAttribute('data-game', game);
            range.setAttribute('data-setting', settingName);
            range.setAttribute('data-option', i);
            range.setAttribute('min', 0);
            range.setAttribute('max', 50);
            range.addEventListener('change', updateRangeSetting);
            range.value = currentSettings[game][settingName][i] || 0;
            tdMiddle.appendChild(range);
            tr.appendChild(tdMiddle);

            const tdRight = document.createElement('td');
            tdRight.setAttribute('id', `${game}-${settingName}-${i}`)
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
          optionInput.setAttribute('id', `${game}-${settingName}-option`);
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
            const optionInput = document.getElementById(`${game}-${settingName}-option`);
            let option = optionInput.value;
            if (!option || !option.trim()) { return; }
            option = parseInt(option, 10);
            if ((option < setting.min) || (option > setting.max)) { return; }
            optionInput.value = '';
            if (document.getElementById(`${game}-${settingName}-${option}-range`)) { return; }

            const tr = document.createElement('tr');
            const tdLeft = document.createElement('td');
            tdLeft.classList.add('td-left');
            tdLeft.innerText = option;
            tr.appendChild(tdLeft);

            const tdMiddle = document.createElement('td');
            tdMiddle.classList.add('td-middle');
            const range = document.createElement('input');
            range.setAttribute('type', 'range');
            range.setAttribute('id', `${game}-${settingName}-${option}-range`);
            range.setAttribute('data-game', game);
            range.setAttribute('data-setting', settingName);
            range.setAttribute('data-option', option);
            range.setAttribute('min', 0);
            range.setAttribute('max', 50);
            range.addEventListener('change', updateRangeSetting);
            range.value = currentSettings[game][settingName][parseInt(option, 10)];
            tdMiddle.appendChild(range);
            tr.appendChild(tdMiddle);

            const tdRight = document.createElement('td');
            tdRight.setAttribute('id', `${game}-${settingName}-${option}`)
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

          Object.keys(currentSettings[game][settingName]).forEach((option) => {
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
              range.setAttribute('id', `${game}-${settingName}-${option}-range`);
              range.setAttribute('data-game', game);
              range.setAttribute('data-setting', settingName);
              range.setAttribute('data-option', option);
              range.setAttribute('min', 0);
              range.setAttribute('max', 50);
              range.addEventListener('change', updateRangeSetting);
              range.value = currentSettings[game][settingName][parseInt(option, 10)];
              tdMiddle.appendChild(range);
              tr.appendChild(tdMiddle);

              const tdRight = document.createElement('td');
              tdRight.setAttribute('id', `${game}-${settingName}-${option}`)
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
            range.setAttribute('id', `${game}-${settingName}-${option}-range`);
            range.setAttribute('data-game', game);
            range.setAttribute('data-setting', settingName);
            range.setAttribute('data-option', option);
            range.setAttribute('min', 0);
            range.setAttribute('max', 50);
            range.addEventListener('change', updateRangeSetting);
            range.value = currentSettings[game][settingName][option];
            tdMiddle.appendChild(range);
            tr.appendChild(tdMiddle);

            const tdRight = document.createElement('td');
            tdRight.setAttribute('id', `${game}-${settingName}-${option}`)
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

        Object.values(gameItems).forEach((item) => {
          const itemRow = document.createElement('div');
          itemRow.classList.add('list-row');

          const itemLabel = document.createElement('label');
          itemLabel.setAttribute('for', `${game}-${settingName}-${item}`)

          const itemCheckbox = document.createElement('input');
          itemCheckbox.setAttribute('id', `${game}-${settingName}-${item}`);
          itemCheckbox.setAttribute('type', 'checkbox');
          itemCheckbox.setAttribute('data-game', game);
          itemCheckbox.setAttribute('data-setting', settingName);
          itemCheckbox.setAttribute('data-option', item.toString());
          itemCheckbox.addEventListener('change', updateListSetting);
          if (currentSettings[game][settingName].includes(item)) {
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

        Object.values(gameLocations).forEach((location) => {
          const locationRow = document.createElement('div');
          locationRow.classList.add('list-row');

          const locationLabel = document.createElement('label');
          locationLabel.setAttribute('for', `${game}-${settingName}-${location}`)

          const locationCheckbox = document.createElement('input');
          locationCheckbox.setAttribute('id', `${game}-${settingName}-${location}`);
          locationCheckbox.setAttribute('type', 'checkbox');
          locationCheckbox.setAttribute('data-game', game);
          locationCheckbox.setAttribute('data-setting', settingName);
          locationCheckbox.setAttribute('data-option', location.toString());
          locationCheckbox.addEventListener('change', updateListSetting);
          if (currentSettings[game][settingName].includes(location)) {
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

        Object.values(settings[settingName].options).forEach((listItem) => {
          const customListRow = document.createElement('div');
          customListRow.classList.add('list-row');

          const customItemLabel = document.createElement('label');
          customItemLabel.setAttribute('for', `${game}-${settingName}-${listItem}`)

          const customItemCheckbox = document.createElement('input');
          customItemCheckbox.setAttribute('id', `${game}-${settingName}-${listItem}`);
          customItemCheckbox.setAttribute('type', 'checkbox');
          customItemCheckbox.setAttribute('data-game', game);
          customItemCheckbox.setAttribute('data-setting', settingName);
          customItemCheckbox.setAttribute('data-option', listItem.toString());
          customItemCheckbox.addEventListener('change', updateListSetting);
          if (currentSettings[game][settingName].includes(listItem)) {
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
        console.error(`Unknown setting type for ${game} setting ${settingName}: ${setting.type}`);
        return;
    }

    settingsWrapper.appendChild(settingWrapper);
  });

  return settingsWrapper;
};

const buildItemsDiv = (game, items) => {
  // Sort alphabetical, in pace
  items.sort();

  const currentSettings = JSON.parse(localStorage.getItem('weighted-settings'));
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

  // Create container divs for each category
  const availableItemsWrapper = document.createElement('div');
  availableItemsWrapper.classList.add('item-set-wrapper');
  availableItemsWrapper.innerText = 'Available Items';
  const availableItems = document.createElement('div');
  availableItems.classList.add('item-container');
  availableItems.setAttribute('id', `${game}-available_items`);
  availableItems.addEventListener('dragover', itemDragoverHandler);
  availableItems.addEventListener('drop', itemDropHandler);

  const startInventoryWrapper = document.createElement('div');
  startInventoryWrapper.classList.add('item-set-wrapper');
  startInventoryWrapper.innerText = 'Start Inventory';
  const startInventory = document.createElement('div');
  startInventory.classList.add('item-container');
  startInventory.setAttribute('id', `${game}-start_inventory`);
  startInventory.setAttribute('data-setting', 'start_inventory');
  startInventory.addEventListener('dragover', itemDragoverHandler);
  startInventory.addEventListener('drop', itemDropHandler);

  const localItemsWrapper = document.createElement('div');
  localItemsWrapper.classList.add('item-set-wrapper');
  localItemsWrapper.innerText = 'Local Items';
  const localItems = document.createElement('div');
  localItems.classList.add('item-container');
  localItems.setAttribute('id', `${game}-local_items`);
  localItems.setAttribute('data-setting', 'local_items')
  localItems.addEventListener('dragover', itemDragoverHandler);
  localItems.addEventListener('drop', itemDropHandler);

  const nonLocalItemsWrapper = document.createElement('div');
  nonLocalItemsWrapper.classList.add('item-set-wrapper');
  nonLocalItemsWrapper.innerText = 'Non-Local Items';
  const nonLocalItems = document.createElement('div');
  nonLocalItems.classList.add('item-container');
  nonLocalItems.setAttribute('id', `${game}-non_local_items`);
  nonLocalItems.setAttribute('data-setting', 'non_local_items');
  nonLocalItems.addEventListener('dragover', itemDragoverHandler);
  nonLocalItems.addEventListener('drop', itemDropHandler);

  // Populate the divs
  items.forEach((item) => {
    if (Object.keys(currentSettings[game].start_inventory).includes(item)){
      const itemDiv = buildItemQtyDiv(game, item);
      itemDiv.setAttribute('data-setting', 'start_inventory');
      startInventory.appendChild(itemDiv);
    } else if (currentSettings[game].local_items.includes(item)) {
      const itemDiv = buildItemDiv(game, item);
      itemDiv.setAttribute('data-setting', 'local_items');
      localItems.appendChild(itemDiv);
    } else if (currentSettings[game].non_local_items.includes(item)) {
      const itemDiv = buildItemDiv(game, item);
      itemDiv.setAttribute('data-setting', 'non_local_items');
      nonLocalItems.appendChild(itemDiv);
    } else {
      const itemDiv = buildItemDiv(game, item);
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
};

const buildItemDiv = (game, item) => {
  const itemDiv = document.createElement('div');
  itemDiv.classList.add('item-div');
  itemDiv.setAttribute('id', `${game}-${item}`);
  itemDiv.setAttribute('data-game', game);
  itemDiv.setAttribute('data-item', item);
  itemDiv.setAttribute('draggable', 'true');
  itemDiv.innerText = item;
  itemDiv.addEventListener('dragstart', (evt) => {
    evt.dataTransfer.setData('text/plain', itemDiv.getAttribute('id'));
  });
  return itemDiv;
};

const buildItemQtyDiv = (game, item) => {
  const currentSettings = JSON.parse(localStorage.getItem('weighted-settings'));
  const itemQtyDiv = document.createElement('div');
  itemQtyDiv.classList.add('item-qty-div');
  itemQtyDiv.setAttribute('id', `${game}-${item}`);
  itemQtyDiv.setAttribute('data-game', game);
  itemQtyDiv.setAttribute('data-item', item);
  itemQtyDiv.setAttribute('draggable', 'true');
  itemQtyDiv.innerText = item;

  const inputWrapper = document.createElement('div');
  inputWrapper.classList.add('item-qty-input-wrapper')

  const itemQty = document.createElement('input');
  itemQty.setAttribute('value', currentSettings[game].start_inventory.hasOwnProperty(item) ?
    currentSettings[game].start_inventory[item] : '1');
  itemQty.setAttribute('data-game', game);
  itemQty.setAttribute('data-setting', 'start_inventory');
  itemQty.setAttribute('data-option', item);
  itemQty.setAttribute('maxlength', '3');
  itemQty.addEventListener('keyup', (evt) => {
    evt.target.value = isNaN(parseInt(evt.target.value)) ? 0 : parseInt(evt.target.value);
    updateItemSetting(evt);
  });
  inputWrapper.appendChild(itemQty);
  itemQtyDiv.appendChild(inputWrapper);

  itemQtyDiv.addEventListener('dragstart', (evt) => {
    evt.dataTransfer.setData('text/plain', itemQtyDiv.getAttribute('id'));
  });
  return itemQtyDiv;
};

const itemDragoverHandler = (evt) => {
  evt.preventDefault();
};

const itemDropHandler = (evt) => {
  evt.preventDefault();
  const sourceId = evt.dataTransfer.getData('text/plain');
  const sourceDiv = document.getElementById(sourceId);

  const currentSettings = JSON.parse(localStorage.getItem('weighted-settings'));
  const game = sourceDiv.getAttribute('data-game');
  const item = sourceDiv.getAttribute('data-item');

  const oldSetting = sourceDiv.hasAttribute('data-setting') ? sourceDiv.getAttribute('data-setting') : null;
  const newSetting = evt.target.hasAttribute('data-setting') ? evt.target.getAttribute('data-setting') : null;

  const itemDiv = newSetting === 'start_inventory' ? buildItemQtyDiv(game, item) : buildItemDiv(game, item);

  if (oldSetting) {
    if (oldSetting === 'start_inventory') {
      if (currentSettings[game][oldSetting].hasOwnProperty(item)) {
        delete currentSettings[game][oldSetting][item];
      }
    } else {
      if (currentSettings[game][oldSetting].includes(item)) {
        currentSettings[game][oldSetting].splice(currentSettings[game][oldSetting].indexOf(item), 1);
      }
    }
  }

  if (newSetting) {
    itemDiv.setAttribute('data-setting', newSetting);
    document.getElementById(`${game}-${newSetting}`).appendChild(itemDiv);
    if (newSetting === 'start_inventory') {
      currentSettings[game][newSetting][item] = 1;
    } else {
      if (!currentSettings[game][newSetting].includes(item)){
        currentSettings[game][newSetting].push(item);
      }
    }
  } else {
    // No setting was assigned, this item has been removed from the settings
    document.getElementById(`${game}-available_items`).appendChild(itemDiv);
  }

  // Remove the source drag object
  sourceDiv.parentElement.removeChild(sourceDiv);

  // Save the updated settings
  localStorage.setItem('weighted-settings', JSON.stringify(currentSettings));
};

const buildHintsDiv = (game, items, locations) => {
  const currentSettings = JSON.parse(localStorage.getItem('weighted-settings'));

  // Sort alphabetical, in place
  items.sort();
  locations.sort();

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
  items.forEach((item) => {
    const itemRow = document.createElement('div');
    itemRow.classList.add('list-row');

    const itemLabel = document.createElement('label');
    itemLabel.setAttribute('for', `${game}-start_hints-${item}`);

    const itemCheckbox = document.createElement('input');
    itemCheckbox.setAttribute('type', 'checkbox');
    itemCheckbox.setAttribute('id', `${game}-start_hints-${item}`);
    itemCheckbox.setAttribute('data-game', game);
    itemCheckbox.setAttribute('data-setting', 'start_hints');
    itemCheckbox.setAttribute('data-option', item);
    if (currentSettings[game].start_hints.includes(item)) {
      itemCheckbox.setAttribute('checked', 'true');
    }
    itemCheckbox.addEventListener('change', updateListSetting);
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
  locations.forEach((location) => {
    const locationRow = document.createElement('div');
    locationRow.classList.add('list-row');

    const locationLabel = document.createElement('label');
    locationLabel.setAttribute('for', `${game}-start_location_hints-${location}`);

    const locationCheckbox = document.createElement('input');
    locationCheckbox.setAttribute('type', 'checkbox');
    locationCheckbox.setAttribute('id', `${game}-start_location_hints-${location}`);
    locationCheckbox.setAttribute('data-game', game);
    locationCheckbox.setAttribute('data-setting', 'start_location_hints');
    locationCheckbox.setAttribute('data-option', location);
    if (currentSettings[game].start_location_hints.includes(location)) {
      locationCheckbox.setAttribute('checked', '1');
    }
    locationCheckbox.addEventListener('change', updateListSetting);
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
};

const buildLocationsDiv = (game, locations) => {
  const currentSettings = JSON.parse(localStorage.getItem('weighted-settings'));
  locations.sort(); // Sort alphabetical, in-place

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
  locations.forEach((location) => {
    const locationRow = document.createElement('div');
    locationRow.classList.add('list-row');

    const locationLabel = document.createElement('label');
    locationLabel.setAttribute('for', `${game}-priority_locations-${location}`);

    const locationCheckbox = document.createElement('input');
    locationCheckbox.setAttribute('type', 'checkbox');
    locationCheckbox.setAttribute('id', `${game}-priority_locations-${location}`);
    locationCheckbox.setAttribute('data-game', game);
    locationCheckbox.setAttribute('data-setting', 'priority_locations');
    locationCheckbox.setAttribute('data-option', location);
    if (currentSettings[game].priority_locations.includes(location)) {
      locationCheckbox.setAttribute('checked', '1');
    }
    locationCheckbox.addEventListener('change', updateListSetting);
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
  locations.forEach((location) => {
    const locationRow = document.createElement('div');
    locationRow.classList.add('list-row');

    const locationLabel = document.createElement('label');
    locationLabel.setAttribute('for', `${game}-exclude_locations-${location}`);

    const locationCheckbox = document.createElement('input');
    locationCheckbox.setAttribute('type', 'checkbox');
    locationCheckbox.setAttribute('id', `${game}-exclude_locations-${location}`);
    locationCheckbox.setAttribute('data-game', game);
    locationCheckbox.setAttribute('data-setting', 'exclude_locations');
    locationCheckbox.setAttribute('data-option', location);
    if (currentSettings[game].exclude_locations.includes(location)) {
      locationCheckbox.setAttribute('checked', '1');
    }
    locationCheckbox.addEventListener('change', updateListSetting);
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
};

const updateVisibleGames = () => {
  const settings = JSON.parse(localStorage.getItem('weighted-settings'));
  Object.keys(settings.game).forEach((game) => {
    const gameDiv = document.getElementById(`${game}-div`);
    const gameOption = document.getElementById(`${game}-game-option`);
    if (parseInt(settings.game[game], 10) > 0) {
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

const updateRangeSetting = (evt) => {
  const options = JSON.parse(localStorage.getItem('weighted-settings'));
  const game = evt.target.getAttribute('data-game');
  const setting = evt.target.getAttribute('data-setting');
  const option = evt.target.getAttribute('data-option');
  document.getElementById(`${game}-${setting}-${option}`).innerText = evt.target.value;
  if (evt.action && evt.action === 'rangeDelete') {
    delete options[game][setting][option];
  } else {
    options[game][setting][option] = parseInt(evt.target.value, 10);
  }
  localStorage.setItem('weighted-settings', JSON.stringify(options));
};

const updateListSetting = (evt) => {
  const options = JSON.parse(localStorage.getItem('weighted-settings'));
  const game = evt.target.getAttribute('data-game');
  const setting = evt.target.getAttribute('data-setting');
  const option = evt.target.getAttribute('data-option');

  if (evt.target.checked) {
    // If the option is to be enabled and it is already enabled, do nothing
    if (options[game][setting].includes(option)) { return; }

    options[game][setting].push(option);
  } else {
    // If the option is to be disabled and it is already disabled, do nothing
    if (!options[game][setting].includes(option)) { return; }

    options[game][setting].splice(options[game][setting].indexOf(option), 1);
  }
  localStorage.setItem('weighted-settings', JSON.stringify(options));
};

const updateItemSetting = (evt) => {
  const options = JSON.parse(localStorage.getItem('weighted-settings'));
  const game = evt.target.getAttribute('data-game');
  const setting = evt.target.getAttribute('data-setting');
  const option = evt.target.getAttribute('data-option');
  if (setting === 'start_inventory') {
    options[game][setting][option] = evt.target.value.trim() ? parseInt(evt.target.value) : 0;
  } else {
    options[game][setting][option] = isNaN(evt.target.value) ?
      evt.target.value : parseInt(evt.target.value, 10);
  }
  localStorage.setItem('weighted-settings', JSON.stringify(options));
};

const validateSettings = () => {
  const settings = JSON.parse(localStorage.getItem('weighted-settings'));
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
};

const exportSettings = () => {
  const settings = validateSettings();
  if (!settings) { return; }

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
  const settings = validateSettings();
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
};
