import datetime
import telebot

bot = telebot.TeleBot('7482911793:AAE2Ym8rXyxf2oTk1bxDE3PzRak-uIEsaPk')

user_sleep_data = {}


@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m,
                 'Привет! Я буду помогать тебе отслеживать параметры сна. Используй команды /sleep, /wake, /quality и /notes')


@bot.message_handler(commands=['sleep'])
def sleep_time(message):
    user_id = message.from_user.id

    if user_id not in user_sleep_data:
        user_sleep_data[user_id] = {'sleep_start_time': None, 'sleep_quality': None, 'sleep_notes': None}

    user_sleep_data[user_id]['sleep_start_time'] = datetime.datetime.now()
    bot.reply_to(message, 'Спокойной ночи! Не забудь сообщить мне, когда проснешься командой /wake.')


@bot.message_handler(commands=['wake'])
def wake_time(message):
    user_id = message.from_user.id

    if user_id in user_sleep_data and user_sleep_data[user_id]['sleep_start_time'] is not None:
        wake_time = datetime.datetime.now()
        sleep_duration = wake_time - user_sleep_data[user_id]['sleep_start_time']
        sleep_duration_seconds = round(sleep_duration.total_seconds(), 3)
        bot.reply_to(message,
                     f'Доброе утро! Ты спал {sleep_duration_seconds} секунд. Не забудь оценить качество сна командой /quality и оставить заметки командой /notes.')
        user_sleep_data[user_id]['sleep_start_time'] = None
    else:
        bot.send_message(message.chat.id, 'Я не вижу, что ты сообщил мне о начале сна. Используй команду /sleep.')


@bot.message_handler(commands=['quality'])
def quality_rating(message):
    user_id = message.from_user.id

    if user_id in user_sleep_data:
        try:
            quality_score = int(message.text.split()[1])
            if 1 <= quality_score <= 10:
                user_sleep_data[user_id]['sleep_quality'] = quality_score
                bot.reply_to(message, f'Спасибо за оценку качества сна')
            else:
                bot.send_message(message.chat.id, 'Оценка должна быть от 1 до 10.')
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, 'Неверный формат команды. Используйте /quality [оценка от 1 до 10].')
    else:
        bot.send_message(message.chat.id, 'Я не вижу, что ты сообщил мне о начале сна. Используй команду /sleep.')


@bot.message_handler(commands=['notes'])
def notes(message):
    user_id = message.from_user.id

    if user_id in user_sleep_data:
        if message.text.split() == ['/notes']:
            bot.send_message(message.chat.id, 'Введите заметку о сне используя команду /notes [заметка].')
        else:
            user_sleep_data[user_id]['sleep_notes'] = ' '.join(message.text.split()[1:])
            bot.reply_to(message, 'Заметка успешно сохранена!')
    else:
        bot.send_message(message.chat.id, 'Я не вижу, что ты сообщил мне о начале сна. Используй команду /sleep.')


bot.polling()