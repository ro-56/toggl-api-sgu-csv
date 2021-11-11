from togglsgu.lib.lib import get_config, print_csv_report, get_workspace_id

def cli_make_example(output_file: str) -> None:
    pass

def cli_make_full_report(config_file: str, output_file: str) -> None:
    config = get_config(config_file)

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
