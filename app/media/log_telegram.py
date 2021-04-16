import telegram

bot = telegram.Bot(token='1782655884:AAEBfkvnC_dX8J_P9UqwK94HUgDxNonrwZU')
chat_id = -1001179245276


def send_log(msg):
    bot.sendMessage(chat_id=chat_id, text=msg)
