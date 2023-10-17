# Guía de instalación para Pokémon Red and Blue: Archipelago

## Importante

Al usar BizHawk, esta guía solo es aplicable en los sistemas de Windows y Linux.

## Software Requerido

- BizHawk: [BizHawk Releases en TASVideos](https://tasvideos.org/BizHawk/ReleaseHistory)
  - La versión 2.3.1 y posteriores son soportadas. Se recomienda la versión 2.9.1.
  - Instrucciones de instalación detalladas para BizHawk se pueden encontrar en el enlace de arriba.
  - Los usuarios de Windows deben ejecutar el instalador de prerrequisitos (prereq installer) primero, que también se 
    encuentra en el enlace de arriba.
- El cliente incorporado de Archipelago, que se puede encontrar [aquí](https://github.com/ArchipelagoMW/Archipelago/releases)
  (selecciona `Pokemon Client` durante la instalación).
- Los ROMs originales de Pokémon Red y/o Blue. La comunidad de Archipelago no puede proveerlos.

## Software Opcional

- [Tracker de mapa para Pokémon Red and Blue Archipelago](https://github.com/j-imbo/pkmnrb_jim/releases/latest), para usar con [PopTracker](https://github.com/black-sliver/PopTracker/releases)


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

Puedes generar un archivo YAML or descargar su plantilla en la [página de configuración de jugador de Pokémon Red and Blue](/games/Pokemon%20Red%20and%20Blue/player-settings)

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

### Obtener tu parche de Pokémon

Cuando te unes a un juego multiworld, se te pedirá que entregues tu archivo YAML a quien lo esté organizando.
Una vez que la generación acabe, el anfitrión te dará un enlace a tu archivo, o un .zip con los archivos de
todos. Tu archivo tiene una extensión `.apred` o `.apblue`.

Haz doble clic en tu archivo `.apred` o `.apblue` para que se ejecute el cliente y realice el parcheado del ROM.
Una vez acabe ese proceso (esto puede tardar un poco), el cliente y el emulador se abrirán automáticamente (si es que se
ha asociado la extensión al emulador tal como fue recomendado)

### Conectarse al multiserver

Una vez ejecutado tanto el cliente como el emulador, hay que conectarlos. Abre la carpeta de instalación de Archipelago,
luego abre `data/lua`, y simplemente arrastra el archivo `connector_pkmn_rb.lua` a la ventana principal de Emuhawk.
(Alternativamente, puedes abrir la consola de Lua manualmente. En Emuhawk ir a Tools > Lua Console, luego ir al menú
`Script` 〉 `Open Script`, navegar a la ubicación de `connector_pkmn_rb.lua` y seleccionarlo.)

Para conectar el cliente con el servidor, simplemente pon `<dirección>:<puerto>` en la caja de texto superior y presiona
enter (si el servidor tiene contraseña, en la caja de texto inferior escribir `/connect <dirección>:<puerto> [contraseña]`)

Ahora ya estás listo para tu aventura en Kanto.

## Auto-Tracking

Pokémon Red and Blue tiene un mapa completamente funcional que soporta seguimiento automático. 

1. Descarga el [Tracker de mapa para Pokémon Red and Blue Archipelago](https://github.com/j-imbo/pkmnrb_jim/releases/latest) y [PopTracker](https://github.com/black-sliver/PopTracker/releases). 
2. Abre PopTracker, y carga el pack de Pokémon Red and Blue.
3. Haz clic en el símbolo "AP" en la parte superior.
4. Ingresa la dirección de AP, nombre del slot y contraseña (si es que hay).

¡Y ya, el resto debería hacerse solo! Los items y checks serán marcados automáticamente, e incluso reconocerá tus
configuraciones - Ocultará checks y ajustará la lógica según corresponda.
