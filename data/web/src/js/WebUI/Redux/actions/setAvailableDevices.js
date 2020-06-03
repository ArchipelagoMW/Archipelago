const SET_AVAILABLE_DEVICES = 'SET_AVAILABLE_DEVICES';

const setAvailableDevices = (devices) => ({
  type: SET_AVAILABLE_DEVICES,
  devices,
});

export default setAvailableDevices;
