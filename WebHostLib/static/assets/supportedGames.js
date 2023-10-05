window.addEventListener('load', () => {
  const gameHeaders = document.getElementsByClassName('collapse-toggle');
  Array.from(gameHeaders).forEach((header) => {
    const gameName = header.getAttribute('data-game');
    header.addEventListener('click', () => {
      const gameArrow = document.getElementById(`${gameName}-arrow`);
      const gameInfo = document.getElementById(gameName);
      if (gameInfo.classList.contains('collapsed')) {
        gameArrow.innerText = '▼';
        gameInfo.classList.remove('collapsed');
      } else {
        gameArrow.innerText = '▶';
        gameInfo.classList.add('collapsed');
      }
    });
  });

  // Handle game filter input
  const gameSearch = document.getElementById('game-search');
  gameSearch.value = '';

  gameSearch.addEventListener('input', (evt) => {
    if (!evt.target.value.trim()) {
      // If input is empty, display all collapsed games
      return Array.from(gameHeaders).forEach((header) => {
        header.style.display = null;
        const gameName = header.getAttribute('data-game');
        document.getElementById(`${gameName}-arrow`).innerText = '▶';
        document.getElementById(gameName).classList.add('collapsed');
      });
    }

    // Loop over all the games
    Array.from(gameHeaders).forEach((header) => {
      const gameName = header.getAttribute('data-game');
      const gameArrow = document.getElementById(`${gameName}-arrow`);
      const gameInfo = document.getElementById(gameName);

      // If the game name includes the search string, display the game. If not, hide it
      if (gameName.toLowerCase().includes(evt.target.value.toLowerCase())) {
        header.style.display = null;
        gameArrow.innerText = '▼';
        gameInfo.classList.remove('collapsed');
      } else {
        console.log(header);
        header.style.display = 'none';
        gameArrow.innerText = '▶';
        gameInfo.classList.add('collapsed');
      }
    });
  });

  document.getElementById('expand-all').addEventListener('click', expandAll);
  document.getElementById('collapse-all').addEventListener('click', collapseAll);
});

const expandAll = () => {
  const gameHeaders = document.getElementsByClassName('collapse-toggle');
  // Loop over all the games
    Array.from(gameHeaders).forEach((header) => {
      const gameName = header.getAttribute('data-game');
      const gameArrow = document.getElementById(`${gameName}-arrow`);
      const gameInfo = document.getElementById(gameName);

      if (header.style.display === 'none') { return; }
      gameArrow.innerText = '▼';
      gameInfo.classList.remove('collapsed');
    });
};

const collapseAll = () => {
  const gameHeaders = document.getElementsByClassName('collapse-toggle');
  // Loop over all the games
    Array.from(gameHeaders).forEach((header) => {
      const gameName = header.getAttribute('data-game');
      const gameArrow = document.getElementById(`${gameName}-arrow`);
      const gameInfo = document.getElementById(gameName);

      if (header.style.display === 'none') { return; }
      gameArrow.innerText = '▶';
      gameInfo.classList.add('collapsed');
    });
};
