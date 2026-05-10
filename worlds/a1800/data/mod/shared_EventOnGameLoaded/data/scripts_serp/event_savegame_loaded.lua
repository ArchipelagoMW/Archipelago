
-- ###################################################
-- ###################################################

-- Unfortunately there is no xml event (which works) to fire on every savegame load. So most mods execute their stuff on SessionEnter, but this fires quite often.

-- My Execute_SavegameLoadedEvent function unlocks a FeatureUnlock ~1 second after a savegame was loaded (and locks it directly again). 
-- (It may be the very same game though, eg. go to main menu and back into game).
-- it is for sure better to execute your possibly expensive code with help of this event, instead on every single SessionEnter, if it is enough to call it once per savegame load
 -- If your code is not expensive, you can of course simply call it on your own once per SessionEnter, if that is no problem.

local LoadingScreenLeft_ID = 60
-- this integer is passed with the games OnLeaveUIState event whenever we leave the loading screen.
-- It also happens when we went from within a SP game to the main menu and then again back into the same game, so its not a 100% "load game"!





local function g_OnLeaveUIState_serp(UILeft_ID)
  if UILeft_ID == LoadingScreenLeft_ID then
    -- modlog("g_OnLeaveUIState_serp")
    system.start(function()
      -- use a delay (at least 0.7 second), because multiplayer needs this for the code to be executed already ingame (because LeaveUIState fires too fast there)
      system.waitForGameTimeDelta(700)
      ts.Unlock.SetRelockNet(1500004636) -- Execute_SavegameLoadedEvent, lock this FeatureUnlock to notify other mods
    end)
    
  end
end

if event.OnLeaveUIState["shared_LuaOnGameLoaded_Serp"] == nil then -- only add it once
  
  -- define a global variable early (before other scripts are executed with help of this mod)
  -- This can be used by other mods to be used like g_LuaScriptBlockers.MyMod = true/nil
  -- When you add your script with ActionExecuteScript to the xml 1500004636 FeatureUnlock, then it will be executed for every Human Participant in Multiplayer,
   -- causing your script to be executed multiple times also for the local player.
    -- To make sure your script is only executed once per load per local player, you can check and define g_LuaScriptBlockers.MyMod = true
     -- and set it to nil again within a thread after eg. 5000 ms, to be unblocked for the next game loading. 
  g_LuaScriptBlockers = {}
  
  event.OnLeaveUIState["shared_LuaOnGameLoaded_Serp"] = g_OnLeaveUIState_serp
  
  -- The first time this script is called with help of SessionEnter, it will already be too late for the very first OnLeaveUIState,
   -- because right now we can only execute lua with help of xml, while xml is not yet available when we first enter the main menu or are in the first loading screen
    -- that means if g_OnLeaveUIState_serp was not yet added, Anno was just recently started, so the first SessionEnter for sure means a savegame was loaded.
    -- after that, the lua event.OnLeaveUIState will continue to work outside of a savegame, so also in main menu, so checking for LoadingScreenLeft_ID is enough then, to catch another savegame load without restarting the whole game
  -- modlog("register OnLeaveUIState")
  ts.Unlock.SetRelockNet(1500004636) -- Execute_SavegameLoadedEvent, lock this FeatureUnlock to notify other mods
end




-- ######################################################################
-- ######################################################################
-- ######################################################################

-- below my tests what UILeft_ID the game uses:


-- Testwerte von LeaveUIState:
-- Problem ist an sich nur, dass für das erstmalige registern ein tirgger notwendig ist, welcher erst im spiel, nach dem Laden verfügbar ist
 -- Aber nachdem event einmal registered wurde, funzt es auch weiterhin und auch im hautpmenü, solange spiel nicht neu gestartet wird
 -- dh wir können evtl. erkennen, wenn ein spieler schon im spiel ist und ein weiteres/anderes savegame läd und in so einem Fall
  -- alle lua Werte resetten, die in einem potentiell anderem savegame nochmal geprüft werden sollen

-- On Leave UIState Test mit Singleplayer Spielstand

-- registered OnLeaveUIState

-- von session in worldmap
-- OnLeaveUIState: 50
-- OnLeaveUIState: 54
-- OnLeaveUIState: 66
-- OnLeaveUIState: 128
-- OnLeaveUIState: 125
-- OnLeaveUIState: 127
-- OnLeaveUIState: 126
-- OnLeaveUIState: 164
-- OnLeaveUIState: 13
-- OnLeaveUIState: 45
-- OnLeaveUIState: 39

-- wieder in session
-- OnLeaveUIState: 197
-- OnLeaveUIState: 39

-- von SP Spiel zum hauptmenü
-- OnLeaveUIState: 63
-- OnLeaveUIState: 171
-- OnLeaveUIState: 170
-- OnLeaveUIState: 45
-- OnLeaveUIState: 50
-- OnLeaveUIState: 54
-- OnLeaveUIState: 66
-- OnLeaveUIState: 128
-- OnLeaveUIState: 125
-- OnLeaveUIState: 127
-- OnLeaveUIState: 126
-- OnLeaveUIState: 164
-- OnLeaveUIState: 151
-- OnLeaveUIState: 13
-- OnLeaveUIState: 132
-- OnLeaveUIState: 41

-- wieder ins spiel
-- OnLeaveUIState: 82
-- OnLeaveUIState: 184
-- OnLeaveUIState: 173
-- OnLeaveUIState: 59
-- OnLeaveUIState: 60
-- OnLeaveUIState: 191

-- zum "Spiel laden" screen direkt ohne hauptmenü
-- OnLeaveUIState: 151

-- spielstand laden (Ladebildschirm):
-- OnLeaveUIState: 142
-- OnLeaveUIState: 59
-- OnLeaveUIState: 63
-- OnLeaveUIState: 171
-- OnLeaveUIState: 170
-- OnLeaveUIState: 45
-- OnLeaveUIState: 50
-- OnLeaveUIState: 54
-- OnLeaveUIState: 66
-- OnLeaveUIState: 128
-- OnLeaveUIState: 125
-- OnLeaveUIState: 127
-- OnLeaveUIState: 126
-- OnLeaveUIState: 164
-- OnLeaveUIState: 68
-- OnLeaveUIState: 180
-- OnLeaveUIState: 41
-- OnLeaveUIState: 13
-- OnLeaveUIState: 132
-- OnLeaveUIState: 151

-- von Ladebildschirm in Session (Segel setzen)
-- OnLeaveUIState: 60
-- OnLeaveUIState: 59

-- von SP spiel ins hauptmenü
-- OnLeaveUIState: 63
-- OnLeaveUIState: 171
-- OnLeaveUIState: 170
-- OnLeaveUIState: 45
-- OnLeaveUIState: 50
-- OnLeaveUIState: 54
-- OnLeaveUIState: 66
-- OnLeaveUIState: 128
-- OnLeaveUIState: 125
-- OnLeaveUIState: 127
-- OnLeaveUIState: 126
-- OnLeaveUIState: 164
-- OnLeaveUIState: 151
-- OnLeaveUIState: 13
-- OnLeaveUIState: 132
-- OnLeaveUIState: 41

-- vom Hauptmenü zum "spiel laden"
-- OnLeaveUIState: 184
-- OnLeaveUIState: 191

-- spielstand laden (Ladebildschirm) aus Hauptmenü:
-- OnLeaveUIState: 142
-- OnLeaveUIState: 82
-- OnLeaveUIState: 173
-- OnLeaveUIState: 59
-- OnLeaveUIState: 68
-- OnLeaveUIState: 180
-- OnLeaveUIState: 41

-- von Ladebildschirm in Session (Segel setzen)
-- OnLeaveUIState: 60
-- OnLeaveUIState: 59

-- #####

-- Multiplayer (ist etwas anders, weil man da das spiel komplett verlässt, wenn man aus dem spiel ins hjauptmenü oder zu den savegames geht)

-- Vom Hauptmenü-Ladebildschrim auswählen eines Multiplayer-Savegames und dadurch öffnen der MP-Lobby
-- OnLeaveUIState: 142
-- OnLeaveUIState: 68
-- OnLeaveUIState: 180
-- OnLeaveUIState: 41

-- MP spielstand laden (Ladebildschirm) aus Hauptmenü:
-- OnLeaveUIState: 82
-- OnLeaveUIState: 72
-- OnLeaveUIState: 173
-- OnLeaveUIState: 59

-- von Ladebildschirm in Session (Segel setzen)
-- OnLeaveUIState: 60
-- OnLeaveUIState: 59

-- von MP Spiel in ESC-Menü auswählen von "Spiel laden", was einen aus dem Spiel wirft und in den Bildschirm zum auswählen der savegames schickt
-- OnLeaveUIState: 181
-- OnLeaveUIState: 180
-- OnLeaveUIState: 41
-- OnLeaveUIState: 63
-- OnLeaveUIState: 171
-- OnLeaveUIState: 170
-- OnLeaveUIState: 45
-- OnLeaveUIState: 50
-- OnLeaveUIState: 54
-- OnLeaveUIState: 66
-- OnLeaveUIState: 128
-- OnLeaveUIState: 125
-- OnLeaveUIState: 127
-- OnLeaveUIState: 126
-- OnLeaveUIState: 9
-- OnLeaveUIState: 82
-- OnLeaveUIState: 184
-- OnLeaveUIState: 173
-- OnLeaveUIState: 59
-- OnLeaveUIState: 164
-- OnLeaveUIState: 191
-- OnLeaveUIState: 151
-- OnLeaveUIState: 13
-- OnLeaveUIState: 132
-- OnLeaveUIState: 190

-- MP savegame auswählen und in MP Lobby
-- OnLeaveUIState: 142
-- OnLeaveUIState: 68
-- OnLeaveUIState: 180
-- OnLeaveUIState: 41

-- MP spielstand laden (Ladebildschirm):
-- OnLeaveUIState: 82
-- OnLeaveUIState: 72
-- OnLeaveUIState: 173
-- OnLeaveUIState: 59

-- von Ladebildschirm in Session (Segel setzen)
-- OnLeaveUIState: 60
-- OnLeaveUIState: 59

-- Von MP Spiel zurück ins Hauptmenü
-- OnLeaveUIState: 181
-- OnLeaveUIState: 180
-- OnLeaveUIState: 41
-- OnLeaveUIState: 63
-- OnLeaveUIState: 171
-- OnLeaveUIState: 170
-- OnLeaveUIState: 45
-- OnLeaveUIState: 50
-- OnLeaveUIState: 54
-- OnLeaveUIState: 66
-- OnLeaveUIState: 128
-- OnLeaveUIState: 125
-- OnLeaveUIState: 127
-- OnLeaveUIState: 126
-- OnLeaveUIState: 9
-- OnLeaveUIState: 82
-- OnLeaveUIState: 184
-- OnLeaveUIState: 173
-- OnLeaveUIState: 59
-- OnLeaveUIState: 164
-- OnLeaveUIState: 191
-- OnLeaveUIState: 151
-- OnLeaveUIState: 13
-- OnLeaveUIState: 132
-- OnLeaveUIState: 190
-- OnLeaveUIState: 59


-- ###############################