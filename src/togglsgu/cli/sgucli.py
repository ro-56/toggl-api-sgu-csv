from togglsgu.lib.lib import get_config, print_csv_report, get_workspace_id

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
    pass

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
