window.addEventListener('load', () => {
    document.getElementById('check-button').addEventListener('click', () => {
        document.getElementById('file-input').click();
    });

    document.getElementById('file-input').addEventListener('change', () => {
        document.getElementById('check-form').submit();
    });
});
