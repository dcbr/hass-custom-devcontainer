import uuid
import json
import os
import pathlib
import sys

def install_plugins(config_path, urls=None):
    # Load already installed plugins
    plugins = load_plugins(config_path)
    # Iterate over all local workspace modules and downloaded github modules
    local_plugins = fetch_local_plugins(config_path)
    for url, meta in local_plugins.items():
        if url not in plugins:
            # Add the local plugin if it is not already installed
            plugins[url] = {}
        # Update the timestamp of the local plugin
        plugins[url]['timestamp'] = meta['timestamp']
    # Delete local workspace modules that are no longer available
    deleted_plugins = set(plugins.keys()) - set(local_plugins.keys())
    for url in deleted_plugins:
        del plugins[url]
    # Add the passed module urls if they are not already installed
    if urls is not None:
        for url in urls:
            if url not in plugins:
                plugins[url] = {}
    # Save all plugins
    save_plugins(config_path, plugins)

def load_plugins(config_path):
    # Load the already installed plugins
    existing_plugins = {}
    try:
        with open(config_path / '.storage' / 'lovelace_resources', 'r') as f:
            res_data = json.load(f)
            for item in res_data['data']['items']:
                url, timestamp, *_ = item['url'].split('?t=') + [None]
                existing_plugins[url] = {
                    'id': item['id'],
                    'timestamp': timestamp,
                }
    except FileNotFoundError:
        pass
    return existing_plugins

def fetch_local_plugins(config_path):
    local_plugins = []
    # Fetch all local workspace modules
    local_files_path = config_path / 'www' / 'workspace'
    local_plugins.extend(local_files_path.rglob('*.js'))
    local_plugins.extend(local_files_path.rglob('*.mjs'))
    # Fetch all downloaded github modules
    github_files_path = config_path / 'www' / 'github'
    local_plugins.extend(github_files_path.glob('*.js'))
    # Retrieve timestamps (last modified time) and convert to relative paths
    local_plugins = {
        str('local' / plugin.relative_to(config_path / 'www')): {
            'timestamp': int(os.path.getmtime(plugin))
        }
        for plugin in local_plugins
    }
    return local_plugins

def save_plugins(config_path, plugins):
    # Build resources data structure
    res_data = {
        'version': 1,
        'minor_version': 1,
        'key': 'lovelace_resources',
        'data': {
            'items': [
                {
                    'id': f"{meta.get('id', uuid.uuid4())!s}",
                    'type': 'module',
                    'url': f"{url}{'?t={}'.format(meta['timestamp']) if 'timestamp' in meta else ''}"
                } for url, meta in plugins.items()
            ]
        }
    }
    # Write as json to storage
    with open(config_path / '.storage' / 'lovelace_resources', 'w') as f:
        json.dump(res_data, f, indent=4)

if __name__ == "__main__":
    install_plugins(pathlib.Path('/config'))
