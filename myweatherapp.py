import os
import sys

from cli.application import load_env_file, cli, CLIRenderer
from cli.controllers import forcast_command, current_command

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
        'forecast': {
            'handler': forcast_command,
            'description': 'Get the weather forecast for max 5 days for the given location.',
            'arguments': [
                {'name': 'location'}
            ],
            'options': [
                {
                    'id': 'days',
                    'name': ['-d:', '--days='],
                    'default': 1,
                    'description': 'The number of days to retrieve forecast data for, 1 by default',
                },
                {
                    'id': 'units',
                    'name': ['-u:', '--units='],
                    'default': 'metric',
                    'description': 'Units of measurement must be metric or imperial, metric by default.',
                }
            ]
        },
    })
