from togglreports.core import report_factory
from togglreports import togglapi
from togglreports import config as cfg


def build_report(report_type: str, **kwargs):
    """ Build the report """
    data = get_report_data(**kwargs)
    config = cfg.get_report_config(report_type)
    base_config = cfg.get_config_section('reports')
    report_factory.create_report(report_type, data=data, config=config, base_config=base_config)


def get_report_data(**kwargs):
    """ Get the report data """
    api_token = cfg.get_config_value('toggl.user', 'api_token')
    workspace_id = cfg.get_config_value('toggl.workspace', 'id')

    data = togglapi.get_detailed_report(api_token=api_token, workspace_id=workspace_id, **kwargs)
    return data
