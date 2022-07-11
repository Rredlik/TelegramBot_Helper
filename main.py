import telebot
from telebot import types

import random_methods
import weather_parser

bot = telebot.TeleBot('5526113848:AAHXJKLH5BEDyogSFUbaupnrE1H2NoehBoI', parse_mode=None)


def main_menu_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    taskmanager_button = types.KeyboardButton('✅ Таск менеджер')
    weather_button = types.KeyboardButton('🌤️ Погода')
    chart_button = types.KeyboardButton('📈 Курсы валют')
    smth_button = types.KeyboardButton('котик')
    markup.row(weather_button)
    markup.row(taskmanager_button, chart_button)
    markup.row(smth_button)

    bot.send_message(message.chat.id,
                     "Это меню бота",
                     parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}!'
    bot.send_message(message.chat.id, mess, parse_mode='html')

    main_menu_buttons(message)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "✅ Таск менеджер":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        task_create = types.KeyboardButton('➕ Добавить заметку')
        task_list = types.KeyboardButton('🗂️ Список дел')
        back = types.KeyboardButton('🔙 В главное меню')
        markup.row(task_create, task_list)
        markup.row(back)

        bot.send_message(message.chat.id,
                         "Здесь можно писать дела на день",
                         parse_mode='html',
                         reply_markup=markup)

    elif message.text == "🌤️ Погода":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        weather_today = types.KeyboardButton('Погода на сегодня')
        weather_week = types.KeyboardButton('Погода на неделю')
        back = types.KeyboardButton('🔙 В главное меню')
        markup.row(weather_today, weather_week)
        markup.row(back)

        bot.send_message(message.chat.id,
                         "Тут отображается погода",
                         parse_mode='html',
                         reply_markup=markup)

    elif message.text == "Погода на сегодня":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        weather_message = weather_parser.weather_on_hours()

        weather_today = types.KeyboardButton('Погода на сегодня')
        weather_week = types.KeyboardButton('Погода на неделю')
        back = types.KeyboardButton('🔙 В главное меню')
        markup.row(weather_today, weather_week)
        markup.row(back)

        bot.send_message(message.chat.id,
                         weather_message,
                         parse_mode='html',
                         reply_markup=markup)

    elif message.text == "Погода на неделю":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        weather_message = weather_parser.weather_on_week()

        weather_today = types.KeyboardButton('Погода на сегодня')
        weather_week = types.KeyboardButton('Погода на неделю')
        back = types.KeyboardButton('🔙 В главное меню')
        markup.row(weather_today, weather_week)
        markup.row(back)

        bot.send_message(message.chat.id,
                         weather_message,
                         parse_mode='html',
                         reply_markup=markup)

    elif message.text == "📈 Курсы валют":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        weather_today = types.KeyboardButton('Курс доллара')
        weather_week = types.KeyboardButton('Курс евро')
        back = types.KeyboardButton('🔙 В главное меню')
        markup.row(weather_today, weather_week)
        markup.row(back)

        bot.send_message(message.chat.id,
                         "Тут отображаются выбранные тобой курсы валют",
                         parse_mode='html',
                         reply_markup=markup)

    elif message.text == "котик":
        photo_name = random_methods.cats_photo_name(1, 10)
        img_kitty = open(photo_name, 'rb')
        bot.send_photo(message.chat.id, img_kitty)

    elif message.text == "🔙 В главное меню":
        main_menu_buttons(message)


bot.polling(none_stop=True)
