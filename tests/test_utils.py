import datetime as dt
import pytest

import src.togglreports.utils as tr_utils


class TestUtils:

    @pytest.mark.parametrize("date,days", [
        ((2022, 1, 28), 31),
        ((2022, 2, 15), 28),
        ((2020, 2, 3), 29),
    ])
    def test_get_last_day_of_month(self, date, days):
        date_today = dt.datetime(*date)
        last_day = tr_utils.get_last_day_of_month(date_today)
        assert last_day.day == days

    @pytest.mark.parametrize("period,start,format,reference,p_start_exp,P_end_exp", [
        ("thisweek", None, None, "2022-08-31", "2022-08-29", "2022-09-04"),
        (None, None, None, "2022-08-31", "2022-08-29", "2022-09-04"),
        ("thisweek", None, None, "2022-08-23", "2022-08-22", "2022-08-28"),
        (None, None, None, "2022-08-23", "2022-08-22", "2022-08-28"),
        ("lastweek", None, None, "2022-08-31", "2022-08-22", "2022-08-28"),
        ("thismonth", None, None, "2022-08-14", "2022-08-01", "2022-08-31"),
        ("today", None, None, "2022-08-23", "2022-08-23", "2022-08-23"),
        (None, "2022-08-04", None, "2022-08-23", "2022-08-04", "2022-08-23"),
        (None, "2022-04-15", None, "2022-07-04", "2022-04-15", "2022-07-04"),
        (None, "15/04/2022", "%d/%m/%Y", "04/07/2022", "15/04/2022", "04/07/2022"),
    ])
    def test_get_period_start_end(self, period, start, format, reference, p_start_exp, P_end_exp):
        kwargs = {
            "period": period,
            "start": start,
            "format": format,
            "reference": reference
        }

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        P_start, p_end = tr_utils.get_period_start_end(**kwargs)
        assert P_start == p_start_exp
        assert p_end == P_end_exp

    @pytest.mark.parametrize("format,reference", [
        ("%d-%g-%u", "2022-08-29"),
        ("%Y-%m-%d", "29/08/2022"),
        ("15/04/2022", "2022-08-29"),
    ])
    def test_get_period_start_end_invalid_format(self, format, reference):
        kwargs = {
            "format": format,
            "reference": reference,
        }

        with pytest.raises(ValueError):
            _, _ = tr_utils.get_period_start_end(**kwargs)

    def test_get_period_start_end_conflicting_args(self):
        with pytest.raises(Exception):
            _, _ = tr_utils.get_period_start_end(start="2022-01-01", period="thisweek")
