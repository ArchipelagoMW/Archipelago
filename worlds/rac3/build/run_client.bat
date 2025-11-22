@echo on

cd /d %~dp0\..\Archipelago
python -m worlds.rac3.client.Rac3Client --connect Player1:None@localhost:38281
