import telegram
from telegram.ext import Updater, CommandHandler


class TelegramBot:
    def __init__(self, name, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token)
        self.id = -1001479099558
        # self.id = 743979607
        self.name = name

    def sendMessage(self, text):
        self.core.sendMessage(chat_id=self.id, text=text)

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()


class Bot(TelegramBot):
    def __init__(self):
        self.token = '1376763471:AAH31TgenrrAW9V3Rzja6oWw7rgQMtaX5HQ'
        # self.token = '789952118:AAH3LMKetfaK0Gy4zlSKUUdMLLOIis8tAGI'
        TelegramBot.__init__(self, 'sj', self.token)


def check(message):
    sj = Bot()
    sj.sendMessage(message)
