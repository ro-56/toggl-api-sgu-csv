#!/usr/bin/env python

from requests import get
from pandas import DataFrame
from datetime import datetime, timedelta
from yaml import safe_load, YAMLError
from .. import config


def get_week_start_end() -> tuple[str , str]:
    """
    Get this weeks start and end date.
    """
    format="%Y-%m-%d"
    dt = datetime.today()
    start_report_date = dt - timedelta(days=dt.weekday())
    end_report_date = start_report_date + timedelta(days=6)

    start_report_date = start_report_date.strftime(format)
    end_report_date = end_report_date.strftime(format)
    
    print(f'[DEBUG] Start report date: {start_report_date} | End report date: {end_report_date}') if config.__DEBUG__ else None
    
    return start_report_date, end_report_date

def get_report(api_token, user_agent, workspace_id) -> dict:
    url = 'https://api.track.toggl.com/reports/api/v2/details'

    start_report_date, end_report_date = get_week_start_end()

    payload = {
        "user_agent": user_agent,
        "workspace_id": workspace_id,
        "display_hours": "minutes",
        "since": start_report_date,
        "until": end_report_date
    }
    response = get(url, auth=(api_token, 'api_token'), params=payload).json()
    retval = response.get('data')

    if response.get('error'):
        print(f'[ERROR] Error with the Toggl API. Message: {response.get("error").get("message")}, \
            Tip: {response.get("error").get("tip")}, Code: {response.get("error").get("code")}') if config.__DEBUG__ else None
        raise Exception('Error returned from Toggl')

    print(f'[DEBUG] Toggl report: {retval}') if config.__DEBUG__ else None

    return retval


def get_sgu_dict(data, username: str) -> dict:
    entries = []
    for entry in data:
        if len(entry['tags']):
            categ = entry['tags'][0]
        else:
            categ = ''

        entries.append({
            'DATA': datetime.strptime(entry['start'], "%Y-%m-%dT%H:%M:%S-03:00").strftime("%d/%m/%Y"),
            'PROJETO': entry['project'],
            'CATEGORIA': categ,
            'ATIVIDADE': entry['description'][:50],
            'OPORTUNIDADE': '',
            'HORAS': str(float(entry['dur'])/3600000).replace('.', ','),
            'USERNAME': username
        })

    print(f'[DEBUG] sgu entries: {entries}') if config.__DEBUG__ else None

    return entries


def sgu_dict_to_csv(data: dict, filename: str) -> None:
    DataFrame.from_dict(data).to_csv(filename, index=False, encoding='ansi', sep=';')
    return None


def get_workspace_id(api_token: str):
    url = 'https://api.track.toggl.com/api/v8/workspaces'
    response = get(url, auth=(api_token, 'api_token'))

    try:
        retval = response.json()
    except:
        print(f'[ERROR] Invalid response from Toggl: {response}') if config.__DEBUG__ else None
        raise Exception('Invalid response from Toggl')

    print(f'[DEBUG] workspace ids: {retval}') if config.__DEBUG__ else None

    return retval


def print_csv_report(email: str, workspace_id: str, api_token: str, sgu_username: str, output_file_name: str) -> None:
    try:
        r = get_report(
            user_agent=email,
            workspace_id=workspace_id,
            api_token=api_token)
    except Exception as e:
        raise e

    entries = get_sgu_dict(r, sgu_username)

    sgu_dict_to_csv(data=entries, filename=output_file_name+'.csv')

    return None


def get_config(filename: str) -> dict:
    print(f'[DEBUG] Filename: {filename}') if config.__DEBUG__ else None
    if filename.endswith('.yaml'):
        try:
            with open(filename, 'r') as yaml_file:
                contents = safe_load(yaml_file)

                print(f'[DEBUG] yaml file contents: {contents}') if config.__DEBUG__ else None

                return contents
        except YAMLError as exc:
            raise exc
    else:
        raise Exception('Invalid file extension')
