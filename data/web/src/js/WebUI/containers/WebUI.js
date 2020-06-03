import React, { Component } from 'react';
import { connect } from 'react-redux';
import HeaderBar from '../../HeaderBar/components/HeaderBar';
import Monitor from '../../Monitor/components/Monitor';
import WidgetArea from '../../WidgetArea/containers/WidgetArea';
import '../../../styles/WebUI/containers/WebUI.scss';

// Redux actions
import setWebSocket from '../Redux/actions/setWebSocket';
import WebSocketUtils from '../../global/WebSocketUtils';
import updateGameState from '../../global/Redux/actions/updateGameState';

const mapReduxStateToProps = (reduxState) => ({
  connections: reduxState.gameState.connections,
});

const mapDispatchToProps = (dispatch) => ({
  doSetWebSocket: (webSocket) => dispatch(setWebSocket(webSocket)),
  handleIncomingMessage: (message) => dispatch(WebSocketUtils.handleIncomingMessage(message)),
  doUpdateGameState: (gameState) => dispatch(updateGameState(gameState)),
});

class WebUI extends Component {
  constructor(props) {
    super(props);
    this.webSocket = null;
    this.webUiRef = React.createRef();
  }

  componentDidMount() {
    this.webSocketConnect();
  }

  webSocketConnect = () => {
    const getParams = new URLSearchParams(document.location.search.substring(1));
    const port = getParams.get('port');
    if (!port) { throw new Error('Unable to determine socket port from GET parameters'); }

    const webSocketAddress = `ws://localhost:${port}`;
    try {
      this.props.webSocket.close();
      this.props.doSetWebSocket(null);
    } catch (error) {
      // Ignore errors caused by attempting to close an invalid WebSocket object
    }

    const webSocket = new WebSocket(webSocketAddress);
    webSocket.onerror = () => {
      this.props.doUpdateGameState({
        connections: {
          snesDevice: this.props.connections.snesDevice,
          snesConnected: false,
          serverAddress: this.props.connections.serverAddress,
          serverConnected: false,
        },
      });
      setTimeout(this.webSocketConnect, 5000);
    };
    webSocket.onclose = () => {
      // If the WebSocket connection is closed for some reason, attempt to reconnect
      this.props.doUpdateGameState({
        connections: {
          snesDevice: this.props.connections.snesDevice,
          snesConnected: false,
          serverAddress: this.props.connections.serverAddress,
          serverConnected: false,
        },
      });
      setTimeout(this.webSocketConnect, 5000);
    };

    // Dispatch a custom event when websocket messages are received
    webSocket.onmessage = (message) => {
      this.props.handleIncomingMessage(message);
    };

    // Store the webSocket object in the Redux store so other components can access it
    webSocket.onopen = () => {
      this.props.doSetWebSocket(webSocket);
      webSocket.send(WebSocketUtils.formatSocketData('webStatus', 'connections'));
    };
  };

  render() {
    return (
      <div id="web-ui" ref={ this.webUiRef }>
        <HeaderBar />
        <div id="content-middle">
          <Monitor />
          <WidgetArea />
        </div>
      </div>
    );
  }
}

export default connect(mapReduxStateToProps, mapDispatchToProps)(WebUI);
