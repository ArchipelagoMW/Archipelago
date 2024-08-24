async function doAction(action, assetId)
{
    let route = `action?action=${action}`;
    if (assetId !== undefined)
    {
        route += `&assetId=${assetId}`;
    }
    let response = await fetch(route);

    return await handleActionResponse(response);
}

async function doActionWithFormDataAsset(action, formData)
{
    let route = `action?action=${action}`;
    let response = await fetch(route, {
        method : 'POST',
        body: formData
    });
    
    return await handleActionResponse(response);
}

async function handleActionResponse(response)
{
    if (!response.ok)
    {
        return { error: `HTTP ${response.status} : ${response.statusText}` };
    }

    let json = await response.json();

    if (json.action === 'save')
    {
        let dataStr = atob(json.data);
        let data = new Uint8Array(dataStr.length);
        for (let i = 0; i < dataStr.length; i++)
        {
            data[i] = dataStr.charCodeAt(i);
        }

        let a = document.createElement("a");

        a.href = URL.createObjectURL(new Blob([data], { type: json.mimetype }));
        a.setAttribute("download", json.filename);
        a.style.display = "none";
        document.body.appendChild(a);
        setTimeout(function() {
                a.click();
                document.body.removeChild(a);
                setTimeout(function(){ self.URL.revokeObjectURL(a.href); }, 250 );
            }, 66);
    }

    return json;
}
