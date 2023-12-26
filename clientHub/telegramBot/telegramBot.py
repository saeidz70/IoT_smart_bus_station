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
        self.authority_names = json.loads(self.telegram_authority)
        return self.authority_names

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
            markup.add(*buttonDict)
            if "stations" in self.address:
                addKeyButton = telebot.types.KeyboardButton('Add Key')
                addValueButton = telebot.types.KeyboardButton('Add Value')
                deleteButton = telebot.types.KeyboardButton('Delete')
                markup.add(addKeyButton, addValueButton, deleteButton)
            if len(self.address) > 0:
                backButton = telebot.types.KeyboardButton('Go Back')
                markup.add(backButton)
            if not self.key_list:
                pass

            self.bot.send_message(message.chat.id, "Choose from buttons: ", reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message)
        def handle_services(message):
            if message.text in self.key_list:
                if len(self.address) <= 5:
                    self.address.append(message.text)
                    end_point = "/".join(self.address)
                    self.services_data = self.get_catalog_data(end_point)
                    if self.services_data:
                        if "telegram_authority" in self.address:
                            self.bot.send_message(message.chat.id,
                                                  f"{message.text}:\n{json.dumps(self.services_data, indent=2)}")
                            handle_authority(message)
                        elif isinstance(self.services_data, dict):
                            self.key_list.clear()
                            for key in self.services_data:
                                self.key_list.append(key)
                            show_services(message)
                        else:
                            self.bot.send_message(message.chat.id,
                                                  f"{message.text}:\n{json.dumps(self.services_data, indent=2)}")
                            handle_edit(message)
                    elif self.services_data == {}:
                        self.bot.send_message(message.chat.id, "There is no information to show, if you want to add "
                                                               "something, press ADD button.")
                        self.key_list.clear()
                        show_services(message)
                    else:
                        self.bot.send_message(message.chat.id, "Failed to fetch services information")
                else:
                    self.bot.send_message(message.chat.id, "You can not add more items! Check catalog's hierarchy")
                    show_services(message)
            elif message.text == "Go Back" or message.text == "/go_back":
                if len(self.address) > 0:
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
                if isinstance(self.services_data, list):
                    self.services_data.append(str(message.text))
                    new_value = self.services_data
                elif isinstance(self.services_data, int):
                    if int(message.text):
                        new_value = int(message.text)
                    else:
                        raise ValueError(f"Unsupported data type: {message.text}")
                        pass
                elif isinstance(self.services_data, float):
                    new_value = float(message.text)
                elif isinstance(self.services_data, str):
                    new_value = str(message.text)
                else:
                    raise ValueError(f"Unsupported data type: {message.text}")

                self.put_catalog_data(new_value)
                self.bot.send_message(message.reply_to_message.chat.id, f"Value has been changed to {new_value}")
                message.text = "Go Back"
                handle_services(message)

            elif message.text == "Add Key":
                self.bot.send_message(message.chat.id, "Please type the new item name (key):",
                                      reply_markup=telebot.types.ForceReply())

            elif message.reply_to_message and message.reply_to_message.text == "Please type the new item name (key):":
                new_key = message.text
                self.post_catalog_data(new_key, "key")
                self.bot.send_message(message.reply_to_message.chat.id, f"{new_key} has been added to catalog")
                message.text = "Go Back"
                handle_services(message)

            elif message.text == "Add Value":
                self.bot.send_message(message.chat.id, "Be careful the value will be replaced with "
                                                       "all contents in this level!")
                self.bot.send_message(message.chat.id, "Please type the new item (value):",
                                      reply_markup=telebot.types.ForceReply())

            elif message.reply_to_message and message.reply_to_message.text == "Please type the new item (value):":
                new_value = message.text
                self.post_catalog_data(new_value, "value")
                self.bot.send_message(message.reply_to_message.chat.id, f"{new_value} has been added to catalog")
                message.text = "Go Back"
                handle_services(message)

            elif message.text == "Delete":
                self.bot.send_message(message.chat.id, "The item only can be deleted if it DOES NOT contain a "
                                                       "dictionary!")
                self.bot.send_message(message.chat.id,
                                      "Type the item you want to delete. Be careful! put '-' before the item you want "
                                      "to delete!", reply_markup=telebot.types.ForceReply())

            elif message.reply_to_message and message.reply_to_message.text == ("Type the item you want to delete. Be "
                                                                                "careful! put '-' before the item you"
                                                                                " want to delete!"):
                delete_value = message.text.strip('- ').strip()
                if delete_value in self.key_list:
                    self.address.append(delete_value)
                    end_point = "/".join(self.address)
                    services_data = self.get_catalog_data(end_point)
                    if isinstance(services_data, dict) and len(services_data) > 0:
                        self.bot.send_message(message.reply_to_message.chat.id,
                                              f"{delete_value} can not be deleted from catalog!")

                    else:
                        self.delete_catalog_data(end_point)
                        self.bot.send_message(message.reply_to_message.chat.id, f"{delete_value} has been deleted "
                                                                                f"from catalog")

                else:
                    self.bot.send_message(message.reply_to_message.chat.id, f"{delete_value} is wrong!")

                message.text = "Go Back"
                handle_services(message)

            elif message.text == "Add Member":
                self.bot.send_message(message.chat.id, "Please type the new member's name:",
                                      reply_markup=telebot.types.ForceReply())

            elif message.reply_to_message and message.reply_to_message.text == "Please type the new member's name:":
                self.services_data.append(str(message.text))
                new_name = self.services_data
                self.put_catalog_data(new_name)
                self.bot.send_message(message.reply_to_message.chat.id, f"{new_name} is the new member")
                message.text = "Go Back"
                handle_services(message)

            elif message.text == "Delete Member":
                self.bot.send_message(message.chat.id, "Be careful! put '-' before the name!")
                self.bot.send_message(message.chat.id, "Please type the name to delete:",
                                      reply_markup=telebot.types.ForceReply())

            elif message.reply_to_message and message.reply_to_message.text == "Please type the name to delete:":
                delete_name = message.text.strip('- ').strip()
                self.services_data.remove(delete_name)
                new_list = self.services_data
                self.put_catalog_data(new_list)
                self.bot.send_message(message.reply_to_message.chat.id, f"{new_list} is deleted from the list!")
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
        def handle_authority(message):
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            deleteButton = telebot.types.KeyboardButton('Delete Member')
            addButton = telebot.types.KeyboardButton('Add Member')
            backButton = telebot.types.KeyboardButton('Go Back')
            markup.add(addButton, deleteButton, backButton)
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
        try:
            body = {"address": self.address, "data": data}
            response = requests.put(uri, json=body)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching information:", str(e))
        return None

    def post_catalog_data(self, data, data_type):
        uri = "http://127.0.0.1:8080"
        if data_type == "key":
            self.address.append(data)
            body = {"address": self.address, "data": {}}
        elif data_type == "value":
            body = {"address": self.address, "data": data}

        if len(self.address) <= 6:
            response = requests.post(uri, json=body)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception("Error post_catalog_data")
        else:
            raise Exception("Error for catalog hierarchy limitations")

    def delete_catalog_data(self, endpoint):
        try:
            response = requests.delete(f"http://127.0.0.1:8080/{endpoint}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint} information:", str(e))
        return None

    def start(self):
        self.bot.polling()


if __name__ == "__main__":
    try:
        token_uri = "http://127.0.0.1:8080/settings/telegram_token"
        bot_token = requests.get(token_uri).json()
        time.sleep(1)
        bot_instance = TelegramBot(bot_token)
        bot_instance.start()
    except Exception as e:
        print("Error fetching information:", str(e))
