# A docker container for developing and testing custom Home Assistant plugins and integrations

## Usage

```
docker run --rm -it \
    -p 5000:8123 \
    -v $(pwd)/test:/workspace/test \
    -v $(pwd)/dist:/workspace/dist \
    -e LOVELACE_PLUGINS="thomasloven/lovelace-card-mod custom-cards/button-card" \
    dcbr/hass-custom-devcontainer
```

The default action of the image is to run `container`, which will
- Make sure there's a basic Home Assistant configuration in `/config` based on the test configuration provided in the workspace (`/workspace/test/config`).
- Add a default admin user to Home Assistant.
- Skip the onboarding procedure.
- Download and install [HACS](https://hacs.xyz) (optionally).
- Download lovelace plugins from github.
- Add downloaded and local plugins to lovelace configuration. The local plugins are fetched from the distribution folder in the workspace (`/workspace/dist`).
- Start Home Assistant with `-v`.

## Changelog

This is a fork from [thomasloven/hass-custom-devcontainer](https://github.com/thomasloven/hass-custom-devcontainer) with following changes:
  - Updated python environment and dependencies
  - Auto discovery and installation of locally developped plugins mounted in the `/workspace/dist` folder
  - Test configuration files mounted in the `/workspace/test/config` folder are preprocessed and copied to `/config` to be used by Home Assistant
  - Added support for bypassing the login form and for trusting the specified proxies
  - Built-in support for running this container as a codespace (see below)

### Environment Variables

| Name | Description | Default |
|---|---|---|
| `HASS_USERNAME` | The username of the default user | `dev` |
| `HASS_PASSWORD` | The password of the default user | `dev` |
| `HASS_BYPASS_LOGIN` | Flag indicating whether to bypass the login form | `false` |
| `HASS_TRUSTED_PROXIES` | Semicolon separated list of proxy ip addresses to trust | Empty (`::1` in codespace) |
| `INSTALL_HACS` | Flag indicating whether to install HACS | `false` |
| `LOVELACE_PLUGINS` | Semicolon separated list of lovelace plugins to download from github | Empty |
| `ENV_FILE` | Path to environment file | Empty |
| `CODESPACE_DIST` | Path to the distribution folder containing the modules of the locally worked on plugins | `$pwd/dist` |
| `CODESPACE_TEST` | Path to the test folder containing the configuration files for the test environment | `$pwd/test` |

### Mount Points

A `/workspace` volume is set up to make local files available in the container. More specifically, all test related files
can be mounted in `/workspace/test` and all locally built javascript modules can be mounted in `/workspace/dist`.

Custom configuration files for Home Assistant should be placed inside the `config` folder of the test mount point.
Note that the configuration file might be modified while launching the container, depending on the value of certain
environment variables. To avoid unwanted modifications to your ogininal configuration file, the contents of
`/workspace/test/config` are *copied* to `/config` before starting Home Assistant. As a result, any updates to this
test configuration will only take effect after a full relaunch.

**Note**: When working in a codespace, the active workspace files can be bound through the `CODESPACE_DIST` and
`CODESPACE_TEST` environment variables.

### About Lovelace Plugins
The dowload and installation of plugins is *very* basic. This is not HACS.

`LOVELACE_PLUGINS` should be a semicolon separated list of author/repo pairs, e.g. `thomasloven/lovelace-card-mod;kalkih/mini-media-player`

Any locally developped javascript modules mounted in `/workspace/dist` are also installed.

### Container Script

```bash
container
```
Set up and launch Home Assistant

```bash
container setup
```
Perform download and setup parts but do not launch Home Assistant

```bash
container launch
```
Launch Home Assistant with `hass -c /config -v`

## devcontainer.json example

```json
{
  "image": "dcbr/hass-custom-devcontainer",
  "postCreateCommand": "sudo -E container setup && npm add",
  "forwardPorts": [8123],
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind,readonly"
  ],
  "runArgs": ["--env-file", "${localWorkspaceFolder}/test/test.env"]
}
```

## Github codespace example

```json
{
  "image": "dcbr/hass-custom-devcontainer",
  "postCreateCommand": "sudo -E container setup && npm add",
  "forwardPorts": [8123],
  "containerEnv": {
    "CODESPACE_DIST": "${localWorkspaceFolder}/es",
    "CODESPACE_TEST": "${localWorkspaceFolder}/test",
    "ENV_FILE": "${localWorkspaceFolder}/test/test.env"
  }
}
```

See also [dcbr/ha-template-eval-card](https://github.com/dcbr/ha-template-eval-card) for an example repository.
