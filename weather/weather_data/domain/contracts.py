from abc import abstractmethod, ABCMeta
from typing import Iterable, Optional

from weather.weather_data.domain.models import WeatherData, Location


class WeatherService(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def current(self, location: Location) -> Optional[WeatherData]:
        pass

    @abstractmethod
    def forecast(self, location: Location, days: int) -> Iterable[WeatherData]:
        pass
