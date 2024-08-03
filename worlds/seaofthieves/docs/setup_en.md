# Sea of Thieves MultiWorld Setup Guide

## Required Software

- Sea of Thieves must be installed (agnostic of launcher, console works too)
- You must have Captain status in Sea of Thieves or be playing in the same world as someone who does
- Must be able to login to [view your captaincy](https://www.seaofthieves.com/profile/captaincy)

## Setup Procedure

1. Configure your Options by navigating to supported games, Sea of Thieves, and clicking options on the Archipelago
   website. Then once configured, export your YAML file. Do this for each world in your game

2. Host a world from your YAML files, during generation there should be an output file with the extension "sotci"
   for each player. Each player needs to save their file and load their appropriate file when starting the client.

3. You must now [login](https://www.seaofthieves.com/profile/captaincy/) to the Sea of Thieves website.

4. While on the website, open the developer tools and look at the network information. There is an XHR request named "
   captaincy", if you do not see one, hard refresh your page (cntrl+F5).

5. View the "Request Headers" section of the "captaincy" HXR GET request. In the header is a field named "Cookie". Copy
   the value of the "Cookie" field and save it to a text file on your computer like "cookie.txt". Make sure you do not
   save extra newlines at the top of the file. At this point you should have two files, the sotci file and the cookie
   file. Verify you did not copy "Set-Cookie" but instead the "Cookie" field.

6. Each player that is connecting to the hosted world must run the client, the Sea of Thieves client can be found in the
   launcher.

7. When the client opens, it asks you to select your sotci file, do this.

8. If you would like to play a manual, connect to the host by entering user@ip:port in the connect bar and connecting. Otherwise if you intend to use the auto-tracker, do not connect and continue.
7. To setup auto-tracker:
    - Run `/setcookie` to set your cookie. If your file is invalid, there will be a warning message
    - Run `/setmode <mode>` to set your initial game mode to pirate or ship. If you want to run pirate mode,
      run `/setmode NA`. If you want to run ship mode, run `/setmode #` where # is the integer value of your ship
      starting at 0. You can figure this number out by
      opening [view your captaincy](https://www.seaofthieves.com/profile/captaincy) and viewing your ships. Starting
      left to right, number your ships 0, 1, 2 ... This is the number of your ship.

8. Connect to the host with user@ip:port in the connect bar

9. If there are no errors in the client, then Open Sea of Thieves and you are all set to play. See the general Sea of
   Thieves guide for game/client information.
