import MonitorTools from './MonitorTools';

// Redux actions
import appendMessage from '../Monitor/Redux/actions/appendMessage';
import updateGameState from './Redux/actions/updateGameState';
import setAvailableDevices from '../WebUI/Redux/actions/setAvailableDevices';

class WebSocketUtils {
  static formatSocketData = (eventType, content) => JSON.stringify({
    type: eventType,
    content,
  });

  /**
   * Handle incoming websocket data and return appropriate data for dispatch
   * @param message
   * @returns Object
   */
  static handleIncomingMessage = (message) => {
    try {
      const data = JSON.parse(message.data);

      switch (data.type) {
        // Client sent snes and server connection statuses
        case 'connections':
          return updateGameState({
            connections: {
              snesDevice: data.content.snesDevice ? data.content.snesDevice : '',
              snesConnected: parseInt(data.content.snes, 10) === 3,
              serverAddress: data.content.serverAddress ? data.content.serverAddress.replace(/^.*\/\//, '') : null,
              serverConnected: parseInt(data.content.server, 10) === 1,
            },
          });

        case 'availableDevices':
          return setAvailableDevices(data.content.devices);

        // Client unable to automatically connect to multiworld server
        case 'serverAddress':
          return appendMessage(MonitorTools.createTextDiv(
            'Unable to automatically connect to multiworld server. Please enter an address manually.',
          ));

        case 'itemSent':
          return appendMessage(MonitorTools.sentItem(data.content.finder, data.content.recipient,
            data.content.item, data.content.location, parseInt(data.content.iAmFinder, 10) === 1,
            parseInt(data.content.iAmRecipient, 10) === 1));

        case 'itemReceived':
          return appendMessage(MonitorTools.receivedItem(data.content.finder, data.content.item,
            data.content.location, data.content.itemIndex, data.content.queueLength));

        case 'itemFound':
          return appendMessage(MonitorTools.foundItem(data.content.finder, data.content.item, data.content.location,
            parseInt(data.content.iAmFinder, 10) === 1));

        case 'hint':
          return appendMessage(MonitorTools.hintMessage(data.content.finder, data.content.recipient,
            data.content.item, data.content.location, parseInt(data.content.found, 10) === 1,
            parseInt(data.content.iAmFinder, 10) === 1, parseInt(data.content.iAmRecipient, 10) === 1,
            data.content.entranceLocation));

        case 'gameInfo':
          return updateGameState({
            clientVersion: data.content.clientVersion,
            forfeitMode: data.content.forfeitMode,
            remainingMode: data.content.remainingMode,
            hintCost: parseInt(data.content.hintCost, 10),
            checkPoints: parseInt(data.content.checkPoints, 10),
          });

        case 'locationCheck':
          return updateGameState({
            totalChecks: parseInt(data.content.totalChecks, 10),
            lastCheck: data.content.lastCheck,
            hintPoints: parseInt(data.content.hintPoints, 10),
          });

        // The client prints several types of messages to the console
        case 'critical':
        case 'error':
        case 'warning':
        case 'info':
        case 'chat':
          return appendMessage(MonitorTools.createTextDiv(
            (typeof (data.content) === 'string') ? data.content : JSON.stringify(data.content),
          ));
        default:
          console.warn(`Unknown message type received: ${data.type}`);
          console.warn(data.content);
          return { type: 'NO_OP' };
      }
    } catch (error) {
      console.error(message);
      console.error(error);
      // The returned value from this function will be dispatched to Redux. If an error occurs,
      // Redux and the SPA in general should live on. Dispatching something with the correct format
      // but that matches no known Redux action will cause the state to update to itself, which is
      // treated as a no-op.
      return { type: 'NO_OP' };
    }
  };
}

export default WebSocketUtils;
