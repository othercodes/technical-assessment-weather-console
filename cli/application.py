import getopt
import os
from typing import List, Optional, Dict, Any, Callable, Union, Tuple

from weather.shared.domain.contracts import Renderer

Command = Dict[str, Union[str, List[Dict[str, Any]], Callable]]


def _make_help_message(name: List[str], command: Command) -> str:
    name = " ".join([item for item in name if item is not None])

    if command.get('commands', {}):
        arguments = "<command>"
    else:
        arguments = " ".join([f"<{item.get('name')}>" for item in command.get('arguments', [])])

    tpl = f'Usage: {name} {arguments} [options]\n\nOptions:\n'
    for option in command.get('options', []):
        tpl += f' {" ".join(option.get("name"))}\t{option.get("description")}\n'

    if command.get('commands', {}):
        tpl += '\nCommands:\n'
        for sub, schema in command.get('commands', {}).items():
            tpl += f' {sub}\t{schema.get("description", "")}\n'

    return tpl


def _make_command_not_found(command: str) -> dict:
    def command_not_found(renderer: Renderer):
        renderer.render(f'> Command <{command}> not found.')

    return {
        'handler': command_not_found
    }


def _make_command(argv: List[str], commands) -> Tuple[Optional[str], Command]:
    try:
        if argv[0].startswith('-'):
            # if the first argument starts with (-) it is an option for the main app
            # so just raise an IndexError to load the main command definition
            raise IndexError
        # load the command definition, load command not found controller otherwise.
        command = commands.get(argv[0], _make_command_not_found(argv[0]))
        cid = argv[0]
    except IndexError:
        # if the command is not passed, load main definition.
        command = {
            'description': 'Get the weather information.',
            'commands': commands,
            'options': []
        }
        cid = None

    command.get('options', []).append({
        'id': 'help',
        'name': ['-h', '--help'],
        'default': False,
        'description': 'Shows this help message.'
    })

    return cid, command


def _make_arguments(argv: List[str], command: Command) -> Dict[str, str]:
    arguments = {}
    # process the arguments
    for index, argument in enumerate(command.get('arguments', [])):
        try:
            if argv[1 + index].startswith('-'):
                return {}

            arguments.update({
                argument['name']: argv[1 + index]
            })
        except IndexError:
            raise ValueError(f'Missing argument {argument["name"]}.')

    return arguments


def _make_options(opts: List[str], command: Command) -> Dict[str, Any]:
    short = str()
    long = list()

    # process the option forms (-x or --xxxx).
    for option in command.get('options', []):
        for form in [form.strip('-') for form in option.get('name')]:
            if len(form) <= 2:
                short += form
            else:
                long.append(form)

    # parse the real argument line to extract the options.
    opts, _ = getopt.getopt(opts, short, long)

    options = dict()
    # match the option value with the option name.
    for option in command.get('options', []):
        def match_opt_name(option: dict):
            forms = [form.strip('-:=') for form in option.get('name')]
            return lambda opt: opt[0].strip('-') in forms

        try:
            pair = next(filter(match_opt_name(option), opts))
            options.update({
                option['id']: True if len(pair[1].strip()) == 0 else pair[1]
            })
        except StopIteration:
            options.update({
                option['id']: option['default']
            })

    return options


class CLIRenderer(Renderer):
    def render(self, template: str, context: Optional[Dict[str, str]] = None):
        print(template.format(**context if context else {}))


def load_env_file(dotenv_path: str, override: bool = False):
    with open(dotenv_path) as file:
        lines = file.read().splitlines()

    dotenv_vars = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", maxsplit=1)
        dotenv_vars.setdefault(key, value)

    if override:
        os.environ.update(dotenv_vars)
    else:
        for key, value in dotenv_vars.items():
            os.environ.setdefault(key, value)


def cli(argv: List[str], renderer: Renderer, commands: Dict[str, Command]):
    """
    Command Line Interface

    Handles the incoming console input.

    :param argv: Raw list of arguments.
    :param renderer: The renderer service to print messages.
    :param commands: The list of available commands.
    :return: None
    """
    try:
        cid, command = _make_command(argv[1:], commands)
        arguments = _make_arguments(argv[1:], command)
        options = _make_options(
            [opt for opt in argv[2 + len(arguments.keys()):] if opt not in arguments.values()],
            command,
        )

        # display the help message if required.
        if options.get('help', False) or 'handler' not in command:
            return renderer.render(_make_help_message(
                name=[argv[0]] if cid is None else [argv[0], cid],
                command=command,
            ))

    except Exception as e:
        return renderer.render(f'> {type(e).__name__}: {e}')

    try:
        # delete the help option as is no more need from this point.
        del options['help']
    except KeyError:
        pass

    try:
        # execute the selected command and handle any error.
        return command['handler'](renderer, **arguments, **options)
    except Exception as e:
        return renderer.render(f'> {type(e).__name__}: {e}')
