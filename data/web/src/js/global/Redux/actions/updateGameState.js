const UPDATE_GAME_STATE = 'UPDATE_GAME_STATE';

const updateGameState = (gameState) => ({
  type: UPDATE_GAME_STATE,
  gameState,
});

export default updateGameState;
