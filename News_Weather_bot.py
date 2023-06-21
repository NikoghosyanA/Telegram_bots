import requests
import telebot


def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=9e61f9eb5c090f4e59c4974d96677ff4&units=metric'
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    message = f'Погода в городе {city}: {description}, температура: {temperature}°C'
    return message


bot = telebot.TeleBot('token')


@bot.message_handler(commands=["start"])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("Погода", callback_data="func1")
    button2 = telebot.types.InlineKeyboardButton("Новости", callback_data="func2")
    markup.add(button1, button2)
    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}! Выбери что хочешь".format(message.from_user),
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'func1':
        bot.send_message(call.message.chat.id, "Введите название города:")
    elif call.data == 'func2':
        response = requests.get("https://newsdata.io/api/1/news?apikey=pub_187024cf00c9888613837a785570e7e0cc04a&q"
                                "=russia&country=ru ")
        data = response.json()
        articles = data["results"]
        for article in articles:
            message = f"{article['title']}\n{article['link']}"
            bot.send_message(call.message.chat.id, message)
    elif call.data == 'func3':
        bot.send_message(call.message.chat.id, 'Нажми /start')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    city = message.text
    weather = get_weather(city)
    markup = telebot.types.InlineKeyboardMarkup()
    button3 = telebot.types.InlineKeyboardButton("Назад", callback_data='func3')
    markup.add(button3)
    bot.send_message(message.chat.id, weather, reply_markup=markup)


bot.polling(none_stop=True, interval=0)
