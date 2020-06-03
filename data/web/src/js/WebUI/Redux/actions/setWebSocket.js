const SET_WEBSOCKET = 'SET_WEBSOCKET';

const setWebSocket = (webSocket) => ({
  type: SET_WEBSOCKET,
  webSocket,
});

export default setWebSocket;
