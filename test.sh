#!/bin/bash

ports=('-p' '5002:8123')
mounts=('-v' "$(pwd):/workspace")
environment=('-e' 'LOVELACE_PLUGINS=thomasloven/lovelace-card-mod;dcbr/ha-template-eval-card;custom-cards/button-card;kalkih/mini-media-player' \
             '-e' 'ENV_FILE=/workspace/test/test.env')

if [ "$CODESPACES" == "true" ]; then
    # If we are running in a codespace, add this container's ip addresses
    # to the trusted proxies list
    ips=$(hostname -I)
    ips=${ips// /;}
    environment=("${environment[@]}" \
                 '-e' "HASS_TRUSTED_PROXIES=$ips")
fi

docker run --rm --name test -it \
    "${ports[@]}" \
    "${mounts[@]}" \
    "${environment[@]}" \
    dcbr/hass-custom-devcontainer sudo -E container run-dev
