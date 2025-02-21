import polars as pl
import datetime
import numpy as np
import os


class _Counter:
    HOLIDAY_PATH = (
        os.environ["onedrive"] + r"\Trading\files_static\dictionaries\holidays_b3.parquet"
    )

    def __init__(self):
        self.get_holidays()

    def get_holidays(self):
        holidays_b3 = pl.read_parquet(self.HOLIDAY_PATH)
        holidays_b3 = holidays_b3.select(pl.col("Data").cast(pl.Utf8))
        self.holidays_numpy = holidays_b3[:, 0].to_numpy()
        self.holidays_numpy=np.array(self.holidays_numpy, dtype='datetime64[D]')

    def count_days_class(self, start, end, business_days=True):
        start_string = self.test_date(start)
        end_string = self.test_date(end)
        if business_days:
            valid_days = "Mon Tue Wed Thu Fri"
            return np.busday_count(
                start_string,
                end_string,
                holidays=self.holidays_numpy,
                weekmask=valid_days,
            )
        else:
            valid_days = "Mon Tue Wed Thu Fri Sat Sun"
            return np.busday_count(start_string, end_string)

    def test_date(self, date):
        if type(date) == datetime.datetime:
            return date.strftime("%Y-%m-%d")
        elif type(date) == str:
            if int(date[2:4]) < 0 or int(date[2:4]) > 12:
                raise Personal_exception(
                    "Data em formato errado, deve ser: " + "ddmmyy"
                )
            date = datetime.datetime.strptime(date, "%d%m%y").strftime("%Y-%m-%d")
            return date
        else:
            raise Personal_exception(
                "Tentou obter dias úteis sem ser por string ou datetime"
            )

    def get_last_business_day(self, date=None):
        if not date:
            date = datetime.date.today()
        else:
            date = self.test_date(date)
        last_business_day = np.busday_offset(date, -1, holidays=self.holidays_numpy)
        last_business_day = last_business_day.item()
        last_business_day = datetime.datetime(
            last_business_day.year, last_business_day.month, last_business_day.day
        )
        return last_business_day

    def get_next_business_day(self, date=None, days=None):
        if not days:
            days = 1
        if not date:
            date = datetime.date.today()
        else:
            date = self.test_date(date)
        next_business_day = np.busday_offset(date, days, roll='backward', holidays=self.holidays_numpy)
        next_business_day = next_business_day.item()
        next_business_day = datetime.datetime(
            next_business_day.year, next_business_day.month, next_business_day.day
        )
        return next_business_day


class Personal_exception(Exception):
    def __init__(self, error_msg):
        print(error_msg)


def count_days(start: str|datetime.datetime, end: str|datetime.datetime = None, business_days=True):
    """Includes start date and excludes end date.
    If no specified end date, it will count from start date to today.
    Day format: ddmmyy"""
    if end is None:
        end = datetime.datetime.today()

    counter = _Counter()
    return counter.count_days_class(start, end, business_days)


def obtain_last_business_day(date=None):
    """Day format: ddmmyy"""
    return _Counter().get_last_business_day(date)


def obtain_next_business_day(date=None, days=None):
    """Day format: ddmmyy"""
    return _Counter().get_next_business_day(date,days)
