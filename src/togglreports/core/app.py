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
        # Initialize the configuration if not present
        if not config.config_exists():
            config.init_config()

        self._parser = cli_parser.create_parser()
        if not self._parser:
            raise Exception('Parser not initialized')
            exit(1)

    def _load_plugins(self):
        plugin_loader.load_plugins()
