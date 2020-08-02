window.addEventListener('load', () => {
    document.getElementById('upload-button').addEventListener('click', () => {
        document.getElementById('file-input').click();
    });

    document.getElementById('file-input').addEventListener('change', () => {
        document.getElementById('upload-form').submit();
    });
});
