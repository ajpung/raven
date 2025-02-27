import datetime
import dateparser


# Correct timezone to UTC
def correct_timezone(date_string):
    # If lacking tzinfo, assume UTC
    datetime_object = dateparser.parse(date_string)
    if datetime_object.tzinfo is None:
        datetime_object = datetime_object.replace(tzinfo=datetime.timezone.utc)
    # But if it has tzinfo, convert to UTC
    else:
        datetime_object = datetime_object.astimezone(datetime.timezone.utc)
    return datetime_object


# Convert timezone-aware datetime object to epoch
def datetime_to_epoch(datetime_object):
    return int(datetime_object.timestamp())
