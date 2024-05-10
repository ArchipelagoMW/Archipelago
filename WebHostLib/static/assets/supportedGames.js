window.addEventListener('load', () => {
  // Add toggle listener to all elements with .collapse-toggle
  const toggleButtons = document.querySelectorAll('.collapse-toggle');
  toggleButtons.forEach((e) => e.addEventListener('click', toggleCollapse));

  // Handle game filter input
  const gameSearch = document.getElementById('game-search');
  gameSearch.value = '';
  gameSearch.addEventListener('input', (evt) => {
    if (!evt.target.value.trim()) {
      // If input is empty, display all collapsed games
      return toggleButtons.forEach((header) => {
        header.style.display = null;
        header.firstElementChild.innerText = '▶';
        header.nextElementSibling.classList.add('collapsed');
      });
    }

    // Loop over all the games
    toggleButtons.forEach((header) => {
      // If the game name includes the search string, display the game. If not, hide it
      if (header.getAttribute('data-game').toLowerCase().includes(evt.target.value.toLowerCase())) {
        header.style.display = null;
        header.firstElementChild.innerText = '▼';
        header.nextElementSibling.classList.remove('collapsed');
      } else {
        header.style.display = 'none';
        header.firstElementChild.innerText = '▶';
        header.nextElementSibling.classList.add('collapsed');
      }
    });
  });

  document.getElementById('expand-all').addEventListener('click', expandAll);
  document.getElementById('collapse-all').addEventListener('click', collapseAll);
});

const toggleCollapse = (evt) => {
  const gameArrow = evt.target.firstElementChild;
  const gameInfo = evt.target.nextElementSibling;
  if (gameInfo.classList.contains('collapsed')) {
    gameArrow.innerText = '▼';
    gameInfo.classList.remove('collapsed');
  } else {
    gameArrow.innerText = '▶';
    gameInfo.classList.add('collapsed');
  }
};

const expandAll = () => {
  document.querySelectorAll('.collapse-toggle').forEach((header) => {
    if (header.style.display === 'none') { return; }
    header.firstElementChild.innerText = '▼';
    header.nextElementSibling.classList.remove('collapsed');
  });
};

const collapseAll = () => {
  document.querySelectorAll('.collapse-toggle').forEach((header) => {
    if (header.style.display === 'none') { return; }
    header.firstElementChild.innerText = '▶';
    header.nextElementSibling.classList.add('collapsed');
  });
};
