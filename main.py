# https://medium.com/swlh/telegram-bot-with-python-for-todoist-89d6cb13a04
# https://github.com/ieCecchetti/ToDo-bot-Telegram?ysclid=l66d94l5e9146289468
# https://pythobyte.com/building-a-chatbot-using-telegram-and-python-part-2-sqlite-databse-backend-m7o96jger-5e5fbcf0/?ysclid=l6a9jo72xv879672112

from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.custom_filters import AdvancedCustomFilter
from telebot import types, TeleBot
from config import BOT_API_TOKEN

import random_methods
import weather_api
from task_manager import db_manipulations
from joke_parser import print_joke

bot = TeleBot(BOT_API_TOKEN)


def main_menu_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    taskmanager_button = types.KeyboardButton('✅ Таск менеджер')
    weather_button = types.KeyboardButton('🌤️ Погода')
    # chart_button = types.KeyboardButton('📈 Курсы валют')
    smth_button = types.KeyboardButton('котик 🐈')
    # test = types.KeyboardButton('test')
    joke_button = types.KeyboardButton('🤣 Анекдот 😂')

    markup.row(taskmanager_button)
    markup.row(weather_button)  # , chart_button
    markup.row(smth_button, joke_button)

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}!'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    main_menu_buttons()
    try:
        create_new_user_tables(message)
    except Exception as _e:
        print("[Main error] button start: ", repr(_e))


# Создание необходимых таблиц для пользователя
def create_new_user_tables(message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    try:
        operation = ['create_new_user', f'{user_id}', f'{user_first_name}']
        db_manipulations(operation)
    except Exception as _e:
        print("[Main error] into def create_new_user_tables: ", repr(_e))


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "✅ Таск менеджер":
        bot.send_message(
            chat_id=message.chat.id,
            text='Здесь можно записать или посмотреть дела на день!',
            reply_markup=task_menu_keyboard())

    elif message.text == "🌤️ Погода":
        bot.send_message(
            chat_id=message.chat.id,
            text='Тут отображается погода',
            reply_markup=weather_menu_keyboard())

    # elif message.text == "📈 Курсы валют":
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #
    #     weather_today = types.KeyboardButton('Курс доллара')
    #     weather_week = types.KeyboardButton('Курс евро')
    #     back = types.KeyboardButton('🔙 В главное меню')
    #     markup.row(weather_today, weather_week)
    #     markup.row(back)
    #
    #     bot.send_message(message.chat.id,
    #                      "Тут отображаются выбранные тобой курсы валют",
    #                      parse_mode='html',
    #                      reply_markup=markup)

    elif message.text == "котик 🐈":
        photo_name = random_methods.cats_photo_name(11, 36)
        img_kitty = open(photo_name, 'rb')
        bot.send_photo(message.chat.id, img_kitty)

    elif message.text == "🤣 Анекдот 😂":
        some_joke = print_joke().format()
        bot.send_message(message.chat.id,
                         text=some_joke,
                         parse_mode='html')

    # elif message.text == "test":
    #     markup = types.ReplyKeyboardRemove(selective=False)
    #     bot.send_message(message.chat.id, message, reply_markup=markup)

    elif message.text == "🔙 В главное меню":
        bot.send_message(message.chat.id,
                         "Это меню бота, нажимай на кнопки ниже, чтобы выбрать нужное действие\n\n"
                         "✅ Таск менеджер: это твой личный список дел/заметок/мыслей. "
                         "Записывай что хочешь, чтобы не забыть!\n\n"
                         "🌤️ Погода: отображает погоду на сегодня/на три дня вперед\n\n"
                         "🐈 котик: пожалуй, самая важная функция которая здесь есть))"
                         "🤣 Анекдот 😂: бот отправит тебе случайный анекдот",
                         parse_mode='html',
                         reply_markup=main_menu_buttons())

    elif message.text.lower() == "test admin message":
        bot.send_message(message.chat.id, message)

    else:
        bot.send_message(message.chat.id,
                         "Это меню бота, нажимай на кнопки ниже, чтобы выбрать нужное действие\n\n"
                         "✅ Таск менеджер: это твой личный список дел/заметок/мыслей. "
                         "Записывай что хочешь, чтобы не забыть!\n\n"
                         "🌤️ Погода: отображает погоду на сегодня/на три дня вперед\n\n"
                         "🐈 котик: пожалуй, самая важная функция которая здесь есть))"
                         "🤣 Анекдот 😂: бот отправит тебе случайный анекдот",
                         parse_mode='html',
                         reply_markup=main_menu_buttons())


# Инлайн кнопки для погоды
def weather_menu_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [types.InlineKeyboardButton(text='Погода на сегодня', callback_data="pogoda_today")],
            [types.InlineKeyboardButton(text='Погода на неделю', callback_data="pogoda_week")],
            [types.InlineKeyboardButton(text='❌ Закрыть меню ❌', callback_data="close_mess")]
        ]
    )


# Инлайн кнопки для заметок
def task_menu_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [types.InlineKeyboardButton(text='➕ Добавить заметку ➕', callback_data="add_task_to_db")],
            [types.InlineKeyboardButton(text='🗂️ Список дел 🗂️', callback_data="print_task_list")],
            [types.InlineKeyboardButton(text='❌ Закрыть меню ❌', callback_data="close_mess")]
        ]
    )


def task_list_keyboard(tasks):
    task_list = types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=f"{task[1]}",
                    callback_data=task_list_for_user.new(task_id=task[0])
                )
            ]
            for task in tasks

        ]

    )
    task_list.add(types.InlineKeyboardButton(
        text="❌ Закрыть меню ❌",
        callback_data="close_tab"
    ))
    return task_list


task_list_for_user = CallbackData('task_id', prefix='task_number_')


class TasksCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


@bot.callback_query_handler(func=lambda call: call.data == 'print_task_list')
def print_task_inline_method(call: types.CallbackQuery):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Подожди, загружаю твой список дел..")

    try:
        operation = ['print_data', f'{call.from_user.id}']
        tasks = db_manipulations(operation)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.from_user.id,
                         text="--------------Твой список дел--------------\n\n"
                              "Нажми на кнопку заметки чтобы удалить ее, "
                              "будь вниметелнее, их нельзя восстановить!!",
                         reply_markup=task_list_keyboard(tasks))

    except Exception as _e:
        print("[Main error] get_user_task_list: ", repr(_e))


@bot.callback_query_handler(func=None, config=task_list_for_user.filter())
def delete_user_tasks(call: types.CallbackQuery):
    callback_data: dict = task_list_for_user.parse(callback_data=call.data)
    task_id = int(callback_data['task_id'])
    user_id = call.from_user.id

    operation = ['delete_data', f'{user_id}', f'{task_id}']
    tasks = db_manipulations(operation)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="~~~~~~~~~~~Заметка удалена~~~~~~~~~~~", reply_markup=task_list_keyboard(tasks))


@bot.callback_query_handler(func=lambda call: call.data == 'add_task_to_db')
def add_task_inline_method_del_msg(call: types.CallbackQuery):
    try:
        markup = types.InlineKeyboardMarkup()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)

        markup.add(types.InlineKeyboardButton(
            text="❌ Отмена ❌",
            callback_data="cancel_inserting"
        ))
        msg = bot.send_message(call.from_user.id, "Напиши заметку, которую хочешь добавить в список дел.\n\n\n"
                                                  "Нажмите ОТМЕНА, если передумали!", reply_markup=markup)

        bot.register_next_step_handler(msg, get_new_users_task)

    except Exception as _e:
        print("[Main error] weather: ", repr(_e))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Какая-то ошибка...", reply_markup=task_menu_keyboard())


# Внесение данных в созданные ранее таблицы
def get_new_users_task(message):
    user_task_text = message.text

    if user_task_text.lower() == "отмена" or \
            user_task_text == "✅ Таск менеджер" or \
            user_task_text == "📈 Курсы валют" or \
            user_task_text == "котик 🐈" or \
            user_task_text == "🔙 В главное меню" or \
            user_task_text == "🌤️ Погода" or \
            user_task_text == "test" or \
            user_task_text == "🤣 Анекдот 😂":
        bot.send_message(message.from_user.id, 'Добавление заметки отменено!')
    else:
        operation = ['insert_data', f'{message.from_user.id}', f'{user_task_text}']
        db_manipulations(operation)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        bot.send_message(message.from_user.id, 'Заметка добавлена ➕')


# Обработка инлайн кнопок
@bot.callback_query_handler(func=None)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)

    if call.data == 'pogoda_today':
        try:
            weath_text = weather_api.hours_weather()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=weath_text, reply_markup=weather_menu_keyboard(), parse_mode='html')
        except Exception as _e:
            print("[Main error] weather: ", repr(_e))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Какая-то ошибка...", reply_markup=weather_menu_keyboard())

    elif call.data == 'pogoda_week':
        try:
            weath_text = weather_api.weekday_weather()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=weath_text, reply_markup=weather_menu_keyboard())
        except Exception as _e:
            print("[Main error] weather: ", repr(_e))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Какая-то ошибка...", reply_markup=weather_menu_keyboard())

    elif call.data == 'close_mess':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)

    elif call.data == 'close_tab':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'cancel_inserting':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)


if __name__ == '__main__':
    try:
        bot.add_custom_filter(TasksCallbackFilter())
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print("[Main error] ", repr(e))
