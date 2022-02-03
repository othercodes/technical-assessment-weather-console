from typing import Iterable

import pytest

from weather.weather_data.application.services import WeatherFinder
from weather.weather_data.domain.exceptions import WeatherDataNotFound
from weather.weather_data.domain.models import Location, WeatherData


def test_finder_should_get_current_weather_info_by_location(weather_data_factory, weather_data_service):
    def current(location: Location) -> WeatherData:
        return weather_data_factory(location.city, location.country)

    service = weather_data_service(
        on_current=current,
        on_forecast=lambda location, days: [],
    )

    finder = WeatherFinder(service)
    weather = finder.current(Location('Santander', 'ES'))

    assert isinstance(weather, WeatherData)


def test_finder_should_not_get_current_weather_info_by_location(weather_data_factory, weather_data_service):
    service = weather_data_service(
        on_current=lambda location: None,
        on_forecast=lambda location, days: [],
    )

    finder = WeatherFinder(service)

    with pytest.raises(WeatherDataNotFound):
        finder.current(Location('Santander', 'ES'))


def test_finder_should_get_forecast_by_location_for_given_number_of_days(weather_data_factory, weather_data_service):
    def forecast(location: Location, days: int) -> Iterable[WeatherData]:
        for _ in range(days):
            yield weather_data_factory(location.city, location.country)

    service = weather_data_service(
        on_current=lambda location: None,
        on_forecast=forecast,
    )

    finder = WeatherFinder(service)
    weather = finder.forecast(Location('Santander', 'ES'), 2)

    assert sum(1 for _ in weather) == 2
