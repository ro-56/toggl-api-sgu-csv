from configparser import ConfigParser

from togglreports.core import report_factory
from togglreports import togglapi
from togglreports import config as cfg


def build_report(report_type: str):
    """ Build the report """
    data = get_report_data()
    config = cfg.get_report_config(report_type)
    report_factory.create_report(report_type, data=data, config=config)


def get_report_data():
    """ Get the report data """
    api_token = cfg.get_config_value('toggl.user', 'api_token')
    workspace_id = cfg.get_config_value('toggl.workspace', 'id')

    data = togglapi.get_detailed_report(api_token=api_token, workspace_id=workspace_id)
    return data
