from telegram_bot import TelegramBot
from urllib import request, parse
from datetime import date
import json
import random

dishes_url = "https://www.studentenwerk-potsdam.de//essen/unsere-mensen-cafeterien/detailinfos" \
             "/?tx_typoscriptrendering%5Bcontext%5D=%7B%22record%22%3A%22pages_66%22%2C%22path%22%3A%22tt_content" \
             ".list.20.ddfmensa_ddfmensajson%22%7D&tx_ddfmensa_ddfmensajson%5Bmensa%5D=4&cHash" \
             "=b14a1168346e0b7db67da056660d3a0e "
noodles_available = False
no_noodles_messages = ["Keine Nudeln... Wieso?!", "Mensa ohne Nudeln ist wie GdS ohne Wollowski!", "Schon wieder ein "
                                                                                                   "nudelfreier -> "
                                                                                                   "verlorener Tag.",
                       "Ich zahl auch €3 für die Nudeln!", "Wo bleibt die HPI-Mensa mit täglich Nudeln?"]

update_id = None
bot = TelegramBot("config.cfg")
rand = random.Random()


def make_reply(msg):
    reply = None
    if msg == "/noodle":
        if date.today().weekday() < 5:
            today = date.today().strftime("%d.%m.%Y")
            reply = "Angebote+der+Mensa+f%C3%BCr+den+" + str(today) + ":%0A%0A"
            all_dishes = get_todays_dishes()
            for offer in all_dishes:
                reply += get_todays_offer(offer) + "%0A"
            if not noodles_available:
                reply += parse.quote(rand.choice(no_noodles_messages))
        else:
            reply = "Wer geht am Wochenende schon zur Mensa?"
    return reply


def get_todays_offer(offer):  # noodles_available = True if corresponding title
    title = offer["titel"]
    dish = offer["beschreibung"]
    price = offer["preis_s"]
    return parse.quote(f"{title}: {dish} (€{price})")


def get_todays_dishes():
    r = request.urlopen(dishes_url).read().decode("utf-8")
    content = json.loads(r)
    return content["wochentage"][0]["datum"]["angebote"]


while True:
    noodles_available = False
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = item["message"]["text"]
            except KeyError:
                message = None
            from_ = item["message"]["from"]["id"]
            reply_ = make_reply(message)
            bot.send_message(from_, reply_)

