# pi_statusdisplay

Small Python status script, which displays information on a 2.7" OLED.

## Getting Started

These instruction will help you to run my pi_statusdisplay script. It shows a clock, the weather for two cities, storm warnings (for Germany), PiHole status, a public transport timetable (for German stations) and information about your Pi like temperature or IP-address.  
  
**Important:**
This script is built for my SSD1325 OLED. Thanks to luma.oled it *may* work out-of-the-box on other displays, but don't expect too much. I'm working on making it more customizable and working on different screens but at the moment you probably have to tweak a few things in the code, to make it do what you want to.


### Prerequisites

* Python3
* A Wired up OLED working with [luma.oled](https://github.com/rm-hull/luma.oled)  
> If you want to make sure your display is working, use [luma.examples](https://github.com/rm-hull/luma.examples) and run some example scripts.



### Installing

1. Clone this repository on your Pi
2. Download the fonts from [luma.examples](https://github.com/rm-hull/luma.examples) and put them in a folder named **fonts**
3. Download the [FontAwesome](https://fontawesome.com/) - Solid as **fa-solid.ttf** and also put it into the fonts folder.
   
   
## Configuring

There are several things that can (and have to) be customized.

### Weather

```python
####CONFIG####

#Weather API
CITY1='#######' #City1-ID
CITY2='#######' #City2-ID
API_KEY='YOURKEY'#OpenWeatherMap API-Key

#Storm API
LOCATION_ID = '#######'#Location id from dwd.de for storm warnings

##############
```

* Open **getWeather.py** and enter city-IDs for the cities you want to get weather data for
* Enter your OpenWeatherMap API-Key
* Enter your Location ID from dwd.de 
(This works only for Germany! Unfortunately the API is not documented. You can only get the ID if your district has an active warning right now)
* If you want to have the weather in other languages or units, just change the "weather_url" query to your liking.

<br>

```python
        #Wetter CITY1
        name1 = oled.center("CITY1")#CHANGE ME
        [...]
        #Wetter CITY2
        name2 = oled.center("CITY2")#CHANGE ME
```

Change the two city names in **main.py** inside of the weather function.


> For information regarding the city-IDs and the query parameters, see the [OpenWeatherMap-API Documentation](https://openweathermap.org/current).
   
   
### PiHole

```python
ip = 'CHANGE ME' #PiHole IP
```

Change the IP-address from your PiHole in **pihole.py**.
  
  
### Timetable

This only works for German stations!
```python
    ####CONFIG####

    STATION='Koeln Hbf'

    ##############
```

Change the station name in **timetable.py** to your liking.

```python
haltestelle = "Köln Hbf"
```
Change it in **main.py** inside of the timetable function aswell.

## Running

To run simply start the **main.py** with Python3 and the configuration for your display.   
For example an ssd1325 display:   
```
python3 main.py -f path/to/your/ssd1325.conf
```

For new weather data, the **getWeather.py** has to be run. For automatic weather updates, create a cronjob which runs the script periodically. Just be careful you don't hit the quota for the OpenWeatherMap-API.

## Author

* **Dominik Bieber** - [d-bieber](https://github.com/d-bieber)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Thanks to

* [luma.oled](https://github.com/rm-hull/luma.oled)
* [finalrewind.org](https://finalrewind.org/)
