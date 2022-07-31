from io import BytesIO
from functools import lru_cache
from dataclasses import dataclass

import aiohttp
from vkbottle import Keyboard, Text
from vkbottle.bot import Message

from photo_generator import Color
from state_manager import state_manager
from localization import get_color_translation

from .base import random_sid, photo_message_uploader


COLOR_KB_COLS = 2

PATTERN_LINKS = [
    'photo-214739218_457239017',
    'photo-214739218_457239018',
    'photo-214739218_457239019',
    'photo-214739218_457239020',
    'photo-214739218_457239021',
    'photo-214739218_457239022'
]


@dataclass
class Sticker:
    url: str
    width: int
    height: int


@lru_cache()
def _generate_pattern_keyboard() -> str:
    """
    Генерирует клавиатуру для выбора узора

    :return: Json созданной клавиатуры для отправки в сообщении
    """

    keyboard = Keyboard(one_time=True)
    for i in range(len(PATTERN_LINKS)):
        keyboard.add(Text(
            f'Узор {i + 1}',
            {'pattern': i, 'sid': random_sid}
        ))
        if i != len(PATTERN_LINKS) - 1:
            keyboard.row()
    kb_json = keyboard.get_json()
    return kb_json


@lru_cache()
def _generate_color_keyboard() -> str:
    """
    Генерирует клавиатуру для выбора цвета

    :return: Json созданной клавиатуры для отправки в сообщении
    """

    buttons = []
    for color in Color:
        buttons.append(Text(
            get_color_translation(color.name),
            {'color': color.value, 'sid': random_sid}
        ))
    buttons = [buttons[i:i + COLOR_KB_COLS] for i in range(0, len(buttons), COLOR_KB_COLS)]
    keyboard = Keyboard(one_time=True)
    for i, row in enumerate(buttons):
        for button in row:
            keyboard.add(button)
        if i != len(buttons) - 1:
            keyboard.row()
    kb_json = keyboard.get_json()
    return kb_json


async def get_sticker(event: Message) -> Sticker:
    """
    Выбирает лучшее изображение стикера (url) и его размеры

    :param event: сообщение со стикером
    :return: Sticker
    """

    sticker = event.attachments[0].sticker
    max_height, sticker_image_url = 0, ''
    width, height = 0, 0
    for image in sticker.images:
        if image.height > max_height:
            sticker_image_url = image.url
            width, height = image.width, image.height
    return Sticker(url=sticker_image_url, width=width, height=height)


async def get_content(url: str) -> BytesIO:
    """
    Загружает фото по url и возвращает его данные

    :param url: ссылка на изображение
    :return: фото в io.BytesIO
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as request:
            content = BytesIO()
            content.write(await request.read())
            content.seek(0)
            return content


async def choose_pattern(event: Message):
    """
    Выбор узора
    """

    kb = _generate_pattern_keyboard()
    await event.answer(
        message="👏🏻 Отлично! Теперь выбери узор для фона:",
        attachment=",".join(PATTERN_LINKS),
        keyboard=kb
    )


async def choose_color(event: Message):
    """
    Выбор цвета
    """

    kb = _generate_color_keyboard()
    await event.answer(
        message="👏🏻 Продолжаем! Далее выбери цвет оформления:",
        keyboard=kb
    )


async def generate_image(event: Message):
    """
    Создание конечного изображения и отправка его пользователю
    """

    await event.answer("✅ Параметры изображения выбраны! Его генерация может занять некоторое время...")
    avatar = await state_manager.generate_image(event.from_id)
    image = await photo_message_uploader.upload(avatar.getvalue(), peer_id=event.peer_id)
    await event.answer("🔥 Ваше изображение успешно создано!", attachment=image)
