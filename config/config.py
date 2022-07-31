from typing import List
import json


__all__ = [
    'BOT_TOKEN',
    'API_VERSION',
    'LOGGING_LEVEL',
    'RANDOM_SID_LENGTH',
    'PREFIXES',
    'STICKER_PRODUCT_IDS'
]


with open(r'config.json', 'r') as _config_file:
    config = json.load(_config_file)


BOT_TOKEN: str = config.get('bot_token')   # Токен вашего бота
API_VERSION: str = config.get('api_version')   # Версия VK API (unused)

LOGGING_LEVEL: str = config.get('logging_level')   # Уровень логирования
RANDOM_SID_LENGTH: int = config.get('random_sid_length')   # Длина случайного идентификатора

PREFIXES: List[str] = config.get('prefixes', [''])   # Префиксы для команд
STICKER_PRODUCT_IDS: List[int] = config.get('sticker_product_ids', [])   # Разрешенные наборы стикеров для генерации
