from .cli.sgucli import cli_make_example, cli_make_full_report, cli_get_workspace_id
from argparse import ArgumentParser
from . import config

def main():    
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode')
    
    parser_build = subparsers.add_parser('build', help='Builds the application defined in a configuration file')
    parser_build.add_argument('filepath', help='The filepath of the configuration file')
    parser_build.add_argument('destination', nargs='?', help='The destination of the generated csv file')

    subparsers.add_parser('example', help='Returns an example of the .yaml configuration file')

    workspaceIdParser = subparsers.add_parser('getIds', help='Returns workspace ids related to the api token')
    workspaceIdParser.add_argument('filepath', help='The filepath of the configuration file')
    
    parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
    args = parser.parse_args()

    if args.debug:
        config.__DEBUG__ = True

    if args.mode == 'example':
        cli_make_example()
        return
    
    if args.mode == 'geWorkspacetIds':
        cli_get_workspace_id(args.filepath)
        return
    
    if args.mode == 'build':
        if args.filepath:
            if args.destination:
                cli_make_full_report(args.filepath, args.destination)
            else:
                cli_make_full_report(args.filepath)
    else:
        print('No valid mode specified')
        raise Exception('Invalid mode')