window.addEventListener('load', () => {
  let tables = $(".autodatatable").DataTable({
        "paging": false,
        "ordering": true,
        "info": false,
        "dom": "t",
    });
  console.log(tables);
});
