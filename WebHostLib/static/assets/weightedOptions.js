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

  // TODO: Handle creating new rows for Range options

  // Detect form submission
  document.getElementById('weighted-options-form').addEventListener('submit', (evt) => {
    // TODO: Save data to localStorage
    evt.preventDefault();
  });

  // TODO: Populate all settings from localStorage on page initialisation
});
