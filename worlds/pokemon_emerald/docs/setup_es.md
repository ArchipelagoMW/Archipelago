# Guía de Configuración para Pokémon Emerald

## Software Requerido

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Una ROM de Pokémon Emerald en Inglés. La comunidad de Archipelago no puede proveerla.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 o posterior

### Configuración de BizHawk

Una vez que hayas instalado BizHawk, abre `EmuHawk.exe` y cambia las siguientes configuraciones:

- Si estás usando BizHawk 2.7 o 2.8, ve a `Config > Customize`. En la pestaña Advanced, cambia el Lua Core de
`NLua+KopiLua` a `Lua+LuaInterface`, luego reinicia EmuHawk. (Si estás usando BizHawk 2.9, puedes saltar este paso.)
- En `Config > Customize`, activa la opción "Run in background" para prevenir desconexiones del cliente mientras
la aplicación activa no sea EmuHawk.
- Abre el archivo `.gba` en EmuHawk y luego ve a `Config > Controllers…` para configurar los controles. Si no puedes
hacer clic en `Controllers…`, debes abrir cualquier ROM `.gba` primeramente.
- Considera limpiar tus macros y atajos en `Config > Hotkeys…` si no quieres usarlas de manera intencional. Para
limpiarlas, selecciona el atajo y presiona la tecla Esc.

## Software Opcional

- [Pokémon Emerald AP Tracker](https://github.com/seto10987/Archipelago-Emerald-AP-Tracker/releases/latest), para usar
con [PopTracker](https://github.com/black-sliver/PopTracker/releases)

## Generando y Parcheando el Juego

1. Crea tu archivo de configuración (YAML). Puedes hacerlo en
[Página de Opciones de Pokémon Emerald](../../../games/Pokemon%20Emerald/player-options).
2. Sigue las instrucciones generales de Archipelago para
[Generar un juego](../../Archipelago/setup/en#generating-a-game). Esto generará un archivo de salida (output file) para
ti. Tu archivo de parche tendrá la extensión de archivo `.apemerald`.
3. Abre `ArchipelagoLauncher.exe`
4. Selecciona "Open Patch" en el lado derecho y elige tu archivo de parcheo.
5. Si esta es la primera vez que vas a parchear, se te pedirá que selecciones la ROM sin parchear.
6. Un archivo parcheado con extensión `.gba` será creado en el mismo lugar que el archivo de parcheo.
7. La primera vez que abras un archivo parcheado con el BizHawk Client, se te preguntará donde está localizado
`EmuHawk.exe` en tu instalación de BizHawk.

Si estás jugando una seed Single-Player y no te interesa el auto-tracking o las pistas, puedes parar aquí, cierra el
cliente, y carga la ROM ya parcheada en cualquier emulador. Pero para partidas multi-worlds y para otras
implementaciones de Archipelago, continúa usando BizHawk como tu emulador.

## Conectando con el Servidor

Por defecto, al abrir un archivo parcheado, se harán de manera automática 1-5 pasos. Aun así, ten en cuenta lo
siguiente en caso de que debas cerrar y volver a abrir la ventana en mitad de la partida por algún motivo.

1. Pokémon Emerald usa el Archipelago BizHawk Client. Si el cliente no se encuentra abierto al abrir la rom
parcheada, puedes volver a abrirlo desde el Archipelago Launcher.
2. Asegúrate que EmuHawk está corriendo la ROM parcheada.
3. En EmuHawk, ve a `Tools > Lua Console`. Debes tener esta ventana abierta mientras juegas.
4. En la ventana de Lua Console, ve a `Script > Open Script…`.
5. Ve a la carpeta donde está instalado Archipelago y abre `data/lua/connector_bizhawk_generic.lua`.
6. El emulador y el cliente eventualmente se conectarán uno con el otro. La ventana de BizHawk Client indicará que te
has conectado y reconocerá Pokémon Emerald.
7. Para conectar el cliente con el servidor, ingresa la dirección y el puerto de la sala (ej. `archipelago.gg:38281`)
en el campo de texto que se encuentra en la parte superior del cliente y haz click en Connect.

Ahora deberías poder enviar y recibir ítems. Debes seguir estos pasos cada vez que quieras reconectarte. Es seguro
jugar de manera offline; se sincronizará todo cuando te vuelvas a conectar.

## Tracking Automático

Pokémon Emerald tiene un Map Tracker completamente funcional que soporta auto-tracking.

1. Descarga [Pokémon Emerald AP Tracker](https://github.com/seto10987/Archipelago-Emerald-AP-Tracker/releases/latest) y
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Coloca la carpeta del Tracker en la carpeta packs/ dentro de la carpeta de instalación del PopTracker.
3. Abre PopTracker, y carga el Pack de Pokémon Emerald Map Tracker.
4. Para utilizar el auto-tracking, haz click en el símbolo "AP" que se encuentra en la parte superior.
5. Entra la dirección del Servidor de Archipelago (la misma a la que te conectaste para jugar), nombre del jugador, y
contraseña (deja vacío este campo en caso de no utilizar contraseña).
