if system.internal.coroutines["polling"] == nil then
    system.start(function ()
        while true
        do
            console.startScript("data/archipelago/scripts/poll_server.py")
            coroutine.yield()
        end
    end, "polling")
end
