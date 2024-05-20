import os
from dotenv import load_dotenv
from emoji import emojize

load_dotenv()

TOKEN = os.getenv('TOKEN')
NAME_DB = os.getenv('NAME_DB')
VERSION = os.getenv('VERSION')
AUTHOR = os.getenv('AUTHOR')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB)

COUNT = 0

KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Обрати книгу'),
    'INFO': emojize(':speech_balloon: Про магазин'),
    'SETTINGS': emojize('⚙️ Інструкція до використання'),
    'CLASIC_LITERATURE': emojize('📚 Класична література'),
    'FICTION': emojize('📚 Фантастика'),
    'FANTASY': emojize('📚 Фенетезі'),
    'ROMANTIC_PROSE': emojize('📚 Романтична проза'),
    'Thriller': emojize('📚 Трилери та жахи'),
    'Mystery': emojize('📚 Детективи'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ Замовлення'),
    'X': emojize('❌'),
    'DOUWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLAY': '✅ Оформити замовлення',
    'COPY': '©️',
    'DATA': 'Напишіть, будь ласка, ПІБ отримувача, місто та відділення пошти для отримання',
    'THANKS': 'Дякуємо за замовлення! Найближчим часом з Вами зв\'яжеться наш менеджер '
}

CATEGORY = {
    'Mystery': 1,
    'Thriller': 2,
}

COMMANDS = {
    'START': "start",
    'HELP': "help",
}

