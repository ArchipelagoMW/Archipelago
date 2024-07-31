# Guia instalación de Minecraft Randomizer

# Instalacion automatica para el huesped de partida

- descarga e instala [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) and activa el
  modulo `Minecraft Client`

## Software Requerido

- [Minecraft Java Edition](https://www.minecraft.net/en-us/store/minecraft-java-edition)

## Configura tu fichero YAML

### Que es un fichero YAML y potque necesito uno?

Tu fichero YAML contiene un numero de opciones que proveen al generador con informacion sobre como debe generar tu
juego. Cada jugador de un multiworld entregara u propio fichero YAML. Esto permite que cada jugador disfrute de una
experiencia personalizada a su gusto y diferentes jugadores dentro del mismo multiworld pueden tener diferentes opciones

### Where do I get a YAML file?

Un fichero basico yaml para minecraft tendra este aspecto.

```yaml
description: Basic Minecraft Yaml
# Tu nombre en el juego. Espacios seran sustituidos por guinoes bajos y
# hay un limite de 16 caracteres
name: TuNombre
game: Minecraft

# Opciones compartidas por todos los juegos:
accessibility: full
progression_balancing: 50
# Opciones Especficicas para Minecraft

Minecraft:
  # Numero de logros requeridos (87 max) para que aparezca el Ender Dragon y completar el juego.
  advancement_goal: 50

  # Numero de trozos de huevo de dragon a obtener (30 max) antes de que el Ender Dragon aparezca. 
  egg_shards_required: 10

  # Numero de huevos disponibles en la partida (30 max).
  egg_shards_available: 15

  # Modifica el nivel de objetos logicamente requeridos para 
  # explorar areas peligrosas y luchar contra jefes.
  combat_difficulty:
    easy: 0
    normal: 1
    hard: 0

  # Si off, los logros que dependan de suerte o sean tediosos tendran objetos de apoyo, no necesarios para completar el juego.
  include_hard_advancements:
    on: 0
    off: 1

  # Si off, los logros muy dificiles tendran objetos de apoyo, no necesarios para completar el juego.
  # Solo afecta a How Did We Get Here? and Adventuring Time.
  include_insane_advancements:
    on: 0
    off: 1

  # Algunos logros requieren derrotar al Ender Dragon;
  # Si esto se queda en off, dichos logros no tendran objetos necesarios.
  include_postgame_advancements:
    on: 0
    off: 1

  # Permite el mezclado de villas, puesto, fortalezas, bastiones y ciudades de END. 
  shuffle_structures:
    on: 0
    off: 1

  # Añade brujulas de estructura al juego,
  # apuntaran a la estructura correspondiente mas cercana.  
  structure_compasses:
    on: 0
    off: 1

  # Reemplaza un porcentaje de objetos innecesarios por trampas abeja
  # las cuales crearan multiples abejas agresivas alrededor de los jugadores cuando se reciba.   
  bee_traps:
    0: 1
    25: 0
    50: 0
    75: 0
    100: 0
```

## Unirse a un juego MultiWorld

### Obten tu ficheros de datos Minecraft

**Solo un fichero yaml es necesario por mundo minecraft, sin importar el numero de jugadores que jueguen en el.**

Cuando te unes a un juego multiworld, se te pedirá que entregues tu fichero YAML a quien sea que hospede el juego
multiworld (no confundir con hospedar el mundo minecraft). Una vez la generación acabe, el anfitrión te dará un enlace a
tu fichero de datos o un zip con los ficheros de todos. Tu fichero de datos tiene una extensión `.apmc`.

Haz doble click en tu fichero `.apmc` para que se arranque el cliente de minecraft y el servidor forge se ejecute.

### Conectar al multiserver

Despues de poner tu fichero en el directorio `APData`, arranca el Forge server y asegurate que tienes el estado OP
tecleando `/op TuUsuarioMinecraft` en la consola del servidor y entonces conectate con tu cliente Minecraft.

Una vez en juego introduce `/connect <AP-Address> (Port) (<Password>)` donde `<AP-Address>` es la dirección del
servidor. `(Port)` solo es requerido si el servidor Archipelago no esta usando el puerto por defecto 38281.
`(<Password>)`
solo se necesita si el servidor Archipleago tiene un password activo.

### Jugar al juego

Cuando la consola te diga que te has unido a la sala, estas lista/o para empezar a jugar. Felicidades por unirte
exitosamente a un juego multiworld! Llegados a este punto cualquier jugador adicional puede conectarse a tu servidor
forge.

## Procedimiento de instalación manual

Solo es requerido si quieres usar una instalacion de forge por ti mismo, recomendamos usar el instalador de Archipelago

### Software Requerido

- [Minecraft Forge](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)
- [Minecraft Archipelago Randomizer Mod](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)
  **NO INSTALES ESTO EN TU CLIENTE MINECRAFT**

### Instalación de servidor dedicado

Solo una persona ha de realizar este proceso y hospedar un servidor dedicado para que los demas jueguen conectandose a
él.

1. Descarga el instalador de **Minecraft Forge** 1.16.5 desde el enlace proporcionado, siempre asegurandose de bajar la
   version mas reciente.

2. Ejecuta el fichero `forge-1.16.5-xx.x.x-installer.jar` y elije **install server**.
    - En esta pagina elegiras ademas donde instalar el servidor, importante recordar esta localización en el siguiente
      paso.

3. Navega al directorio donde hayas instalado el servidor y abre `forge-1.16.5-xx.x.x.jar`
    - La primera vez que lances el servidor se cerrara (o no aparecerá nada en absoluto), debería haber un fichero nuevo
      en el directorio llamado `eula.txt`, el cual que contiene un enlace al EULA de minecraft, cambia la linea
      a `eula=true` para aceptar el EULA y poder utilizar el software de servidor.
    - Esto creara la estructura de directorios apropiada para el siguiente paso

4. Coloca el fichero `aprandomizer-x.x.x.jar` del segundo enlace en el directorio `mods`
    - Cuando se ejecute el servidor de nuevo, generara el directorio `APData` que se necesitara para jugar
