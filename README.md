# A docker container for developing and testing custom Home Assistant plugins and integrations

## Usage

```
docker run --rm -it \
    -p 5000:8123 \
    -v $(pwd)/test:/workspace/test \
    -v $(pwd)/dist:/workspace/dist \
    -v $(pwd)/custom_components:/workspace/custom_components \
    -e LOVELACE_PLUGINS="thomasloven/lovelace-card-mod;custom-cards/button-card" \
    dcbr/hass-custom-devcontainer
```

The default action of the image is to run `container`, which will
- Make sure there's a basic Home Assistant configuration in `/config` based on the test configuration provided in the workspace (`/workspace/test/config`).
- Add a default admin user to Home Assistant.
- Skip the onboarding procedure.
- Download and install [HACS](https://hacs.xyz) (optionally).
- Download lovelace plugins from github (optionally).
- Add downloaded and local plugins to lovelace configuration. The local plugins are fetched from the distribution folder in the workspace (`/workspace/dist`).
- Add local integrations to the configuration. The local integrations are fetched from the custom components folder in the workspace (`/workspace/custom_components`).
- Start Home Assistant with `-v`.

## Changelog

This is a fork from [thomasloven/hass-custom-devcontainer](https://github.com/thomasloven/hass-custom-devcontainer) with following changes:
  - Updated python environment and dependencies
  - Auto discovery and installation of locally developed plugins and integrations mounted in the `/workspace/dist` and `/workspace/custom_components` folders
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
| `HASS_AUTO_RESTART` | Flag indicating whether Home Assistant should be automatically restarted once a change in the test configuration or local module files is detected | `true` |
| `INSTALL_HACS` | Flag indicating whether to install HACS | `false` |
| `LOVELACE_PLUGINS` | Semicolon separated list of lovelace plugins to download from github | Empty |
| `ENV_FILE` | Path to environment file | Empty |
| `CODESPACE_PLUGINS` | Path to the distribution folder containing the modules of the locally worked on plugins | `$pwd/dist` |
| `CODESPACE_INTEGRATIONS` | Path to the custom components folder containing the files of the locally worked on integrations | `$pwd/custom_components` |
| `CODESPACE_TEST` | Path to the test folder containing the configuration files for the test environment | `$pwd/test` |

### Mount Points

A `/workspace` volume is set up to make local files available in the container. More specifically, all test related files
can be mounted in `/workspace/test`, all locally built javascript modules (plugins) can be mounted in `/workspace/dist`
and all locally developed python modules (integrations) can be mounted in `/workspace/custom_components`.

Custom configuration files for Home Assistant should be placed inside the `config` folder of the test mount point.
Note that the configuration file might be modified while launching the container, depending on the value of certain
environment variables. To avoid unwanted modifications to your ogininal configuration file, the contents of
`/workspace/test/config` are copied to `/config` before starting Home Assistant.
Similarly the contents of the `/workspace/dist` folder are copied to `/config/www/workspace` and the contents of
the `/workspace/custom_components` folder are copied to `/config/custom_components`.
When the container script is launched, each mount point is continuously watched for any changes. These changes are
then immediately reflected in Home Assistant's configuration folder.

**Note**: When working in a codespace, the active workspace files can be bound through the `CODESPACE_PLUGINS`,
`CODESPACE_INTEGRATIONS` and `CODESPACE_TEST` environment variables.

### About Lovelace Plugins
The dowload and installation of plugins is *very* basic. This is not HACS.

`LOVELACE_PLUGINS` should be a semicolon separated list of author/repo pairs, e.g. `thomasloven/lovelace-card-mod;kalkih/mini-media-player`

Any locally developed javascript modules mounted in `/workspace/dist` are also installed.

### About Integrations
If a locally developed integration is not manually configured in the test configuration, it is automatically added.

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
  "postStartCommand": "sudo -E container launch",
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
  "postStartCommand": "sudo -E container launch",
  "forwardPorts": [8123],
  "containerEnv": {
    "CODESPACE_INTEGRATIONS": "${localWorkspaceFolder}/integration",
    "CODESPACE_PLUGINS": "${localWorkspaceFolder}/es",
    "CODESPACE_TEST": "${localWorkspaceFolder}/test",
    "ENV_FILE": "${localWorkspaceFolder}/test/test.env"
  }
}
```

See also [dcbr/ha-templated-card](https://github.com/dcbr/ha-templated-card) for an example repository.
