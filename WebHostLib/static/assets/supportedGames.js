window.addEventListener('load', () => {
  const allDetails = document.querySelectorAll('details');

  // Handle game filter input
  const gameSearch = document.getElementById('game-search');
  gameSearch.value = '';
  gameSearch.addEventListener('input', (evt) => {
    if (!evt.target.value.trim()) {
      // If input is empty, display all collapsed games
      return allDetails.forEach((detail) => {
        detail.style.display = null;
        detail.open = false;
      });
    }

    // Loop over all the games
    allDetails.forEach((details) => {
      // If the game name includes the search string, display the game. If not, hide it
      if (details.getAttribute('data-game').toLowerCase().includes(evt.target.value.toLowerCase())) {
        details.style.display = null;
        details.open = true;
      } else {
        details.style.display = 'none';
        details.open = false;
      }
    });
  });

  document.getElementById('expand-all').addEventListener('click', expandAll);
  document.getElementById('collapse-all').addEventListener('click', collapseAll);
});

const expandAll = () => {
  document.querySelectorAll('details').forEach((details) => {
    details.open = true;
  });
};

const collapseAll = () => {
  document.querySelectorAll('details').forEach((details) => {
    details.open = false;
  });
};
