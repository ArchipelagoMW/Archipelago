import React, { Component } from 'react';
import { connect } from 'react-redux';
import '../../../styles/WidgetArea/containers/WidgetArea.scss';

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
              <div id="notes">
                <div id="notes-title">
                  <div>Notes:</div>
                  <button className="collapse-button" onClick={ this.toggleCollapse }>↪</button>
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

export default connect()(WidgetArea);
