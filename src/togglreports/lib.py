"""
"""
from datetime import datetime, timedelta
import logging as log
from yaml import safe_load, YAMLError

from pandas import DataFrame
from requests import get


def get_week_start_end() -> tuple[str, str]:
    """
    Get this weeks start and end date.
    """
    date_format = "%Y-%m-%d"
    date_today = datetime.today()
    start_report_date = date_today - timedelta(days=date_today.weekday() + 8)
    end_report_date = start_report_date + timedelta(days=6)

    start_report_date = start_report_date.strftime(date_format)
    end_report_date = end_report_date.strftime(date_format)

    log.debug(f'Start report date: {start_report_date} | End report date: {end_report_date}')

    return start_report_date, end_report_date


def get_report(api_token, user_agent, workspace_id) -> dict:
    """
    """
    url = 'https://api.track.toggl.com/reports/api/v2/details'

    start_report_date, end_report_date = get_week_start_end()

    payload = {
        "user_agent": user_agent,
        "workspace_id": workspace_id,
        "display_hours": "minutes",
        "since": start_report_date,
        "until": end_report_date,
        "page": 1,
    }
    response = get(url, auth=(api_token, 'api_token'), params=payload).json()
    time_entries = response.get('data')

    # If there are more entries than the page size, get the next page
    num_entries = response.get('total_count', 0)
    entries_per_page = response.get('per_page', 0)
    while (num_entries > entries_per_page):
        payload['page'] += 1
        response = get(url, auth=(api_token, 'api_token'), params=payload).json()
        time_entries += response.get('data')
        num_entries -= entries_per_page

    # If there is an error, raise an exception
    if response.get('error'):
        log.error(f'Error with the Toggl API. Message: {response.get("error").get("message")}, \
                Tip: {response.get("error").get("tip")}, Code: {response.get("error").get("code")}')
        raise Exception('Error returned from Toggl')

    log.debug(f'Toggl report: {time_entries}')

    return time_entries


def get_sgu_dict(data, username: str) -> dict:
    """
    """
    entries = []
    for entry in data:
        if len(entry['tags']):
            categ = entry['tags'][0]
        else:
            categ = ''

        entries.append({
            'DATA': datetime.strptime(entry['start'],
                                    "%Y-%m-%dT%H:%M:%S-03:00").strftime("%d/%m/%Y"),
            'PROJETO': entry['project'],
            'CATEGORIA': categ,
            'ATIVIDADE': entry['description'][:50],
            'OPORTUNIDADE': '',
            'HORAS': str(float(entry['dur'])/3600000).replace('.', ','),
            'USERNAME': username
        })

    log.debug(f'Sgu entries: {entries}')

    return entries


def sgu_dict_to_csv(data: dict, filename: str) -> None:
    """
    """
    DataFrame.from_dict(data).to_csv(filename, index=False, encoding='ansi', sep=';')
    return None


def get_workspace_id(api_token: str):
    """
    """
    url = 'https://api.track.toggl.com/api/v8/workspaces'
    response = get(url, auth=(api_token, 'api_token'))

    try:
        retval = response.json()
    except Exception:
        log.error(f'Invalid response from Toggl: {response}')
        raise Exception('Invalid response from Toggl')

    log.debug(f'Workspace ids: {retval}')

    return retval


def print_csv_report(email: str,
                    workspace_id: str,
                    api_token: str,
                    sgu_username: str,
                    output_file_name: str) -> None:
    """
    """
    try:
        report = get_report(
                user_agent=email,
                workspace_id=workspace_id,
                api_token=api_token)
    except Exception as exc:
        raise exc

    entries = get_sgu_dict(report, sgu_username)

    sgu_dict_to_csv(data=entries, filename=output_file_name+'.csv')

    return None


def get_config(filename: str) -> dict:
    """
    """
    log.debug(f'Filename: {filename}')
    if filename.endswith('.yaml'):
        try:
            with open(filename, 'r') as yaml_file:
                contents = safe_load(yaml_file)
                log.debug(f'Yaml file contents: {contents}')
                return contents
        except YAMLError as exc:
            raise exc
    else:
        raise Exception('Invalid file extension')
