import json
import pathlib
import sys

def install_plugins(config_path, plugins):
    # Create list of downloaded plugins
    plugins = plugins.strip(';').split(';')
    # Add all local workspace modules
    local_files_path = config_path / 'www' / 'workspace'
    plugins.extend(local_files_path.glob('*.js'))
    plugins.extend(local_files_path.glob('*.mjs'))
    # Build resources data structure
    res_data = {
        'version': 1,
        'minor_version': 1,
        'key': 'lovelace_resources',
        'data': {
            'items': [
                {
                    'id': f'{i}',
                    'type': 'module',
                    'url': f"local/{pathlib.Path(plugin).relative_to(config_path / 'www')!s}"
                } for (i, plugin) in enumerate(plugins)
            ]
        }
    }
    # Write as json to storage
    with open(config_path / '.storage' / 'lovelace_resources', 'w') as f:
        json.dump(res_data, f, indent=4)

if __name__ == "__main__":
    install_plugins(pathlib.Path('/config'), sys.argv[1])
