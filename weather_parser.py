import requests
from bs4 import BeautifulSoup as BS


def weather_on_hours():
    temp_inhours = []
    template_text = ['', '  ', ', ощущается как ']
    temp_text = ''

    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080',
    }

    url = 'https://world-weather.ru/pogoda/russia/yekaterinburg/24hours/'
    response = requests.get(url, proxies=proxies)
    html = BS(response.content, 'html.parser')


    for el in html.select('tr.day'):
        time = el.select('.weather-day')[0].text
        temp = el.select('.weather-temperature')[0].text
        temp_feeling = el.select('.weather-feeling')[0].text
        temp_inhours.append([time, temp, temp_feeling])

    for i in range(0, 6):
        for j in range(0, 3):
            temp_text += (template_text[j] + temp_inhours[i][j])
        temp_text += '\n'
        temp_text += '\n'

    return temp_text


def weather_on_week():
    temp_onweek = []
    template_text = ['','\n🌑', '  ', ', ощущается как ', '\n🌞', '  ', ', ощущается как ']
    temp_text = ''

    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080',
    }

    url = 'https://world-weather.ru/pogoda/russia/yekaterinburg/7days/'
    response = requests.get(url, proxies=proxies)
    html = BS(response.content, 'html.parser')


    for el in html.select('div.weather-short'):
        date = el.select('div.dates')[0].text
        night = el.select('.night .weather-day')[0].text
        temp_night = el.select('.night .weather-temperature')[0].text
        temp_feeling_night = el.select('.night .weather-feeling')[0].text
        day = el.select('.day .weather-day')[0].text
        temp_day = el.select('.day .weather-temperature')[0].text
        temp_feeling_day = el.select('.day .weather-feeling')[0].text
        temp_onweek.append([date, night, temp_night, temp_feeling_night, day, temp_day, temp_feeling_day])

    for i in range(0, 7):
        for j in range(0, 7):
            temp_text += (template_text[j] + temp_onweek[i][j])
        temp_text += '\n'
        temp_text += '\n'

    return temp_text
