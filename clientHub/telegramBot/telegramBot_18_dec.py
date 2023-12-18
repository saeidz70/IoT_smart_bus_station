import time
import telebot
import requests
import json


class TelegramBot:
    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(bot_token)
        self.max_attempts = 3
        self.authority()
        self.setup_handlers()

    def authority(self):
        self.telegram_authority = requests.get("http://127.0.0.1:8080/settings/telegram_authority").text
        names = json.loads(self.telegram_authority)
        print(names)
        return names

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            link_button = telebot.types.InlineKeyboardButton("GitHub",
                                                             url="https://github.com/saeidz70/IoT_smart_bus_station")
            markup_url = telebot.types.InlineKeyboardMarkup(row_width=1)
            markup_url.add(link_button)
            self.bot.send_message(message.chat.id, "Welcome! This is smart station telegram bot",
                                  reply_markup=markup_url)

            self.bot.send_message(message.chat.id, "Please type your ID!")

            @self.bot.message_handler(func=lambda m: True)
            def authorized_id(message):
                name = message.text.lower()
                if name in self.authority():
                    self.bot.send_message(message.chat.id, "authorized")
                    show_services(message)
                else:
                    self.bot.send_message(message.chat.id, "not_authorized")
                    telebot.types.ReplyKeyboardRemove()
                    self.bot.clear_reply_handlers(message)

        @self.bot.message_handler(func=lambda message: message.text in self.authority())
        def handle_services(message):
            show_services(message)

        @self.bot.message_handler(func=lambda message: message.text == 'Show Services')
        def show_services(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item_services = telebot.types.KeyboardButton('Services')
            item_sensors = telebot.types.KeyboardButton('Sensors')
            item_thresholds = telebot.types.KeyboardButton('Thresholds')
            markup.add(item_services, item_sensors, item_thresholds)
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
            thresholds_data = self.get_catalog_data('stations/station_1/threshold')
            if thresholds_data:
                humidity = thresholds_data["humidity"]
                print(humidity)
                temperature_cold = thresholds_data["temperature_cold"]
                print(temperature_cold)
                temperature_hot = thresholds_data["temperature_hot"]
                print(temperature_hot)
                self.bot.send_message(message.chat.id, f"Thresholds:\n Humidity: {humidity}\n "
                                                       f"Temperature Cold: {temperature_cold}\n "
                                                       f"Temperature Hot: {temperature_hot}")

                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup_change_threshold = telebot.types.KeyboardButton('Change Threshold')
                markup_back_to_services = telebot.types.KeyboardButton('Show Services')
                markup.add(markup_change_threshold, markup_back_to_services)
                self.bot.send_message(message.chat.id, "Do you want to change the thresholds or get back to Services?",
                                      reply_markup=markup)

            else:
                self.bot.send_message(message.chat.id, "Failed to fetch thresholds information")

        @self.bot.message_handler(func=lambda message: message.text == 'Change Threshold')
        def change_thresholds(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item_humidity = telebot.types.KeyboardButton('Humidity')
            item_temperature_cold = telebot.types.KeyboardButton('Temperature Cold')
            item_temperature_hot = telebot.types.KeyboardButton('Temperature Hot')
            markup.add(item_humidity, item_temperature_cold, item_temperature_hot)

            self.bot.send_message(message.chat.id, "Which value do you want to change?",
                                  reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text == 'Humidity')
        def change_humidity(message):
            self.bot.send_chat_action(message.chat.id, "typing")
            # self.bot.reply_to(message, "hello")

            self.bot.send_message(message.chat.id, "Please type the new threshold:", reply_markup=telebot.types.ForceReply())

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        def handle_message(message):
            if message.reply_to_message:
                new_threshold = message.text


                self.bot.send_message(message.chat.id, f"New threshold saved as: {new_threshold}")

        #TODO: change the threshold

                # self.bot.send_message(message.chat.id, f"Services:\n{json.dumps(services_data, indent=2)}")

                # self.bot.send_message(message.chat.id, "Failed to fetch services information")



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


# TODO: set threshold by telegram bot
# TODO: show information to user in a friendly manner

if __name__ == "__main__":
    try:
        # token_uri = "http://127.0.0.1:8080/settings/telegram_token"
        # bot_token = requests.get(token_uri).text
        bot_token = "6604931438:AAFQtXjW60brIofOhH0zUQKcMZDZByTgiQ0"
        # print(bot_token)
        # time.sleep(1)
        bot_instance = TelegramBot(bot_token)
        bot_instance.start()
    except Exception as e:
        print("Error fetching information:", str(e))
