let oldOnload = window.onload;

function converterChanged(value)
{
    let generalOnlyRows = ["octave_range"];
    generalOnlyRows.forEach((field) => {
        let row = document.getElementById(`assetfieldrow__${field}`);
        row.style.opacity = (value == "general" ? "1" : "0.2");
        let fieldElem = document.getElementById(`assetfield__${field}`);
        fieldElem.disabled = (value != "general");
    });
}

window.addEventListener("load", () => {
    converterChanged(document.getElementById("assetfield__converter").value);
    subscribeToField("converter", converterChanged);
});
