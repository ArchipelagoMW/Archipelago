import _assign from 'lodash-es/assign';

const initialState = {
  clientVersion: null,
  forfeitMode: null,
  remainingMode: null,
  connections: {
    snesDevice: '',
    snesConnected: false,
    serverAddress: null,
    serverConnected: false,
  },
  totalChecks: 0,
  lastCheck: null,
  hintCost: null,
  checkPoints: null,
  hintPoints: 0,
};

const gameStateReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'UPDATE_GAME_STATE':
      return _assign({}, state, action.gameState);

    default:
      return state;
  }
};

export default gameStateReducer;
