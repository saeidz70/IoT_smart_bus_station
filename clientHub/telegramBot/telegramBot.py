import time

import telebot
import requests
import json


class TelegramBot:
    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(bot_token)
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            link_button = telebot.types.InlineKeyboardButton("GitHub",
                                                             url="https://github.com/saeidz70/IoT_smart_bus_station")
            markup_url = telebot.types.InlineKeyboardMarkup(row_width=1)
            markup_url.add(link_button)
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item_services = telebot.types.KeyboardButton('Services')
            item_sensors = telebot.types.KeyboardButton('Sensors')
            item_thresholds = telebot.types.KeyboardButton('Thresholds')
            markup.add(item_services, item_sensors, item_thresholds)
            self.bot.send_message(message.chat.id, "Welcome! This is smart station telegram bot",
                                  reply_markup=markup_url)
            self.bot.send_message(message.chat.id, "What information would you like to see?",
                                  reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text == 'Services')
        def handle_services(message):
            services_data = self.get_catalog_data('services')
            if services_data:
                self.bot.send_message(message.chat.id, f"Services:\n{json.dumps(services_data, indent=2)}")
            else:
                self.bot.send_message(message.chat.id, "Failed to fetch services information")

        @self.bot.message_handler(func=lambda message: message.text == 'Sensors')
        def handle_sensors(message):
            sensors_data = self.get_catalog_data('sensors')
            if sensors_data:
                self.bot.send_message(message.chat.id, f"Sensors:\n{json.dumps(sensors_data, indent=2)}")
            else:
                self.bot.send_message(message.chat.id, "Failed to fetch sensors information")

        @self.bot.message_handler(func=lambda message: message.text == 'Thresholds')
        def handle_thresholds(message):
            thresholds_data = self.get_catalog_data('threshold')
            if thresholds_data:
                # message = thresholds_data["humidity"]
                self.bot.send_message(message.chat.id, f"Thresholds:\n{json.dumps(thresholds_data, indent=2)}")
            else:
                self.bot.send_message(message.chat.id, "Failed to fetch thresholds information")

    def get_catalog_data(self, endpoint):
        try:
            response = requests.get(f"http://127.0.0.1:8080/{endpoint}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint} information:", str(e))
        return None

    def put_catalog_data(self, endpoint, value):
        try:
            body = json.dumps(value)
            response = requests.put(f"http://127.0.0.1:8080/{endpoint}", data=body)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint} information:", str(e))
        return None

    def start(self):
        self.bot.polling()


if __name__ == "__main__":
    try:
        # token_uri = "http://127.0.0.1:8080/telegram_token"
        # bot_token = requests.get(token_uri).text
        bot_token = "6604931438:AAFQtXjW60brIofOhH0zUQKcMZDZByTgiQ0"
        # print(bot_token)
        # time.sleep(1)
        bot_instance = TelegramBot(bot_token)
        bot_instance.start()
    except Exception as e:
        print("Error fetching information:", str(e))
