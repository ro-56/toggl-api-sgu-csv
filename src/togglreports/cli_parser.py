""" Create a parser for the command line arguments """
from argparse import ArgumentParser

from togglreports.core import report_factory
from togglreports import build
from togglreports import config
from togglreports import utils


def process_arguments(parser: ArgumentParser) -> None:
    """ Process the parser """
    args = parser.parse_args()
    if args.cmd == 'build':
        if (args.start is None and args.end is not None):
            parser.error("argument -e/--end requires argument -s/--start")
        build.build_report(args.type, period=args.period, start=args.start, end=args.end)
    elif args.cmd == 'config':
        config.init_config()
    else:
        parser.print_help()
        exit(1)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest='cmd')

    _add_build_subparser(subparsers)
    _add_config_subparser(subparsers)

    return parser


def _add_build_subparser(subparser: ArgumentParser) -> None:
    """ Add the build subparser to the parser """

    parser = subparser.add_parser('build', help='Generate a report')
    parser.add_argument('type', choices=report_factory.PLUGINS, help='The report type to generate')

    group_1 = parser.add_mutually_exclusive_group()
    peri_arg = group_1.add_argument('-p', '--period', choices=utils.PERIODS, help='The period to generate the report for')
    group_1.add_argument('-s', '--start', help='The starting date of the report. Expects YYYY-MM-DD format')

    group_2 = parser.add_mutually_exclusive_group()
    group_2._group_actions.append(peri_arg)
    group_2.add_argument('-e', '--end', help='The ending date of the report. Expects YYYY-MM-DD format')

    parser.set_defaults(command='build')

    return None


def _add_config_subparser(subparser: ArgumentParser) -> None:
    """ Add the config subparser to the parser """

    parser = subparser.add_parser('config', help='Change the configuration')
    parser.set_defaults(command='config')

    return None
