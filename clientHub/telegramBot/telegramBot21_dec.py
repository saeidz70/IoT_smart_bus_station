import time
import telebot
import requests
import json


class TelegramBot:
    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(bot_token)
        self.authority()
        self.setup_handlers()
        self.key_list = []
        self.get_keys()
        self.address = []
        self.services_data = None

    def authority(self):
        self.telegram_authority = requests.get("http://127.0.0.1:8080/settings/telegram_authority").text
        names = json.loads(self.telegram_authority)
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

            self.bot.send_message(message.chat.id, "Please type your ID!",
                                  reply_markup=telebot.types.ReplyKeyboardRemove())

        @self.bot.message_handler(func=lambda message: message.text in self.authority())
        def handle_services(message):
            show_services(message)

        @self.bot.message_handler(func=lambda message: message.text == 'Show Services')
        def show_services(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttonDict = []
            for item in self.key_list:
                button = telebot.types.KeyboardButton(item)
                buttonDict.append(button)
            backButton = telebot.types.KeyboardButton('Go Back')
            markup.add(*buttonDict)
            if "stations" in self.address:
                addButton = telebot.types.KeyboardButton('Add')
                markup.add(addButton)
            markup.add(backButton)
            self.bot.send_message(message.chat.id, "Choose the information you would like to see!",
                                  reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message)
        def handle_services(message):
            if message.text in self.key_list:
                self.address.append(message.text)
                end_point = "/".join(self.address)
                self.services_data = self.get_catalog_data(end_point)
                if self.services_data:
                    if isinstance(self.services_data, dict):
                        self.key_list.clear()
                        for key in self.services_data:
                            self.key_list.append(key)
                        show_services(message)
                    else:
                        self.bot.send_message(message.chat.id,
                                              f"{message.text}:\n{json.dumps(self.services_data, indent=2)}")
                        handle_edit(message)

                else:
                    self.bot.send_message(message.chat.id, "Failed to fetch services information")
            elif message.text == "Go Back" and len(self.address) > 0:
                self.address.pop()
                end_point = "/".join(self.address)
                services_data = self.get_catalog_data(end_point)
                if services_data:
                    self.key_list.clear()
                    for key in services_data:
                        self.key_list.append(key)
                    show_services(message)

            elif message.text == "Edit":
                self.bot.send_message(message.chat.id, f"Please type the new value instead of {self.services_data}:",
                                      reply_markup=telebot.types.ForceReply())

            elif message.reply_to_message and message.reply_to_message.text == f"Please type the new value instead of {self.services_data}:":
                # try:
                if isinstance(self.services_data, list):
                    self.services_data.append(str(message.text))
                    new_value = self.services_data

                elif isinstance(self.services_data, int):
                    if int(message.text):
                        new_value = int(message.text)
                        print("it is int")
                        print("type is: ", type(self.services_data))
                        print(self.address)
                    else:
                        raise ValueError(f"Unsupported data type: {message.text}")
                        pass
                elif isinstance(self.services_data, float):
                    new_value = float(message.text)
                elif isinstance(self.services_data, str):
                    new_value = str(message.text)
                    print("it is str")
                else:
                    raise ValueError(f"Unsupported data type: {message.text}")

                self.put_catalog_data(new_value)
                self.bot.send_message(message.reply_to_message.chat.id, f"Value has been changed to {new_value}")
                message.text = "Go Back"
                handle_services(message)

            elif message.reply_to_message and message.reply_to_message.text == "Please type the new value:":
                while True:
                    try:
                        new_value = type(self.services_data)(message.text)
                        self.put_catalog_data(new_value)
                        self.bot.send_message(message.reply_to_message.chat.id,
                                              f"Value has been changed to {new_value}")
                        break
                    except (ValueError, TypeError):
                        self.bot.send_message(
                            message.reply_to_message.chat.id,
                            f"Error: Invalid input or incompatible data type. Please provide a valid {type(self.services_data).__name__} value."
                        )
                        # Prompt the user again for a valid value
                        self.bot.send_message(message.reply_to_message.chat.id, "Please type the new value:")

                message.text = "Go Back"
                handle_services(message)

            elif message.text == "Add":
                self.bot.send_message(message.chat.id, "Please add the value in dictionary format:",
                                      reply_markup=telebot.types.ForceReply())

            elif message.reply_to_message and message.reply_to_message.text == "Please add the value in dictionary format:":
                try:
                    new_value = int(message.text)
                    self.put_catalog_data(new_value)
                    self.bot.send_message(message.reply_to_message.chat.id, f"Value has been changed to {new_value}")
                except ValueError:
                    self.put_catalog_data(message.text)
                    self.bot.send_message(message.reply_to_message.chat.id, f"Value has been changed to {message.text}")

                message.text = "Go Back"
                handle_services(message)

        @self.bot.message_handler(func=lambda message: message.text == 'Edit')
        def handle_edit(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            backButton = telebot.types.KeyboardButton('Go Back')
            editButton = telebot.types.KeyboardButton('Edit')
            markup.add(editButton, backButton)
            self.bot.send_message(message.chat.id, "Do you want to edit this value?",
                                  reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text == 'Add')
        def handle_add(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            backButton = telebot.types.KeyboardButton('Go Back')
            addButton = telebot.types.KeyboardButton('Add')
            markup.add(addButton, backButton)
            self.bot.send_message(message.chat.id, "Do you want to add new information?",
                                  reply_markup=markup)

    def get_keys(self):
        try:
            response = requests.get(f"http://127.0.0.1:8080/")
            if response.status_code == 200:
                data = requests.get("http://127.0.0.1:8080/").json()
                for key in data:
                    self.key_list.append(key)
                return response.json()
        except Exception as e:
            print(f"Error fetching information:", str(e))
        return None

    def get_catalog_data(self, endpoint):
        try:
            response = requests.get(f"http://127.0.0.1:8080/{endpoint}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint} information:", str(e))
        return None

    def put_catalog_data(self, data):
        uri = "http://127.0.0.1:8080"
        print("data: ", data)
        try:
            body = {"address": self.address, "data": data}
            print("body: ", body)
            response = requests.put(uri, json=body)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching information:", str(e))
        return None

    def start(self):
        self.bot.polling()


# TODO: set threshold by telegram bot

if __name__ == "__main__":
    try:
        token_uri = "http://127.0.0.1:8080/settings/telegram_token"
        bot_token = requests.get(token_uri).json()
        time.sleep(1)
        bot_instance = TelegramBot(bot_token)
        bot_instance.start()
    except Exception as e:
        print("Error fetching information:", str(e))
