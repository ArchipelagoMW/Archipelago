import { FlagSet as FlagSet_4_0_0 } from './flags-4.0.0.js'
import { FlagSet as FlagSet_4_0_1 } from './flags-4.0.1.js'
import { FlagSet as FlagSet_4_1_0 } from './flags-4.1.0.js'
import { FlagSet as FlagSet_4_2_0 } from './flags-4.2.0.js'
import { FlagSet as FlagSet_4_2_1 } from './flags-4.2.1.js'
import { FlagSet as FlagSet_4_3_0 } from './flags-4.3.0.js'
import { FlagSet as FlagSet_4_3_1 } from './flags-4.3.1.js'
import { FlagSet as FlagSet_4_4_0 } from './flags-4.4.0.js'
import { FlagSet as FlagSet_4_4_1 } from './flags-4.4.1.js'
import { FlagSet as FlagSet_4_4_2 } from './flags-4.4.2.js'
import { FlagSet as FlagSet_4_5_0 } from './flags-4.5.0.js'
import { FlagSet } from './flags.js'

const LEGACY_FLAGSET_CLASSES = [
    [[4, 0, 0], FlagSet_4_0_0],
    [[4, 0, 1], FlagSet_4_0_1],
    [[4, 1, 0], FlagSet_4_1_0],
    [[4, 2, 0], FlagSet_4_2_0],
    [[4, 2, 1], FlagSet_4_2_1],
    [[4, 3, 0], FlagSet_4_3_0],
    [[4, 3, 1], FlagSet_4_3_1],
    [[4, 4, 0], FlagSet_4_4_0],
    [[4, 4, 1], FlagSet_4_4_1],
    [[4, 4, 2], FlagSet_4_4_2],
    [[4, 5, 0], FlagSet_4_5_0],
    ];

function compareVersions(versionArray1, versionArray2)
{
    for (let i = 0; i < 3; i++)
    {
        if (versionArray1[i] < versionArray2[i])
        {
            return -1;
        }
        else if (versionArray1[i] > versionArray2[i])
        {
            return 1;
        }
    }

    return 0;
}

function b64decode(encoded)
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

function b64encode(byte_array)
{
    let srcString = String.fromCharCode(...byte_array);
    let encoded = btoa(srcString);
    encoded = encoded.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
    return encoded;
}

function renameFlag(oldName, newName, flagList, result)
{
    let index = flagList.indexOf(oldName);
    if (index >= 0)
    {
        flagList.splice(index, 1);
        flagList.push(newName);
        result.details.push(oldName + ' has been renamed to ' + newName);
    }
}

function upconvertBinaryFlags(binaryFlagStr)
{
    let result = {
        flagset: null,
        details: [],
        error: null
    };

    let version = b64decode(binaryFlagStr.substr(1, 4));

    if (compareVersions(version, [4, 0, 0]) < 0)
    {
        throw new Error('Cannot upgrade binary flag strings from before version 4.0.0.');
    }

    // load flagset from appropriate class
    let [originalFlagSetVersion, originalFlagSetClass] = LEGACY_FLAGSET_CLASSES[LEGACY_FLAGSET_CLASSES.length - 1];
    for (let i = 0; i < LEGACY_FLAGSET_CLASSES.length; i++)
    {
        let v = LEGACY_FLAGSET_CLASSES[i][0];
        if (compareVersions(version, v) < 0)
        {
            [originalFlagSetVersion, originalFlagSetClass] = LEGACY_FLAGSET_CLASSES[i - 1];
            break;
        }
    }

    let originalFlagSet = new originalFlagSetClass();

    // need to spoof the original version bytes
    let reversionedBinaryFlagString = 'b' + b64encode(originalFlagSetVersion) + binaryFlagStr.substr(5);
    originalFlagSet.load(reversionedBinaryFlagString);
    let flagList = originalFlagSet.get_list();

    // apply changes to the raw flag list as needed per version upgrade
    if (compareVersions(version, [4, 1, 0]) < 0)
    {
        let index = flagList.indexOf('-vanilla:exp');
        if (index >= 0)
        {
            flagList.splice(index, 1);
            flagList.push('-exp:split', '-exp:noboost', '-exp:nokeybonus');
            result.details.push('-vanilla:exp has been split into -exp:split, -exp:noboost, and -exp:nobonus');
        }
    }

    if (compareVersions(version, [4, 2, 0]) < 0)
    {
        renameFlag('-spoiler', '-spoil:all', flagList, result);
        renameFlag('Squarter', 'Ssell:quarter', flagList, result);
    }

    if (compareVersions(version, [4, 5, 0]) < 0)
    {
        renameFlag('Orandom:gated_quest', 'Orandom:tough_quest', flagList, result);
        renameFlag('-supersmith', '-smith:super', flagList, result);
        renameFlag('Nkey', 'Knofree', flagList, result);
        renameFlag('Nchars', 'Cnofree', flagList, result);
        renameFlag('Nbosses', 'Bnofree', flagList, result);

        let index = flagList.indexOf('Nnone');
        if (index >= 0)
        {
            flagList.splice(index, 1);
        }
    }

    if (compareVersions(version, [4, 6, 0]) < 0)
    {
        renameFlag('Ktrap', 'Kmiab', flagList, result);
        renameFlag('-kit:trap', '-kit:miab', flagList, result);
        renameFlag('-kit2:trap', '-kit2:miab', flagList, result);
        renameFlag('-kit3:trap', '-kit3:miab', flagList, result);
        renameFlag('-vanilla:traps', '-vanilla:miabs', flagList, result);
        renameFlag('-spoil:traps', '-spoil:miabs', flagList, result);
    }

    // build the new flagset from the transformed list of raw flags
    let upconvertedFlagSet = new FlagSet();
    flagList.forEach( (flag) => { upconvertedFlagSet.set(flag); } );

    result.flagset = upconvertedFlagSet;
    return result;
}

window.upconvertBinaryFlags = upconvertBinaryFlags;
export default upconvertBinaryFlags;
