# Vmojitar
Vmojitar — это простой бот VK для генерации аватарок из стикеров vmoji.
## Принцип работы
Пользователь присылает боту интересующий стикер и выбирает один из предложенных узоров и цветов, после чего бот создаёт конечное изображение и присылает его пользователю.
Пример такого фото:

<img src="https://github.com/Fy5tew/vmojitar/blob/master/vmojitar.jpg" width="150" alt="https://github.com/Fy5tew/vmojitar/blob/master/vmojitar.jpg" />

## Зависимости
В проекте используется Python3.9. Скачать его можно с [официального сайта](https://www.python.org/).

Для работы с VK BOT API используется асинхронный фреймворк [VKBottle](https://github.com/vkbottle/vkbottle). Для создания изображений используется форк популярной библиотеки PIL — [Pillow](https://github.com/python-pillow/Pillow).
Полный список зависимостей находится в файле [requirements.txt](https://github.com/Fy5tew/vmojitar/blob/master/requirements.txt).
## Настройка
Настройки бота указываются в файле `config.json`. Его структура описана в [файле](https://github.com/Fy5tew/vmojitar/blob/master/config.json.example).
## Запуск бота
1. Клонирование репозитория
```
git clone https://github.com/Fy5tew/vmojitar.git
```
2. Установка зависимостей
```
pip install -r requirements.txt
```
3. Запуск бота
```
python main.py
```
**Перед запуском бота необходимо создать файл `config.json`**