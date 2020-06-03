const APPEND_MESSAGE = 'APPEND_MESSAGE';

const appendMessage = (content) => ({
  type: APPEND_MESSAGE,
  content,
});

export default appendMessage;
