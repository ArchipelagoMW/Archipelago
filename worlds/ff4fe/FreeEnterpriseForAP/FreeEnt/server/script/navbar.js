// This is a bit kludgey, but with a static site this is a way
// to share the navbar across multiple pages.

var NAVBAR_HTML = `
  <div id="nav">
    <a class="home" href="/">FF4FE</a>
    <a href="/make">Play</a>
    <a href="/resources">Resources</a>
    <a href="/changelog">Changelog</a>
    <span class="version">Current version: {VERSION}</span>
    <div class="spacer"></div>    
    <a href="https://discord.gg/AVeUqkb" target="_blank">Discord</a>
  </div>
  `;

document.write(NAVBAR_HTML);
