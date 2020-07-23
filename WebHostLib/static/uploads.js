window.onload = () => {
    document.getElementById('upload-button').addEventListener('click', () => {
        document.getElementById('file-input').click();
    });

    document.getElementById('file-input').addEventListener('change', () => {
        document.getElementById('upload-form').submit();
    });

    $(".table").DataTable({
        "paging": false,
        "ordering": true,
        "order": [[ 3, "desc" ]],
        "info": false,
        "dom": "t",
    });
};
