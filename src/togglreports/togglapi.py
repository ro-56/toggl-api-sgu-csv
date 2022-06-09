import logging as log
import requests as req

from togglreports import utils


def get_workspaces(api_token: str) -> list[dict]:
    """
    """
    url = 'https://api.track.toggl.com/api/v8/workspaces'
    response = req.get(url, auth=(api_token, 'api_token'))

    try:
        retval = response.json()
    except Exception:
        log.error(f'Invalid response from Toggl: {response}')
        raise Exception('Invalid response from Toggl')

    log.debug(f'Workspace ids: {retval}')

    return retval


def get_me(api_token: str) -> dict:
    """
    """
    url = 'https://api.track.toggl.com/api/v8/me'
    response = req.get(url, auth=(api_token, 'api_token'))

    try:
        retval = response.json()
    except Exception:
        log.error(f'Invalid response from Toggl: {response}')
        raise Exception('Invalid response from Toggl')

    log.debug(f'Me: {retval}')

    return retval


def get_detailed_report(api_token: str, workspace_id: int, user_agent: str = 'reportApi', **kwargs) -> dict:
    """
    options:
    {
        'user_agent': str,
        'period': str,
        'start': str,
    }
    """
    url = 'https://api.track.toggl.com/reports/api/v2/details'

    # Get report horizon
    start_report_date, end_report_date = utils.get_period_start_end(period=kwargs.get('period', None), start=kwargs.get('start', None))

    # Make request
    payload = {
        'workspace_id': workspace_id,
        "page": 1,
        "user_agent": user_agent,
        "since": start_report_date,
        "until": end_report_date,

    }
    payload = {key: value for key, value in payload.items() if value is not None}

    response = req.get(url, auth=(api_token, 'api_token'), params=payload).json()
    time_entries = response.get('data')

    # If there are more entries than the page size, get the next page
    num_entries = response.get('total_count', 0)
    entries_per_page = response.get('per_page', 0)
    while (num_entries > entries_per_page):
        payload['page'] += 1
        response = req.get(url, auth=(api_token, 'api_token'), params=payload).json()
        time_entries += response.get('data')
        num_entries -= entries_per_page

    # If there is an error, raise an exception
    if response.get('error'):
        log.error(f'Error with the Toggl API. Message: {response.get("error").get("message")}, \
                Tip: {response.get("error").get("tip")}, Code: {response.get("error").get("code")}')
        raise Exception('Error returned from Toggl')

    log.debug(f'Toggl report: {time_entries}')

    return time_entries


if __name__ == '__main__':
    get_detailed_report('', 1)
