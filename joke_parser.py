import requests
from bs4 import BeautifulSoup as BS


def print_joke():

    joke_text = ''
    url = 'https://www.anekdots.com/Случайный_анекдот/'
    response = requests.get(url)
    html = BS(response.content, 'html.parser')

    for el in html.findAll('div', class_='marg10'):

        joke_text += str(el)
        joke_text = joke_text[56:]

        while '<br/>' in joke_text:
            index_symb = joke_text.find('<br/>')
            joke_text = joke_text[:index_symb] + f'\n' + joke_text[index_symb+5:]

        index_symb = joke_text.find('</div>')
        joke_text = joke_text[:index_symb]

    return joke_text


# print(print_joke())
#return joke_mess
