import datetime

from raven.core.date_time import correct_timezone
from raven.core.date_time import datetime_to_epoch


def test_dt_convert() -> None:
    date_string = "February 26, 2025, 12:00 PM"
    datetime_object = correct_timezone(date_string)
    assert datetime_object.tzinfo == datetime.timezone.utc
    assert datetime_object == datetime.datetime(
        2025, 2, 26, 12, 0, tzinfo=datetime.timezone.utc
    )
    date_string = "2025-02-26T12:00:0Z"
    datetime_object = correct_timezone(date_string)
    assert datetime_object.tzinfo == datetime.timezone.utc
    assert datetime_object == datetime.datetime(
        2025, 2, 26, 12, 0, tzinfo=datetime.timezone.utc
    )
    date_string = "February 26, 2025, 7:00AM EST"
    datetime_object = correct_timezone(date_string)
    assert datetime_object.tzinfo == datetime.timezone.utc
    assert datetime_object == datetime.datetime(
        2025, 2, 26, 12, 0, tzinfo=datetime.timezone.utc
    )


def test_calculate_utc() -> None:
    date_string = "February 26, 2025, 12:00 PM"
    datetime_object = correct_timezone(date_string)
    datetime_epoch = datetime_to_epoch(datetime_object)
    assert datetime_epoch == 1740571200
    date_string = "2025-02-26T12:00:0Z"
    datetime_object = correct_timezone(date_string)
    datetime_epoch = datetime_to_epoch(datetime_object)
    assert datetime_epoch == 1740571200
    date_string = "February 26, 2025, 7:00AM EST"
    datetime_object = correct_timezone(date_string)
    datetime_epoch = datetime_to_epoch(datetime_object)
    assert datetime_epoch == 1740571200
