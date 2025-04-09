"""
This file contains time-related functions.
"""

import pytz
from datetime import datetime, timedelta, time


def ist_to_utc(ist_time):
    """
    Convert IST (Indian Standard Time) to UTC (Coordinated Universal Time).
    Args:
        ist_time: datetime object representing time in IST.
    Returns:
        datetime object representing time in UTC.
    """
    try:
        ist_timezone = pytz.timezone("Asia/Kolkata")
        utc_timezone = pytz.timezone("UTC")
        return ist_timezone.localize(ist_time).astimezone(utc_timezone)
    except Exception as e:
        raise e.args[0]

def utc_to_ist(utc_time):
    """
    Convert UTC (Coordinated Universal Time) to IST (Indian Standard Time).
    Args:
        utc_time: datetime object representing time in UTC.
    Returns:
        datetime object representing time in IST.
    """
    try:
        utc_timezone = pytz.timezone("UTC")
        ist_timezone = pytz.timezone("Asia/Kolkata")
        return utc_timezone.localize(utc_time).astimezone(ist_timezone)
    except Exception as e:
        raise e.args[0]

def get_current_datetime_timezone(timezone: str, to_datetime: bool = True):
    """
    Get the current time in the specified timezone.
    Args:
        timezone (str): The timezone string (e.g., 'Asia/Kolkata', 'UTC').
        to_datetime (bool, optional): If True, return datetime object, else return date object. Default is True.
    Returns:
        datetime or date: Current datetime or date object in the specified timezone.
    """
    try:
        time_zone = pytz.timezone(timezone)
        current_time = datetime.now(time_zone)
        return current_time if to_datetime else current_time.date()
    except Exception as e:
        raise e.args[0]

def get_timezones() -> list:
    """
    Get a list of all available timezones.
    Returns:
        list: List of strings representing all available timezones.
    """
    try:
        return pytz.all_timezones
    except Exception as e:
        raise e.args[0]

def convert_datetime_to_unix_timestamp(datetime: datetime):
    """
    Convert a datetime object to a Unix timestamp.
    Args:
        dt: datetime object to be converted.
    Returns:
        int: Unix timestamp representing the given datetime.
    """
    try:
        return int(datetime.timestamp())
    except Exception as e:
        raise e.args[0]

def convert_unix_timestamp_to_datetime(timestamp):
    """
    Convert a Unix timestamp to a datetime object.
    Args:
        timestamp: Unix timestamp to be converted.
    Returns:
        datetime: Datetime object representing the given Unix timestamp.
    """
    try:
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        raise e.args[0]

def add_hours(time, hours):
    """
    Add a specified number of hours to a given time.
    Args:
        time: Time object to which hours will be added.
        hours: Number of hours to add.
    Returns:
        time: Updated time object.
    """
    return (datetime.combine(datetime.min, time) + timedelta(hours=hours)).time()

def add_minutes(time, minutes):
    """
    Add a specified number of minutes to a given time.
    Args:
        time: Time object to which minutes will be added.
        minutes: Number of minutes to add.
    Returns:
        time: Updated time object.
    """
    return (datetime.combine(datetime.min, time) + timedelta(minutes=minutes)).time()

def add_seconds(time, seconds):
    """
    Add a specified number of seconds to a given time.
    Args:
        time: Time object to which seconds will be added.
        seconds: Number of seconds to add.
    Returns:
        time: Updated time object.
    """
    return (datetime.combine(datetime.min, time) + timedelta(seconds=seconds)).time()

def format_time(time: time, format_str="%H:%M:%S"):
    """
    Format a time object into a string with the specified format.
    Args:
        time: Time object to be formatted.
        format_str (str): Format string to format the time. Default is '%H:%M:%S' (HH:MM:SS).
    Returns:
        str: Formatted time string.
    """
    return time.strftime(format_str)

def time_to_seconds(t: time):
    """
    Convert a time object to the total number of seconds.
    Args:
        t: Time object to be converted.
    Returns:
        int: Total number of seconds represented by the given time.
    """
    return t.hour * 3600 + t.minute * 60 + t.second

def seconds_to_time(seconds):
    """
    Convert the total number of seconds to a time object.
    Args:
        seconds: Total number of seconds to be converted.
    Returns:
        time: Time object representing the given total seconds.
    """
    return time(seconds // 3600, (seconds % 3600) // 60, seconds % 60)

def round_time(t: time):
    """
    Rounds a given time to the nearest minute.
    Args:
        t: Time object to be rounded.
    Returns:
        time: Rounded time object.
    """
    seconds = (t.minute * 60 + t.second + 30) // 60 * 60
    return t.replace(minute=seconds // 60, second=0)

def time_difference(start_time, end_time):
    try:
        """
        Calculates the difference between two time objects.
        Args:
            start_time: Start time.
            end_time: End time.
        Returns:
            timedelta: Time difference between start_time and end_time.
        """
        start_datetime = datetime.combine(datetime.min, start_time)
        end_datetime = datetime.combine(datetime.min, end_time)
        return end_datetime - start_datetime

    except Exception as e:
        raise e.args[0]

def is_time_between(time_to_check, start_time, end_time):
    """
    Checks if a given time falls within a specified time range.
    Args:
        time_to_check: Time to check.
        start_time: Start time of the range.
        end_time: End time of the range.
    Returns:
        bool: True if time_to_check is between start_time and end_time, False otherwise.
    """
    if start_time <= end_time:
        return start_time <= time_to_check <= end_time
    else:
        return start_time <= time_to_check or time_to_check <= end_time

def time_to_string(t: time, format_str="%H:%M:%S"):
    """
    Converts a time object to a string.
    Args:
        t: Time object to be converted.
        format_str (str): Format string to format the time. Default is '%H:%M:%S' (HH:MM:SS).
    Returns:
        str: Formatted time string.
    """
    return t.strftime(format_str)

def string_to_time(time_str, format_str="%H:%M:%S", to_time=True):
    """
    Converts a string to a time object.
    Args:
        time_str (str): Time string to be converted.
        format_str (str): Format string to parse the time. Default is '%H:%M:%S' (HH:MM:SS).
        to_time (bool): If True, return a time object. If False, return a datetime object.
    Returns:
        time | datetime: Time object if to_time is True, otherwise datetime object.
    """
    if to_time:
        return datetime.strptime(time_str, format_str).time()
    else:
        return datetime.strptime(time_str, format_str)

def is_time_relative(t: time, is_past: bool = False):
    """
    Checks if a given time is in the future or the past compared to the current time.
    Args:
        t: Time object to be checked.
        is_past (bool): If True, check if the time is in the past. If False, check if it's in the future. Default is False.

    Returns:
        bool: True if the time is in the specified direction (future or past), False otherwise.
    """
    current_time = datetime.now().time()
    return t < current_time if is_past else t > current_time

def get_time_zone_offset(timezone):
    """
    Retrieves the UTC offset for a specified timezone.
    Args:
        timezone (str): Timezone string (e.g., 'Asia/Kolkata').
    Returns:
        int: UTC offset in seconds.
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    return now.utcoffset().total_seconds()

def get_current_utc_time(to_datetime=False):
    """
    Retrieves the current time in UTC timezone.
    Returns:
        time: Current time in UTC.
    """
    if to_datetime:
        return datetime.utcnow()
    else:
        return datetime.utcnow().time()

def get_current_local_time(to_datetime=False):
    """
    Retrieves the current time in the local timezone.
    Returns:
        time: Current time in local timezone.
    """
    if to_datetime:
        return datetime.now()
    else:
        return datetime.now().time()

def delay(value: int = 1, unit: str = "minutes", to_datetime: bool = False):
    """
    Returns a timedelta or future datetime based on the provided delay.

    Args:
        value (int): The amount of time to delay.
        unit (str): The unit of time ('seconds', 'minutes', 'hours'). Default is 'minutes'.
        to_datetime (bool): If True, returns a future datetime. Otherwise, returns a timedelta.

    Returns:
        datetime | timedelta: Future datetime if `to_datetime=True`, otherwise a timedelta.

    Raises:
        ValueError: If an invalid unit is provided.
    """
    if unit not in ["seconds", "minutes", "hours"]:
        raise ValueError("Invalid unit. Choose from 'seconds', 'minutes', or 'hours'.")

    delta = timedelta(**{unit: value})

    return datetime.now() + delta if to_datetime else delta