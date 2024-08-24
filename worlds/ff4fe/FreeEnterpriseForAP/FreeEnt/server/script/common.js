function addClassName(elem, className)
{
    if(typeof(elem) === 'string')
    {
        elem = document.getElementById(elem);
    }

    if(elem)
    {
        var classNames = elem.className.split(" ");
        if(classNames.indexOf(className) === -1)
        {
            elem.className += " " + className;
        }
    }
}

function removeClassName(elem, className)
{
    if(typeof(elem) === 'string')
    {
        elem = document.getElementById(elem);
    }

    if(elem)
    {
        var classNames = elem.className.split(" ");
        var index = classNames.indexOf(className);
        if(index !== -1)
        {
            classNames.splice(index, 1);
            elem.className = classNames.join(" ");
        }
    }
}

// auto-expanding text areas
// ( https://stackoverflow.com/questions/454202/creating-a-textarea-with-auto-resize )
function enableAutoResizeTextAreas()
{
    var tx = document.getElementsByTagName('textarea');
    for (var i = 0; i < tx.length; i++) {
      //tx[i].setAttribute('style', 'height:' + (tx[i].scrollHeight) + 'px;overflow-y:hidden;');
      tx[i].addEventListener("input", OnInput, false);
    }

    function OnInput() {
      this.style.height = 'auto';
      this.style.height = (this.scrollHeight) + 'px';
    }
}

// https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
function getUrlQueryParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

// -----------------------
// https://stackoverflow.com/questions/3163615/how-to-scroll-html-page-to-given-anchor
function scrollToElement(name) {
  _scrollToElementResolver(document.getElementById(name));
}

function _scrollToElementResolver(elem) {
  var jump = parseInt(elem.getBoundingClientRect().top * .4);
  document.body.scrollTop += jump;
  document.documentElement.scrollTop += jump;
  if (!elem.lastjump || elem.lastjump > Math.max(1, Math.abs(jump))) {
    elem.lastjump = Math.abs(jump);
    setTimeout(function() { _scrollToElementResolver(elem);}, "50");
  } else {
    elem.lastjump = null;
  }
}
