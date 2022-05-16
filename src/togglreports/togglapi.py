import logging as log
from requests import get

def get_workspaces(api_token: str) -> list[dict]:
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


def get_me(api_token: str) -> dict:
    """
    """
    url = 'https://api.track.toggl.com/api/v8/me'
    response = get(url, auth=(api_token, 'api_token'))

    try:
        retval = response.json()
    except Exception:
        log.error(f'Invalid response from Toggl: {response}')
        raise Exception('Invalid response from Toggl')

    log.debug(f'Me: {retval}')

    return retval
