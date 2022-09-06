import datetime as dt


PERIODS = ['thisweek', 'lastweek', 'thismonth', 'today']


def get_period_start_end(period: str = None, start: str = None, end: str = None, format: str = "%Y-%m-%d", reference: str = None) -> tuple[str, str]:
    """ Get datetime for start and end of a predetermined period.
    If no period is specified, get this weeks start and end date.
    """

    if period and (start or end):
        raise Exception("Conflicting arguments: period and start/end")

    if (start is None and end is not None):
        raise Exception("Got ending date without a start")

    try:
        _ = dt.datetime.today().strftime(format)
    except ValueError:
        raise ValueError("Incorrect data format")

    if reference is not None:
        try:
            reference_date = dt.datetime.strptime(reference, format)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    else:
        reference_date = dt.datetime.today()

    if (start is not None and end is None):
        try:
            start_report_date = dt.datetime.strptime(start, format)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        end_report_date = reference_date.replace(hour=23, minute=59, second=59)

    elif (start is not None and end is not None):
        try:
            start_report_date = dt.datetime.strptime(start, format)
            end_report_date = dt.datetime.strptime(end, format).replace(hour=23, minute=59, second=59)
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    else:
        if period not in PERIODS:
            period = 'thisweek'

        reference_weekday = reference_date.weekday()

        if period == 'thisweek':
            start_report_date = reference_date - dt.timedelta(days=reference_weekday)
            end_report_date = start_report_date + dt.timedelta(days=6)
        elif period == 'lastweek':
            start_report_date = reference_date - dt.timedelta(days=reference_weekday + 7)
            end_report_date = start_report_date + dt.timedelta(days=6)
        elif period == 'thismonth':
            start_report_date = reference_date.replace(day=1)
            end_report_date = get_last_day_of_month(start_report_date)
        elif period == 'today':
            start_report_date = reference_date.replace(hour=0, minute=0, second=0)
            end_report_date = reference_date.replace(hour=23, minute=59, second=59)

    return start_report_date.strftime(format), end_report_date.strftime(format)


def get_last_day_of_month(this_month: dt.datetime) -> dt.datetime:
    """ Get the last day of the month for any day. """
    next_month = this_month.replace(day=28) + dt.timedelta(days=4)
    last_day_date = next_month - dt.timedelta(days=next_month.day)
    return last_day_date
