
let getMaxLevel = (itemname) => {
    return parseInt(document.getElementById(itemname).getAttribute("data-max-level"));
}

let setProgressiveAcquiredLevel = (itemname, level) => {
    let targetLevel = Math.min(getMaxLevel(itemname), level);
    document.getElementById(itemname).setAttribute("class", "progressive lvl-" + targetLevel);
}

let setAcquired = (itemname) => {
    let targetElement = document.getElementById(itemname);
    if (targetElement == null) {
        console.error("Unable to find element for " + itemname);
    } else if (targetElement.tagName === "IMG") {
        targetElement.setAttribute("class", "acquired");
    } else {
        targetElement.setAttribute("class", "progressive lvl-1");
    }
}

let getKeyCounts = () => {
    let keyNodes = document.getElementById("keylist").children;
    let result = {};
    for (let i = 0; i < keyNodes.length; ++i) {
        result[keyNodes[i].id] = parseInt(keyNodes[i].getAttribute("data-count"));
    }
    return result;
}

let addKeyNode = (keyname) => {
    let newNode = document.createElement("li");
    newNode.id = keyname;
    newNode.setAttribute("data-count", 1);
    newNode.appendChild(document.createTextNode(keyname));
    document.getElementById("keylist").appendChild(newNode);
}

let addKey = (keyname) => {
    let keyCounts = getKeyCounts();
    if (keyCounts[keyname] != null) {
        let keyNode = document.getElementById(keyname);
        keyNode.setAttribute("data-count", keyCounts[keyname] + 1);
        keyNode.innerText = keyname + " (" + keyNode.getAttribute("data-count") + ")"
    } else {
        addKeyNode(keyname);
    }
}

onload = () => {
    // test code
    // setAcquired("Ghost");
    // setAcquired("Shaped Blast (Siege Tank)");
    // setAcquired("Valkyrie");
    // setAcquired("Shockwave Missile Battery (Banshee)");
    // let elements = document.querySelectorAll("div.progressive");
    // for (let i = 0; i < elements.length; ++i) {
    //     elements[i].setAttribute("class", "progressive lvl-1");
    // }
}
