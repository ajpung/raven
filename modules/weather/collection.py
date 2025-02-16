import requests

def collect_tomorrow(apikey):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location=toronto&apikey={apikey}"

    headers = {
        "accept": "application/json",
        "accept-encoding": "deflate, gzip, br"
    }

    response = requests.get(url, headers=headers)

    return response.json()