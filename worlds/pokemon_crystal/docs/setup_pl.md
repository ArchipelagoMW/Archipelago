# Instrukcja konfiguracji Pokémon Crystal

## Wymagane oprogramowanie

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Angielska (UE) wersja ROM Pokémon Crystal v1.0 lub v1.1. Społeczność Archipelago nie może jej zapewnić.
    - Prawidłowy ROM v1.1 można wyodrębnić z wersji gry wydanej w sklepie 3DS eShop.
- Jedno z poniższych:
    - [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 lub nowszy. Zalecana jest wersja 2.10.
    - [mGBA](https://mgba.io) 0.10.3 lub nowszy.
        - Potrzebny będzie również skrypt [mGBA to Bizhawk Client connector](https://gist.github.com/gerbiljames/7b92dc62843794bd5902aad191b65efc).
          Należy go dodać do katalogu `data/lua/` w instalacji Archipelago.

### Konfiguracja BizHawk

Po zainstalowaniu BizHawk otwórz plik `EmuHawk.exe` i zmień następujące ustawienia:

- W BizHawk 2.8 lub wcześniejszych wersjach przejdź do `Config -> Customize` i kliknij zakładkę Advanced. Zmień rdzeń Lua
  z `NLua+KopiLua` na `Lua+LuaInterface`, a następnie uruchom ponownie EmuHawk. Ten krok nie jest wymagany w BizHawk 2.9 lub nowszych wersjach.
- W sekcji `Config -> Customize -> Advanced` upewnij się, że pole AutoSaveRAM jest zaznaczone, a następnie kliknij przycisk 5s.
  Zmniejsza to ryzyko utraty zapisanych danych w przypadku awarii emulatora.
- W sekcji `Config -> Customize` włącz opcję `Run in background`. Zapobiegnie to utracie połączenia z klientem
  po przełączeniu się do innego okna.
- Aby dostosować ustawienia kontrolera, otwórz grę Game Boy lub Game Boy Color (`.gb` lub `.gbc`), a następnie przejdź do sekcji
  `Config -> Controllers...`. To menu może być niedostępne, jeśli gra nie jest jeszcze otwarta.
- Upewnij się, że opcja `Config -> Preferred Cores -> GB in SGB` jest wyłączona.

### Konfiguracja mGBA

Po zainstalowaniu mGBA otwórz `mGBA`, przejdź do Ustawienia/Preferencje i zmień następujące ustawienia:

- W `Game Boy`, w sekcji Modele, wybierz `Game Boy Color (CGB)` dla wszystkich modeli.

### Konfiguracja mGBA

Po zainstalowaniu mGBA otwórz `mGBA`, przejdź do Ustawienia/Preferencje i zmień następujące ustawienia:

- W `Game Boy`, w sekcji Modele, wybierz `Game Boy Color (CGB)` dla wszystkich modeli.

## Oprogramowanie opcjonalne

[Pokémon Crystal AP Tracker](https://github.com/palex00/crystal-ap-tracker/releases/latest) do użytku z [PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generowanie i łatka gry

1. Dodaj plik `pokemon_crystal.apworld` do folderu `custom_worlds` w instalacji Archipelago. Nie powinien on znajdować się w folderze
   `lib\worlds`.
2. Utwórz plik opcji (YAML). Możesz go utworzyć, wybierając opcję Generate Templates
   w programie Archipelago Launcher. Następnie możesz edytować plik `.yaml` w dowolnym edytorze tekstu.
3. Postępuj zgodnie z ogólnymi instrukcjami Archipelago
   dotyczącymi [generowania gry w lokalnej instalacji](https://archipelago.gg/tutorial/Archipelago/setup/en#on-your-local-installation).
   Spowoduje to wygenerowanie pliku wyjściowego. Plik poprawki będzie miał rozszerzenie `.apcrystal` i będzie znajdował się
   w pliku wyjściowym.
4. Otwórz plik `ArchipelagoLauncher.exe`.
5. Wybierz opcję `Open Patch` (Otwórz poprawkę) po lewej stronie i wybierz plik poprawki.
6. Jeśli jest to Twoja pierwsza poprawka, zostaniesz poproszony o zlokalizowanie oryginalnego pliku ROM.
7. Plik `.gbc` z poprawką zostanie utworzony w tym samym miejscu, co plik poprawki.
8. Przy pierwszym otwarciu poprawki za pomocą BizHawk Client zostaniesz również poproszony o zlokalizowanie pliku `EmuHawk.exe` w instalacji BizHawk
 . Użytkownicy mGBA mogą wybrać opcję `Cancel` i ręcznie otworzyć mGBA.

Jeśli grasz w trybie dla jednego gracza i nie zależy Ci na automatycznym śledzeniu lub podpowiedziach, możesz zatrzymać się w tym miejscu, zamknąć
klienta i załadować załatany plik ROM w dowolnym emulatorze. Jednak w przypadku multiworlds i innych funkcji Archipelago kontynuuj
poniżej, używając BizHawk lub mGBA jako emulatora.

## Łączenie się z serwerem

Domyślnie otwarcie pliku poprawki spowoduje automatyczne wykonanie kroków 1-5 poniżej. Mimo to warto je zapamiętać na
wypadek, gdyby z jakiegoś powodu trzeba było zamknąć i ponownie otworzyć okno w trakcie gry.

1. Pokémon Crystal korzysta z klienta BizHawk firmy Archipelago. Jeśli klient nie jest nadal otwarty od momentu załatania gry,
   można go ponownie otworzyć z poziomu programu uruchamiającego.
2. Upewnij się, że EmuHawk lub mGBA uruchamia załatany ROM.
3. W EmuHawk:
    - Przejdź do `Tools > Lua Console`. To okno musi pozostać otwarte podczas gry.
    - W oknie konsoli Lua przejdź do `Script > Open Script...`.
    - Przejdź do folderu instalacyjnego Archipelago i otwórz plik `data/lua/connector_bizhawk_generic.lua`.
4. W mGBA:
    - Przejdź do `Tools > Scripting…`. Okno to musi pozostać otwarte podczas gry.
    - Przejdź do `File > Load Script...`.
    - Przejdź do folderu instalacyjnego Archipelago i otwórz plik `data/lua/connector_bizhawkclient_mgba.lua`.
5. Emulator i klient ostatecznie połączą się ze sobą. Okno klienta BizHawk powinno wskazywać, że
   połączył się i rozpoznał Pokémon Crystal.

Teraz powinieneś móc odbierać i wysyłać przedmioty. Te czynności należy powtarzać za każdym razem, gdy chcesz ponownie nawiązać połączenie.
Postępy w trybie offline są całkowicie bezpieczne; wszystko zostanie ponownie zsynchronizowane po ponownym nawiązaniu połączenia.

## Automatyczne śledzenie

Pokémon Crystal posiada w pełni funkcjonalny moduł śledzenia mapy, który obsługuje automatyczne śledzenie.

1. Pobierz [Pokémon Crystal AP Tracker](https://github.com/palex00/crystal-ap-tracker/releases/latest) oraz
   [PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Umieść pakiet śledzenia w folderze `packs/` w instalacji PopTracker.
3. Otwórz PopTracker i załaduj pakiet Pokémon Crystal.
4. Aby włączyć automatyczne śledzenie, kliknij symbol `AP` u góry.
5. Wprowadź adres serwera Archipelago (ten, z którym połączyłeś swojego klienta), nazwę slotu i hasło. Jeśli nie ustawiłeś hasła dla swojego pokoju, pozostaw to pole puste.



