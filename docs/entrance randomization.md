# Entrance Randomization

This document discusses the API and underlying implementation of the generic entrance randomization algorithm
exposed in [entrance_rando.py](/entrance_rando.py). Throughout the doc, entrance randomization is frequently abbreviated
as "ER."

This doc assumes familiarity with Archipelago's graph logic model. If you don't have a solid understanding of how
regions work, you should start there.

## Entrance Randomization Concepts

### Terminology

Some important terminology to understand when reading this doc and working with ER is listed below.

* Entrance rando - sometimes called "room rando," "transition rando," "door rando," or similar,
  this is a game mode in which the game map itself is randomized.
  In Archipelago, these things are often represented as `Entrance`s in the region graph, so we call it Entrance rando.
* Entrances and exits - entrances are ways into your region, exits are ways out of the region. In code, they are both
  represented as `Entrance` objects. In this doc, the terms "entrances" and "exits" will be used in this sense; the
  `Entrance` class will always be referenced in a code block with an uppercase E.
* Dead end - a region which can never give access to additional randomized transitions

### Basic Randomization Strategy

The Generic ER algorithm works by using the logic structures you are already familiar with. To give a basic example,
let's assume a toy world is defined with the vanilla region graph modeled below. In this diagram, the smaller boxes
represent regions while the larger boxes represent scenes. Scenes are not an Archipelago concept, the grouping is
purely illustrative.

```mermaid
%%{init: {"graph": {"defaultRenderer": "elk"}} }%%
graph LR
    subgraph startingRoom [Starting Room]
        S[Starting Room Right Door]
    end
    subgraph sceneB [Scene B]
        BR1[Scene B Right Door]
    end
    subgraph sceneA [Scene A]
        AL1[Scene A Lower Left Door] <--> AR1[Scene A Right Door]
        AL2[Scene A Upper Left Door] <--> AR1
    end
    subgraph sceneC [Scene C]
        CL1[Scene C Left Door] <--> CR1[Scene C Upper Right Door]
        CL1 <--> CR2[Scene C Lower Right Door]
    end
    subgraph sceneD [Scene D]
        DL1[Scene D Left Door] <--> DR1[Scene D Right Door]
    end
    subgraph endingRoom [Ending Room]
        EL1[Ending Room Upper Left Door] <--> Victory
        EL2[Ending Room Lower Left Door] <--> Victory
    end
    Menu --> S
    S <--> AL2
    BR1 <--> AL1
    AR1 <--> CL1
    CR1 <--> DL1
    DR1 <--> EL1
    CR2 <--> EL2
    
    classDef hidden display:none;
```

First, the world begins by splitting the `Entrance`s which should be randomized. This is essentially all that has to be
done on the world side; calling the `randomize_entrances` function will do the rest, using your region definitions and
logic to generate a valid world layout by connecting the partially connected edges you've defined. After you have done
that, your region graph might look something like the following diagram. Note how each randomizable entrance/exit pair
(represented as a bidirectional arrow) is disconnected on one end.

```mermaid
%%{init: {"graph": {"defaultRenderer": "elk"}} }%%
graph LR
    subgraph startingRoom [Starting Room]
        S[Starting Room Right Door]
    end
    subgraph sceneA [Scene A]
        AL1[Scene A Upper Left Door] <--> AR1[Scene A Right Door]
        AL2[Scene A Lower Left Door] <--> AR1
    end
    subgraph sceneB [Scene B]
        BR1[Scene B Right Door]
    end
    subgraph sceneC [Scene C]
        CL1[Scene C Left Door] <--> CR1[Scene C Upper Right Door]
        CL1 <--> CR2[Scene C Lower Right Door]
    end
    subgraph sceneD [Scene D]
        DL1[Scene D Left Door] <--> DR1[Scene D Right Door]
    end
    subgraph endingRoom [Ending Room]
        EL1[Ending Room Upper Left Door] <--> Victory
        EL2[Ending Room Lower Left Door] <--> Victory
    end
    Menu --> S
    S <--> T1:::hidden
    T2:::hidden <--> AL1
    T3:::hidden <--> AL2
    AR1 <--> T5:::hidden
    BR1 <--> T4:::hidden
    T6:::hidden <--> CL1
    CR1 <--> T7:::hidden
    CR2 <--> T11:::hidden
    T8:::hidden <--> DL1
    DR1 <--> T9:::hidden
    T10:::hidden <--> EL1
    T12:::hidden <--> EL2
    
    classDef hidden display:none;
```

From here, you can call the `randomize_entrances` function and Archipelago takes over. Starting from the Menu region,
the algorithm will sweep out to find eligible region exits to randomize. It will then select an eligible target entrance
and connect them, prioritizing giving access to unvisited regions first until all regions are placed. Once the exit has
been connected to the new region, placeholder entrances are deleted. This process is visualized in the diagram below
with the newly connected edge highlighted in red.

```mermaid
%%{init: {"graph": {"defaultRenderer": "elk"}} }%%
graph LR
    subgraph startingRoom [Starting Room]
        S[Starting Room Right Door]
    end
    subgraph sceneA [Scene A]
        AL1[Scene A Upper Left Door] <--> AR1[Scene A Right Door]
        AL2[Scene A Lower Left Door] <--> AR1
    end
    subgraph sceneB [Scene B]
        BR1[Scene B Right Door]
    end
    subgraph sceneC [Scene C]
        CL1[Scene C Left Door] <--> CR1[Scene C Upper Right Door]
        CL1 <--> CR2[Scene C Lower Right Door]
    end
    subgraph sceneD [Scene D]
        DL1[Scene D Left Door] <--> DR1[Scene D Right Door]
    end
    subgraph endingRoom [Ending Room]
        EL1[Ending Room Upper Left Door] <--> Victory
        EL2[Ending Room Lower Left Door] <--> Victory
    end
    Menu --> S
    S <--> CL1
    T2:::hidden <--> AL1
    T3:::hidden <--> AL2
    AR1 <--> T5:::hidden
    BR1 <--> T4:::hidden
    CR1 <--> T7:::hidden
    CR2 <--> T11:::hidden
    T8:::hidden <--> DL1
    DR1 <--> T9:::hidden
    T10:::hidden <--> EL1
    T12:::hidden <--> EL2
    
    classDef hidden display:none;
    linkStyle 8 stroke:red,stroke-width:5px;
```

This process is then repeated until all disconnected `Entrance`s have been connected or deleted, eventually resulting
in a randomized region layout.

```mermaid
%%{init: {"graph": {"defaultRenderer": "elk"}} }%%
graph LR
    subgraph startingRoom [Starting Room]
        S[Starting Room Right Door]
    end
    subgraph sceneA [Scene A]
        AL1[Scene A Upper Left Door] <--> AR1[Scene A Right Door]
        AL2[Scene A Lower Left Door] <--> AR1
    end
    subgraph sceneB [Scene B]
        BR1[Scene B Right Door]
    end
    subgraph sceneC [Scene C]
        CL1[Scene C Left Door] <--> CR1[Scene C Upper Right Door]
        CL1 <--> CR2[Scene C Lower Right Door]
    end
    subgraph sceneD [Scene D]
        DL1[Scene D Left Door] <--> DR1[Scene D Right Door]
    end
    subgraph endingRoom [Ending Room]
        EL1[Ending Room Upper Left Door] <--> Victory
        EL2[Ending Room Lower Left Door] <--> Victory
    end
    Menu --> S
    S <--> CL1
    AR1 <--> DL1
    BR1 <--> EL2
    CR1 <--> EL1
    CR2 <--> AL1
    DR1 <--> AL2
    
    classDef hidden display:none;
```

## Using Generic ER

### Defining Entrances to be Randomized

### Entrance Groups

### Imposing Custom Constraints on Randomization

## Implementation Details