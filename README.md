# Technical Assessment - Weather Console

Implement a console-based weather viewer satisfying the scenarios below.

## Scenarios

**Get the current weather data for the given location.**

Arguments:

* Location, in "`{city},{country code}`" format.

Options:

* --units: Units of measurement must be `metric` or `imperial`, `metric` by default.

Example:
```bash
$ myweatherapp current Irvine,US --units=imperial
IRVINE (US)
Jan 31, 2022 
> Weather: Clear sky.
> Temperature: 48.72 ºF
```

**Get the weather forecast for max 5 days for the given location.**

Arguments:

* Location, in "`{city},{country code}`" format.

Options:

* --days: The number of days to retrieve forecast data for, `1` by default.
* --units: Units of measurement must be `metric` or `imperial`, `metric` by default.

Example:
```bash
$ myweatherapp forecast Santander,ES --days=3
SANTANDER (ES)
Feb 01, 2022 
> Weather: Clouds.
> Temperature: 11.1 ºC
Feb 02, 2022 
> Weather: Broken clouds.
> Temperature: 14 ºC
Feb 03, 2022 
> Weather: Sunny.
> Temperature: 16 ºC
```

## Details

* Use the language you feel more comfortable.
* The application must use the console for input and output.
* The application must have a small help message (just as normal console commands).
* You can name your application as you wish (in the examples above is "myweatherapp").
* You must use at least one of the following APIs to get the weather data (registration and usage is free).
    * https://developer.accuweather.com/apis
    * https://openweathermap.org/api
* Please follow best practices on storing your API Keys.
* Add instructions about how to run the application.

## What we are looking for:

* Don't use any framework, we want to see you code.
* Pay attention about how your code is organized.
* How you are reflecting the domain in the code.
* We love clean code.
* We love tests, 95% of coverage will be appreciated but not required.
* Logging support will be appreciated but not required.
