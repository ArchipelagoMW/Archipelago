# DSZeldaClient
Shared Archipelago Client Submodule for Zelda: Phantom Hourglass and Spirit Tracks

# I'm bad at git so here are command line instructions to future me
Apparently pycharm *can* handle submodules just fine! i think you still need to set it up in command line, but once it's in pycharm can push submodule updates!

Setting up the submodule in a new local, while in the world folder (tloz_xx)
```
git submodule add https://github.com/carrotinator/DSZeldaClient/
```

You made an edit to DSZC, and need to push to remote. do this inside the submodule folder (DSZeldaClient)
```
git status
git add <files to add>
git commit -am "<commit message>"
git push
```

Kat made an edit and you want to fetch it. do this inside the submodule folder (DSZeldaClient)
```
git fetch
git status
git pull
```

Branch managing, cause that's usually a good idea
```
git branch <branch name>
git checkout <branch name>
git push --set-upstream origin <branch name>
```
