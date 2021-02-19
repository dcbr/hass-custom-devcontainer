#!/bin/bash

docker run --rm -it \
    -p 5002:8123 \
    -v $(pwd):/workspaces/test \
    -v $(pwd):/config/www/workspace \
    -e LOVELACE_PLUGINS="thomasloven/lovelace-card-mod thomasloven/lovelace-auto-entities custom-cards/button-card kalkih/mini-media-player" \
    thomasloven/hass-custom-devcontainer