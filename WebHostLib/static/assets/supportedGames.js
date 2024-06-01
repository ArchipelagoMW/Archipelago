window.addEventListener('load', () => {
  // Add toggle listener to all elements with .collapse-toggle
  const toggleButtons = document.querySelectorAll('details');

  // Handle game filter input
  const gameSearch = document.getElementById('game-search');
  gameSearch.value = '';
  gameSearch.addEventListener('input', (evt) => {
    if (!evt.target.value.trim()) {
      // If input is empty, display all games as collapsed
      return toggleButtons.forEach((header) => {
        header.style.display = null;
        header.removeAttribute('open');
      });
    }

    // Loop over all the games
    toggleButtons.forEach((header) => {
      // If the game name includes the search string, display the game. If not, hide it
      if (header.getAttribute('data-game').toLowerCase().includes(evt.target.value.toLowerCase())) {
        header.style.display = null;
        header.setAttribute('open', '1');
      } else {
        header.style.display = 'none';
        header.removeAttribute('open');
      }
    });
  });

  document.getElementById('expand-all').addEventListener('click', expandAll);
  document.getElementById('collapse-all').addEventListener('click', collapseAll);
});

const expandAll = () => {
  document.querySelectorAll('details').forEach((detail) => {
    detail.setAttribute('open', '1');
  });
};

const collapseAll = () => {
  document.querySelectorAll('details').forEach((detail) => {
    detail.removeAttribute('open');
  });
};
