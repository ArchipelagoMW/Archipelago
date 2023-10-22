# Guía de instalación para A Link to the Past Randomizer Multiworld

<div id="tutorial-video-container">
    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/mJKEHaiyR_Y" frameborder="0"
      allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
    </iframe>
</div>

## Software requerido

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- [QUsb2Snes](https://github.com/Skarsnik/QUsb2snes/releases) (Incluido en Multiworld Utilities)
- Hardware o software capaz de cargar y ejecutar archivos de ROM de SNES
    - Un emulador capaz de ejecutar scripts Lua
      ([snes9x rr](https://github.com/gocha/snes9x-rr/releases),
       [BizHawk](https://tasvideos.org/BizHawk), o
       [RetroArch](https://retroarch.com?page=platforms) 1.10.1 o más nuevo). O,
    - Un flashcart SD2SNES, [FXPak Pro](https://krikzz.com/store/home/54-fxpak-pro.html), o otro hardware compatible
- Tu archivo ROM japones v1.0, probablemente se llame `Zelda no Densetsu - Kamigami no Triforce (Japan).sfc`

## Procedimiento de instalación

### Instalación en Windows

1. Descarga e instala MultiWorld Utilities desde el enlace anterior, asegurando que instalamos la versión más reciente.
   **El archivo esta localizado en la sección "assets" en la parte inferior de la información de versión**. Si tu
   intención es jugar la versión normal de multiworld, necesitarás el archivo `Setup.Archipelago.exe`
    - Si estas interesado en jugar la variante que aleatoriza las puertas internas de las mazmorras, necesitaras bajar '
      Setup.BerserkerMultiWorld.Doors.exe'
    - Durante el proceso de instalación, se te pedirá donde esta situado tu archivo ROM japonés v1.0. Si ya habías
      instalado este software con anterioridad y simplemente estas actualizando, no se te pedirá la localización del
      archivo una segunda vez.
    - Puede ser que el programa pida la instalación de Microsoft Visual C++. Si ya lo tienes en tu ordenador (
      posiblemente por que un juego de Steam ya lo haya instalado), el instalador no te pedirá su instalación.

2. Si estas usando un emulador, deberías asignar la versión capaz de ejecutar scripts Lua como programa por defecto para
   lanzar ficheros de ROM de SNES.
    1. Extrae tu emulador al escritorio, o cualquier sitio que después recuerdes.
    2. Haz click derecho en un fichero de ROM (ha de tener la extensión sfc) y selecciona **Abrir con...**
    3. Marca la opción **Usar siempre esta aplicación para abrir los archivos .sfc**
    4. Baja hasta el final de la lista y haz click en la opción **Buscar otra aplicación en el equipo** (Si usas Windows
       10 es posible que debas hacer click en **Más aplicaciones**)
    5. Busca el archivo .exe de tu emulador y haz click en **Abrir**. Este archivo debe estar en el directorio donde
       extrajiste en el paso 1.

### Instalación en Macintosh

- ¡Necesitamos voluntarios para rellenar esta seccion! Contactad con **Farrak Kilhn** (en inglés) en Discord si queréis
  ayudar.

## Configurar tu archivo YAML

### Que es un archivo YAML y por qué necesito uno?

Tu archivo YAML contiene un conjunto de opciones de configuración que proveen al generador con información sobre como
debe generar tu juego. Cada jugador en una partida de multiworld proveerá su propio fichero YAML. Esta configuración
permite que cada jugador disfrute de una experiencia personalizada a su gusto, y cada jugador dentro de la misma partida
de multiworld puede tener diferentes opciones.

### Donde puedo obtener un fichero YAML?

La página "[Generate Game](/games/A%20Link%20to%20the%20Past/player-settings)" en el sitio web te permite configurar tu
configuración personal y descargar un fichero "YAML".

### Configuración YAML avanzada

Una version mas avanzada del fichero Yaml puede ser creada usando la pagina ["Weighted settings"](/weighted-settings),
la cual te permite tener almacenadas hasta 3 preajustes. La pagina "Weighted Settings" tiene muchas opciones
representadas con controles deslizantes. Esto permite elegir cuan probable los valores de una categoría pueden ser
elegidos sobre otros de la misma.

Por ejemplo, imagina que el generador crea un cubo llamado "map_shuffle", y pone trozos de papel doblado en él por cada
sub-opción. Ademas imaginemos que tu valor elegido para "on" es 20 y el elegido para "off" es 40.

Por tanto, en este ejemplo, habrán 60 trozos de papel. 20 para "on" y 40 para "off". Cuando el generador esta decidiendo
si activar o no "map shuffle" para tu partida, meterá la mano en el cubo y sacara un trozo de papel al azar. En este
ejemplo, es mucho mas probable (2 de cada 3 veces (40/60)) que "map shuffle" esté desactivado.

Si quieres que una opción no pueda ser escogida, simplemente asigna el valor 0 a dicha opción. Recuerda que cada opción
debe tener al menos un valor mayor que cero, si no la generación fallará.

### Verificando tu archivo YAML

Si quieres validar que tu fichero YAML para asegurarte que funciona correctamente, puedes hacerlo en la pagina
[YAML Validator](/check).

## Generar una partida para un jugador

1. Navega a [la pagina Generate game](/games/A%20Link%20to%20the%20Past/player-settings), configura tus opciones, haz
   click en el boton "Generate game".
2. Se te redigirá a una pagina "Seed Info", donde puedes descargar tu archivo de parche.
3. Haz doble click en tu fichero de parche, y el emulador debería ejecutar tu juego automáticamente. Como el Cliente no
   es necesario para partidas de un jugador, puedes cerrarlo junto a la pagina web (que tiene como titulo "Multiworld
   WebUI") que se ha abierto automáticamente.

## Unirse a una partida MultiWorld

### Obtener el fichero de parche y crea tu ROM

Cuando te unes a una partida multiworld, debes proveer tu fichero YAML a quien sea el creador de la partida. Una vez
este hecho, el creador te devolverá un enlace para descargar el parche o un fichero zip conteniendo todos los ficheros
de parche de la partida Tu fichero de parche debe tener la extensión `.aplttp`.

Pon tu fichero de parche en el escritorio o en algún sitio conveniente, y haz doble click. Esto debería ejecutar
automáticamente el cliente, y ademas creara la rom en el mismo directorio donde este el fichero de parche.

### Conectar al cliente

#### Con emulador

Cuando el cliente se lance automáticamente, QUsb2Snes debería haberse ejecutado también. Si es la primera vez que lo
ejecutas, puedes ser que el firewall de Windows te pregunte si le permites la comunicación.

##### snes9x-rr

1. Carga tu fichero de ROM, si no lo has hecho ya
2. Abre el menu "File" y situa el raton en **Lua Scripting**
3. Haz click en **New Lua Script Window...**
4. En la nueva ventana, haz click en **Browse...**
5. Navega hacia el directorio donde este situado snes9x-rr, entra en el directorio `lua`, y
   escoge `multibridge.lua`
6. Observa que se ha asignado un nombre al dispositivo, y el cliente muestra "SNES Device: Connected", con el mismo
   nombre en la esquina superior izquierda.

##### BizHawk

1. Asegurate que se ha cargado el nucleo BSNES. Debes hacer esto en el menu Tools y siguiento estas opciones:
   `Config --> Cores --> SNES --> BSNES`  
   Una vez cambiado el nucleo cargado, BizHawk ha de ser reiniciado.
2. Carga tu fichero de ROM, si no lo has hecho ya.
3. Haz click en el menu Tools y en la opción **Lua Console**
4. Haz click en el botón para abrir un nuevo script Lua.
5. Navega al directorio de instalación de MultiWorld Utilities, y en los siguiente directorios:  
   `QUsb2Snes/Qusb2Snes/LuaBridge`
6. Selecciona `luabridge.lua` y haz click en Abrir.
7. Observa que se ha asignado un nombre al dispositivo, y el cliente muestra "SNES Device: Connected", con el mismo
   nombre en la esquina superior izquierda.

##### RetroArch 1.10.1 o más nuevo

Sólo hay que segiur estos pasos una vez.

1. Comienza en la pantalla del menú principal de RetroArch.
2. Ve a Ajustes --> Interfaz de usario. Configura "Mostrar ajustes avanzados" en ON.
3. Ve a Ajustes --> Red. Configura "Comandos de red" en ON. (Se encuentra bajo Request Device 16.) Deja en 55355 (el
   default) el Puerto de comandos de red.

![Captura de pantalla del ajuste Comandos de red](/static/generated/docs/A%20Link%20to%20the%20Past/retroarch-network-commands-en.png)
4. Ve a Menú principal --> Actualizador en línea --> Descargador de núcleos. Desplázate y selecciona "Nintendo - SNES /
   SFC (bsnes-mercury Performance)".

Cuando cargas un ROM, asegúrate de seleccionar un núcleo **bsnes-mercury**. Estos son los sólos núcleos que permiten
que herramientas externas lean datos del ROM.

#### Con Hardware

Esta guía asume que ya has descargado el firmware correcto para tu dispositivo. Si no lo has hecho ya, hazlo ahora. Los
usuarios de SD2SNES y FXPak Pro pueden descargar el firmware apropiado
[aqui](https://github.com/RedGuyyyy/sd2snes/releases). Los usuarios de otros dispositivos pueden encontrar información
[en esta página](http://usb2snes.com/#supported-platforms).

1. Cierra tu emulador, el cual debe haberse autoejecutado.
2. Cierra QUsb2Snes, el cual fue ejecutado junto al cliente.
3. Ejecuta la version correcta de QUsb2Snes (v0.7.16).
4. Enciende tu dispositivo y carga la ROM.
5. Observa en el cliente que ahora muestra "SNES Device: Connected", y aparece el nombre del dispositivo.

### Conecta al MultiServer

El fichero de parche que ha lanzado el cliente debe haberte conectado automaticamente al MultiServer. Hay algunas
razonas por las que esto puede que no pase, incluyendo que el juego este hospedado en el sitio web pero se genero en
algún otro sitio. Si el cliente muestra "Server Status: Not Connected", preguntale al creador de la partida la dirección
del servidor, copiala en el campo "Server" y presiona Enter.

El cliente intentara conectarse a esta nueva dirección, y debería mostrar "Server Status: Connected" en algún momento.
Si el cliente no se conecta al cabo de un rato, puede ser que necesites refrescar la pagina web.

### Jugando

Cuando ambos SNES Device and Server aparezcan como "connected", estas listo para empezar a jugar. Felicidades por unirte
satisfactoriamente a una partida de multiworld!

## Hospedando una partida de multiworld

La manera recomendad para hospedar una partida es usar el servicio proveído en
[el sitio web](/generate). El proceso es relativamente sencillo:

1. Recolecta los ficheros YAML de todos los jugadores que participen.
2. Crea un fichero ZIP conteniendo esos ficheros.
3. Carga el fichero zip en el sitio web enlazado anteriormente.
4. Espera a que la seed sea generada.
5. Cuando esto acabe, se te redigirá a una pagina titulada "Seed Info".
6. Haz click en "Create New Room". Esto te llevara a la pagina del servidor. Pasa el enlace a esta pagina a los
   jugadores para que puedan descargar los ficheros de parche de ahi.  
   **Nota:** Los ficheros de parche de esta pagina permiten a los jugadores conectarse al servidor automaticamente,
   mientras que los de la pagina "Seed info" no.
7. Hay un enlace a un MultiWorld Tracker en la parte superior de la pagina de la sala. Deberías pasar también este
   enlace a los jugadores para que puedan ver el progreso de la partida. A los observadores también se les puede pasar
   este enlace.
8. Una vez todos los jugadores se han unido, podeis empezar a jugar.

## Auto-Tracking

Si deseas usar auto-tracking para tu partida, varios programas ofrecen esta funcionalidad.  
El programa recomentdado actualmente es:
[OpenTracker](https://github.com/trippsc2/OpenTracker/releases).

### Instalación

1. Descarga el fichero de instalacion apropiado para tu ordenador (Usuarios de windows quieren el fichero ".msi").
2. Durante el proceso de insatalación, puede que se te pida instalar Microsoft Visual Studio Build Tools. Un enlace este
   programa se muestra durante la proceso, y debe ser ejecutado manualmente.

### Activar auto-tracking

1. Con OpenTracker ejecutado, haz click en el menu Tracking en la parte superior de la ventana, y elige **
   AutoTracker...**
2. Click the **Get Devices** button
3. Selecciona tu "SNES device" de la lista
4. Si quieres que las llaves y los objetos de mazmorra tambien sean marcados, activa la caja con nombre **Race Illegal
   Tracking**
5. Haz click en el boton **Start Autotracking**
6. Cierra la ventana AutoTracker, ya que deja de ser necesaria
