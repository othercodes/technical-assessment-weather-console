from datetime import datetime
from typing import Iterable, Optional

import requests

from weather.weather_data.domain.contracts import WeatherService
from weather.weather_data.domain.models import Location, WeatherData, Temperature, TemperatureUnit


class OpenWeather(WeatherService):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key

    def current(self, location: Location) -> Optional[WeatherData]:
        response = requests.get(f'{self.api_url}/data/2.5/weather', params={
            'appid': self.api_key,
            'q': location,
            'units': 'metric'
        })

        content = response.json()

        return WeatherData(
            location=location,
            date=datetime.fromtimestamp(content['dt']),
            description=content['weather'][0]['main'],
            temperature=Temperature(
                value=content['main']['temp'],
                unit=TemperatureUnit.CELSIUS
            ),
        )

    def forecast(self, location: Location, days: int) -> Iterable[WeatherData]:
        response = requests.get(f'{self.api_url}/data/2.5/forecast/daily', params={
            'appid': self.api_key,
            'q': location,
            'units': 'metric',
            'cnt': days,
        })

        content = response.json()

        weather = []
        for data in content.get('list', []):
            weather.append(WeatherData(
                location=location,
                date=datetime.fromtimestamp(data['dt']),
                description=data['weather'][0]['main'],
                temperature=Temperature(
                    value=data['temp']['day'],
                    unit=TemperatureUnit.CELSIUS
                ),
            ))

        return weather
