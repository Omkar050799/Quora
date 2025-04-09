""" imports """
from datetime import date, datetime, timedelta

""" functions """

def str_to_datetime(date_: str, to_datetime: bool = False) -> any:
    """
    Convert a string date to a datetime or date object.

    Args: 
        date_ (str): The input string date to be converted into date or datetime.
        to_datetime (bool, optional): Specify whether to convert date_str into a datetime or date object. Default is False.
    Returns:
        datetime | date : Returns a date or datetime object based on the to_datetime parameter (default is date).
        Returns None if conversion fails.
    """
    if not isinstance(date_, str):
        raise TypeError(f"Expected a str object but got {type(date_)}")
    try:
        return datetime.strptime(date_, '%Y-%m-%d %H:%M:%S') if to_datetime else datetime.strptime(date_, '%Y-%m-%d').date()
    except ValueError as e:
        return None

def datetime_to_str(date_, to_datetime: bool=False)-> str:
    """
    Convert a date or datetime object to a string.

    Args:
        date_ (date | datetime): The input date or datetime object to be converted into a string.
        to_datetime (bool, optional): Specify whether to convert 'date_' into a string representation of datetime.
            Default is False.
    Returns:
        str | None: Returns a string representation of the input date or datetime object based on the 'to_datetime' parameter.
            Returns None if conversion fails.
    """
    if not isinstance(date_, (datetime, date)):
        raise TypeError(f"Expected a datetime or date object but got {type(date_)}")
    try:
        return datetime.strftime(date_, '%Y-%m-%d %H:%M:%S') if to_datetime else datetime.strftime(date_, '%Y-%m-%d')
    except Exception as e:
        return None

def is_future_or_past_date(date_:any, is_future_date: bool=False, is_datetime: bool=False)-> bool:
    """
    Check if a given date is in the future or the past.

    Args:
        date_ (str | datetime | date): The input string, date, or datetime to check whether it is a future or past date.
        is_future_date (bool, optional): Specify whether to check for a future date. Default is False (check for a past date).
        is_datetime (bool, optional): Specify whether 'date_' is a datetime or date. Default is False.

    Returns:
        bool: True if the date is in the specified (future or past), False otherwise.
    """
    try:
        today = datetime.now()
        if is_future_date:
            if isinstance(date_, str):
                date_ = str_to_datetime(date_=date_, to_datetime=is_datetime)

            if is_datetime:
                return True if date_ >= today else False
            else:
                return True if date_ >= today.date() else False
        else:
            if isinstance(date_, str):
                date_ = str_to_datetime(date_=date_, to_datetime=is_datetime)

            if is_datetime:
                return True if date_ < today else False
            else:
                return True if date_ < today.date() else False
            
    except Exception as e:
        return e.args[0]

def get_date_difference(start_date: any, end_date: any) -> int:
    """
    Get the difference in days between two dates.

    Args:
        start_date (str | date | datetime): The start date.
        end_date (str | date | datetime): The end date.

    Returns:
        int: The absolute difference in days between the end date and start date.
    """
    try:
        if isinstance(start_date, str):
            start_date = str_to_datetime(start_date)

        if isinstance(end_date, str):
            end_date = str_to_datetime(end_date)

        return abs((end_date - start_date).days)

    except ValueError as e:
        raise e.args[0]

def extend_date(from_date: any = datetime.now(), extend_by_days: int = 1) -> any:
    """
    Extend the given date by the specified number of days.

    Args:
        from_date (str | date | datetime, optional): The date to extend. Defaults to the current date and time.
        extend_by_days (int, optional): How many days to extend. Defaults to 1.

    Returns:
        datetime | date: The extended date or datetime object.
    """
    try:
        if isinstance(from_date, str):
            from_date = str_to_datetime(date_=from_date)
        return from_date + timedelta(days=extend_by_days)
    except ValueError as e:
        raise e.args[0]

def is_start_date_greater_than_end_date(start_date:any, end_date:any) -> bool:
    """
    Compare two dates to ensure the start date is not greater than the end date.

    Args:
        start_date (str | date | datetime): The start date for comparison.
        end_date (str | date | datetime): The end date for comparison.

    Returns:
        bool: True if the start date is greater than the end date, False otherwise.
    """
    try:
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if isinstance(start_date, datetime):
            start_date = start_date.date()

        if isinstance(end_date, datetime):
            end_date = end_date.date()

        return start_date > end_date

    except ValueError as e:
        raise e.args[0]

def get_todays_date(is_datetime: bool=False, to_str:bool=False)-> any:
    """Returns the todays date | datetime"""
    try:
        if to_str:
            return datetime_to_str(datetime.now(), to_datetime=True) if is_datetime else datetime_to_str(datetime.now())
        else:
            return datetime.now() if is_datetime else datetime.now().date()
    except Exception as e:
        raise e.args[0]

def check_date_format(date_: any, is_datetime: bool = False) -> any:
    """
    To check if the date or datetime format is valid or not.
    Args:
        date_ (str | date | datetime, optional): The date to validate.
        is_datetime (boolean): Specify whether to convert 'date_' into a string representation of datetime.

    Returns:
        datetime | boolean: Return False if the date formay is corect else return error.
    """
    try:
        if isinstance(date_, str):
            _ = str_to_datetime(date_=date_, to_datetime=is_datetime)
        else:
            _ = date_ if not is_datetime else datetime.combine(date_, datetime.min.time())
        return False
    except ValueError as e:
        return f"Invalid date format of {date_}"

def date_to_datetime(date_: date) -> datetime:
    """
    Convert a date to a datetime.
    Args:
        date_: date to convert the date to datetime
    Returns:
        datetime: converted datetime from the given date
    """
    try:
        return datetime.combine(date_, datetime.min.time())
    except Exception as e:
        return f"Invalid date format of {date_}"

def calculate_age(birth_date) -> int:
    """
    Calculate the age based on the birth_date and the current date.

    Args:
        birth_date (str | date): The birth date.
    Returns:
        int: The age in years.
    """
    try:
        today = datetime.now().date()
        if isinstance(birth_date, str):
            birth_date: date = str_to_datetime(birth_date)

        delta = today - birth_date

        age = delta.days // 365
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    except Exception as e:
        return e.args[0]
