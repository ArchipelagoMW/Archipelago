export const showUserMessage = (message) => {
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

// Loads the options JSON for the game with the given name from the given root-relative url.
//
// If the user has options for this name in local storage and it's out-of-date relative to the
// server data, displays a warning.
//
// The name may be a game name, or "weighted-settings" for the multi-game weighted options page.
export const loadOptions = async (url, name) => {
  const data = await fetch(new Request(`${window.location.origin}${url}`))
      .then(response => response.json());

  const newHash = md5(JSON.stringify(data));
  const storedHash = localStorage.getItem(`${name}-hash`);
  if (!storedHash) {
    // If no hash data has been set before, set it now.
    localStorage.setItem(`${name}-hash`, newHash);
    localStorage.removeItem(name);
  } else if (newHash !== storedHash) {
    showUserMessage(
        'Your options are out of date! Click here to update them! Be aware this will reset them ' +
        'all to default.'
    );
    document.getElementById('user-message').addEventListener('click', () => {
      localStorage.removeItem(name);
      localStorage.removeItem(`${name}-hash`);
      localStorage.removeItem(`${name}-preset`);
      window.location.reload();
    });
  }

  return data;
};

// Create an anchor and trigger a download of a text file.
export const download = (filename, text) => {
  const downloadLink = document.createElement('a');
  downloadLink.setAttribute('href','data:text/yaml;charset=utf-8,'+ encodeURIComponent(text))
  downloadLink.setAttribute('download', filename);
  downloadLink.style.display = 'none';
  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
};

// An abstract class encapsulating options for an individual game.
export class BaseGameOptions {
  // The name of this game.
  name;

  // The data from the server describing the types of settings available for
  // this game, as a JSON-safe blob.
  get data() {
    throw new Error("Child classes must override data().");
  }

  // The settings chosen by the user as they'd appear in the YAML file, stored
  // to and retrieved from local storage.
  get current() {
    throw new Error("Child classes must override current().");
  }

  constructor(name) {
    if (this.constructor === BaseGameOptions) {
      throw new Error("BaseGameOptions is abstract and can't be instantiated directly.");
    }

    this.name = name;
  }

  // Saves the current settings to local storage.
  save() {
    throw new Error("Child classes must override save().");
  }

  // Builds and returns the options UI for this game.
  buildUI() {
    throw new Error("Child classes must override buildUI().");
  }

  // A protected method that adds common UI for options to the end of the given div.
  buildBaseUI(div) {
    this.current.start_inventory ??= {};
    this.current.exclude_locations ??= [];
    this.current.priority_locations ??= [];
    this.current.local_items ??= [];
    this.current.non_local_items ??= [];
    this.current.start_hints ??= [];
    this.current.start_location_hints ??= [];

    const itemPoolDiv = this.#buildItemPoolDiv();
    div.appendChild(itemPoolDiv);

    const hintsDiv = this.#buildHintsDiv();
    div.appendChild(hintsDiv);

    const locationsDiv = this.#buildPriorityExclusionDiv();
    div.appendChild(locationsDiv);
  }

  #buildItemPoolDiv() {
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
      if (this.current.start_inventory.hasOwnProperty(item)) {
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
    const startInventory = this.current.start_inventory ?? {};
    itemQty.setAttribute('value', startInventory.hasOwnProperty(item) ? startInventory[item] : '1');
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

    const itemHintsDiv = this.buildItemsDiv('start_hints');
    itemHintsWrapper.appendChild(itemHintsDiv);
    itemHintsContainer.appendChild(itemHintsWrapper);

    // Starting Location Hints
    const locationHintsWrapper = document.createElement('div');
    locationHintsWrapper.classList.add('hints-wrapper');
    locationHintsWrapper.innerText = 'Starting Location Hints';

    const locationHintsDiv = this.buildLocationsDiv('start_location_hints');
    locationHintsWrapper.appendChild(locationHintsDiv);
    itemHintsContainer.appendChild(locationHintsWrapper);

    hintsDiv.appendChild(itemHintsContainer);
    return hintsDiv;
  }

  #buildPriorityExclusionDiv() {
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

    const priorityLocationsDiv = this.buildLocationsDiv('priority_locations');
    priorityLocationsWrapper.appendChild(priorityLocationsDiv);
    locationsContainer.appendChild(priorityLocationsWrapper);

    // Exclude Locations
    const excludeLocationsWrapper = document.createElement('div');
    excludeLocationsWrapper.classList.add('locations-wrapper');
    excludeLocationsWrapper.innerText = 'Exclude Locations';

    const excludeLocationsDiv = this.buildLocationsDiv('exclude_locations');
    excludeLocationsWrapper.appendChild(excludeLocationsDiv);
    locationsContainer.appendChild(excludeLocationsWrapper);

    locationsDiv.appendChild(locationsContainer);
    return locationsDiv;
  }

  // Builds a div for a setting whose value is a list of locations.
  buildLocationsDiv(setting) {
    return this.buildListDiv(setting, this.data.gameLocations, {
      groups: this.data.gameLocationGroups,
      descriptions: this.data.gameLocationDescriptions,
    });
  }

  // Builds a div for a setting whose value is a list of items.
  buildItemsDiv(setting) {
    return this.buildListDiv(setting, this.data.gameItems, {
      groups: this.data.gameItemGroups,
      descriptions: this.data.gameItemDescriptions
    });
  }

  // Builds a div for a setting named `setting` with a list value that can
  // contain `items`.
  //
  // The `groups` option can be a list of additional options for this list
  // (usually `item_name_groups` or `location_name_groups`) that are displayed
  // in a special section at the top of the list.
  //
  // The `descriptions` option can be a map from item names or group names to
  // descriptions for the user's benefit.
  buildListDiv(setting, items, {groups = [], descriptions = {}} = {}) {
    const div = document.createElement('div');
    div.classList.add('simple-list');

    groups.forEach((group) => {
      const row = this.#addListRow(setting, group, descriptions[group]);
      div.appendChild(row);
    });

    if (groups.length > 0) {
      div.appendChild(document.createElement('hr'));
    }

    items.forEach((item) => {
      const row = this.#addListRow(setting, item, descriptions[item]);
      div.appendChild(row);
    });

    return div;
  }

  // Builds and returns a row for a list of checkboxes.
  //
  // If `help` is passed, it's displayed as a help tooltip for this list item.
  #addListRow(setting, item, help = undefined) {
    const row = document.createElement('div');
    row.classList.add('list-row');

    const label = document.createElement('label');
    label.setAttribute('for', `${this.name}-${setting}-${item}`);

    const checkbox = document.createElement('input');
    checkbox.setAttribute('type', 'checkbox');
    checkbox.setAttribute('id', `${this.name}-${setting}-${item}`);
    checkbox.setAttribute('data-game', this.name);
    checkbox.setAttribute('data-setting', setting);
    checkbox.setAttribute('data-option', item);
    if (this.current[setting].includes(item)) {
      checkbox.setAttribute('checked', '1');
    }
    checkbox.addEventListener('change', (evt) => this.#updateListSetting(evt));
    label.appendChild(checkbox);

    const name = document.createElement('span');
    name.innerText = item;

    if (help) {
      const helpSpan = document.createElement('span');
      helpSpan.classList.add('interactive');
      helpSpan.setAttribute('data-tooltip', help);
      helpSpan.innerText = '(?)';
      name.innerText += ' ';
      name.appendChild(helpSpan);

      // Put the first 7 tooltips below their rows. CSS tooltips in scrolling
      // containers can't be visible outside those containers, so this helps
      // ensure they won't be pushed out the top.
      if (helpSpan.parentNode.childNodes.length < 7) {
        helpSpan.classList.add('tooltip-bottom');
      }
    }

    label.appendChild(name);

    row.appendChild(label);
    return row;
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
}

