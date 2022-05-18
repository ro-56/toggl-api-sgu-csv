import os
from configparser import ConfigParser

import togglreports.togglapi as togglapi


CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__),"../../data","config.ini"))


def init_config():
    ensure_config_path()
    config = ConfigParser()

    print("Initializing TogglReports...")

    config['toggl'] = {
        'fields': ['description', 'start', 'end', 'dur', 'user', 'client', 'project', 'tags'],
    }

    # Get user email
    while True:
        toggl_user_apitoken = input("api token: ")

        if not toggl_user_apitoken:
            print("Please enter an api token.")
            continue

        try: 
            user_data = togglapi.get_me(toggl_user_apitoken).get('data')
        except Exception:
            print("Invalid api token.")
            continue

        break

    config['toggl.user'] = {
        'email': user_data.get('email'),
        'api_token': user_data.get('api_token'),
    }

    # Get workspace
    possible_workspaces = togglapi.get_workspaces(toggl_user_apitoken)
    if not possible_workspaces:
        print("No workspaces found.")
        exit(1)
    print("Select a workspace:")
    for i, workspace in enumerate(possible_workspaces):
        print(f"{i} - {workspace['name']}")
    while True:
        input_workspace_idx = input("workspace number (0): ")

        if (input_workspace_idx
            and (not input_workspace_idx.isdigit()
                or int(input_workspace_idx) >= len(possible_workspaces))
        ):
            print("Please enter a valid workspace number.")
            continue

        workspace_idx = 0 if not input_workspace_idx else int(input_workspace_idx)

        toggl_workspace = possible_workspaces[workspace_idx]
        break
    
    config['toggl.workspace'] = {
        'id': toggl_workspace.get('id'),
        'name': toggl_workspace.get('name'),
    }

    # Get optional output file configuration
    input_reports_name = input("report name (toggl_report): ")
    reports_name = 'toggl_report' if not input_reports_name else input_reports_name

    input_reports_add_date = input("use current date as prefix (y): ")
    reports_add_date = True if ((input_reports_add_date == 'y') or (not input_reports_add_date)) else False
    
    config['reports'] = {
        'name': reports_name,
        'add_date': reports_add_date,
    }

    # Get sgu report configuration
    while True:
        reports_sgu_username = input("sgu username: ")

        if not reports_sgu_username:
            print("Please enter a sgu username.")
            continue

        break

    config['reports.sgu'] = {
        'username': reports_sgu_username,
    }

    # Write config file
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


def read_config() -> ConfigParser:
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config


def config_exists() -> bool:
    return os.path.exists(CONFIG_FILE)


def ensure_config_path() -> None:
    if not config_exists():
        os.mkdir(os.path.dirname(CONFIG_FILE))
    return None


def get_config_value(section: str, key: str) -> str:
    config = read_config()
    return config.get(section, key)


def get_report_config(report: str, report_section_prefix: str = 'reports.') -> dict:
    section = f'{report_section_prefix}{report}'
    config = read_config()
    options = config.options(section)
    data = {}
    for option in options:
        data[option] = config.get(section, option)
    
    return data


if __name__ == '__main__':
    init_config()
