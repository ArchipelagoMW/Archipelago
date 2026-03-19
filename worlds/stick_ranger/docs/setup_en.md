# Stick Ranger Randomizer Setup Guide

## Required Software

- A browser!
- Optional for local installation and play: [Node.js and npm](https://nodejs.org/) installed on your computer, if you want to run the game locally.

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

You can customize your settings by visiting the 
[Stick Ranger Player Options Page](/games/Stick%20Ranger/player-options).

## Where to play the game

### Option 1: Play Online (Recommended)

- Go to the [Stick Ranger Website](https://kryen112.github.io/).
  - This is the easiest option—no installation required. If the website is unavailable, use the next option.

### Option 2: Run the Game Locally

If the website is unavailable, or you wish to use your own copy:

1. Download the latest release:
    - Visit [Stick Ranger Release](https://github.com/Kryen112/Kryen112.github.io/releases/latest).
    - Download and extract the zip file containing the source code to a folder on your computer.
2. Install Node.js and npm (if not already installed):
    - Download and install from [nodejs.org](https://nodejs.org/).
3. Open a terminal/command prompt in the folder where you extracted the files.
4. Install dependencies:
    ```sh
    npm install
    ```
5. Start the local development server:
    ```sh
    npm run dev
    ```
    - The server will start and print a local address (usually `http://localhost:5173/` or similar).
    - Open this address in your browser.

#### Troubleshooting & Tips
- npm: command not found?  
    Make sure Node.js and npm are installed and added to your system PATH.
- Port in use error:  
    If you get an error that the port is already in use, either stop the other process or use `npm run dev -- --port=YOURPORT` to specify another port.
- Game not loading?  
    Double-check you are in the correct folder and all files were extracted.

## Joining a multiworld game

1. Enter your **server address**, **port**, **slot name** and **password** (if applicable).
2. Click **Connect** and log in.
3. You can now play Stick Ranger with Archipelago integration!  
   The website includes a built-in client where you can chat and use client commands.   