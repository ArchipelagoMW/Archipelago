# Guía de instalación para Pokémon Red and Blue: Archipelago

## Importante

Al usar BizHawk, esta guía solo es aplicable en los sistemas de Windows y Linux.

## Software Requerido

- BizHawk: [BizHawk Releases en TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - La versión 2.3.1 y posteriores son soportadas. Se recomienda la versión 2.9.1.
  - Instrucciones de instalación detalladas para BizHawk se pueden encontrar en el enlace de arriba.
  - Los usuarios de Windows deben ejecutar el instalador de prerrequisitos (prereq installer) primero, que también se 
    encuentra en el enlace de arriba.
- El cliente incorporado de Archipelago, que se puede encontrar [aquí](https://github.com/ArchipelagoMW/Archipelago/releases).
- Los ROMs originales de Pokémon Red y/o Blue. La comunidad de Archipelago no puede proveerlos.

## Software Opcional

- [Tracker de mapa para Pokémon Red and Blue Archipelago](https://github.com/coveleski/rb_tracker/releases/latest), para usar con [PopTracker](https://github.com/black-sliver/PopTracker/releases)


## Configurando BizHawk

Una vez que Bizhawk se haya instalado, abre Emuhawk y cambia las siguientes configuraciones:

- (≤ 2.8) Abrir EmuHawk e ir a Config > Customize. Abrir la pestaña Advanced, y en la opción de Lua Core cambiar desde
  "NLua+KopiLua" a "Lua+LuaInterface". Luego reinicia EmuHawk. Esto es fundamental para que el script de Lua funcione
  correctamente.
  **NOTA: Incluso si "Lua+LuaInterface" ya estaba seleccionado, cambia entre las opciones y vuélvelo a seleccionar.
  Algunas instalaciones de versiones nuevas de EmuHawk tienen una tendencia a mostrar "Lua+LuaInterface" por defecto
  pero siguen cargando "NLua+KopiLua" hasta completar este paso.**
- Aun en la pestaña Advanced, asegurate que la casilla de AutoSaveRAM esté marcada, y selecciona también la casilla 5s.
  Esto reduce la posibilidad de que se pierdan datos guardados en el caso de que el emulador deje de funcionar (crash).
- En Config > Customize, pestaña General, marcar la casilla "Run in background". Esto evitará que te desconectes del
  cliente mientras EmuHawk se está ejecutando en segundo plano.

Es muy recomendado asociar los archivos GB (\*.gb) al emulador EmuHawk que se acaba de instalar.
Para hacerlo, simplemente busca uno de los ROMs de gameboy, presiona con el clic derecho sobre él y selecciona
"Abrir con...", despliega la lista que aparece y selecciona la opción al final de la lista "Buscar otra aplicación en
el equipo", luego navega a la carpeta de Bizhawk y selecciona EmuHawk.exe.

## Configura tu archivo YAML

### ¿Qué es un archivo YAML y por qué necesito uno?

Tu archivo YAML contiene un número de opciones que proveen al generador con información sobre como debe generar tu
juego. Cada jugador de un multiworld entregará su propio archivo YAML. Esto permite que cada jugador disfrute de una
experiencia personalizada a su manera, y que diferentes jugadores dentro del mismo multiworld pueden tener diferentes
opciones.

### ¿Dónde puedo obtener un archivo YAML?

Puedes generar un archivo YAML or descargar su plantilla en la [página de configuración de jugador de Pokémon Red and Blue](/games/Pokemon%20Red%20and%20Blue/player-options)

Es importante tener en cuenta que la opción `game_version` determina el ROM que será parcheado.
Tanto el jugador como la persona que genera (si está generando localmente) necesitarán el archivo del ROM
correspondiente.

Para las opciones `trainer_name` y `rival_name`, los siguientes caracteres normales son permitidos:

* `‘’“”·… ABCDEFGHIJKLMNOPQRSTUVWXYZ():;[]abcdefghijklmnopqrstuvwxyzé'-?!.♂$×/,♀0123456789`

Y los siguientes caracteres especiales (cada uno ocupa un carácter):
* `<'d>`
* `<'l>`
* `<'t>`
* `<'v>`
* `<'r>`
* `<'m>`
* `<PK>`
* `<MN>`
* `<MALE>` alias para `♂`
* `<FEMALE>` alias para `♀`

## Unirse a un juego MultiWorld

### Generar y parchar un juego

1. Crea tu archivo de opciones (YAML).
2. Sigue las instrucciones generales de Archipelago para [generar un juego](../../Archipelago/setup/en#generating-a-game).
Haciendo esto se generará un archivo de salida. Tu parche tendrá la extensión de archivo `.apred` o `.apblue`.
3. Abre `ArchipelagoLauncher.exe`
4. Selecciona "Open Patch" en el lado izquierdo y selecciona tu parche.
5. Si es tu primera vez parchando, se te pedirá que selecciones tu ROM original.
6. Un archivo `.gb` parchado será creado en el mismo lugar donde está el parche.
7. La primera vez que abras un parche con BizHawk Client, también se te pedira ubicar `EmuHawk.exe` en tu
instalación de BizHawk.

Si estás jugando una semilla single-player y no te importa tener seguimiento ni pistas, puedes terminar aqui, cerrar el
cliente, y cargar el ROM parchado en cualquier emulador. Sin embargo, para multiworlds y otras funciones de Archipelago,
continúa con los pasos abajo, usando el emulador BizHawk.

### Conectarse al multiserver

Por defecto, abrir un parche hará los pasos del 1 al 5 automáticamente. Incluso asi, es bueno memorizarlos en caso de
que tengas que cerrar y volver a abrir el juego por alguna razón.

1. Pokémon Red/Blue usa el BizHawk Client de Archipelago. Si el cliente no está abierto desde cuando parchaste tu juego,
puedes volverlo a abrir desde el Launcher.
2. Asegúrate que EmuHawk esta cargando el ROM parchado.
3. En EmuHawk, ir a `Tools > Lua Console`. Esta ventana debe quedarse abierta mientras se juega.
4. En la ventana de Lua Console, ir a `Script > Open Script…`.
5. Navegar a tu carpeta de instalación de Archipelago y abrir `data/lua/connector_bizhawk_generic.lua`.
6. El emulador se puede congelar por unos segundos hasta que logre conectarse al cliente. Esto es normal. La ventana del
BizHawk Client debería indicar que se logro conectar y reconocer Pokémon Red/Blue.
7. Para conectar el cliente al servidor, ingresa la dirección y el puerto (por ejemplo, `archipelago.gg:38281`) en el
campo de texto superior del cliente y y haz clic en Connect.

Para conectar el cliente al multiserver simplemente escribe `<dirección>:<puerto>` en el campo de texto superior y
presiona enter (si el servidor usa contraseña, escribe en el campo de texto inferior
`/connect <dirección>:<puerto>[contraseña]`)

## Auto-Tracking

Pokémon Red and Blue tiene un mapa completamente funcional que soporta seguimiento automático. 

1. Descarga el [Tracker de mapa para Pokémon Red and Blue Archipelago](https://github.com/coveleski/rb_tracker/releases/latest) y [PopTracker](https://github.com/black-sliver/PopTracker/releases). 
2. Abre PopTracker, y carga el pack de Pokémon Red and Blue.
3. Haz clic en el símbolo "AP" en la parte superior.
4. Ingresa la dirección de AP, nombre del slot y contraseña (si es que hay).

¡Y ya, el resto debería hacerse solo! Los items y checks serán marcados automáticamente, e incluso reconocerá tus
configuraciones - Ocultará checks y ajustará la lógica según corresponda.
