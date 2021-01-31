from environs import Env
from utils.db_api.db import Base
# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str

IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
