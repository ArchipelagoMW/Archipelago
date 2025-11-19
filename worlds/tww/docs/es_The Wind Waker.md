# The Wind Waker

## ¿Dónde está la página de opciones?

La [página de opciones de jugador para este juego](../player-options) contiene todas las opciones que necesitas
para configurar y exportar un archivo de configuración.

## ¿Qué se randomiza en este juego?

Los objetos cambian de localización entre las distintas zonas del juego, haciendo que cada partida sea única.
La ubicación de los objetos incluye cofres, objetos recibidos de NPC y tesoros recuperados del fondo del océano.
El randomizador también incluye mejoras de calidad de vida, como que el mundo esté completamente abierto,
removiendo muchas cinemáticas, incrementando la velocidad de navegación y más.

## ¿Qué localizaciones están randomizadas?

Solo las localizaciones que se agreguen en la lógica del mundo van a ser randomizadas. Las localizaciones restantes
tendrán una Rupia amarilla, la cual incluye un mensaje indicando que la localización no ha sido randomizada.

## ¿Cuál es la meta en The Wind Waker?

Derrotar a Ganondorf en la cima de la Torre de Ganon. Esto requiere las 8 piezas de la Trifuerza del Valor,
la Espada Maestra al máximo poder (a menos que la espada sea opcional o sea el modo sin espada), Flechas de Luz
y cualquier otro objeto necesario para llegar a Ganondorf.

## ¿Qué aspecto tienen los objetos de otro mundo en TWW?

Los objetos que pertenecen a otros mundos que no sean de TWW son representados por la Carta del Padre
(la carta que Medli te da para que se la entregues a Komali), el cual es un objeto que no es usado en el
randomizador.

## ¿Qué pasa cuando el jugador recibe un objeto?

Cuando el jugador recibe un objeto, este se agregará automáticamente al inventario de Link. Link **no**
sostendrá el objeto por encima de su cabeza como en muchos otros randomizadores de Zelda.

## ¡Necesito ayuda! ¿Qué puedo hacer?

Primero ve la sección de preguntas frecuentes [FAQ](https://lagolunatic.github.io/wwrando/faq/) (solo en inglés).
Después, intenta con los pasos de solución de problemas en la
[Guía de configuración](/tutorial/The%20Wind%20Waker/setup/en). Si no puedes avanzar, por favor pregunta en el
canal de Wind Waker en el servidor de Archipielago.

## ¡Abrí el juego en Dolphin, pero no tengo mis objetos iniciales!

Debes conectarte al multijugador para recibir objetos, incluyendo tu inventario inicial.

## Errores conocidos

- Rupias tiradas aleatoriamente, la Bolsa de cebo también se le dará al jugador que recoja el objeto.
  El objeto se enviará de manera correcta, pero el jugador que la recoja recibirá una copia extra.
- Los objetos demo (objetos que se sostienen sobre la cabeza de Link) que **no** estén randomizados,
  ya sean rupias de tesoros recuperados de luces aleatorias del océano o recompensas de minijuegos,
  no funcionarán.
- Los mensajes de obtención de objetos progresivos recibidos en ubicaciones que se envían antes de lo
  previsto serán incorrectos. Esto no afecta la jugabilidad.
- El número de Fragmentos de Corazón en los mensajes de obtención de objetos estará desfasado en uno.
  Esto no afecta la jugabilidad.
- Se ha informado que los enlaces de objetos pueden presentar fallos. No es nada grave, pero conviene
  tenerlo en cuenta.

¡No dudes en informar sobre cualquier otro problema o sugerir mejoras en el canal de Wind Waker del servidor
Archipielago!

## Consejos y trucos

### ¿Dónde se encuentran los secretos en las mazmorras?

[Este documento](https://docs.google.com/document/d/1LrjGr6W9970XEA-pzl8OhwnqMqTbQaxCX--M-kdsLos/edit?usp=sharing)
contiene imágenes de cada uno de los secretos en las mazmorras.

### ¿Qué hacen exactamente las opciones de dificultad obscure y precise?

Las opciones `logic_obscurity` y `logic_precision` modifican la lógica del randomizador agregando varios trucos y
técnicas en la lógica.
[Este documento](https://docs.google.com/spreadsheets/d/14ToE1SvNr9yRRqU4GK2qxIsuDUs9Edegik3wUbLtzH8/edit?usp=sharing)
enumera claramente los cambios que agregan. Las opciones son progresivas, por ejemplo, la dificultad hard obscure
incluye tanto los trucos normal como hard obscure. Algunos cambios requieren la combinación de ambas opciones.
Por ejemplo, para que los cañones de Forsaken Fortress destruyan la puerta por ti, en tu lógica requieres tanto
la dificultad obscure como precise para que sea puesto al menos a normal.

### ¿Cuáles son las diferentes opciones predefinidas?

Algunas opciones predefinidas están disponibles en la [página de opciones de jugador](../player-options)
para su conveniencia.

- **Tournament S8**: Estos son (lo más aproximados posible) los ajustes utilizados en el servidor de
  carreras de WWR [Torneo Temporada 8](https://docs.google.com/document/d/1b8F5DL3P5fgsQC_URiwhpMfqTpsGh2M-KmtTdXVigh4).
  La configuración incluye 4 jefes obligatorios (con Kranos como requerido garantizado), entradas aleatorias
  a mazmorras, dificultad hard obscurity, y diversos checks en el mundo abierto. Si bien la lista de opciones
  de progresión habilitadas puede parecer intimidante, la configuración predefinida también excluye varias
  ubicaciones y te proporciona un puñado de objetos al inicio.
- **Miniblins 2025**: Estos son (lo más aproximados posible) los ajustes utilizados en el servidor de carreras
  de WWR [2025 Temporada de Miniblins](https://docs.google.com/document/d/19vT68eU6PepD2BD2ZjR9ikElfqs8pXfqQucZ-TcscV8).
  Esta configuración es genial si eres nuevo en Wind Waker. No hay demasiadas localizaciones en el mundo, y solo
  necesitas completar dos mazmorras. Además, empiezas con muchos objetos útiles, como el doble de magia,
  una mejora de capacidad para tu arco y bombas, y seis corazones.
- **Mixed Pools**: Estos son los ajustes utilizados en el servidor de carreras de WWR
  [Mixed Pools Torneo Cooperativo](https://docs.google.com/document/d/1YGPTtEgP978TIi0PUAD792OtZbE2jBQpI8XCAy63qpg).
  Esta configuración incluye entradas completamente aleatorias y la mayoría de ubicaciones tras una entrada
  aleatoria. También hay muchas localizaciones en el mundo abierto, ya que esta configuración está pensada para
  jugarse en modo cooperativo de dos personas. La configuración también tiene 6 jefes obligatorios, pero como
  las entradas son aleatorias, ¡los jefes pueden encontrarse en cualquier parte! Consulta tu Carta Náutica
  para averiguar en qué isla se encuentran los jefes.

## Mejoras planeadas

- CTMC dinámico basado en las opciones habilitadas.
- Implementación de pistas del randomizador base (opciones para colocación de pistas y tipos de pistas)
- Integración con el sistema de pistas de Archipielago (por ejemplo, subasta de pistas)
- Soporte de EnergyLink
- Lógica de Vela como opción.
- Corrección de errores de manera continua.

## Créditos

Este randomizador no pudo haber sido posible de no ser por la ayuda de:

- BigSharkZ: (arte del icono)
- Celeste (Maëlle): (corrección de lógica y errores tipográficos, programación adicional)
- Chavu: (documento de dificultad lógica)
- CrainWWR: (asistencia en la memoria del multijugador y Dolphin, programación adicional)
- Cyb3R: (referencias para `TWWClient`)
- DeamonHunter: (programación adicional)
- Dev5ter: (implementación adicional del TWW AP)
- Gamma / SageOfMirrors: (programación adicional)
- LagoLunatic: (randomizador base, asistencia adicional)
- Lunix: (soporte de Linux, programación adicional)
- mobby45: (traducción al francés de las guías)
- Mysteryem: (soporte del tracker, programación adicional)
- Necrofitz: (documentación adicional)
- Ouro: (soporte del tracker)
- tal (matzahTalSoup): (guía de secretos de las mazmorras)
- Tubamann: (programación adicional)
- ChinchyPandora7: (traducción al español de las guías)

El logo de Archipielago © 2022 por Krista Corkos y Christopher Wilson, bajo la licencia
[CC BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/).