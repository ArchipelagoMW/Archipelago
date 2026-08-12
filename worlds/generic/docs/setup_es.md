# Guía de Configuración de Archipelago

Esta guía pretende proporcionar un resumen de cómo:
- Instalar, configurar y ejecutar el software de Archipelago
- Generar y hostear partidas
- Conectar a la partida después de empezar a hostearla

Esta guía solo explica lo más básico. Para pasos más específicos, dirígete a la [guía de configuración](/tutorial) del juego que estés intentando configurar.

Algunos pasos asumen que estás usando Windows, así que puede variar con tu SO.

## Instalar el software de Archipelago

La versión pública más reciente de Archipelago puede encontrarse en GitHub:
[Github Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest).

Ejecuta el archivo .exe, y después de aceptar el acuerdo de licencia te preguntará qué componentes deseas instalar.

Las instalaciones de Archipelago tienen automáticamente empaquetados algunos programas. Esto incluye un launcher, un generador, un servidor y algunos clientes.

- El launcher te deja acceder rápidamente a los distintos componentes y programas de Archipelago. Lo encontrarás con el nombre `ArchipelagoLauncher` y se puede encontrar en el directorio principal de tu instalación de Archipelago.

- El generador te permite generar partidas en tu ordenador. Por favor ve a la sección 'Generar una partida' de esta guía para más información.

- El servidor te permite hostear la partida en tu ordenador. Hostear en tu ordenador requiere enviar el puerto en el que estás hosteando. El puerto por defecto para Archipelago es el `38281`. Sino estás seguro de como hacerlo hay muchas otras guías en Internet que serán más apropiadas para tu hardware.

- Los clientes son lo que se usa para conectar tu juego a la partida. Algunos juegos usan un cliente que se instala automáticamente con la instalación de Archipelago. Puedes acceder a esos clientes en el launcher o en tu instalación de Archipelago.

## Generar una partida

### ¿Qué es un YAML?

YAML es el formato de archivo que Archipelago usa para configurar el mundo de un jugador. Te deja determinar el juego que vas a jugar y las opciones que has elegido para ese juego.

YAML es un formato muy similar a JSON salvo que es más fácil de leer para una persona. Sino estás seguro de la validez de tu archivo YAML puedes confirmar su validez subiéndolo en la web de Archipelago: [Página de Validación de YAML](/check)

### Crear un YAML

Los archivos YAML se pueden generar en la web de Archipelago visitando la  [página de juegos](/games) y clicando el link que pone "Options Page" debajo del juego que quieras configurar. Clicar "Export Options" en una de estás páginas descargará el YAML a tu ordenador.

También puedes ejecutar `ArchipelagoLauncher.exe` y clicar en `Generate Template Options` para crear un conjunto de plantillas YAML para cada juego en tu instalación de Archipelago (incluyendo los APWorlds). Estas se colocarán en la carpeta `Players/Templates`.

En una partida debe haber un YAML por juego. Cualquier número de jugadores puede jugar a cada juego usando el sistema cooperativo nativo del juego o usando el soporte cooperativo de Archipelago. Cada juego tendrá una ranura en la partida con un nombre, además, si el juego lo requiere también habrá archivos asociados a la partida.

Si varias personas planean jugar una partida cooperativa solo necesitarán un YAML de su juego. Si cada uno planea jugar su propia partida cada uno necesitará un YAML por juego. 

### Generando una partida para un solo jugador

#### En la web

La manera más fácil de empezar una partida de Archipelago, después de seguir la guía básica de la guía del juego, que se encuentra en la [Lista de Juegos de Archipelago](/games), clica en `Options Page`, elige las opciones que quieres tener, y clica  `Generate Game` al final de la página. Esto creará una página para la semilla, desde la que podrás crear una sala y luego [conectarte](#connecting-to-an-archipelago-server).

Si te has descargado las opciones, o has creado el archivo de configuración manualmente, este archivo se puede subir a la [Página de Generación](/generate) donde puedes cambiar algunos ajustes de hosteo.

#### En tu ordenador

Para generar una partida en tu ordenador, después de instalar Archipelago. Muévete por tu instalación (normalmente C:\ProgramData\Archipelago), y coloca el archivo de configuración que has creado o descargado de la web en la carpeta `Players`.

Ejecuta `ArchipelagoGenerate.exe`, o clica en `Generate` en el launcher, y te informará si la generación fue exitosa o no. Si fue exitosa, habrá una carpeta comprimida en la carpeta `output` (normalmente llamada parecida a `AP_XXXXX.zip`). Esta contendrá toda la información relevante de la partida, incluyendo el archivo de spoilers, si se generaron.

Recuerda que algunos juegos requieren que poseas sus ROMs para generarlos ya que se necesitan para generar los parches necesarios para jugar. Cuando generas con una ROM por primera vez te pedirá que le digas dónde está. Este paso solo es necesario la primera vez que lo haces.

### Generar una partida multijugador

Archipelago es un programa que puede usar un numero ilimitado de jugadores y juegos. Aunque hay que tener en cuenta que actualmente la web tiene un máximo de 30 jugadores por partida. Si quieres generar una partida mayor a esa, debe hacerse en una instalación local. Normalmente, es mejor generar localmente para liberar recursos del servidor, y hostear la partida resultante en la web.

#### Obtener los YAMLs de Todos los Jugadores

Todos los jugadores que deseen jugar una partida deben tener un archivo YAML que contiene las opciones elegidas para su juego. Una persona debe obtener todos los YAMLs de todos los jugadores. Un solo jugador puede tener varios juegos o incluso tener varios slots con el mismo juego, pero cada YAML debe tener un nombre de jugador único.

#### En la web

Obten todos los YAMLs en un solo ordenador, luego ve a la [Página de Generación](/generate). Selecciona los ajustes que quieras, clica en `Upload File(s)`, y selecciona los YAMLs de todos los jugadores. La web también acepta carpetas `zip` que contengan archivos YAML.

Después de un rato, te redigirá a una página de información de la semilla que mostrará la semilla generada, la fecha en la que fue creada, el número de jugadores, el archivo de spoilers (si fue creado) y todas las salas creadas con esa semilla.

#### En tu instalación local

Es posible generar una partida local usando la instalación de Archipelago. Esto de hace entrando en la carpeta de Archipelago (normalmente C:\ProgramData\Archipelago) y colocando cada archivo YAML en la carpeta `Players`. Si la carpeta no existe se debe crear manualmente. Los archivos aquí no deben estar comprimidos.

Después de llenar la carpeta `Players`, ejecuta `ArchipelagoGenerate.exe` o clica `Generate` en el launcher. Lo que genere acabará en la carpeta `output` (normalmente algo llamado `AP_XXXXX.zip`).

Recuerda que algunos juegos requieren te poseas sus ROMs para generarlos ya que se necesitan para generar los parches necesarios para jugar. Cuando generas con una ROM por primera vez te pedirá que le digas dónde está. Este paso solo es necesario la primera vez que lo haces.

##### Cambiar ajustes locales para la generación

A veces hay varios ajustes que quieres cambiar antes de generar una partida, por ejemplo, activar el modo carrera, auto-liberar, o ponerle contraseña.

Todos estos ajustes y más se pueden cambiar modificando el archivo `host.yaml` en la carpeta de Archipelago. Puedes acceder rápidamente a este archivo clicando en `Open host.yaml` en el launcher. Los ajustes elegidos se colocan en el archivo `.archipelago` que se genera al crear una partida, así que si generas en tu ordenador, asegúrate que este archivo está editado como te gusta **antes** de generar la partida. Este archivo se sobreescribe al ejecutar el Software de Instalación de Archipelago. Si has editado los ajustes de este archivo, y quieres mantenerlos, puedes renombrar el archivo a `opciones.yaml`.

### Jugar juegos personalizados

Si estás generando en tu ordenador, puedes jugar juegos no incluidos en la instalación de Archipelago. Para ello se necesita el archivo `.apworld` correspondiente a ese juego. Para añadir el juego a tu instalación, clica en "Install APWorld" en el launcher y selecciona el archivo `.apworld` que deseas instalar. También puedes mover el archivo `.apworld` al launcher o hacer doble click en el propio archivo (si estás en Windows). Cuando el archivo esté instalado funcionará como los juegos que vienen con Archipelago. Ten en cuenta que solo se pueden generar localmente pero una vez generado se pueden hostear en la web como cualquier otro juego.

Recomendamos que te asegures que la fuente del `.apworld` es segura y fiable cuándo juegues un juego personalizado. Los APWorlds instalados pueden ejecutar código en tu ordenador cuando abres Archipelago.

#### Versiones alternativas de juegos incluidos

Si quieres jugar con una versión alternativa de un juego incluido en Archipelago, deberás eliminar el APWorld después de completar la instalación que seguiste antes. Para hacerlo, ve a tu carpeta de instalación de Archipelago y ve al directorio `lib/worlds`. Luego mueve el `.apworld` o la carpeta del juego correspondiente al que quieres jugar de forma alternativa a otra carpeta como backup. Si quieres volver a jugar a la versión original, devuélvela a `lib/worlds` y elimina la otra versión, que estará en la carpeta `custom_worlds`.

Nota: Actualmente, esto no se puede hacer en la versión "Linux AppImage".

## Hostear un servidor de archipelago

Cuando se genera una semilla, los datos saldrán como un `.archipelago`. Si la partida se generó de manera local, una carpeta comprimida estará en `/output` y contendrá el `.archipelago`, los archivos de spoilers, y todos los archivos relevantes para los juegos generados.

### Hostear en la web

Cuando la página de la semilla se haya creado en la web, clicar en `Create Room` creará una sala en el servidor y una página que podrá ser enviada a los otros jugadores para que puedan ver la información necesaria para conectarse, obtener sus archivos y conectarse a la partida. Solo tienes que copiar la url y enviársela a tus amigos. La sala se cerrará después de 2 horas de inactividad, salvando el progreso de la partida. La sala se abrirá al volver a la pestaña y se podrá seguir jugando la partida. Si el enlace a la sala se pierde el creador de puede encontrarla en su [Página de Contenido del Usuario](/user-content). La persona que crea la sala es el "dueño" de la sala, y como tal, tiene acceso a la consola del servidor. Limpiar las cookies eliminará acceso a esta consola y no hay forma de volver obtener acceso. Si se creó una contraseña al generar la partida, se pueden obtener privilegios de administrador al poner `!admin <contraseña&gt;>` desde el `ArchipelagoTextClient.exe`.

#### La página de la sala

[Captura de la página de la sala](example_room.png)
1. Servidor/Nombre de Host
2. Puerto
3. Nombre de Jugador
4. Link de descarga para los archivos de un juego
5. Link para el tracker de este jugador

#### De una partida generada en la web

Después de generar una partida en la web, serás redirigido a la página de la semilla. Para empezar a jugar clica en `Create Room` para crear una nueva página de sala y servidor para tu partida.

#### De una partida generada de manera local

Después de generar una partida, una carpeta comprimida se creará en la carpeta `/output`. Ve a 
[Página para Hostear Partida de Archipelago](/uploads), clica en `Upload File`, ve a tu instalación de Archipelago, y selecciona la carpeta generada. Se creará una nueva página de semilla usando la información de esta carpeta.

### Hostear en tu ordenador

El archivo `.archipelago` puede ser extraído de la carpeta comprimida. Hacer doble click en el archivo abrirá `ArchipelagoServer.exe` para hostear la partida en tu ordenador. Además, ejecutar 
`ArchipelagoServer.exe` y elegir el archivo `.archipelago` o la carpeta comprimida generada también empezará a hostear.

## Conectarse a un servidor de Archipelago

El método para conectarte varía según el juego, así que, sigue la guía para ese juego pero todos usaran los términos que se describen debajo.

### Información de conexión

Para conectar el juego con el servidor necesitarás esta información. Los juegos que necesitan archivos normalmente tienen la información de conexión en esos archivos cuando se hostea desde la web de Archipelago. Si se necesita que la información se ponga manualmente, normalmente se divide en cuatro secciones distintas.

* `Server`, `Server Name` o `Host Name` se usan para referirse al dominio o la IP del servidor. Si la partida se hostea de la web de Archipelago este será `archipelago.gg`. Si se hostea en tu ordenador `localhost` funcionará. Si se hostea en el ordenador de otra persona entonces tendrás que poner su dirección IP pública.

* `Port` es el puerto en el que se está hosteando la partida. En las salas de la página web saldrá  `archipelago.gg:<puerto>`. La mayoría de los clientes aceptarán la información tal cual sale. Si la información se tiene que poner por separado, entonces el puerto es la secuencia de números después de `:`, y los `:` no son necesarios. Si la partida se hostea desde `ArchipelagoServer.exe`, este sera el  `38281` por defecto pero se puede cambiar en el `host.yaml`.

* `Slot Name` es el nombre de tu ranura de jugador. Este es el nombre que elegiste al crear tu [archivo YAML](#creating-a-yaml). Si la partida se hostea en la web también saldrá en la página de la sala. El nombre detecta mayúsculas y minúsculas.

* `Password` es la contraseña que el anfitrón eligió para unirse a la partida. Por defecto está vacía y casi nunca se requiere, pero se puede elegir una al generar la partida. Normalmente, deja vacío este campo si existe salvo que sepas que se ha puesto una contraseña y sepas cual es.