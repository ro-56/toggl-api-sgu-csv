#!/usr/bin/env python

from requests import get
from pandas import DataFrame
from datetime import datetime, timedelta
from yaml import safe_load, YAMLError

def get_week_start_end() -> tuple[str,str]:
    """
    Get this weeks start and end date.
    """
    format="%Y-%m-%d"
    dt = datetime.today()
    start_report_date = dt - timedelta(days=dt.weekday())
    end_report_date = start_report_date + timedelta(days=6)
    return start_report_date.strftime(format), end_report_date.strftime(format)

def get_report(api_token, user_agent, workspace_id) -> dict:
    url='https://api.track.toggl.com/reports/api/v2/details'

    start_report_date, end_report_date = get_week_start_end()

    payload = {
        "user_agent": user_agent,
        "workspace_id": workspace_id,
        "display_hours": "minutes",
        "since": start_report_date,
        "until": end_report_date
    }
    return get(url, auth=(api_token, 'api_token'), params=payload).json()['data']

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
        
    return entries

def sgu_dict_to_csv(data: dict, filename: str) -> None:
    DataFrame.from_dict(data).to_csv(filename, index=False, encoding='ansi', sep=';')
    return None

def get_workspace_id(api_token: str):
    url = 'https://api.track.toggl.com/api/v8/workspaces'
    return get(url, auth=(api_token, 'api_token')).json()

def print_csv_report(email: str, workspace_id: str, api_token: str, sgu_username: str, output_file_name: str) -> None:
    r = get_report(
        user_agent=email,
        workspace_id=workspace_id,
        api_token=api_token)

    entries = get_sgu_dict(r, sgu_username)

    sgu_dict_to_csv(data=entries, filename=output_file_name+'.csv')

    return None

def get_config(filename: str) -> dict:
    if filename.endswith('.yaml'):
        try:
            with open(filename, 'r') as yaml_file:
                return safe_load(yaml_file)
        except YAMLError as exc:
            raise exc
    else:
        raise Exception('Invalid file extension')
