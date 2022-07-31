from io import BytesIO
from typing import Mapping
from collections import defaultdict
from dataclasses import dataclass

from photo_generator import generate_avatar


@dataclass
class Sticker:
    content: BytesIO = None
    width: int = None
    height: int = None


@dataclass
class State:
    sticker: Sticker = None
    pattern: int = None
    color: str = None


class StateManager:
    """
    Класс для хранинения ввода пользователей и дальнейшей генерации аватарок
    """

    states: Mapping[int, State] = defaultdict(State)

    async def delete_state(self, user_id: int):
        """
        Удаляет данные пользователя из хранилища

        :param user_id: Идентификатор пользователя
        """

        if user_id in self.states.keys():
            del self.states[user_id]

    async def set_sticker(self, *, user_id: int, content: BytesIO, width: int, height: int):
        """
        Добавляет информацию о выбранном пользователем стикере

        :param user_id: Идентификатор пользователя
        :param content: Изображение стикера в io.BytesIO
        :param width: Ширина изображения
        :param height: Высота изображения
        """

        sticker = Sticker(
            content=content,
            width=width,
            height=height
        )
        self.states[user_id].sticker = sticker

    async def set_pattern(self, user_id: int, pattern_number: int):
        """
        Добавляет информацию о выбранном пользователем узоре

        :param user_id: Идентификатор пользователя
        :param pattern_number: Номер узора
        """

        self.states[user_id].pattern = pattern_number

    async def set_color(self, user_id: int, color: str):
        """
        Добавляет информацию о выбранном пользователем цвете

        :param user_id: Идентификатор пользователя
        :param color: Цвет в hex
        """

        self.states[user_id].color = color

    async def generate_image(self, user_id: int) -> BytesIO:
        """
        Генерация изображения на основе введенных пользователем данных

        :param user_id: Идентификатор пользователя
        :return: Конечное изображение в io.BytesIO
        """

        state = self.states[user_id]
        avatar = generate_avatar(
            sticker_content=state.sticker.content,
            pattern=state.pattern,
            color=state.color
        )
        await self.delete_state(user_id)
        return avatar


state_manager = StateManager()   # Создание единственного менеджера
