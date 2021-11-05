from requests import get
from pandas import DataFrame
from datetime import datetime, timedelta
import importlib


def new_func():
    if importlib.util.find_spec("config"):
        import config
        return config
    else:
        print(f'No config file.')
        exit()

def get_week_start_end(format="%Y-%m-%d") -> tuple[str,str]:
    """
    Get this weeks start and end date.
    """
    dt = datetime.today()
    start_report_date = dt - timedelta(days=dt.weekday())
    end_report_date = start_report_date + timedelta(days=6)
    return start_report_date.strftime(format), end_report_date.strftime(format)

def get_report(api_token, user_agent, workspace_id, url='https://api.track.toggl.com/reports/api/v2/details') -> dict:
    start_report_date, end_report_date = get_week_start_end()
    payload = {
        "user_agent": user_agent,
        "workspace_id": workspace_id,
        "display_hours": "minutes",
        "since": start_report_date,
        "until": end_report_date
    }
    return get(url, auth=(api_token, 'api_token'), params=payload).json()['data']

def get_sgu_dict(data, username):
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

def sgu_dict_to_csv(data, filename):
    DataFrame.from_dict(data).to_csv(filename, index=False, encoding='ansi', sep=';')

def get_workspace_ids(api_token: str):
    return get('https://api.track.toggl.com/api/v8/workspaces', auth=(api_token, 'api_token')).json()

def print_csv_report(email: str, workspace_id: str, api_token: str, sgu_username: str, output_file_name: str) -> None:
    r = get_report(
        user_agent=email,
        workspace_id=workspace_id,
        api_token=api_token)

    entries = get_sgu_dict(r, sgu_username)

    sgu_dict_to_csv(data=entries, filename=output_file_name+'.csv')

    return None

def main() -> None:
    config = new_func()

    # print(get_workspace_ids(
    #     api_token=config.API_TOKEN))

    print_csv_report(email=config.EMAIL,
        workspace_id=config.WORKSPACE_ID,
        api_token=config.API_TOKEN,
        sgu_username=config.SGU_USERNAME,
        output_file_name='test')
    
    return None

if __name__ == '__main__':
    main()