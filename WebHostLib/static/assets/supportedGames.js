window.addEventListener('load', () => {
  // Add toggle listener to all elements with .collapse-toggle
  const toggleButtons = document.querySelectorAll('details');

  // Favorites functionality
  const FAVORITES_STORAGE_KEY = 'ashipelago_favorite_games';
  const favoritesSection = document.getElementById('favorites-section');
  const favoritesList = document.getElementById('favorites-list');
  let favoriteGames = new Set();
  let originalElements = new Map(); // Store original elements for cloning

  // Load favorites from localStorage
  function loadFavorites() {
    try {
      const stored = localStorage.getItem(FAVORITES_STORAGE_KEY);
      if (stored) {
        favoriteGames = new Set(JSON.parse(stored));
      }
    } catch (e) {
      console.warn('Failed to load favorites from localStorage:', e);
    }
  }

  // Save favorites to localStorage
  function saveFavorites() {
    try {
      localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify([...favoriteGames]));
    } catch (e) {
      console.warn('Failed to save favorites to localStorage:', e);
    }
  }

  // Update star icon appearance
  function updateStarIcon(starIcon, isFavorited) {
    if (isFavorited) {
      starIcon.classList.add('favorited');
      starIcon.title = 'Remove from favorites';
    } else {
      starIcon.classList.remove('favorited');
      starIcon.title = 'Add to favorites';
    }
  }

  // Toggle favorite status
  function toggleFavorite(gameName) {
    const wasFavorited = favoriteGames.has(gameName);

    if (wasFavorited) {
      favoriteGames.delete(gameName);
    } else {
      favoriteGames.add(gameName);
    }
    saveFavorites();
    updateFavoritesSection();
    updateMainListVisibility();

    // Clear search bar when adding a new favorite
    if (!wasFavorited) {
      const gameSearch = document.getElementById('game-search');
      if (gameSearch) {
        gameSearch.value = '';
        // Trigger the search input event to update visibility
        gameSearch.dispatchEvent(new Event('input'));
      }
    }
  }

  // Update the favorites section
  function updateFavoritesSection() {
    if (favoriteGames.size === 0) {
      favoritesSection.style.display = 'none';
      // Update star icons in the main list when favorites section is hidden
      document.querySelectorAll('.star-icon').forEach(starIcon => {
        const gameName = starIcon.getAttribute('data-game');
        if (gameName) {
          updateStarIcon(starIcon, favoriteGames.has(gameName));
        }
      });
      return;
    }

    favoritesSection.style.display = 'block';
    favoritesList.innerHTML = '';

    // Sort favorites alphabetically by display name
    const sortedFavorites = Array.from(favoriteGames).sort((a, b) => {
      const elementA = originalElements.get(a);
      const elementB = originalElements.get(b);

      if (!elementA || !elementB) return 0;

      const displayNameA = elementA.getAttribute('data-game') || a;
      const displayNameB = elementB.getAttribute('data-game') || b;

      return displayNameA.toLowerCase().localeCompare(displayNameB.toLowerCase());
    });

    sortedFavorites.forEach(gameName => {
      // Get the original element from our stored map
      const originalElement = originalElements.get(gameName);
      if (!originalElement) return;

      const clone = originalElement.cloneNode(true);
      clone.classList.add('favorite-game-item');

      // Update the star icon in the clone
      const starIcon = clone.querySelector('.star-icon');
      if (starIcon) {
        updateStarIcon(starIcon, true);
        starIcon.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          toggleFavorite(gameName);
        });
      }

      favoritesList.appendChild(clone);
    });

    // Update star icons in the main list
    document.querySelectorAll('.star-icon').forEach(starIcon => {
      const gameName = starIcon.getAttribute('data-game');
      if (gameName) {
        updateStarIcon(starIcon, favoriteGames.has(gameName));
      }
    });
  }

  // Update main list visibility to hide favorited games
  function updateMainListVisibility() {
    // Only target details in the main list, not in the favorites section
    document.querySelectorAll('#games > details').forEach(detail => {
      const gameName = detail.getAttribute('data-game');
      if (gameName && favoriteGames.has(gameName)) {
        detail.style.display = 'none';
      } else {
        detail.style.display = null;
      }
    });
  }

  // Store original elements for cloning
  function storeOriginalElements() {
    document.querySelectorAll('details').forEach(detail => {
      const gameName = detail.getAttribute('data-game');
      if (gameName) {
        originalElements.set(gameName, detail.cloneNode(true));
      }
    });
  }

  // Add click handlers to all star icons
  function initializeStarIcons() {
    document.querySelectorAll('.star-icon').forEach(starIcon => {
      const gameName = starIcon.getAttribute('data-game');
      if (!gameName) return;

      updateStarIcon(starIcon, favoriteGames.has(gameName));

      starIcon.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        toggleFavorite(gameName);
      });
    });
  }

  // Initialize favorites
  loadFavorites();
  storeOriginalElements();
  initializeStarIcons();
  updateFavoritesSection();
  updateMainListVisibility();
  
  // Handle game filter input
  const gameSearch = document.getElementById('game-search');
  gameSearch.value = '';
  gameSearch.addEventListener('input', (evt) => {
    if (!evt.target.value.trim()) {
      // If input is empty, display all games as collapsed
      toggleButtons.forEach((header) => {
        header.style.display = null;
        header.removeAttribute('open');
      });

      // Also restore all favorites to visible
      const favoriteItems = favoritesList.querySelectorAll('.favorite-game-item');
      favoriteItems.forEach(item => {
        item.style.display = null;
        item.removeAttribute('open');
      });

      // Re-apply favorites visibility logic after clearing search
      updateMainListVisibility();
      return;
    }

    // Loop over all the games
    toggleButtons.forEach((header) => {
      // If the game name includes the search string, display the game. If not, hide it
      if (header.getAttribute('data-game-display').toLowerCase().includes(evt.target.value.toLowerCase())) {
        header.style.display = null;
        header.setAttribute('open', '1');
      } else {
        header.style.display = 'none';
        header.removeAttribute('open');
      }
    });
    
    // Also filter favorites section
    const favoriteItems = favoritesList.querySelectorAll('.favorite-game-item');
    favoriteItems.forEach(item => {
      const gameName = item.getAttribute('data-game-display').toLowerCase();

      if (gameName.includes(searchTerm)) {
        item.style.display = null;
        item.setAttribute('open', '1');
      } else {
        item.style.display = 'none';
        item.removeAttribute('open');
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
