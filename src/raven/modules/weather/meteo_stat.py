from datetime import datetime

from meteostat import Hourly  # type: ignore

from raven.core.date_time import datetime_window

current, early = datetime_window()

# Set time period
start = datetime(current.year, current.month, current.day, current.hour - 1)
end = start

# Get hourly data
data = Hourly("72219", start, end)
data = data.fetch()

print(data)
