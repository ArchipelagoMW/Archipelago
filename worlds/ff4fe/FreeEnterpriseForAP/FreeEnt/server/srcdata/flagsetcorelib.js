class FlagSetCoreLib
{
    b64encode(byte_array)
    {
        let srcString = String.fromCharCode(...byte_array);
        let encoded = btoa(srcString);
        encoded = encoded.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
        return encoded;
    }

    b64decode(encoded)
    {
        encoded = encoded.replace(/-/g, "+").replace(/_/g, "/");
        let decoded = atob(encoded);
        let result = new Array();
        for (let i = 0; i < decoded.length; i++)
        {
            result.push(decoded.charCodeAt(i));
        }
        return result;
    }

    re_test(expression, string)
    {
        let regex = new RegExp(expression);
        return regex.test(string);
    }

    re_search(expression, string)
    {
        let regex = new RegExp(expression);
        return regex.exec(string);
    }

    re_sub(expression, replacement, string)
    {
        let regex = new RegExp(expression, 'g');
        return string.replace(regex, replacement);
    }

    push(list, value)
    {
        list.push(value);
    }

    remove(list, value)
    {
        let index = list.indexOf(value);
        if (index >= 0)
        {
            list.splice(index, 1);
        }
    }

    join(list, separator)
    {
        return list.join(separator);
    }

    min(a, b)
    {
        return Math.min(a, b);
    }

    is_string(obj)
    {
        return (typeof(obj) === "string");
    }

    keys(dict)
    {
        return Object.keys(dict);
    }
}

const _FE_CORELIB = new FlagSetCoreLib();

export class FlagSet extends FlagSetCore
{
    constructor()
    {
        super(_FE_FLAGSPEC, _FE_CORELIB);
    }
}

export class FlagLogic extends FlagLogicCore
{
    constructor()
    {
        super(_FE_FLAGSPEC, _FE_CORELIB);
    }
}

export default FlagSet;
