from urllib import request
import configparser
import json


def read_token_from_config_file(config):
    parser = configparser.ConfigParser()
    parser.read(config)
    return parser.get('creds', 'token')


class TelegramBot:

    def __init__(self, config):
        self.token = read_token_from_config_file(config)
        self.base = f"https://api.telegram.org/bot{self.token}/"
        self.timeout = 100

    def get_updates(self, offset=None):
        url = self.base + f"getUpdates?timeout={self.timeout}"
        if offset:
            url = url + f"&offset={offset + 1}"
        print(url)
        r = request.urlopen(url).read().decode("utf-8")
        return json.loads(r)

    def send_message(self, chat_id, msg):
        url = self.base + f"sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            request.urlopen(url)

