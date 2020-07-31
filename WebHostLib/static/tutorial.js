window.addEventListener('load', () => {
    new Promise((resolve, reject) => {
        let ajax = new XMLHttpRequest();
        ajax.onreadystatechange = () => {
            if (ajax.readyState !== 4) { return; }
            if (ajax.status !== 200) { reject('Unable to retrieve tutorial markdown file.') }
            resolve(ajax.responseText);
        };
        ajax.open('GET', 'tutorial.md', true);
        ajax.send();
    }).then((response) => {
        let markdown = new showdown.Converter();
        document.getElementById('tutorial-wrapper').innerHTML = markdown.makeHtml(response);
    }).catch((error) => {
        console.log(error);
    });
});
