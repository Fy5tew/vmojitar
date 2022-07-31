import json
from typing import Iterable

from vkbottle.bot import Message
from vkbottle.dispatch.rules.abc import ABCRule
from vkbottle.dispatch.rules.base import AttachmentTypeRule

import config

from .base import random_sid


class CommandRule(ABCRule):
    """
    Фильтр для проверки команд в сообщении
    """

    def __init__(
            self,
            command_text: Iterable[str],
            prefixes: Iterable[str] = tuple(config.PREFIXES)
    ):
        self.command_text = list(map(lambda c: c.lower(), command_text))
        self.prefixes = list(map(lambda c: c.lower(), prefixes))

    async def check(self, event: Message) -> bool:
        if not event.text:   # Если сообщение является вложением без подписи
            return False
        for prefix in self.prefixes:
            if event.text.startswith(prefix):
                if event.text.lower().replace(prefix, '', 1).split()[0] in self.command_text:
                    return True
        return False


class StickerProductIdRule(ABCRule):
    """
    Фильтр для проверки соответствия product_id набора стикеров
    """

    def __init__(self, product_ids: Iterable[int]):
        self.product_ids = product_ids

    async def check(self, event: Message) -> bool:
        if event.attachments[0].sticker.product_id in self.product_ids:
            return True
        return False


class PayloadRule(ABCRule):
    """
    Фильтр для проверки команд в payload сообщения
    """

    def __init__(self, key: str):
        self.key = key

    async def check(self, event: Message) -> bool:
        if not event.payload:
            return False
        if isinstance(event.payload, str):   # payload может быть как строкой, так и словарём
            event.payload = json.loads(event.payload)
        if ('sid' in event.payload) and (event.payload['sid'] != random_sid):   # Если клавиатура была создана давно
            return False
        if self.key in event.payload:
            return True
        return False
