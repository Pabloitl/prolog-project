import curses

from pyswip import Prolog

import prolog

main_menu_options = [
    "Ver climas cálidos",
    "Ver climas templados",
    "Ver climas polares",
    "Ver climas tropicales",
    "Ver climas secos",
    "Ver climas moderados",
    "Tomar test"
]

def show_main_menu(screen, options: list[str]):
    y, x = screen.getmaxyx()
    max_len = max(list(map(len, options)))
    x = x // 2 - max_len
    y = (y - len(options)) // 2

    screen.clear()
    for i, option in enumerate(options):
        try:
            screen.addstr(y + i, x, f'{i} → {option}')
        except Exception as _:
            pass
    screen.refresh()
    return screen.getch()

def show_list(screen, cities: list[str]):
    if len(cities) == 0:
        screen.clear()
        screen.addstr(0, 0, 'No hay ciudades')
        screen.refresh()
        screen.getch()
        return

    rows, columns = screen.getmaxyx()

    screen.clear()
    acc = 0
    current_max = 0
    for i, city in enumerate(cities):
        y = i % rows

        current_max = max(current_max, len(city))

        try:
            if len(city) + acc >= columns:
                break
            screen.addstr(y, acc, city)
        except Exception as _:
            pass

        if y == rows - 1:
            acc += current_max + 1
            current_max = 0

    screen.refresh()
    screen.getch()

def run_test(screen) -> str:

    def ask_choice(screen, title: str, options: list[str], maps: dict[str, str], query: list[str]):
        y, x = screen.getmaxyx()
        x = x // 2
        y = (y - len(options) - 1) // 2
        choice = ord('r')
        while choice not in list(map(lambda x: ord(str(x)), range(len(options)))):
            screen.clear()
            screen.addstr(y, x - len(title) // 2, title)
            for i, msg in enumerate(options):
                screen.addstr(y + i + 1, x - (len(msg) + len(str(i)) + 3) // 2, f'{i} → {msg}')
            screen.refresh()
            choice = screen.getch()
        selected = options[choice - ord('0')]
        if selected not in maps:
            return
        query.append(maps[selected])

    query: list[str] = []

    ask_choice(screen, 'Temperatura',
               ['Frio', 'Templado', 'Caliente', 'No estoy seguro'],
               {'Frio': 'frio(X)', 'Templado': 'templado(X)', 'Caliente': 'caliente(X)'},
               query)
    ask_choice(screen, 'Rangos de temperatura',
               ['Volatil', 'Estable', 'No estoy seguro'],
               {'Volatil': 'volatil(X)', 'Estable': 'estable(X)'},
               query)
    ask_choice(screen, 'Humedad',
               ['Humedo', 'Seco', 'No estoy seguro'],
               {'Humedo': 'humedo(X)', 'Seco': 'seco(X)'},
               query)
    ask_choice(screen, 'Viento',
               ['Mucho', 'Poco', 'No estoy seguro'],
               {'Mucho': 'vestisca(X)', 'Poco': 'sin_viento(X)'},
               query)
    ask_choice(screen, 'Nubes',
               ['Mucho', 'Poco', 'No estoy seguro'],
               {'Mucho': 'nublado(X)', 'Poco': 'despejado(X)'},
               query)
    ask_choice(screen, 'Clima',
               ['Lluvia', 'Soleado', 'Nieve', 'No estoy seguro'],
               {'Lluvia': 'lloviendo(X)', 'Soleado': 'soleado(X)', 'Nieve': 'nevando(X)'},
               query)

    return ','.join(query) + '.'


def handle_option(screen, option, p: Prolog):
    if option == ord('0'):
        show_list(screen, prolog.query_cities_with_weather('clima_calido', p))
    if option == ord('1'):
        show_list(screen, prolog.query_cities_with_weather('clima_templado', p))
    if option == ord('2'):
        show_list(screen, prolog.query_cities_with_weather('clima_polar', p))
    if option == ord('3'):
        show_list(screen, prolog.query_cities_with_weather('clima_tropical', p))
    if option == ord('4'):
        show_list(screen, prolog.query_cities_with_weather('clima_seco', p))
    if option == ord('5'):
        show_list(screen, prolog.query_cities_with_weather('clima_moderado', p))
    if option == ord('6'):
        show_list(screen, prolog.custom_query(run_test(screen), p))

def main(screen):
    p = prolog.prepare_facts()
    while True:
        option = show_main_menu(screen, main_menu_options)
        if option == ord('q'):
            exit(0)

        handle_option(screen, option, p)

if __name__ == '__main__':
    curses.wrapper(main)
