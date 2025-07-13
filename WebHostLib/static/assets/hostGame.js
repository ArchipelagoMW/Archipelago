window.addEventListener('load', () => {
    document.getElementById('host-game-button').addEventListener('click', () => {
        document.getElementById('file-input').click();
    });

    document.getElementById('file-input').addEventListener('change', () => {
        document.getElementById('host-game-form').submit();
    });
});
