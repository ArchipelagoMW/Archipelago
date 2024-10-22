# Pokémon Emerald Installationsguide

## Programvara som behövs

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Ett engelskt Pokémon Emerald ROM, Archipelago kan inte hjälpa dig med detta.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 eller senare

### Konfigurera BizHawk

När du har installerat BizHawk, öppna `EmuHawk.exe` och ändra följande inställningar:

- Om du använder BizHawk 2.7 eller 2.8, gå till `Config > Customize`. På "Advanced Tab", byt Lua core från
`NLua+KopiLua` till `Lua+LuaInterface`, starta om EmuHawk efteråt. (Använder du BizHawk 2.9, kan du skippa detta steg.)
- Gå till `Config > Customize`. Markera "Run in background" inställningen för att förhindra bortkoppling från
klienten om du alt-tabbar bort från EmuHawk.
- Öppna en `.gba` fil i EmuHawk och gå till `Config > Controllers…` för att konfigurera dina inputs.
Om du inte hittar `Controllers…`, starta ett valfritt `.gba` ROM först.
- Överväg att rensa keybinds i `Config > Hotkeys…` som du inte tänkt använda. Välj en keybind och tryck på ESC
för att rensa bort den.

## Extra programvara

- [Pokémon Emerald AP Tracker](https://github.com/seto10987/Archipelago-Emerald-AP-Tracker/releases/latest),
används tillsammans med
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generera och patcha ett spel

1. Skapa din konfigurationsfil (YAML). Du kan göra en via att använda
[Pokémon Emerald options hemsida](../../../games/Pokemon%20Emerald/player-options).
2. Följ de allmänna Archipelago instruktionerna för att
[Generera ett spel](../../Archipelago/setup/en#generating-a-game).
Detta kommer generera en fil för dig. Din patchfil kommer ha `.apemerald` som sitt filnamnstillägg.
3. Öppna `ArchipelagoLauncher.exe`
4. Välj "Open Patch" på vänstra sidan, och välj din patchfil.
5. Om detta är första gången du patchar, så kommer du behöva välja var ditt ursprungliga ROM är.
6. En patchad `.gba` fil kommer skapas på samma plats som patchfilen.
7. Första gången du öppnar en patch med BizHawk-klienten, kommer du också behöva bekräfta var `EmuHawk.exe` filen är
installerad i din BizHawk-mapp.

Om du bara tänkt spela själv och du inte bryr dig om automatisk spårning eller ledtrådar, så kan du stanna här, stänga
av klienten, och starta ditt patchade ROM med valfri emulator. Dock, för multvärldsfunktionen eller andra
Archipelago-funktioner, fortsätt nedanför med BizHawk.

## Anslut till en server

Om du vanligtsvis öppnar en patchad fil så görs steg 1-5 automatiskt åt dig. Även om det är så, kom ihåg dessa steg
ifall du till exempel behöver stänga ner och starta om något medans du spelar.

1. Pokemon Emerald använder Archipelagos BizHawk-klient. Om klienten inte startat efter att du patchat ditt spel,
så kan du bara öppna den igen från launchern.
2. Dubbelkolla att EmuHawk faktiskt startat med den patchade ROM-filen.
3. I EmuHawk, gå till `Tools > Lua Console`. Luakonsolen måste vara igång medans du spelar.
4. I Luakonsolen, Tryck på `Script > Open Script…`.
5. Leta reda på din Archipelago-mapp och i den öppna `data/lua/connector_bizhawk_generic.lua`.
6. Emulatorn och klienten kommer så småningom ansluta till varandra. I BizHawk-klienten kommer du kunna see om allt är
anslutet och att Pokemon Emerald är igenkänt.
7. För att ansluta klienten till en server, skriv in din lobbyadress och port i textfältet t.ex.
`archipelago.gg:38281`
längst upp i din klient och tryck sen på "Connect".

Du borde nu kunna ta emot och skicka föremål. Du behöver göra dom här stegen varje gång du vill ansluta igen. Det är
helt okej att göra saker offline utan att behöva oroa sig; allt kommer att synkronisera när du ansluter till servern
igen.

## Automatisk Spårning

Pokémon Emerald har en fullt fungerande spårare med stöd för automatisk spårning.

1. Ladda ner [Pokémon Emerald AP Tracker](https://github.com/seto10987/Archipelago-Emerald-AP-Tracker/releases/latest)
och
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Placera tracker pack zip-filen i packs/ där du har PopTracker installerat.
3. Öppna PopTracker, och välj Pokemon Emerald.
4. För att automatiskt spåra, tryck på "AP" symbolen längst upp.
5. Skriv in Archipelago-serverns uppgifter (Samma som du använde för att ansluta med klienten), "Slot"-namn samt
lösenord.
