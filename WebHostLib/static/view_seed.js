window.addEventListener('load', () => {
    const timeElement = document.getElementById('creation-time');
    const creationTime = timeElement.getAttribute('data-creation-time');
    const creationDate = new Date(creationTime);
    timeElement.innerText = creationDate.toLocaleString();
});
