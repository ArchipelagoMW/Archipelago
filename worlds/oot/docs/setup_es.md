# Guia instalación de Ocarina of time Archipelago

## Nota importante

Al usar el cliente y BizHawk, esta guia solo es aplicable en Windows.

## Software Requerido

- [bizhawk+script+Z5Client](https://github.com/ArchipelagoMW/Z5Client/releases) Recomendamos bajar el setup de Z5client
  ya que automatizara varios pasos mas adelante

## Instala emulador y cliente

Descarga el fichero getBizHawk.ps1 del enlace anterior. Colocalo en la carpeta donde desees instalar el emulador, haz
click derecho en él y selecciona "Ejecutar con PowerShell". Esto descargará todas las dependencias necesarias para el
emulador. Puede tardar un rato.

Es recomendable asociar la extensión de las roms de N64 (\*.n64) al BizHawk que hemos instalado anteriormente. Para
hacerlo simplemente debemos buscar alguna rom de n64 que tengamos, hacer click derecho, seleccionar "Abrir con...",
desplegar la lista y buscar la opción "Buscar otra aplicación", navegar hasta el directorio de BizHawk y seleccionar
EmuHawk.exe

Situa el fichero ootMulti.lua del enlace anterior en la carpeta "lua" del emulador recien instalado.

Instala el cliente Z5Client.

## Configura tu fichero YAML

### Que es un fichero YAML y por qué necesito uno?

Tu fichero YAML contiene un numero de opciones que proveen al generador con información sobre como debe generar tu
juego. Cada jugador de un multiworld entregara u propio fichero YAML. Esto permite que cada jugador disfrute de una
experiencia personalizada a su gusto y diferentes jugadores dentro del mismo multiworld pueden tener diferentes opciones

### Where do I get a YAML file?

Un fichero basico yaml para OOT tendra este aspecto. (Hay muchas opciones cosméticas que se han ignorado para este
tutorial, si quieres ver una lista completa, descarga (
Archipelago)[https://github.com/ArchipelagoMW/Archipelago/releases] y buscar el fichero de ejemplo en el directorio "
Players"))

```yaml
description: Default Ocarina of Time Template # Describe tu fichero yalm
  \# Tu nombre en el juego. Los espacio seran reemplazados por _ y hay un limite de 16 caracteres
name: YourName{number}
game:
  Ocarina of Time: 1
requires:
  version: 0.1.7 # Version de archipelago minima.
\# Opciones compartidas por todos los juegos:
accessibility:
  items: 0 # Garantiza que puedes obtener todos los objetos pero no todas las localizaciones
  locations: 50 # Garantiza que puedes obtener todas las localizaciones
  none: 0 # Solo garantiza que el juego pueda completarse.
progression_balancing: # Un sistema para reducir tiempos de espera en una partida multiworld
  0: 0 # Con un número más bajo, es más probable esperar objetos de otros jugadores.
  25: 0
  50: 50
  99: 0 # Objetos importantes al principio del juego, para no esperar
Ocarina of Time:
  logic_rules: # Logica usada por el randomizer.
    glitchless: 50
    glitched: 0
    no_logic: 0
  logic_no_night_tokens_without_suns_song: # Las skulltulas nocturnas requeriran la cancion del sol por logica
    false: 50
    true: 0
  open_forest: # Indica el estado del bosque Kokiri y el camino al Arbol Deku.
    open: 50
    closed_deku: 0
    closed: 0
  open_kakariko: # Indica el estado de la puerta de Kakariko hacia la montaña de la muerte.
    open: 50
    zelda: 0
    closed: 0
  open_door_of_time: # Abre la puerta del tiempo sin la cancion del tiempo.
    false: 0
    true: 50
  zora_fountain: # Indica el estado del rey zora bloqueando el camino a la fuente Zora.
    open: 0
    adult: 0
    closed: 50
  gerudo_fortress: # Indica los requerimientos para acceder a la fortaleza Gerudo.
    normal: 0
    fast: 50
    open: 0
  bridge: # Indica los requerimientos para el puente arco iris.
    open: 0
    vanilla: 0
    stones: 0
    medallions: 50
    dungeons: 0
    tokens: 0
  trials: # Numero de pruebas dentro del castillo de Ganon.
    0: 50 # minimum value
    6: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  starting_age: # Indica la edad con la que empieza link.
    child: 50
    adult: 0
  triforce_hunt: # Reune piezas de trifuerza para completar el juego.
    false: 50
    true: 0
  triforce_goal: # Numero de piezas de trifuerza requeridas. El numero de piezas disponibles es determinado por la opcion "Item pool".
    1: 0 # minimum value
    50: 0 # maximum value
    random: 0
    random-low: 0
    random-high: 0
    20: 50
  bombchus_in_logic: # Los bombchus son considerados para la logica. El primer pack encontrado da 20 chus y las tiendas kokiri y el bazaar los venden. Bombchus abren la bolera.
    false: 50
    true: 0
  bridge_stones: # Numero de piedras para abrir el puente arco iris.
    0: 0 # minimum value
    3: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  bridge_medallions: # Numero de medallones para abrir el puente arco iris.
    0: 0 # minimum value
    6: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  bridge_rewards: # Numero de mazmorras (cualquier combinacion de medallones y piedras) para abrir el puente arco iris.
    0: 0 # minimum value
    9: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  bridge_tokens: # Numero de skultullas de oro requeridas para el puente arco iris.
    0: 0 # minimum value
    100: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  shuffle_mapcompass: # Controla donde pueden aparecer los mapas y las brujulas.
    remove: 0
    startwith: 50
    vanilla: 0
    dungeon: 0
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_smallkeys: # Controla donde pueden aparecer las llaves pequeñas.
    remove: 0
    vanilla: 0
    dungeon: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_hideoutkeys: # Controla donde pueden aparecer las llaves de la fortaleza Gerudo.
    vanilla: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_bosskeys: # Controla donde pueden aparecer las llaves de jefe (excepto la llave del castillo de ganon).
    remove: 0
    vanilla: 0
    dungeon: 50
    overworld: 0
    any_dungeon: 0
    keysanity: 0
  shuffle_ganon_bosskey: # Controla donde puede aparecer la llave del jefe del castillo de Ganon.
    remove: 50
    vanilla: 0
    dungeon: 0
    overworld: 0
    any_dungeon: 0
    keysanity: 0
    on_lacs: 0
  enhance_map_compass: # El mapa indica si una dungeon es clasica o Master Quest. Las brujulas indican la recompensa de mazmorra.
    false: 50
    true: 0
  lacs_condition: # Marca el requerimiento para la escena de las flechas de luz (LACS) en el templo del tiempo.
    vanilla: 50
    stones: 0
    medallions: 0
    dungeons: 0
    tokens: 0
  lacs_stones: # Marca el numero de piedras espirituales requeridas para LACS
    0: 0 # minimum value
    3: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  lacs_medallions: # Marca el numero de medallones requeridas para LACS.
    0: 0 # minimum value
    6: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  lacs_rewards: # Marca el numero de recompensas de mazmorra requeridas para LACS.
    0: 0 # minimum value
    9: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  lacs_tokens: # Marca el numero de Skulltulas de oro requeridas para LACS.
    0: 0 # minimum value
    100: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  shuffle_song_items: # Marca donde pueden aparecer las canciones.
    song: 50
    dungeon: 0
    any: 0
  shopsanity: # Aleatoriza el contenido de las tiendas. "off" para no mezclar las tiendas; "0" mezcla las tiendas pero no permite objetos unicos en ellas.
    0: 0
    1: 0
    2: 0
    3: 0
    4: 0
    random_value: 0
    off: 50
  tokensanity: # Indica si las Skulltulas de oro pueden tener objetos que no sean su ficha.
    off: 50
    dungeons: 0
    overworld: 0
    all: 0
  shuffle_scrubs: # Aleatoriza los objetos de los Scrubs vendedores y marca su precio.
    off: 50
    low: 0
    regular: 0
    random_prices: 0
  shuffle_cows: # Las vacas dan objetos cuando les tocas las cancion de Epona.
    false: 50
    true: 0
  shuffle_kokiri_sword: # Aleatoriza la posicion de la espada Kokiri.
    false: 50
    true: 0
  shuffle_ocarinas: # Aleatoriza la posicion de las ocarinas.
    false: 50
    true: 0
  shuffle_weird_egg: # Aleatoriza la posicion del huevo extraño.
    false: 50
    true: 0
  shuffle_gerudo_card: # Aleatoriza la posicion de la tarjeta de membresia Gerudo.
    false: 50
    true: 0
  shuffle_beans: # Añade un pack de 10 judias magicas al juego y el vendedor vende un solo objeto por 60 rupias.
    false: 50
    true: 0
  shuffle_medigoron_carpet_salesman: # Aleatoriza el objeto que vende Medigoron y el vendedor de la alfombra voladora del paramo maldito.
    false: 50
    true: 0
  skip_child_zelda: # Empieza el juego con la carta de zelda, el objeto que daria impa al enseñar la nana de zelda. Y zelda se considera ya visitada (puedes ir directamente a ver a Saria al bosque y a Malon al rancho)
    false: 50
    true: 0
  no_escape_sequence: # Elimina la huida de link y zelda despues de ganar a Ganondorf.
    false: 0
    true: 50
  no_guard_stealth: # Elimina la escena de sigilo antes de ver a Zelda.
    false: 0
    true: 50
  no_epona_race: # No necesitas hacer la carrera para invocar a Epona.
    false: 0
    true: 50
  skip_some_minigame_phases: # La carrera de Dampe y el minijuego de arco a caballo dan ambras recompensas a la vez si se cumplen las condiciones.
    false: 0
    true: 50
  complete_mask_quest: # Todas las mascaras estan disponibles.
    false: 50
    true: 0
  useful_cutscenes: # Ciertas escenas se mantienen (como los Poes del templo del bosque, Darunia o Twinrova. Principalmente util para modos con Glitches.
    false: 50
    true: 0
  fast_chests: # Los cofres siempre se cogen rapido. Si se desactiva, los objetos importantes tienen animacion lenta. (IMPORTANTE: TODOS LOS OBJETOS QUE VAYAN A OTROS MUNDOS SE CONSIDERAN IMPORTANTES)
    false: 0
    true: 50
  free_scarecrow: # Sacara la ocraina cerca de un punto con espantapajaros invoca a Pierre sin necesidad de la cancion.
    false: 50
    true: 0
  fast_bunny_hood: # La capucha conejo mejora tu velocidad como en Majora's Mask.
    false: 50
    true: 0
  chicken_count: # Numero de Cuccos que Anju necesita en el corral para que te de el objeto.
    0: 0 # minimum value
    7: 50 # maximum value
    random: 0
    random-low: 0
    random-high: 0
  hints: # Marca el requerimiento para que las piedras chivatas den pistas.
    none: 0
    mask: 0
    agony: 0
    always: 50
  hint_dist: # Elije la distribucion de pistas
    balanced: 50
    ddr: 0
    league: 0
    mw2: 0
    scrubs: 0
    strong: 0
    tournament: 0
    useless: 0
    very_strong: 0
  damage_multiplier: # Controla el daño que recibe Link.
    half: 0
    normal: 50
    double: 0
    quadruple: 0
    ohko: 0
  no_collectible_hearts: # No caen corazones de enemigos u objetos.
    false: 50
    true: 0
  starting_tod: # Cambia el momento del dia al empezar el juego.
    default: 50
    sunrise: 0
    morning: 0
    noon: 0
    afternoon: 0
    sunset: 0
    evening: 0
    midnight: 0
    witching_hour: 0
  start_with_consumables: # Empieza el juego con el maximo de palos y nueves Deku que pueda llevar Link.
    false: 50
    true: 0
  start_with_rupees: # Empieza el juego con la cartera llena. Las mejoras de cartera vienen llenas.
    false: 50
    true: 0
  item_pool_value: # Cambia el numero de objetos disponibles en el juego.
    plentiful: 0
    balanced: 50
    scarce: 0
    minimal: 0
  junk_ice_traps: # Añade trampas de hielo.
    off: 0
    normal: 50
    on: 0
    mayhem: 0
    onslaught: 0
  ice_trap_appearance: # Cambia la apariencia de las trampas de hielo cuando aparecen como objetos fuera de cofres.
    major_only: 50
    junk_only: 0
    anything: 0
  logic_earliest_adult_trade: # Objeto mas bajo que puede aparecer en la secuencia de cambios de Link Adulto.
    pocket_egg: 0
    pocket_cucco: 0
    cojiro: 0
    odd_mushroom: 0
    poachers_saw: 0
    broken_sword: 0
    prescription: 50
    eyeball_frog: 0
    eyedrops: 0
    claim_check: 0
  logic_latest_adult_trade: # Objeto mas tardio que puede aparecer en la secuencia de cambios de Link Adulto.
    pocket_egg: 0
    pocket_cucco: 0
    cojiro: 0
    odd_mushroom: 0
    poachers_saw: 0
    broken_sword: 0
    prescription: 0
    eyeball_frog: 0
    eyedrops: 0
    claim_check: 50

```

## Unirse a un juego MultiWorld

### Obten tu parche

Cuando te unes a un juego multiworld, se te pedirá que entregues tu fichero YAML a quien sea que hospede el juego
multiworld. Una vez la generación acabe, el anfitrión te dará un enlace a tu fichero de datos o un zip con los ficheros
de todos. Tu fichero de datos tiene una extensión `.z5ap`.

Haz doble click en tu fichero `.z5ap` para que se arranque el Z5Client y realize el parcheado de la ROM. Una vez acabe
el parcheado de la rom (esto puede llevar un tiempo) se abrira automaticamente el emulador (Si se ha asociado la
extensión al emulador tal como hemos recomendado)

### Conectar al multiserver

Una vez arrancado tanto el Z5Client como el emulador hay que conectarlo entre ellos, para ello simplemente accede al
menú "Tools" y selecciona "Lua console". En la nueva ventana, dale al icono de la carpeta y busca el fichero
ootMulti.lua. Al cargar dicho fichero se conectara automaticamente con el cliente.

Nota: Es muy recomendable que no se abra ningún menú del emulador mientras esten emulador y Z5Client conectados, ya que
el script de conexión se para en ese caso y pueden provocar desconexiones. Si se pierde la conexion, simplemente haz
doble click en el script de nuevo.

Para conectar el cliente con el servidor simplemente pon la direccion_IP:puerto en la caja de texto de arriba y presiona
enter (si el servidor tiene contraseña, en la caja de texto de abajo escribir /connect direccion:puerto contraseña, para
conectar)

Y ya estas listo, para emprender tu aventura por Hyrule.