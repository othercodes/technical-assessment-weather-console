import os

from weather.shared.domain.contracts import Renderer
from weather.weather_data.application.services import WeatherFinder
from weather.weather_data.domain.contracts import WeatherService
from weather.weather_data.domain.models import Location
from weather.weather_data.infrastructure.accuweather import AccuWeather
from weather.weather_data.infrastructure.openweather import OpenWeather


def __make_service() -> WeatherService:
    engines = {
        'openweather': lambda: OpenWeather(
            api_url=os.getenv('OPENWEATHER_API_URL'),
            api_key=os.getenv('OPENWEATHER_API_KEY')
        ),
        'accuweather': lambda: AccuWeather(
            api_url=os.getenv('ACCUWEATHER_API_URL'),
            api_key=os.getenv('ACCUWEATHER_API_KEY')
        )
    }

    engine = engines.get(os.getenv('WEATHER_ENGINE'), None)
    if engine is None:
        raise ValueError('Invalid engine value, must be one of openweather or accuweather')

    return engine()


def current_command(renderer: Renderer, location: str, units: str):
    location = location.split(',', 2)
    if len(location) != 2:
        raise ValueError('Invalid argument location must be <city>,<country code>.')

    use_case = WeatherFinder(__make_service())
    weather = use_case.current(Location(*location))

    temp_conversion = {
        'metric': lambda temperature: temperature.to_celsius(),
        'imperial': lambda temperature: temperature.to_fahrenheit(),
    }
    temp_unit = temp_conversion.get(units)

    renderer.render("{city}({country})\n{date}\n> Weather: {description}\n> Temperature: {temperature}".format(
        city=weather.location.city,
        country=weather.location.country,
        date=weather.date.strftime('%b %m, %Y'),
        description=weather.description,
        temperature=temp_unit(weather.temperature)
    ))
