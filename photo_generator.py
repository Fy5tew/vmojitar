from enum import Enum
from io import BytesIO
from typing import Union

from PIL import Image, ImageDraw, ImageFont


WATERMARK_TEXT = "vmojitar by Fy5tew"
WATERMARK_COLOR = '#000000'
WATERMARK_FONT_PATH = r'assets\fonts\NotoSerifItalic.ttf'

PATTERN_PATH = r"assets\patterns\{id}.png"

STICKER_OFFSET = 50
WATERMARK_OFFSET = 50


class Color(Enum):
    WHITE = '#d5dfe9'
    GREY = '#18222c'
    RED = '#f06a5f'
    GREEN = '#61b06e'
    BLUE = '#008dcf'
    LIGHT_BLUE = '#8bd2cc'
    ORANGE = '#de8751'
    BROWN = '#b17e49'
    PINK = '#ffafb0'
    VIOLET = '#e7bcea'


def generate_background(pattern: int, color: Union[Color, str]) -> Image:
    """
    Генерирует фон с узором и цветом

    :param pattern: Номер узора
    :param color: Цвет
    :return: Изображение фона (PIL.Image)
    """

    im = Image.open(PATTERN_PATH.format(id=pattern))
    im = im.convert('RGBA')
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, color)
        background.paste(im, im.split()[-1])
        im = background
    im.convert('RGB')
    return im


def generate_avatar(*, sticker_content: BytesIO, pattern: int, color: Union[Color, str]) -> BytesIO:
    """
    Создает аватарку из стикера с узором и цветом в качестве фона

    :param sticker_content: Изображение стикера в io.BytesIO
    :param pattern: Номер узора
    :param color: Цвет
    :return: Готовое изображение в io.BytesIO
    """

    sticker: Image = Image.open(sticker_content)
    background = generate_background(pattern, color)

    avatar = _combine(sticker, background)
    _add_watermark(WATERMARK_TEXT, avatar)

    fp = BytesIO()
    avatar.save(fp, format='PNG')
    return fp


def _combine(sticker: Image, bg: Image) -> Image:
    """
    Добавляет стикер на фон

    :param sticker: Стикер
    :param bg: Фон
    :return: Изображение в PIL.Image
    """

    img = bg.copy()
    size = img.width - 2 * STICKER_OFFSET
    sticker = sticker.resize((size, size))

    img.paste(sticker, (STICKER_OFFSET, ((img.height - size) // 2)), mask=sticker)
    return img


def _add_watermark(text: str, img: Image):
    """
    Добавляет водяной знак на изображение

    :param text: Текст знака
    :param img: Изображение
    """

    watermark = ImageDraw.Draw(img)
    font = ImageFont.truetype(WATERMARK_FONT_PATH, size=100)
    watermark.text(
        (img.width - WATERMARK_OFFSET, img.height - WATERMARK_OFFSET),
        text,
        WATERMARK_COLOR,
        font=font,
        anchor='rs'
    )
