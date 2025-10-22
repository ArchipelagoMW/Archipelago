#!/bin/bash

EXPECTED_CLIENT_VERSION=$(python worlds/candybox2/expected_client_version.py)
# Extract the date part (before the hyphen)
DATE_PART=$(echo "$EXPECTED_CLIENT_VERSION" | cut -d'-' -f1)

# Extract the version part (after the hyphen)
VERSION_PART=$(echo "$EXPECTED_CLIENT_VERSION" | cut -d'-' -f2)

# Check if version ends with '+'
if [[ $VERSION_PART == *+ ]]; then
    # Remove the '+' and increment the number
    BASE_VERSION=$(echo "$VERSION_PART" | sed 's/+$//')
    BUILD_NUMBER=$((BASE_VERSION + 1))
else
    # Use the version as-is
    BUILD_NUMBER=$(echo "$VERSION_PART")
fi

# Update the archipelago.json file
jq ".world_version=\"1.$DATE_PART.$BUILD_NUMBER\"" worlds/candybox2/archipelago.json > worlds/candybox2/archipelago.json.tmp && mv worlds/candybox2/archipelago.json.tmp worlds/candybox2/archipelago.json