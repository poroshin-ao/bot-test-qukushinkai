from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
#from apscheduler.schedulers.asyncio import AsyncIOScheduler

storage = MemoryStorage()
storage_memb = MemoryStorage()

token = "6715263617:AAHPOJYm7opPFMguMoeHZfWd2Dd5n-Tmx28"
bot = Bot(token=token)
dp = Dispatcher(storage=storage)

token_memb = "6913065629:AAFVJoH4IG5ZnOYGjwvjmkPqQyWHm6z6VP0"
bot_memb = Bot(token=token_memb)
dp_memb = Dispatcher(storage=storage_memb)
#scheduler = AsyncIOScheduler()


