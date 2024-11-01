import yaml
import os
import pathlib

from utils import CustomSafeLoader, CustomSafeDumper

CODESPACE_TRUSTED_PROXIES = [
    '127.0.0.1',  # Localhost ipv4
    '::1',  # Localhost ipv6
]

BYPASS_LOGIN_AUTH_PROVIDERS = [
    {
        'type': 'trusted_networks',
        'trusted_networks': [
            '0.0.0.0/0',  # Any ipv4 address
            '::/0',  # Any ipv6 address
        ],
        'allow_bypass_login': True,
    },
    {
        'type': 'homeassistant',  # Fallback
    },
]

DEFAULT_LOGGER = {
    'default': 'info'
}

def update_config(config_path):
    with open(config_path / 'configuration.yaml', 'r') as f:
        config = yaml.load(f, Loader=CustomSafeLoader)

    # Configure 'http' forwarding and trusted proxies
    trusted_proxies = os.getenv('HASS_TRUSTED_PROXIES', '').strip(';').split(';')
    if os.getenv('CODESPACES', 'false') == 'true':
        trusted_proxies.extend(CODESPACE_TRUSTED_PROXIES)
    if trusted_proxies:
        config['http'] = config.get('http', {})
        config['http']['use_x_forwarded_for'] = True
        config['http']['trusted_proxies'] = config['http'].get('trusted_proxies', [])
        config['http']['trusted_proxies'].extend(trusted_proxies)

    if os.getenv('HASS_BYPASS_LOGIN', 'false') == 'true':
        # Configure 'auth_providers' to always bypass login if it is not configured yet
        config['homeassistant'] = config.get('homeassistant', {})
        if 'auth_providers' not in config['homeassistant']:
            config['homeassistant']['auth_providers'] = BYPASS_LOGIN_AUTH_PROVIDERS
        else:
            print("Note: Bypass login is not enforced, as the configuration file already contains custom authentication providers.")

    # Setup default 'logger' if not configured yet
    config['logger'] = config.get('logger', DEFAULT_LOGGER)

    with open(config_path / 'configuration.yaml', 'w') as f:
        yaml.dump(config, f, Dumper=CustomSafeDumper)


if __name__ == "__main__":
    update_config(pathlib.Path('/config'))
    print("Configuration file updated.")
