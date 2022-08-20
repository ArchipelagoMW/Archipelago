# Archipelago Architecture
Archipelago is split into several components. All components must operate in tandem to facilitate randomization
and gameplay.

The components are:
* [Archipelago Generator](#archipelago-generator)
* [Archipelago Server](#archipelago-server)
* [Archipelago Game Client](#archipelago-game-client)

Some games require additional components in order to facilitate gameplay or communication with Archipelago.
The additional components vary from game to game but are typically:
* [Retro Console Emulator](#retro-console-emulator)
* [Emulator Communication Bridge (SNI)](#emulator-communication-bridge)

## Archipelago Generator
The Archipelago Generator is the part of Archipelago which takes YAML configuration files as input and produces a ZIP
file containing the data necessary for the Archipelago Server to service a session. The generator software is standalone
from the server or game clients and is run outside the server context. The server may then be pointed to the resulting
file to serve that session.

For more information on using the Archipelago Generator as a user, please visit the user facing MultiWorld Setup Guide 
section on [Rolling a YAML Locally](https://archipelago.gg/tutorial/Archipelago/setup/en#rolling-a-yaml-locally).

The Generator functions by using the classes defined in the `/worlds` folder to understand each game's items, location,
YAML options, and logic. The "World" classes define these properties in code and are loaded by the generator to allow it 
to validate YAML options and create a multiworld with cohesive and solvable logic despite the possibility of disparate
games being played.

## Archipelago Server
The Archipelago Server facilitates gameplay for a multiworld session. A session may have any number of players. 
As Archipelago is client-server software the server is still required for sessions even if only a single player is
present. The server takes a ZIP file or an ARCHIPELAGO file as input and serves the session using the information from
the input to properly serve the game clients over network.

## Archipelago Game Client
Archipelago game clients are currently implemented in two main ways. The first are in-process clients, which operate as
a mod loaded within the game process. The game process will then facilitate the WebSocket communication with the
Archipelago Server. Typically, more "modern" games will use this approach as they are typically easier to mod or are 
easier to inject with code at runtime. 

Some examples of Archipelago games implementing the in-process model are:
* [Risk of Rain 2](https://github.com/Ijwu/Archipelago.RiskOfRain2)
* [Subnautica](https://github.com/Berserker66/ArchipelagoSubnauticaModSrc)
* [Hollow Knight](https://github.com/Ijwu/Archipelago.HollowKnight)

The in-process model can be visualized using the following diagram:
```{mermaid}
flowchart LR
    APS[Archipelago Server]
    APGC[Archipelago Game Client]

    APS <-- WebSockets --> APGC
```

The second model of game client are those which operate out-of-process. The out-of-process clients are shipped with the
Archipelago installation and live within the Archipelago codebase. They are implemented in Python using [CommonClient.py](https://github.com/ArchipelagoMW/Archipelago/blob/main/CommonClient.py)
as a base. This client model is typically used for games in which runtime modification is difficult to impossible and for
games which require additional components such as the emulator communication bridge. This model is also used for clients
which communicate with the game from outside the game process to understand game state; the client then communicates 
updates to the Archipelago server based on the game state. 

Some examples of Archipelago games implementing the out-of-process model are:
* [Starcraft 2](https://github.com/ArchipelagoMW/Archipelago/blob/main/Starcraft2Client.py)
* [Factorio](https://github.com/ArchipelagoMW/Archipelago/blob/main/FactorioClient.py)
* [The Legend of Zelda: Ocarina of Time](https://github.com/ArchipelagoMW/Archipelago/blob/main/OoTClient.py)

The out-of-process model can be visualized using the following diagram:
```{mermaid}
flowchart LR
    APS[Archipelago Server]
    OOPGC[Out-of-Process Game Client]
    GP[Game Process]

    APS <-- WebSockets --> OOPGC <--> GP
```

Games which use the [SNI](https://github.com/alttpo/sni) emulator communication bridge can be connected to Archipelago using the [SNIClient](https://github.com/ArchipelagoMW/Archipelago/blob/main/SNIClient.py).

Games communicating using SNI may be visualized using the following diagram:
```{mermaid}
flowchart LR
    APS[Archipelago Server]
    SNIC[SNIClient]
    SNI[SNI]
    GP[Game Process]

    APS <-- WebSockets --> SNIC <-- WebSockets --> SNI <--> GP
```

## Retro Console Emulator
Some game implementations require the use of an emulator in order to run the game and to communicate with SNI.
These games are typically "retro" games which were released on 8-bit or 16-bit consoles, although newer consoles may be
included for some game implementations.

All emulators currently used in Archipelago game implementations which require them are lua enabled and use a lua script
to communicate with SNI.

## Emulator Communication Bridge
All implementations of game clients for which the game is run in an emulator presently use [SuperNintendoInterface or SNI](https://github.com/alttpo/sni)
to communicate between the emulator and the SNIClient. The emulator uses lua to communicate to SNI which communicates with
the SNIClient which communicates with the Archipelago server.