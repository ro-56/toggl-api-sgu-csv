from argparse import ArgumentParser

from togglreports import cli_parser, config
from togglreports.core import plugin_loader


class Application():
    _parser: ArgumentParser

    def run(self):
        # Load the plugins
        self._load_plugins()

        # Initialize the application
        self._initialize()

        # Parse the arguments
        cli_parser.process_arguments(self._parser)

    def _initialize(self):
        # Initialize parser
        self._parser = cli_parser.create_parser()
        if not self._parser:
            raise Exception('Parser not initialized')
        
        # Check parser for the --help command
        # Prints the help section and exits if --help was used
        self._parser.parse_args()

        # Initialize the configuration if it's not present
        if not config.config_exists():
            config.init_config()


    def _load_plugins(self):
        plugin_loader.load_plugins()
