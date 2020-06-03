import React from 'react';
import ReactDom from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, combineReducers } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension/developmentOnly';
import WebUI from './WebUI/containers/WebUI';
import '../styles/index.scss';

// Redux reducers
import webUI from './WebUI/Redux/reducers/webUIReducer';
import gameState from './global/Redux/reducers/gameStateReducer';
import monitor from './Monitor/Redux/reducers/monitorReducer';

const store = createStore(combineReducers({
  webUI,
  gameState,
  monitor,
}), composeWithDevTools());

const App = () => (
  <Provider store={ store }>
    <WebUI />
  </Provider>
);

window.onload = () => {
  ReactDom.render(<App />, document.getElementById('app'));
};
