import requests
    
class AccuWeather:

    def __init__(self):

        self.__url = "http://dataservice.accuweather.com/forecasts/v1/"

        self.__params = {
            "apikey": "QCYMQo2bDa4bnYRPvHrKckUQUY37JAKL",
            "language": "pt-pt",
            "details": True
        }

        

    def getWeather(self, endpoint = "daily/5day/", location_key = "272831"):
        
        response = requests.post(self.__url + endpoint + location_key, params= self.__params,)
        print(response.json())

api = AccuWeather()

api.getWeather()