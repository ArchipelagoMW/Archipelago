async function mouseoverPreview(assetId, rowElem)
{
    if (previewElem.parentElement)
    {
        previewElem.parentElement.removeChild(previewElem);
    }

    let response = await fetch(`preview?asset=${assetId}`);
    if (response.ok)
    {
        let data = await response.text();
        previewElem.src = 'data:image/png;base64,' + data;

        rowElem.children[1].appendChild(previewElem);
    }
}

setMouseoverHandler(mouseoverPreview);

document.body.onmouseover = () => {
    if (previewElem.parentElement)
    {
        previewElem.parentElement.removeChild(previewElem);
    }
};


let previewElem = document.createElement("img");
previewElem.style.position = 'absolute';
previewElem.style.left = '0';
previewElem.style.bottom = '100%';
previewElem.style.transformOrigin = 'left bottom';
previewElem.style.transform = 'scale(2.0)';
previewElem.style.imageRendering = 'pixelated';
previewElem.style.zIndex = '999';
previewElem.style.pointerEvents = 'none';