#!/bin/bash
set -e

# Cleanup
rm -rf target/

# Build the maps
pushd Maps/ArchipelagoCampaign
./build.sh
popd

# Create the target directory
mkdir -p target

# Copy maps
mkdir -p target/Maps/ArchipelagoCampaign/WoL
cp -- Maps/ArchipelagoCampaign/WoL_build/* target/Maps/ArchipelagoCampaign/WoL/

# Copy mods
mkdir -p target/Mods
cp -r -- Mods/* target/Mods
