window.addEventListener('load', () => {
    document.getElementById('generate-game-button').addEventListener('click', () => {
        document.getElementById('file-input').click();
    });

    document.getElementById('file-input').addEventListener('change', () => {
        document.getElementById('generate-game-form').submit();
    });
});
