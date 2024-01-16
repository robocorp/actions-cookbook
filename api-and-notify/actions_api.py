from robocorp.actions import action
from datetime import datetime, timedelta
import requests
from typing import Dict, List


@action(is_consequential=True)
def get_porssisahko(hours: int = 8) -> str:
    """
    Get the electricity prices for next 8 hours from api.porssisahko.net

    Returned string prices in the following format:
        - HH:MM - PRICE snt/kWh

    :param message: message to send
    :param channel: channel to send message to
    :return: dictionary containing results from API

    """
    response = requests.get("https://api.porssisahko.net/v1/latest-prices.json")
    prices = get_next_prices(response.json(), hours)
    return format_prices_hours_to_string(prices)


def format_prices_hours_to_string(prices_hours: List) -> str:
    formatted_string = ""
    for price, hour in prices_hours:
        formatted_string += f"{hour} - {price} snt/kWh\n"

    return formatted_string.strip()


def get_next_prices(data: Dict, hours: int) -> List:
    time_now = datetime.utcnow()
    start_date_str = time_now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+00:00"
    prices_list = data["prices"]
    prices_list.reverse()

    # Convert start date string to datetime object
    start_date = datetime.fromisoformat(start_date_str)

    # Calculate X hours ahead of the start date
    end_date = start_date + timedelta(hours=hours)

    # Filter and get prices along with hours and minutes
    hours_data = []
    for entry in prices_list:
        entry_start_date = datetime.fromisoformat(
            entry["startDate"].replace("Z", "+00:00")
        )
        if start_date <= entry_start_date < end_date:
            hour_minute = entry_start_date.strftime("%H:%M")
            hours_data.append((entry["price"], hour_minute))

    return hours_data
