from typing import Iterable

from weather.weather_data.domain.contracts import WeatherService
from weather.weather_data.domain.exceptions import WeatherDataNotFound
from weather.weather_data.domain.models import Location, WeatherData


class WeatherFinder:
    def __init__(self, service: WeatherService):
        self.service = service

    def current(self, location: Location) -> WeatherData:
        weather = self.service.current(location)
        if weather is None:
            raise WeatherDataNotFound(f'Weather data for {location} not found.')

        return weather

    def forecast(self, location: Location, days: int = 1) -> Iterable[WeatherData]:
        return self.service.forecast(location, days)
