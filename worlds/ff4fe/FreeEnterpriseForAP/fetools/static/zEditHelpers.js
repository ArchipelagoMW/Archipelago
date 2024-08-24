let pngContainer = document.getElementById("container_png");

let previewElem = document.createElement("img");
previewElem.style.imageRendering = 'pixelated';
pngContainer.insertBefore(previewElem, pngContainer.firstChild);

subscribeToField("png", (binary) => {
    let encoded = btoa(binary);
    previewElem.src = "data:image/png;base64," + encoded;
});
