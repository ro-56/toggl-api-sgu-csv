import datetime as dt


PERIODS = ['thisweek', 'lastweek', 'thismonth']


def get_period_start_end(period: str = '', format: str = "%Y-%m-%d") -> tuple[str, str]:
    """ Get datetime for start and end of a predetermined period. 
    If no period is specified, get this weeks start and end date.
    """
    if period not in PERIODS:
        period = 'thisweek'

    date_today = dt.datetime.today()
    today_weekday = date_today.weekday()

    if period == 'thisweek':
        start_report_date = date_today - dt.timedelta(days=today_weekday)
        end_report_date = start_report_date + dt.timedelta(days=6)
    elif period == 'lastweek':
        start_report_date = date_today - dt.timedelta(days=today_weekday + 7)
        end_report_date = start_report_date + dt.timedelta(days=6)
    elif period == 'thismonth':
        start_report_date = date_today.replace(day=1)
        end_report_date = get_last_day_of_month(start_report_date)

    return start_report_date.strftime(format), end_report_date.strftime(format)


def get_last_day_of_month(this_month: dt.datetime) -> dt.datetime:
    """ Get the last day of the month for any day. """
    next_month = this_month.replace(day=28) + dt.timedelta(days=4)
    last_day_date = next_month - dt.timedelta(days=next_month.day)
    return last_day_date
