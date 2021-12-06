import re
import time
from pyswip import Prolog
from api import get_data

def to_snake_case(string: str) -> str:
    string = string.lower().replace(' ', '_')
    string = re.sub(r'\W+', '', string)
    return string

def from_snake_case(string: str) -> str:
    return string.replace('_', ' ').title()

def kelvin_to_celsius(kelvins: float) -> float:
    return kelvins - 273.15

def prepare_facts(rules_filename='rules.pl') -> Prolog:
    p = Prolog()

    for city in get_data():
        name = to_snake_case(city['city']['name'])
        if not name.isalpha():
            continue
        max_temp = kelvin_to_celsius(city['main']['temp_min'])
        min_temp = kelvin_to_celsius(city['main']['temp_max'])
        humidity = city['main']['humidity']
        wind_speed = city['wind']['speed']
        clouds = city['clouds']['all']

        if max_temp < min_temp:
            max_temp, min_temp = min_temp, max_temp

        p.asserta(f'rango_temperatura({name}, {min_temp}, {max_temp})')
        p.asserta(f'humedad({name}, {humidity})')
        p.asserta(f'velocidad_viento({name}, {wind_speed})')
        p.asserta(f'clouds({name}, {clouds})')

        for clima in city['weather']:
            state = clima['main']

            if state == 'Rain':
                p.asserta(f'lloviendo({name})')
            if state == 'Snow':
                p.asserta(f'nevando({name})')
            if state == 'Clear':
                p.asserta(f'soleado({name})')

    p.consult(rules_filename)

    return p

def query_cities_with_weather(weather: str, p: Prolog) -> list[str]:
    result: list[str] = []

    try:
        for solution in p.query(f'{weather}(X)'):
            result.append(from_snake_case(solution['X']))
    except Exception as _:
        pass

    return list(set(result))

def custom_query(query: str, p: Prolog) -> list[str]:
    result: list[str] = []

    try:
        for solution in p.query(query):
            result.append(from_snake_case(solution['X']))
    except Exception as _:
        pass

    return list(set(result))
