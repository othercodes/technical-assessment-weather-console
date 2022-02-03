from datetime import datetime
from typing import Callable, Iterable, Optional
from unittest.mock import patch

import pytest

from weather.weather_data.domain.models import Location, WeatherData, TemperatureUnit, Temperature


@pytest.fixture
def weather_data_service():
    def _make_service(
            on_current: Callable[[Location], WeatherData],
            on_forecast: Callable[[Location, int], Iterable[WeatherData]],
    ):
        with patch('weather.weather_data.domain.contracts.WeatherService') as mock:
            service = mock.return_value
            service.current = on_current
            service.forecast = on_forecast

        return service

    return _make_service


@pytest.fixture()
def weather_data_factory():
    def _make_model(
            city: Optional[str] = None,
            country: Optional[str] = None,
            date: Optional[datetime] = None,
            description: Optional[str] = None,
            temperature: Optional[float] = None,
            unit: Optional[str] = None,
    ):
        return WeatherData(
            location=Location(
                city if city else 'Santander',
                country if country else 'ES',
            ),
            date=date if date else datetime.now,
            description=description if description else 'Cloudy',
            temperature=Temperature(
                temperature if temperature else 17.2,
                TemperatureUnit(unit) if unit else TemperatureUnit.CELSIUS
            )

        )

    return _make_model
