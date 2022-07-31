import random
from string import ascii_letters

from vkbottle import PhotoMessageUploader
from vkbottle.bot import Bot

import config


# Случайный идентификатор позволяет отсеивать события от старых клавиатур
random_sid = ''.join(random.choices(ascii_letters, k=config.RANDOM_SID_LENGTH))

bot = Bot(config.BOT_TOKEN)
photo_message_uploader = PhotoMessageUploader(bot.api)


def start():
    """
    Запуск Long Poll бота
    """

    bot.run_forever()
