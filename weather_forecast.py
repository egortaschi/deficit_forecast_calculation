import requests
import os
from dotenv import load_dotenv

load_dotenv()

# connecting to the weather API
url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

querystring = {"q": "Saransk", "days": "3"}

headers = {
    'x-rapidapi-key': os.getenv("TOKEN"),
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
temperature_data = response.json()


def make_temperature_list_x1():
    """function for creating a dictionary, where
    the keys are the hours of the day, and
    the values are the temperature values
    obtained using the API (day x-1 (tomorrow))"""

    temp_list_x1 = temperature_data['forecast']['forecastday'][1]['hour']
    n = 1  # create a keys for dict, which will be a hours (1-24)
    h = 0  # create an index for temp_list1
    dict_temp_x1 = {}
    for i in range(24):
        dict_temp_x1[n] = temp_list_x1[h]['temp_c']
        n += 1
        h += 1
    round_temp_dict_x1 = {k: round(v) for k, v in dict_temp_x1.items()}
    return round_temp_dict_x1


def make_temperature_list_x2():
    """function for creating a dictionary, where
    the keys are the hours of the day, and
    the values are the temperature values
    obtained using the API (day x-2 (day after tomorrow))"""

    temp_list_x2 = temperature_data['forecast']['forecastday'][2]['hour']
    n = 1  # create a keys for dict, which will be a hours (1-24)
    h = 0  # create an index for temp_list2
    dict_temp_2 = {}
    for i in range(24):
        dict_temp_2[n] = temp_list_x2[h]['temp_c']
        n += 1
        h += 1
    round_temp_dict_x2 = {k: round(v) for k, v in dict_temp_2.items()}
    return round_temp_dict_x2


if __name__ == "__main__":
    make_temperature_list_x1()
    make_temperature_list_x2()
