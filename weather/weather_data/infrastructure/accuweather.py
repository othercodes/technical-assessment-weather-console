from datetime import datetime
from typing import Iterable, Optional

import requests

from weather.shared.domain.exceptions import WeatherException
from weather.weather_data.domain.contracts import WeatherService
from weather.weather_data.domain.models import Location, WeatherData, Temperature, TemperatureUnit


class AccuWeather(WeatherService):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key

    def _get_location_key(self, location: Location) -> str:
        response = requests.get(f'{self.api_url}/locations/v1/{location.country}/search', params={
            'apikey': self.api_key,
            'q': location.city
        })
        content = response.json()

        if response.status_code != 200:
            raise WeatherException(f"{content['Message']}", content['Code'], {
                'reference': content['Reference']
            })

        if not content:
            raise WeatherException('Unable to find the location')

        return content[0]['Key']

    def current(self, location: Location) -> Optional[WeatherData]:
        location_key = self._get_location_key(location)

        response = requests.get(f'{self.api_url}/currentconditions/v1/{location_key}', params={
            'apikey': self.api_key,
        })

        content = response.json()

        return WeatherData(
            location=location,
            date=datetime.strptime(content[0]['LocalObservationDateTime'], "%Y-%m-%dT%H:%M:%S%z"),
            description=content[0]['WeatherText'],
            temperature=Temperature(
                value=content[0]['Temperature']['Metric']['Value'],
                unit=TemperatureUnit.CELSIUS
            ),
        )

    def forecast(self, location: Location, days: int) -> Iterable[WeatherData]:
        location_key = self._get_location_key(location)

        response = requests.get(f'{self.api_url}/forecasts/v1/daily/5day/{location_key}', params={
            'apikey': self.api_key,
            'metric': True
        })

        content = response.json()

        weather = []
        for data in content.get('DailyForecasts', []):
            weather.append(WeatherData(
                location=location,
                date=datetime.strptime(data['Date'], "%Y-%m-%dT%H:%M:%S%z"),
                description=data['Day']['IconPhrase'],
                temperature=Temperature(
                    value=data['Temperature']['Minimum']['Value'],
                    unit=TemperatureUnit.CELSIUS
                ),
            ))
        return weather[:int(days)]
