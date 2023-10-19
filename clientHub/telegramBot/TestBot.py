import telebot

bot = telebot.TeleBot('6604931438:AAFQtXjW60brIofOhH0zUQKcMZDZByTgiQ0')

link_button = telebot.types.InlineKeyboardButton("GitHub", url="https://github.com/saeidz70/IoT_smart_bus_station")
markup = telebot.types.InlineKeyboardMarkup(row_width=1)
markup.add(link_button)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi, This is smart station telegram bot", reply_markup=markup)


key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
key_markup.add("Status", "Services", "Help", "About")


@bot.message_handler(commands=["help"])
def help_me(message):
    bot.reply_to(message, "What can I do for you", reply_markup=key_markup)


@bot.message_handler()
def keyboard(message):
    if message.text == "Status":
        bot.send_message(message.chat.id, "I will send you the status")
    elif message.text == "Services":
        bot.send_message(message.chat.id, "I will send you the Services")
    elif message.text == "Help":
        bot.send_message(message.chat.id, "What can I do for you")
    elif message.text == "About":
        bot.send_message(message.chat.id, "Hi, This is smart station telegram bot", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "I did not understand")


bot.infinity_polling()
