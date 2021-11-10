from lib.lib import get_config, print_csv_report, get_workspace_id

def make_example(output_file: str) -> None:
    pass

def make_full_report(config_file: str, output_file: str) -> None:
    config = get_config(config_file)

    print_csv_report(
        email=config.email,
        workspace_id=config.workspace_id,
        api_token=config.api_token,
        sgu_username=config.sgu_username,
        output_file_name=output_file)
    
    return None

def get_workspace_id(config_file: str) -> None:
    config = get_config(config_file)
    print(get_workspace_id(config.api_token))
    return None
