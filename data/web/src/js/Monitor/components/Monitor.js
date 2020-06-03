import React from 'react';
import '../../../styles/Monitor/components/Monitor.scss';
import MonitorControls from '../containers/MonitorControls';
import MonitorWindow from '../containers/MonitorWindow';

const Monitor = () => (
  <div id="monitor">
    <MonitorControls />
    <MonitorWindow />
  </div>
);

export default Monitor;
