import os
import sys

from cli.application import load_env_file, cli, CLIRenderer
from cli.controllers import current_command

ENV_FILE = './.env'

if __name__ == "__main__":
    # load the application configuration.
    env_file = os.path.abspath(ENV_FILE)
    if not os.path.exists(env_file):
        print(f'Unable to load the configuration, please check the {env_file} file.')
    load_env_file(env_file)

    # configure and execute.
    cli(sys.argv, CLIRenderer(), {
        'current': {
            'handler': current_command,
            'description': 'Get the current weather data for the given location.',
            'arguments': [
                {'name': 'location'}
            ],
            'options': [
                {
                    'id': 'units',
                    'name': ['-u:', '--units='],
                    'default': 'metric',
                    'description': 'Units of measurement must be metric or imperial, metric by default.',
                }
            ]
        },
    })
