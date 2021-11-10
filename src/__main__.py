from src.cli.sgucli import make_example, make_full_report, get_workspace_id
from argparse import ArgumentParser

def main():    
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode')
    
    parser_build = subparsers.add_parser('build', help='Builds the application defined in a configuration file')
    parser_build.add_argument('filepath', help='The filepath of the configuration file')
    parser_build.add_argument('destination', help='The destination of the generated csv file')

    subparsers.add_parser('example', help='Returns an example of the .yaml configuration file')

    subparsers.add_parser('geWorkspacetIds', help='Returns workspace ids related to the api token')

    args = parser.parse_args()


    if args.mode == 'example':
        make_example()
        return
    
    if args.mode == 'geWorkspacetIds':
        get_workspace_id()
        return
    
    if args.mode == 'build':
        if args.filepath:
            if args.destination:
                make_full_report(args.filepath, args.destination)
            else:
                make_full_report(args.filepath)
    else:
        print('No mode specified')
        raise Exception('Invalid mode')