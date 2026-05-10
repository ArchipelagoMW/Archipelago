if g_location_guid_data == nil then
    console.startScript("data/archipelago/scripts/data.lua")
end

for _, location_guid_data in ipairs(g_location_guid_data) do
    if not location_guid_data[2] and ts.Unlock.GetIsUnlocked(location_guid_data[1]) then
        location_guid_data[2] = true
        console.startScript(
            string.format("data/archipelago/scripts/set_is_unlocked/set_is_unlocked_%d.py", location_guid_data[1]))
    end
end
