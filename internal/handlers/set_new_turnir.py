from aiogram import types, Dispatcher, Router
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from internal.server.bot_init import bot
from internal.logics.set_new_turnir import set_new_tur
import datetime
from aiogram.filters import Command
from internal.handlers.start_handler import menu_command


router = Router()

class FSMNewTurnir(StatesGroup):
    tur_name = State()
    tur_place = State()
    tur_date = State()
    tur_data = State()


time_format = "%Y-%m-%d %H:%M"

button_otmena = KeyboardButton(text = "/Отмена")

keyboard = ReplyKeyboardMarkup(keyboard=[[button_otmena]], resize_keyboard=True, one_time_keyboard=True)

@router.message(
        Command("Отмена"),
        FSMNewTurnir.tur_name

)
async def otmena1(message: types.Message, state: FSMContext):
    await menu_command(message)


@router.message(Command("Новый_турнир"))
async def command_new_turnir(message: types.Message, state: FSMContext):
    await state.set_state(FSMNewTurnir.tur_name)
    await bot.send_message(message.from_user.id,"Введите название турнира", reply_markup=keyboard)


@router.message(
        FSMNewTurnir.tur_name
)
async def load_tur_name(message: types.Message, state: FSMContext):
    await state.update_data(tur_name = message.text)
    await state.set_state(FSMNewTurnir.tur_place)
    await message.answer("Введите место турнира", reply_markup=keyboard)


@router.message(
        Command("Отмена"),
        FSMNewTurnir.tur_place

)
async def otmena2(message: types.Message, state: FSMContext):
    await menu_command(message)


@router.message(
        FSMNewTurnir.tur_place
)
async def load_tur_place(message: types.Message, state: FSMContext):
    await state.update_data(tur_place = message.text)
    await state.set_state(FSMNewTurnir.tur_date)
    await message.answer("Введите дату проведения в формате \"Год-Месяц-День Часы:Минуты\" (Пример: 2024-01-01 01:09)", reply_markup=keyboard)


@router.message(
        Command("Отмена"),
        FSMNewTurnir.tur_date

)
async def otmena3(message: types.Message, state: FSMContext):
    await menu_command(message)


@router.message(
        FSMNewTurnir.tur_date
)
async def load_tur_date(message: types.Message, state: FSMContext):
    dt = 0
    try:
        dt = datetime.datetime.strptime(message.text, time_format)
    except Exception:
        await state.set_state(FSMNewTurnir.tur_date)
        await message.reply("Ввели дату в неправильном формате\nВведите дату проведения в формате \"Год-Месяц-День Часы:Минуты\" (Пример: 2024-01-01 01:09)", reply_markup=keyboard)
        return
    await state.update_data(tur_date = dt)
    await state.set_state(FSMNewTurnir.tur_data)
    await message.answer("Загрузите файл турнира", reply_markup=keyboard)


@router.message(
        Command("Отмена"),
        FSMNewTurnir.tur_data

)
async def otmena4(message: types.Message, state: FSMContext):
    await menu_command(message)


@router.message(
        FSMNewTurnir.tur_data
)
async def load_tur_data(message: types.Message, state: FSMContext):
    file = await bot.get_file(message.document.file_id)
    await state.update_data(tur_data_path = file.file_path, tur_data_id = message.document.file_id)
    data = await state.get_data()
    img_paths = await set_new_tur(data)

    await state.clear()
    for i in img_paths:
        photo = FSInputFile(".\storage\img_setka\setka_"+i)
        await bot.send_photo(message.from_user.id, photo=photo)
    
    await message.answer("Турнир загружен в базу")
    await menu_command(message)
