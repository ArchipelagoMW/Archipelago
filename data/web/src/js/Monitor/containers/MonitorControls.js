import React, { Component } from 'react';
import { connect } from 'react-redux';
import _forEach from 'lodash-es/forEach';
import WebSocketUtils from '../../global/WebSocketUtils';
import '../../../styles/Monitor/containers/MonitorControls.scss';

// Redux actions
import setMonitorFontSize from '../Redux/actions/setMonitorFontSize';
import setShowRelevant from '../Redux/actions/setShowRelevant';

const mapReduxStateToProps = (reduxState) => ({
  fontSize: reduxState.monitor.fontSize,
  webSocket: reduxState.webUI.webSocket,
  availableDevices: reduxState.webUI.availableDevices,
  snesDevice: reduxState.gameState.connections.snesDevice,
  snesConnected: reduxState.gameState.connections.snesConnected,
  serverAddress: reduxState.gameState.connections.serverAddress,
  serverConnected: reduxState.gameState.connections.serverConnected,
});

const mapDispatchToProps = (dispatch) => ({
  updateFontSize: (fontSize) => {
    dispatch(setMonitorFontSize(fontSize));
  },
  doToggleRelevance: (showRelevantOnly) => {
    dispatch(setShowRelevant(showRelevantOnly));
  },
});

class MonitorControls extends Component {
  constructor(props) {
    super(props);
    this.state = {
      deviceId: null,
      serverAddress: this.props.serverAddress,
    };
  }

  componentDidMount() {
    setTimeout(() => {
      if (this.props.webSocket) {
      // Poll for available devices
        this.pollSnesDevices();
      }
    }, 500);
  }

  componentDidUpdate(prevProps) {
    // If there is only one SNES device available, connect to it automatically
    if (
      prevProps.availableDevices.length !== this.props.availableDevices.length &&
      this.props.availableDevices.length === 1
    ) {
      // eslint-disable-next-line react/no-did-update-set-state
      this.setState({ deviceId: this.props.availableDevices[0] }, () => {
        if (!this.props.snesConnected) {
          this.connectToSnes();
        }
      });
    }

    // If we have moved from a disconnected state (default) into a connected state, request the game information
    if (
      (
        (prevProps.snesConnected !== this.props.snesConnected) || // SNES status changed
        (prevProps.serverConnected !== this.props.serverConnected) // OR server status changed
      ) && ((this.props.serverConnected) && (this.props.snesConnected)) // AND both are connected
    ) {
      this.props.webSocket.send(WebSocketUtils.formatSocketData('webStatus', 'gameInfo'));
      this.props.webSocket.send(WebSocketUtils.formatSocketData('webStatus', 'checkData'));
    }
  }

  increaseTextSize = () => {
    if (this.props.fontSize >= 25) return;
    this.props.updateFontSize(this.props.fontSize + 1);
  };

  decreaseTextSize = () => {
    if (this.props.fontSize <= 10) return;
    this.props.updateFontSize(this.props.fontSize - 1);
  };

  generateSnesOptions = () => {
    const options = [];
    // No available devices, show waiting for devices
    if (this.props.availableDevices.length === 0) {
      options.push(<option key="0" value="-1">Waiting for devices...</option>);
      return options;
    }

    // More than one available device, list all options
    options.push(<option key="-1" value="-1">Select a device</option>);
    _forEach(this.props.availableDevices, (device) => {
      options.push(<option key={ device } value={ device }>{device}</option>);
    });
    return options;
  }

  updateDeviceId = (event) => this.setState({ deviceId: event.target.value }, this.connectToSnes);

  pollSnesDevices = () => {
    if (!this.props.webSocket) { return; }
    this.props.webSocket.send(WebSocketUtils.formatSocketData('webStatus', 'devices'));
  }

  connectToSnes = () => {
    if (!this.props.webSocket) { return; }
    this.props.webSocket.send(WebSocketUtils.formatSocketData('webConfig', { deviceId: this.state.deviceId }));
  }

  updateServerAddress = (event) => this.setState({ serverAddress: event.target.value ? event.target.value : null });

  connectToServer = (event) => {
    if (event.key !== 'Enter') { return; }

    // If the user presses enter on an empty textbox, disconnect from the server
    if (!event.target.value) {
      this.props.webSocket.send(WebSocketUtils.formatSocketData('webControl', 'disconnect'));
      return;
    }

    this.props.webSocket.send(
      WebSocketUtils.formatSocketData('webConfig', { serverAddress: this.state.serverAddress }),
    );
  }

  toggleRelevance = (event) => {
    this.props.doToggleRelevance(event.target.checked);
  };

  render() {
    return (
      <div id="monitor-controls">
        <div id="connection-status">
          <div id="snes-connection">
            <table>
              <tbody>
                <tr>
                  <td>SNES Device:</td>
                  <td>
                    <select
                      onChange={ this.updateDeviceId }
                      disabled={ this.props.availableDevices.length === 0 }
                      value={ this.state.deviceId }
                    >
                      {this.generateSnesOptions()}
                    </select>
                  </td>
                </tr>
                <tr>
                  <td>Status:</td>
                  <td>
                    <span className={ this.props.snesConnected ? 'connected' : 'not-connected' }>
                      {this.props.snesConnected ? 'Connected' : 'Not Connected'}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div id="server-connection">
            <table>
              <tbody>
                <tr>
                  <td>Server:</td>
                  <td>
                    <input
                      defaultValue={ this.props.serverAddress }
                      onKeyUp={ this.updateServerAddress }
                      onKeyDown={ this.connectToServer }
                    />
                  </td>
                </tr>
                <tr>
                  <td>Status:</td>
                  <td>
                    <span className={ this.props.serverConnected ? 'connected' : 'not-connected' }>
                      {this.props.serverConnected ? 'Connected' : 'Not Connected'}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div id="accessibility">
          <div>
            Text Size:
            <button disabled={ this.props.fontSize <= 10 } onClick={ this.decreaseTextSize }>-</button>
            { this.props.fontSize }
            <button disabled={ this.props.fontSize >= 25 } onClick={ this.increaseTextSize }>+</button>
          </div>
          <div>
            Only show my items <input type="checkbox" onChange={ this.toggleRelevance } />
          </div>
        </div>
      </div>
    );
  }
}

export default connect(mapReduxStateToProps, mapDispatchToProps)(MonitorControls);
