function downloadBase64(b64string, filename, mimetype)
{
    let dataStr = atob(b64string);
    let data = new Uint8Array(dataStr.length);
    for (let i = 0; i < dataStr.length; i++)
    {
        data[i] = dataStr.charCodeAt(i);
    }

    let a = document.createElement("a");

    a.href = URL.createObjectURL(new Blob([data], { type: mimetype }));
    a.setAttribute("download", filename);
    a.style.display = "none";
    document.body.appendChild(a);
    setTimeout(function() {
            a.click();
            document.body.removeChild(a);
            setTimeout(function(){ self.URL.revokeObjectURL(a.href); }, 250 );
        }, 66);
}
