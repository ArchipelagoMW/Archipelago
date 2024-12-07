function FlagSet(flagStr)
{
    this._flags = {};
    this._version = null;
    this._binarySignifier = "b";
    if(flagStr !== undefined)
    {
        this.load(flagStr);
    }
}

FlagSet.prototype.load = function(flagStr) 
{
    if(flagStr.startsWith(this._binarySignifier))
    {
        this._loadBinary(flagStr);
    }
    else
    {
        this._loadString(flagStr);
    }
};

FlagSet.prototype._loadBinary = function(flagStr)
{
    this._flags = {};

    var cleanFlagStr = flagStr.substring(1).replace(/-/g, '+').replace(/_/g, '/');
    var versionBinaryData = atob(cleanFlagStr.substring(0,4));
    this._version = [
        versionBinaryData.charCodeAt(0),
        versionBinaryData.charCodeAt(1),
        versionBinaryData.charCodeAt(2)
        ];
    var binaryData = atob(cleanFlagStr.substring(4));

    for(var flag of FLAG_SPEC.order)
    {
        var binSpec = FLAG_SPEC.binary[flag];
        if(binSpec.value == 0)
        {
            continue;
        }

        var value = 0;
        var lowByteIndex = (binSpec.offset >> 3);
        if(lowByteIndex < binaryData.length)
        {
            var lowByteShift = (binSpec.offset & 7);
            var value = (binaryData.charCodeAt(lowByteIndex) >> lowByteShift);
            var numOverflowBytes = ((binSpec.size - 1) >> 3) + 1;
            for(var i = 1; i <= numOverflowBytes; i++)
            {
                if(lowByteIndex + i >= binaryData.length)
                {
                    break;
                }
                value |= (binaryData.charCodeAt(lowByteIndex + i) << (8 * i - lowByteShift));
            }

            var mask = (1 << binSpec.size) - 1;
            value &= mask;
        }

        if(binSpec.value > 0 && value == binSpec.value)
        {
            this._flags[flag] = true;
        }
    }
};

FlagSet.prototype._loadString = function(flagStr)
{
    this._flags = {};
    this._version = null;

    flagStr = flagStr.replace(/\s+/g, '');

    var superflagRegex = /^([A-Z]|-[a-z0-9]+)/;
    var subflagListRegex = /^\(([^)]*)\)/;
    var subflagPrefixListRegex = /^([a-z0-9]+)\s*:(.*)$/;
    var subflagRegex = /^([a-z!]|[0-9]+)/;

    var curSuperflag = null;
    while(flagStr.length > 0)
    {
        var match = superflagRegex.exec(flagStr);
        if(match)
        {
            curSuperflag = match[0];
            flagStr = flagStr.substring(match[0].length);
            if (FLAG_SPEC.order.includes(curSuperflag))
            {
                this.add(curSuperflag);
            }

            continue;
        }

        if(curSuperflag === null)
        {
            throw "Found subflag without superflag in flag string around '" + flagStr + '"';
        }

        var match = subflagListRegex.exec(flagStr);
        if(match)
        {
            var content = match[1].trim();
            flagStr = flagStr.substring(match[0].length);

            var prefix = '';
            match = subflagPrefixListRegex.exec(content);
            if(match)
            {
                if(curSuperflag.startsWith('-'))
                {
                    throw "Switch-style superflag '" + curSuperflag + "' does not allow prefixed subflags '" + content + "'";
                }
                prefix = match[1] + ':';
                content = match[2];
            }

            var parts = content.split(',');
            while(parts.length > 0)
            {
                var part = parts.shift();
                if(curSuperflag.startsWith('-'))
                {
                    this.add(curSuperflag + '(' + prefix + part + ')');
                }
                else
                {
                    this.add(curSuperflag + prefix + part);
                }
            }

            continue;
        }

        var match = subflagRegex.exec(flagStr);
        if(match)
        {
            var subflag = match[0];
            flagStr = flagStr.substring(match[0].length);
            if(subflag == "0")
            {
                // remove corresponding standalone superflag
                delete this._flags[curSuperflag];
            }
            else
            {
                this.add(curSuperflag + subflag);
            }
            continue;
        }

        throw "Unrecognized flag string format near '" + flagStr + "'";
    }
};

FlagSet.prototype.add = function(flag)
{
    if(FLAG_SPEC.order.indexOf(flag) === -1)
    {
        throw "Unrecognized flag: " + flag;
    }
    
    for(var mutexSet of FLAG_SPEC.mutex)
    {
        if(mutexSet.indexOf(flag) !== -1)
        {
            for(var i = 0; i < mutexSet.length; i++)
            {
                if(mutexSet[i] != flag && this.has(mutexSet[i]) && FLAG_SPEC.nulls[mutexSet[i]] === undefined)
                {
                    throw "Flag " + flag + " conflicts with already-set flag " + mutexSet[i];
                }
            }
        }
    }

    this._flags[flag] = true;
};

FlagSet.prototype.has = function(flag)
{
    if(FLAG_SPEC.nulls[flag] !== undefined)
    {
        for(var idx = 0; idx < FLAG_SPEC.nulls[flag].length; idx++)
        {
            if(this._flags[FLAG_SPEC.nulls[flag][idx]])
            {
                return false;
            }
        }
        return true;
    }
    else
    {
        return(this._flags[flag]);
    }
};

FlagSet.prototype.getFlagList = function()
{
    var flagList = new Array();
    for(var flag in this._flags)
    {
        flagList.push(flag);
    }
    return flagList;
};

FlagSet.prototype.getVersion = function(flag)
{
    return(this._version);
};

FlagSet.prototype.setVersion = function(major, minor, revision)
{
    this._version = [major, minor, revision];
}

FlagSet.prototype.getVersionString = function(flag)
{
    if(this._version === null)
    {
        return null;
    }
    else
    {
        return 'v' + this._version[0] + '.' + this._version[1] + '.' + this._version[2];
    }
};

FlagSet.prototype.getString = function()
{
    var groups = {};
    var groupOrder = new Array();
    var prefixLists = {};
    var superflagRegex = /^([A-Z]|-[a-z0-9]+)/;
    var prefixRegex = /^([a-z0-9]+:)(.*)$/;

    for(var idx = 0; idx < FLAG_SPEC.order.length; idx++)
    {
        var flag = FLAG_SPEC.order[idx];
        if(this.has(flag))
        {
            var match = superflagRegex.exec(flag);
            var superflag = match[0];
            var subflag = flag.substring(match[0].length);
            if(subflag.startsWith('('))
            {
                // trim off parentheses
                subflag = subflag.substring(1, subflag.length - 1);
            }

            if(groups[superflag] === undefined)
            {
                groups[superflag] = new Array();
                groupOrder.push(superflag)
            }

            match = prefixRegex.exec(subflag);
            if(match)
            {
                var prefix = match[1];
                if(prefixLists[superflag + prefix] === undefined)
                {
                    groups[superflag].push(prefix);
                    prefixLists[superflag + prefix] = new Array();
                }
                prefixLists[superflag + prefix].push(match[2]);
            }
            else if(subflag.length > 0)
            {
                groups[superflag].push(subflag);
            }
        }
    }

    var parts = new Array();
    while(groupOrder.length > 0)
    {
        var superflag = groupOrder.shift();
        var part = superflag;
        if (superflag.startsWith('-') && groups[superflag].length > 0)
        {
            part += '(' + groups[superflag].join(",") + ')';
        }
        else
        {
            for(var idx = 0; idx < groups[superflag].length; idx++)
            {
                var subflag = groups[superflag][idx];
                if(prefixLists[superflag + subflag] !== undefined)
                {
                    part += '(' + subflag + prefixLists[superflag + subflag].join(',') + ')';
                }
                else if(superflag.startsWith('-') || (subflag.length > 1 && subflag.match(/[^0-9]/)))
                {
                    part += '(' + subflag + ')';
                }
                else
                {
                    part += subflag;
                }
            }
        }
        parts.push(part);
    }

    return(parts.join(' '));
};

FlagSet.prototype.getBinary = function()
{
    var versionNumbers = (this._version ? this._version : [0, 0, 0]);
    var versionBinaryData = String.fromCharCode(versionNumbers[0]) + String.fromCharCode(versionNumbers[1]) + String.fromCharCode(versionNumbers[2]);

    var binaryArray = new Array();
    for(var flag of FLAG_SPEC.order)
    {
        if(this.has(flag))
        {
            var binSpec = FLAG_SPEC.binary[flag];
            var byteIndex = (binSpec.offset >> 3);
            var byteShift = (binSpec.offset & 7);

            var value = (binSpec.value << byteShift);
            while(value > 0)
            {
                while(byteIndex >= binaryArray.length)
                {
                    binaryArray.push(0);
                }
                binaryArray[byteIndex] |= (value & 0xFF);
                value >>= 8;
                byteIndex += 1;
            }
        }
    }

    // console.log(binaryArray.join(' '));
    for(var i = 0; i < binaryArray.length; i++)
    {
        binaryArray[i] = String.fromCharCode(binaryArray[i]);
    }
    var binaryData = binaryArray.join('');

    var encoded = btoa(versionBinaryData + binaryData);
    encoded = encoded.replace(/\+/g, '-');
    encoded = encoded.replace(/\//g, '_');
    encoded = encoded.replace(/\=+$/, '');

    return(this._binarySignifier + encoded);
};

