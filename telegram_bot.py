import configparser
from urllib import request
import json

# import requests

r = request.urlopen(
    "https://www.studentenwerk-potsdam.de/essen/unsere-mensen-cafeterien/detailinfos/?tx_ddfmensa_ddfmensa%5Bmensa%5D=6&tx_ddfmensa_ddfmensa%5Baction%5D=show&cHash=42918cc76cdcb7a31c8fb2187b846933").read()
print(r.decode("utf-8"))


def read_token_from_config_file(config):
    parser = configparser.ConfigParser()
    parser.read(config)
    return parser.get('creds', 'token') # NOT COMMIT TO GIT (safety issues)


class TelegramBot:

    def __init__(self, config):
        self.token = read_token_from_config_file(config)
        self.base = f"https://api.telegram.org/bot{self.token}/"
        self.timeout = 100

    def get_updates(self, offset=None):
        url = self.base + f"/getUpdates?timeout={self.timeout}"
        if offset:
            url = url + f"&offset={offset + 1}"
        # r = requests.get(url)
        # r = urllib.openurl(url)
        # return json.loads(r)

    def send_message(self, msg, chat_id):
        url = self.base + f"sendMessage?chat_id={chat_id}&text={msg}"
        # if msg is not None:
        # requests.get(url)
        pass
