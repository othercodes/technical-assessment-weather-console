from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique


@unique
class TemperatureUnit(Enum):
    CELSIUS = 'C'
    FAHRENHEIT = 'F'

    def __str__(self) -> str:
        return self.value


@dataclass
class Temperature:
    value: float
    unit: TemperatureUnit

    def to_fahrenheit(self) -> Temperature:
        if self.unit == TemperatureUnit.FAHRENHEIT:
            return self
        return Temperature((self.value * 9 / 5) + 32, TemperatureUnit.FAHRENHEIT)

    def to_celsius(self) -> Temperature:
        if self.unit == TemperatureUnit.CELSIUS:
            return self
        return Temperature((self.value - 32) * 5 / 9, TemperatureUnit.CELSIUS)

    def __str__(self) -> str:
        return f"{self.value} º{self.unit}"


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
