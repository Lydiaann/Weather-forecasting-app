import requests
import tkinter as tk
import re
from decouple import config

IPBASE_API_KEY = 'ipb_live_tCrJj33dJCpG0vUClJDB47u5wwLGLLZLbYuvnHvg'
IPBASE_API_ENDPOINT = "https://api.ipbase.com/v2/info"

OPEN_WEATHER_MAP_API_KEY = '4c0bf727dcf19d000623c847178d9621'
OPEN_WEATHER_MAP_API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather'


IP_ADDRESS_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

def get_location_weather():
    query_params = {
        "apiKey": IPBASE_API_KEY
    }
    response = requests.get(IPBASE_API_ENDPOINT, params=query_params)
    city_name = response.json()["data"]["location"]["city"]["name"]

    weather_query_params = {
        'q': city_name,
        'appid': OPEN_WEATHER_MAP_API_KEY,
        'units': 'imperial'
    }
    response = requests.get(
        OPEN_WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
    weather_data = response.json()

    # Display weather data
    weather_label.config(
        text=f"{weather_data['name']}: {weather_data['main']['temp']}°F")
    #print(weather_label)
    
def get_weather():
    input_value = input_field.get()

    if IP_ADDRESS_REGEX.match(input_value):
        ipbase_query_params = {
            "apiKey": IPBASE_API_KEY,
            "ip": input_value
        }
        response = requests.get(IPBASE_API_ENDPOINT, params=ipbase_query_params)
        city_name = response.json()["data"]["location"]["city"]["name"]

        weather_query_params = {
            'q': city_name,
            'appid': OPEN_WEATHER_MAP_API_KEY,
            'units': 'imperial'
        }
        response = requests.get(
            OPEN_WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
        weather_data = response.json()

    else:
        # Try to get weather data directly using city name
        weather_query_params = {
            'q': input_value,
            'appid': OPEN_WEATHER_MAP_API_KEY,
            'units': 'imperial'
        }
        response = requests.get(OPEN_WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
        weather_data = response.json()

    # Display weather data
    weather_label.config(text=f"{weather_data['name']}: {weather_data['main']['temp']}°F")

################################################################################################################################
# #the GUI:
root = tk.Tk()
root.title('Weather Forecasting App') #title of window
root.geometry('400x200')  #creates the window size

input_label = tk.Label(root, text='Enter city or IP address:')
input_label.pack()  #allows user to enter the city or IP

input_field = tk.Entry(root)
input_field.pack()

submit_button = tk.Button(root, text='Get Weather', command=get_weather)
submit_button.pack() #retrieces the weather information using the entered value

location_button = tk.Button(root, text='Use Current Location', command=get_location_weather)
location_button.pack() # retrieves the weater for current location

weather_label = tk.Label(root, text='')
weather_label.pack() #displays the retrieved weather info

root.mainloop()


#############################################################################################################################

#gets the location:

api_key = 'ipb_live_tCrJj33dJCpG0vUClJDB47u5wwLGLLZLbYuvnHvg'
ip_address = ''

api_endpoint = 'https://api.ipbase.com/v2/info'
query_params = {'apiKey' : api_key} #stores the API key and optinally the IP address to query
if ip_address:
    query_params['ip'] = ip_address

response = requests.get(api_endpoint, params=query_params) #request.get() method sends a GET request to the API endpoint with the api_endpoint URL
#response from API is stored in the 'response' variable

if response.status_code == 200:
    data = response.json()
    #handle response data
    try:
        location_data = data['data']['location'] #pulls the info from json file to give the city name and prints the city name
        city_name = location_data['city']['name']
        print(city_name)
    except KeyError as e:
        print (f'Error: {e}')

else:
    #handle errors
    print(f'Error: {response.status_code} - {response.text}')

###############################################################################################################################

#gets the temp:
api_key = '4c0bf727dcf19d000623c847178d9621'
city_name = ''

api_endpoint = 'https://api.openweathermap.org/data/2.5/weather'
query_params = {'q': city_name, 'appid': api_key, 'units': 'imperial'}

response = requests.get(api_endpoint, params=query_params)

if response.status_code == 200:
    data = response.json()
    #handle response data
    temperature = data['main']['temp']
    print(f'{temperature}°F')
else:
    #handle error
    print(f'Error: {response.status_code} - {response.text}')


