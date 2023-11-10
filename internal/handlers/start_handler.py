from aiogram import types, Dispatcher, Router, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from internal.server.bot_init import bot
from internal.logics.get_turnir import get_turnir_name_date
import datetime
from aiogram.filters import Command

router = Router()

@router.message(Command(commands = ['start', 'Меню', 'меню']))
async def menu_command(message: types.Message):
    n_tur_b = KeyboardButton(text="/Новый_турнир")
    tur_b = KeyboardButton(text="/Турниры")
    menu_keyboard = ReplyKeyboardMarkup(keyboard=[[n_tur_b],[tur_b]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text = "TurnirManageBot готов к работе!", reply_markup=menu_keyboard)
