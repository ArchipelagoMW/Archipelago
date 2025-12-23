@echo on

cd /d %~dp0\..\Archipelago
python -m worlds.rac3.client.client --connect Player1:None@localhost:38281
