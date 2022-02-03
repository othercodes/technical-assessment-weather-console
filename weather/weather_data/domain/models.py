from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique


@unique
class TemperatureUnit(Enum):
    CELSIUS = 'C'
    FAHRENHEIT = 'F'


@dataclass
class Temperature:
    value: float
    unit: TemperatureUnit


@dataclass
class Location:
    city: str
    country: str

    def __str__(self):
        return f"{self.city}, {self.country}"


@dataclass
class WeatherData:
    location: Location
    date: datetime
    description: str
    temperature: Temperature
