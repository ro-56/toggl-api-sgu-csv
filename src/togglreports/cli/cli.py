from argparse import ArgumentParser
import logging as log

from togglreports.lib.lib import get_config, print_csv_report, get_workspace_id


def main():
    example_arg = 'example'
    build_arg = 'build'
    workspace_arg = 'getIds'

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode')

    parser_build = subparsers.add_parser(build_arg, help='Builds the application defined in a configuration file')
    parser_build.add_argument('filepath', help='The filepath of the configuration file')
    parser_build.add_argument('destination', nargs='?', help='The destination of the generated csv file')

    subparsers.add_parser(example_arg, help='Returns an example of the .yaml configuration file')

    workspace_id_parser = subparsers.add_parser(workspace_arg, help='Returns workspace ids related to the api token')
    workspace_id_parser.add_argument('filepath', help='The filepath of the configuration file')

    parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
    args = parser.parse_args()

    if args.debug:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s - [%(levelname)s] %(message)s', datefmt='%H:%M:%S')

    if args.mode == example_arg:
        cli_make_example()
        return

    if args.mode == workspace_arg:
        cli_get_workspace_id(args.filepath)
        return

    if args.mode == build_arg:
        if args.filepath:
            if args.destination:
                cli_make_full_report(args.filepath, args.destination)
            else:
                cli_make_full_report(args.filepath)
    else:
        print('No valid mode specified')
        raise Exception('Invalid mode')

    return None


def cli_make_example() -> None:
    print(
        '''
        # Example config file (example.yaml)

        email: email@mail.com
        workspace_id: 123456789
        api_token: LoremIpsumDolorSitAmetConsecteturAdipiscingElit
        sgu_username: LoremIpsum
        output_file_name: output.csv
        '''
    )
    return None


def cli_make_full_report(config_file: str, output_file: str = '') -> None:
    config = get_config(config_file)

    if not output_file:
        output_file = config.get('output_file_name')

    print_csv_report(
        email=config.get('email', ''),
        workspace_id=config.get('workspace_id', ''),
        api_token=config.get('api_token', ''),
        sgu_username=config.get('sgu_username', ''),
        output_file_name=output_file)

    return None


def cli_get_workspace_id(config_file: str) -> None:
    config = get_config(config_file)

    print(get_workspace_id(config.get('api_token', '')))

    return None
