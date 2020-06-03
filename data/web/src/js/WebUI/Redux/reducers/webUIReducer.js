import _assign from 'lodash-es/assign';

const initialState = {
  webSocket: null,
  availableDevices: [],
};

const webUIReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_WEBSOCKET':
      return _assign({}, state, {
        webSocket: action.webSocket,
      });

    case 'SET_AVAILABLE_DEVICES':
      return _assign({}, state, {
        availableDevices: action.devices,
      });

    default:
      return state;
  }
};

export default webUIReducer;
