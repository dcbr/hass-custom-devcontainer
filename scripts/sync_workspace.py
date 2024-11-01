import os
import pathlib
import select
import shutil
import subprocess
import sys

from update_configuration import update_config
from install_plugins import install_plugins

WORKSPACE_PLUGINS = pathlib.Path('/workspace/dist')
WORKSPACE_INTEGRATIONS = pathlib.Path('/workspace/custom_components')
WORKSPACE_TEST_CONFIG = pathlib.Path('/workspace/test/config')

def sync_workspace(config_path, directory, event, file):
    src, dst = None, None
    if directory.is_relative_to(WORKSPACE_PLUGINS):
        src = WORKSPACE_PLUGINS
        dst = config_path / 'www' / 'workspace'
    elif directory.is_relative_to(WORKSPACE_INTEGRATIONS):
        src = WORKSPACE_INTEGRATIONS
        dst = config_path / 'custom_components'
    elif directory.is_relative_to(WORKSPACE_TEST_CONFIG):
        src = WORKSPACE_TEST_CONFIG
        dst = config_path
    else:
        return

    # Copy or delete modified file in target location
    target = dst / directory.relative_to(src) / file
    if "DELETE" in event:
        target.rmdir() if target.is_dir() else target.unlink()
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(directory / file, target)
    # Update configuration or reinstall plugins
    if str(target) == "/config/configuration.yaml" or src == WORKSPACE_INTEGRATIONS:
        update_config(config_path)
    if src == WORKSPACE_PLUGINS:
        install_plugins(config_path)

if __name__ == "__main__":
    stream = sys.stdin
    config_path = pathlib.Path('/config')
    should_restart = os.getenv('HASS_AUTO_RESTART', 'true') == 'true'
    timeout = 5.0
    dirty = False
    while True:
        if select.select([stream], [], [], timeout)[0]:
            # Listen for changes on input stream
            line = stream.readline()
            if line:
                directory, event, filename = line.split()
                sync_workspace(config_path, pathlib.Path(directory), event, filename)
                dirty = True
            else:
                break
        else:
            # No changes for 'timeout' seconds
            if dirty and should_restart:
                # Kill Home Assistant process such that it can be restarted
                print('Restarting')
                subprocess.run(['pkill', 'hass'])
            dirty = False
