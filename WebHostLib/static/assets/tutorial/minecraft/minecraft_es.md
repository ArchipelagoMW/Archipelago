# Guia instalación de Minecraft Randomizer

## Software Requerido

### Servidor
- [Minecraft Forge](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)
- [Minecraft Archipelago Randomizer Mod](https://github.com/KonoTyran/Minecraft_AP_Randomizer/releases)

### Jugadores
- [Minecraft Java Edition](https://www.minecraft.net/en-us/store/minecraft-java-edition)

## Procedimiento de instalación

### Instalación de servidor dedicado
Solo una persona ha de realizar este proceso y hospedar un servidor dedicado para que los demas jueguen conectandose a él.
1. Descarga el instalador de **Minecraft Forge** 1.16.15 desde el enlace proporcionado, siempre asegurandose de bajar la version mas reciente.

2. Ejecuta el fichero `forge-1.16.5-xx.x.x-installer.jar` y elije **install server**.
    - En esta pagina elegiras ademas donde instalar el servidor, importante recordar esta localización en el siguiente paso.

3. Navega al directorio donde hayas instalado el servidor y abre `forge-1.16.5-xx.x.x.jar`
    - La primera vez que lances el servidor se cerrara (o no aparecerá nada en absoluto), debería haber un fichero nuevo en el directorio llamado `eula.txt`, el cual que contiene un enlace al EULA de minecraft, cambia la linea a `eula=true` para aceptar el EULA y poder utilizar el software de servidor.
    - Esto creara la estructura de directorios apropiada para el siguiente paso

4. Coloca el fichero `aprandomizer-x.x.x.jar` del segundo enlace en el directorio `mods`
    - Cuando se ejecute el servidor de nuevo, generara el directorio `APData` que se necesitara para jugar

### Instalación basica para jugadores
- Compra e instala Minecraft a traves del tercer enlace.
  **Y listo!**.
  Los jugadores solo necesitan una version no modificada de Minecraft para jugar!

### Instalación avanzada para jugadores
***Esto no es requerido para jugar a minecraft randomizado.***
Sin embargo lo recomendamos porque hace la experiencia mas llevadera.

#### Recomended Mods
- [JourneyMap](https://www.curseforge.com/minecraft/mc-mods/journeymap) (Minimap)


1. Instala y ejecuta Minecraft al menos una vez.
2. Ejecuta el fichero `forge-1.16.5-xx.x.x-installer.jar` y elige **install client**.
    - Ejecuta Minecraft forge al menos una vez para generar los directorios necesarios para el siguiente paso.
3. Navega a la carpeta de instalación de Minecraft y colocal los mods que quieras en el directorio `mods`
    - Los directorios por defecto de instalación son:
        - Windows `%APPDATA%\.minecraft\mods`
        - macOS `~/Library/Application Support/minecraft/mods`
        - Linux `~/.minecraft/mods`

## Configura tu fichero YAML

### Que es un fichero YAML y potque necesito uno?
Tu fichero YAML contiene un numero de opciones que proveen al generador con informacion sobre como debe generar tu juego.
Cada jugador de un multiworld entregara u propio fichero YAML.
Esto permite que cada jugador disfrute de una experiencia personalizada a su gusto y diferentes jugadores dentro del mismo multiworld
pueden tener diferentes opciones

### Where do I get a YAML file?
Un fichero basico yaml para minecraft tendra este aspecto.
```yaml
# Usado para describir tu yaml. Util si tienes multiples ficheros
description: Template Name 
# Tu nombre en el juego. Los espacios son reemplazados por guiones bajos, limitado a 16 caracteres
name: YourName 
game: Minecraft
accessibility: locations
# Recomendado no activar esto ya que el pool de objetos de Minecraft es bastante escueto, ademas hay muchas maneras alternativas de obtener los objetivos de Minecraft.
progression_balancing: off 
# Cuantos avances se necesitan para hacer aparecer el Ender Dragon y acabar el juego. few = 30, normal = 50 , many = 70
advancement_goal: 
  few: 0 
  normal: 1 
  many: 0 
# Modifica el nivel de objetos lógicamente requeridos para explorar areas peligrosas y pelear contra jefes. 
combat_difficulty: 
  easy: 0
  normal: 1
  hard: 0
# Avances que sean tediosos o basados en suerte tendran simplemente experiencia o cosas no necesarias
include_hard_advancements: 
  on: 0
  off: 1
# Los avances extremadamente difíciles no seran requeridos; esto afecta a How Did We Get Here? y Adventuring Time. 
include_insane_advancements: 
  on: 0
  off: 1
# Los avances posteriores a Ender Dragon no tendrán objetos necesarios para que otros jugadores en el caso de un MW acaben su partida.
include_postgame_advancements:
  on: 0
  off: 1
# Actualmente desactivado; permite la mezcla de pueblos, puestos, fortalezas, bastiones y cuidades. 
shuffle_structures: 
  on: 0
  off: 1
```


## Unirse a un juego MultiWorld

### Obten tu ficheros de datos Minecraft
**Solo un fichero yaml es necesario por mundo minecraft, sin importar el numero de jugadores que jueguen en el.**

Cuando te unes a un juego multiworld, se te pedirá que entregues tu fichero YAML a quien sea que hospede el juego multiworld (no confundir con hospedar el mundo minecraft).
Una vez la generación acabe, el anfitrión te dará un enlace a tu fichero de datos o un zip con los ficheros de todos.
Tu fichero de datos tiene una extensión `.apmc`.

Pon tu fichero de datos en el directorio `APData` de tu forge server. Asegurate de eliminar los que hubiera anteriormente


### Conectar al multiserver
Despues de poner tu fichero en el directorio `APData`, arranca el Forge server y asegurate que tienes el estado OP
tecleando `/op TuUsuarioMinecraft` en la consola del servidor y entonces conectate con tu cliente Minecraft.

Una vez en juego introduce `/connect <AP-Address> (<Password>)` donde `<AP-Address>` es la dirección del servidor
Archipelago. `(<Password>)`
solo se necesita si el servidor Archipleago tiene un password activo.

### Jugar al juego
Cuando la consola te diga que te has unido a la sala, estas lista/o para empezar a jugar. Felicidades
por unirte exitosamente a un juego multiworld! Llegados a este punto cualquier jugador adicional puede conectarse a tu servidor forge.

