from vkbottle.bot import Message

import config
from state_manager import state_manager

from .base import bot
from . import filters, logic


__all__ = []


VMOJI_STICKERS_LINK = 'vk.com/stickers/vmoji'
VMOJI_STICKERS_FULL_LINK = f'https://{VMOJI_STICKERS_LINK}'
VMOJI_STICKERS_TEXT = f"🔗 Ваш набор стикеров находится здесь: {VMOJI_STICKERS_FULL_LINK}"


@bot.on.message(filters.CommandRule(['начать', 'привет', 'start']))
async def start_cmd(event: Message):
    user_info = await bot.api.users.get(user_ids=[event.from_id])
    name = user_info[0].first_name
    return (
        f"👋🏻 Привет, {name}!\n"
        f"Я создаю аватарки со стикерами из вашего набора Vmoji. "
        "Отправь интересующий стикер и следуй инструкциям.\n"
        f"{VMOJI_STICKERS_TEXT}"
            )


@bot.on.message(filters.CommandRule(['помощь', 'помоги', 'help']))
async def help_cmd(event: Message):
    await state_manager.delete_state(event.from_id)
    return (
        f"❓ Для создания собственной аватарки отправь мне свой Vmoji, "
        "выбери узор и цвет фона, "
        "а после дай мне немного времени для создания изображения.\n"
        f"{VMOJI_STICKERS_TEXT}"
    )


@bot.on.message(filters.AttachmentTypeRule('sticker'), ~filters.StickerProductIdRule(config.STICKER_PRODUCT_IDS))
async def on_other_sticker(event: Message):
    await state_manager.delete_state(event.from_id)
    return (
        "🤪 Это не Vmoji!\n"
        f"{VMOJI_STICKERS_TEXT}"
    )


@bot.on.message(filters.AttachmentTypeRule('sticker'), filters.StickerProductIdRule(config.STICKER_PRODUCT_IDS))
async def on_allowed_sticker(event: Message):
    sticker = await logic.get_sticker(event)
    content = await logic.get_content(sticker.url)
    await state_manager.set_sticker(
        user_id=event.from_id,
        content=content,
        width=sticker.width,
        height=sticker.height
    )
    await logic.choose_pattern(event)


@bot.on.message(filters.PayloadRule('pattern'))
async def on_pattern_choose(event: Message):
    await state_manager.set_pattern(event.from_id, event.payload['pattern'])
    await logic.choose_color(event)


@bot.on.message(filters.PayloadRule('color'))
async def on_color_choose(event: Message):
    await state_manager.set_color(event.from_id, event.payload['color'])
    await logic.generate_image(event)


@bot.on.message()
async def on_message(event: Message):
    await state_manager.delete_state(event.from_id)
    return (
        "😞 Извини, но я тебя не понимаю... "
        "Напиши 'помощь', чтобы узнать что я умею!"
    )
