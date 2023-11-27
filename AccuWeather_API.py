import requests, json
    
class AccuWeather:

    def __init__(self):

        self.__url = "http://dataservice.accuweather.com/forecasts/v1/"

        self.__params = {
            "apikey": "QCYMQo2bDa4bnYRPvHrKckUQUY37JAKL",
            "language": "pt-pt",
            "details": True
        }

        

    def getWeather(self, endpoint = "daily/5day/", location_key = "272831", offset_day = 1):

        weather = requests.post(self.__url + endpoint + location_key, params= self.__params,)

        if(weather.status_code != 200):

            return None

        weather = weather.json()

        if(offset_day < 0 or offset_day > 4):

            return None
        
        else:

            weather = weather["DailyForecasts"][offset_day]
            return weather
        
    def getRainProbability(self, offset_day = 1, part_of_day = "Day"):

        weather = self.getWeather(offset_day=offset_day)

        if(weather):

            return int(weather[part_of_day]["RainProbability"])
        
        else:

            return weather

        

#inicialização da API
# api = AccuWeather()

#obter o tempo para o dia de amanha
#print(api.getWeather(offset_day=1))

#obter a probabilidade de chuva em percentagem para a parte da noite de amanhã
# print(api.getRainProbability(part_of_day="Night"))