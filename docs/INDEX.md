# Archipelago Docs Index

This is an index meant to act as a quick reference/description for the different files part of Archipelago's
documentation. The docs are organized into sections depending on which purpose they are most relevant to, as for most
devs it is not necessary to read all of them.

## General/Main Repository

Docs for basic setup of development with Archipelago or information relevant to the main Archipelago repository. Docs
with player-facing information are contained in the [generic setup guides](/worlds/generic/docs/) shown on the website,
and may be useful for developers as well.

### [Running from Source](/docs/running%20from%20source.md)

Setup instructions for using a source install of Archipelago (as opposed to a built/"frozen" release), which should be
followed for developing any changes to either Archipelago's core or creating a world.

### [Contributing Guidelines](/docs/contributing.md)

Guidelines for contributing or reviewing changes to the Archipelago repo, including for either the core software or
contained worlds.

### [Code of Conduct](/docs/code_of_conduct.md)

Expectations for interactions with others involving the Archipelago repo.

### [Style Guide](/docs/style.md)

Style guidelines for code/documentation contributions to the Archipelago repo, especially for parts the core software.
Standalone worlds may follow them as well if desired.

### [Codeowners Listing](/docs/CODEOWNERS)

List of maintainers/owners of worlds or documentation contained in the Archipelago repo. Changes to the given parts
of the repo require the approval of a listed owner in addition to a core maintainer.

### [World Maintainer Expectations](/docs/world%20maintainer.md)

Expectations and processes for maintainers of worlds contained within the Archipelago repo.

### [Triage Role Expectations](/docs/triage%20role%20expectations.md)

Expectations for those with triage permissions for issues/pull requests on the Archipelago repo.

## World Development

Docs relevant to implementing an Archipelago integration. The [Running From Source](#running-from-source) doc is a
prerequisite for working on an APWorld, and if intending to merge a world into the main Archipelago repo, some of the
other [general information docs](#general) will be relevant as well.

### [Adding Games](/docs/adding%20games.md)

General overview of steps needed for creating an integration of a new game for Archipelago. Lists basic requirements and
recommendations, but does not include main technical specification.

### [World API](/docs/world%20api.md)

Specification for APWorld plugins to the generation system. Includes expectations for structure and examples for
implementations of world methods.

### [APWorld Specification](/docs/apworld%20specification.md)

Specification for the structure of APWorlds, especially the packaged release format using the `.apworld` extension.
Includes information on the build tool and surrounding metadata.

### [Options API](/docs/options%20api.md)

Information for creating generation options for a world, set by the player for each slot they include in a generation.

### [Settings API](/docs/settings%20api.md)

Information for defining installation-wide configuration for a world in the `host.yaml` file. Most worlds will not
require its use.

### [Network Protocol](/docs/network%20protocol.md)

Specification for the protocol used by clients to communicate with the Archipelago server during play. Contains
information about pre-existing libraries implementing the protocol, which most integrations will be able to use instead
of needing to implement the protocol directly.

### [Shared Cache](/docs/shared_cache.md)

Information on Archipelago's shared cache between that can be re-used between different clients.

### [APWorld Dev FAQ](/docs/apworld_dev_faq.md)

List of information about common questions or issues hit during world development.

### [Tests](/docs/tests.md)

Setup information for running Archipelago's unittests and specification for creating world-specific tests.

### [Rule Builder](/docs/rule%20builder.md)

Specification and reference for using the integrated Rule Builder system to specify world logic.

### [Generic Entrance Randomization](/docs/entrance%20randomization.md)

Setup and implementation information for the Entrance Randomization system meant to generically support implementation
of entrance randomization features between different worlds.

## WebHost Use

Information about running or interfacing with the Archipelago WebHost, which runs the website (for instance, the main
[archipelago.gg](https://archipelago.gg) host).

### [WebHost Configuration Sample](/docs/webhost%20configuration%20sample.yaml)

Template for configuration when running WebHost locally, including descriptions of the settings.

### [WebHost API](/docs/webhost%20api.md)

API specification for interfacing with a WebHost instance. Includes the ability to generate new seeds and fetch tracking
data about given rooms.

### [Deploy Using Containers](/docs/deploy%20using%20containers.md)

Setup information for running the WebHost from a containerized environment.
