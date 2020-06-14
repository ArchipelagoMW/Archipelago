import React, { Component } from 'react';
import { connect } from 'react-redux';
import '../../../styles/WidgetArea/containers/WidgetArea.scss';

const mapReduxStateToProps = (reduxState) => ({
  serverVersion: reduxState.gameState.serverVersion,
  forfeitMode: reduxState.gameState.forfeitMode,
  remainingMode: reduxState.gameState.remainingMode,
  hintCost: reduxState.gameState.hintCost,
  checkPoints: reduxState.gameState.checkPoints,
  hintPoints: reduxState.gameState.hintPoints,
  totalChecks: reduxState.gameState.totalChecks,
  lastCheck: reduxState.gameState.lastCheck,
});

class WidgetArea extends Component {
  constructor(props) {
    super(props);
    this.state = {
      collapsed: false,
    };
  }

  saveNotes = (event) => {
    localStorage.setItem('notes', event.target.value);
  };

  // eslint-disable-next-line react/no-access-state-in-setstate
  toggleCollapse = () => this.setState({ collapsed: !this.state.collapsed });

  render() {
    return (
      <div id="widget-area" className={ `${this.state.collapsed ? 'collapsed' : null}` }>
        {
          this.state.collapsed ? (
            <div id="widget-button-row">
              <button className="collapse-button" onClick={ this.toggleCollapse }>↩</button>
            </div>
          ) : null
        }
        {
          this.state.collapsed ? null : (
            <div id="widget-area-contents">
              <div id="game-info">
                <div id="game-info-title">
                  Game Info:
                  <button className="collapse-button" onClick={ this.toggleCollapse }>↪</button>
                </div>
                <table>
                  <tbody>
                    <tr>
                      <th>Server Version:</th>
                      <td>{this.props.serverVersion}</td>
                    </tr>
                    <tr>
                      <th>Forfeit Mode:</th>
                      <td>{this.props.forfeitMode}</td>
                    </tr>
                    <tr>
                      <th>Remaining Mode:</th>
                      <td>{this.props.remainingMode}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div id="check-data">
                <div id="check-data-title">Checks:</div>
                <table>
                  <tbody>
                    <tr>
                      <th>Total Checks:</th>
                      <td>{this.props.totalChecks}</td>
                    </tr>
                    <tr>
                      <th>Last Check:</th>
                      <td>{this.props.lastCheck}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div id="hint-data">
                <div id="hint-data-title">
                  Hint Data:
                </div>
                <table>
                  <tbody>
                    <tr>
                      <th>Hint Cost:</th>
                      <td>{this.props.hintCost}</td>
                    </tr>
                    <tr>
                      <th>Check Points:</th>
                      <td>{this.props.checkPoints}</td>
                    </tr>
                    <tr>
                      <th>Current Points:</th>
                      <td>{this.props.hintPoints}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div id="notes">
                <div id="notes-title">
                  <div>Notes:</div>
                </div>
                <textarea defaultValue={ localStorage.getItem('notes') } onKeyUp={ this.saveNotes } />
              </div>
              More tools Coming Soon™
            </div>
          )
        }
      </div>
    );
  }
}

export default connect(mapReduxStateToProps)(WidgetArea);
