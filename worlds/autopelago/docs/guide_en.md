# Autopelago Setup Guide

## Required Software

- A browser with JavaScript enabled (you are probably using one right now!).

## Playing the game
Open the Autopelago website. There are two options:
- Cruise over to the [Autopelago Website](https://autopelago.app/). This is the easiest option. If the website is
  unavailable, use the next option.
- Download the latest release from [Autopelago Release](https://github.com/airbreather/Autopelago/releases/latest) and
  unzip the `dist.zip`. You will need to host the files using a web server instead of just opening `index.html` in your
  browser, because of some stuff that browsers do to prevent malicious websites from getting your secrets. Basically any
  web server should work (it's just a static website):
  - If you have Python installed for other reasons, you can run `python -m http.server 8000` in the directory containing
    the files and browse to [http://localhost:8000](http://localhost:8000).
  - If Docker is your jam, you can run `docker run -it --rm -p 8000:80 -v $(pwd):/usr/share/nginx/html nginx` from the
    directory containing the files and then browse to [http://localhost:8000](http://localhost:8000).
  - If you're lost at this point and **really** can't use the main website for some reason, you could try
    [Static Web Server](https://static-web-server.net/getting-started). That link goes to their "Getting Started" page.

Enter the standard login information, change any settings you want (normally, the defaults are fine), and you're off!

The website has a built-in client, where you can chat and send commands.

For more information on generating Archipelago games and connecting to servers, please see the [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en).
