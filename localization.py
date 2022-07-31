color_names = {
    'WHITE': 'БЕЛЫЙ',
    'GREY': 'СЕРЫЙ',
    'RED': 'КРАСНЫЙ',
    'GREEN': 'ЗЕЛЁНЫЙ',
    'BLUE': 'СИНИЙ',
    'LIGHT_BLUE': 'ГОЛУБОЙ',
    'ORANGE': 'ОРАНЖЕВЫЙ',
    'BROWN': 'КОРИЧНЕВЫЙ',
    'PINK': 'РОЗОВЫЙ',
    'VIOLET': 'ФИОЛЕТОВЫЙ',
}


def get_color_translation(color_name: str) -> str:
    """
    Получить название цвета на русском языке

    :param color_name: Название цвета на английском
    :return: Название цвета на русском. Если перевода нет, то возвращается color_name
    """

    return color_names.get(color_name, color_name).title()
