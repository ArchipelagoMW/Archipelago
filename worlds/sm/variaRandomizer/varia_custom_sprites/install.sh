#!/bin/bash
# create symlinks for web2py

# remove symlinks in web2py install first, for first time use
CLEAN=1
if [ "${1}" == "--clean" ]; then
    CLEAN=0
fi

# we are in ~/RandomMetroidSolver/varia_custom_sprites/ as a submodule
BASE=$(dirname $0)/..
cd ${BASE}
CUR=$(pwd)/varia_custom_sprites

CUSTOM_SPRITES=$(python3 -c "from varia_custom_sprites.custom_sprites import customSprites; print(' '.join(list(customSprites.keys())))")
CUSTOM_SHIPS=$(python3 -c "from varia_custom_sprites.custom_ships import customShips; print(' '.join(list(customShips.keys())))")

THUMBNAILS_DIR=~/web2py/applications/solver/static/images
SHEETS_DIR=~/web2py/applications/solver/static/images/sprite_sheets

if [ ${CLEAN} -eq 0 ]; then
    echo "Clean existing web2py symlinks"
    for SPRITE in ${CUSTOM_SPRITES}; do
        rm -f ${THUMBNAILS_DIR}/${SPRITE}.png
        rm -f ${SHEETS_DIR}/${SPRITE}.png
    done
    for SHIP in ${CUSTOM_SHIPS}; do
        rm -f ${THUMBNAILS_DIR}/${SHIP}.png
    done
fi

# add ln for thumbnails & sprite sheets in web2py
echo "Create web2py symlinks"
for SPRITE in ${CUSTOM_SPRITES}; do
    [ -L ${THUMBNAILS_DIR}/${SPRITE}.png ] || ln -s ${CUR}/samus_sprites/${SPRITE}.png ${THUMBNAILS_DIR}/${SPRITE}.png
    [ -L ${SHEETS_DIR}/${SPRITE}.png ] || ln -s ${CUR}/sprite_sheets/${SPRITE}.png ${SHEETS_DIR}/${SPRITE}.png
done

for SHIP in ${CUSTOM_SHIPS}; do
    [ -L ${THUMBNAILS_DIR}/${SHIP}.png ] || ln -s ${CUR}/ship_sprites/${SHIP}.png ${THUMBNAILS_DIR}/${SHIP}.png
done

echo "done"
