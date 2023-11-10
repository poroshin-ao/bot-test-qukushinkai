from aiogram import types, Router, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from internal.server.bot_init import bot_memb
from internal.logics.get_turnir import get_turnir_name_date, get_id_tur_by_num
from aiogram.filters import Command
from internal.logics.get_member import memb_is_exist, get_path_img_by_id
from internal.logics.get_member import get_spisok_to_win, get_m_id_by_tel_id
from internal.logics.set_member import set_memb_tel
from internal.logics.delete_member import delete_tel_id_by_m_id

router = Router()

class FSMMember(StatesGroup):
    turnir = State()
    get_memb = State()
    view_memb = State()
    set_view_memb = State()


@router.message(Command("start"))
async def select_turnir(message: types.Message, state: FSMContext):
    tur_data = get_turnir_name_date()
    buttons = []
    keyboard = []
    if len(tur_data) == 0:
        await bot_memb.send_message(message.from_user.id, "Турниров пока нет")
    for i in range(len(tur_data)):
        s = str(i+1)+". "+ str(tur_data[i][0])+"\n"
        s = s + str(tur_data[i][1]) + "\n"
        s = s + str(tur_data[i][2]) 
        await bot_memb.send_message(message.from_user.id, s)

        buttons.append(KeyboardButton(text=str(i+1)))

    for i in range(0,len(buttons),4):
        r = []
        for j in range(i,min(len(buttons),i+4)):
            r.append(buttons[j])
        keyboard.append(r)

    tur_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)
    await state.set_state(FSMMember.turnir)
    await message.answer("Выберите турнир", reply_markup=tur_keyboard)


@router.message(
    FSMMember.turnir
)
async def view_select(message: types.Message, state: FSMContext):

    data = await state.get_data()
    if message.text.isdigit(): 
        id = get_id_tur_by_num(int(message.text))
        if id == -1:
            await message.answer("Вы выбрали неправильный номер\n\n Попробуйте ещё раз")
            await state.clear()
            await select_turnir(message, state)
            return 
        await state.update_data(tur_id = id)
    elif not message.text.isdigit() and "tur_id" in data.keys():
        id = data["tur_id"]
    else:
        await message.answer("Вы выбрали неправильный номер\n\n Попробуйте ещё раз")
        await state.clear()
        await select_turnir(message, state)
        return
    
    await state.update_data(m_id = -1)
    m_id = get_m_id_by_tel_id(message.from_user.id)
    button_exist_memb = KeyboardButton(text = "Посмотреть статус участника по имени")
    button_otmena = KeyboardButton(text = "Отмена")
    if m_id is None:
        button_real_memb = KeyboardButton(text = "Указать себя как участника")
        keyboard = ReplyKeyboardMarkup(keyboard=[[button_exist_memb],[button_real_memb],[button_otmena]], resize_keyboard=True, one_time_keyboard=True)
    else:
        await state.update_data(m_id = m_id)
        button_real_memb = KeyboardButton(text = "Посмотреть информацию о своей категории")
        button_delete_reg = KeyboardButton(text = "Не учитывать аккаунт как аккаунт участника")
        keyboard = ReplyKeyboardMarkup(keyboard=[[button_exist_memb],[button_real_memb],[button_delete_reg],[button_otmena]], resize_keyboard=True, one_time_keyboard=True)
    await state.set_state(FSMMember.get_memb)
    await message.answer("Здесь вы можете посмотерть информацию по каждому учаснику турнира", reply_markup=keyboard)


@router.message(
    FSMMember.get_memb,
    F.text.lower() == "отмена"
)
async def view_otmena(message: types.Message, state: FSMContext):
    await select_turnir(message, state)


@router.message(
    FSMMember.get_memb,
    F.text.lower() == "посмотреть статус участника по имени"
)
async def get_name(message: types.Message, state: FSMContext):
    await state.set_state(FSMMember.view_memb)
    await state.update_data(m_id = -1)
    button_otmena = KeyboardButton(text = "Отмена")
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_otmena]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Введите фамилю и имя участника\n\n Пример:\n Иванов Иван", reply_markup=keyboard)

@router.message(
    FSMMember.get_memb,
    F.text.lower() == "указать себя как участника"
)
async def set_get_name(message: types.Message, state: FSMContext):
    await state.set_state(FSMMember.set_view_memb)
    button_otmena = KeyboardButton(text = "Отмена")
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_otmena]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Введите свою фамилию и имя\n\nПример:\nИванов Иван",reply_markup=keyboard)


@router.message(
    FSMMember.get_memb,
    F.text.lower() == "не учитывать аккаунт как аккаунт участника"
)
async def delete_tel_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    delete_tel_id_by_m_id(data["m_id"], message.from_user.id)
    await message.answer("Теперь ваш аккаунт не привязан к участнику")
    await view_select(message, state)
    

@router.message(
    FSMMember.get_memb,
    F.text.lower() == "посмотреть информацию о своей категории"
)
async def try_to_view(message: types.Message, state: FSMContext):
    m_id = (await state.get_data())["m_id"]
    if m_id == -1:
        await message.answer("Такого участника нет")
        await view_select(message, state)
        return
    await view_memb(message, state)


@router.message(
    FSMMember.view_memb,
    F.text.lower() == "отмена"
)
async def view_memb_otmena(message: types.Message, state: FSMMember):
    await view_select(message, state)


@router.message(
    FSMMember.view_memb
)
async def view_memb(message: types.Message, state: FSMContext):
    m_id = (await state.get_data())["m_id"]
    if m_id == -1:
        m_id = memb_is_exist(message.text)

    t_id = (await state.get_data())["tur_id"]
    if m_id is None:
        await message.answer("Такого участника нет")
        await state.set_state(FSMMember.get_memb)
        await get_name(message, state)
        return
    
    img_path = get_path_img_by_id(m_id)
    fight = get_spisok_to_win(t_id, m_id)
    photo = FSInputFile(".\storage\img_setka\setka_"+img_path)
    await message.answer_photo(photo=photo)

    if not fight is None:
        s = "Предстоящий бой номер "+ str(fight[1])
        s = s+ "\n\n" + str(fight[3]) +"\n---Против---\n" + str(fight[5])

        await bot_memb.send_message(message.from_user.id, text=s)
    await view_select(message, state)


@router.message(
    FSMMember.set_view_memb,
    F.text.lower() == "отмена"
)
async def set_view_memb_otmena(message: types.Message, state: FSMMember):
    await view_select(message, state)


@router.message(
    FSMMember.set_view_memb
)
async def set_view_memb(message: types.Message, state: FSMContext):
    m_id = memb_is_exist(message.text)


    t_id = (await state.get_data())["tur_id"]
    if m_id is None:
        await message.answer("Такого участника нет")
        await state.set_state(FSMMember.get_memb)
        await set_get_name(message, state)
        return

    set_memb_tel(m_id, message.from_user.id)    

    img_path = get_path_img_by_id(m_id)
    fight = get_spisok_to_win(t_id, m_id)
    photo = FSInputFile(".\storage\img_setka\setka_"+img_path)
    await message.answer_photo(photo=photo)

    if not fight is None:
        s = "Предстоящий бой номер "+ str(fight[1])
        s = s+ "\n\n" + str(fight[3]) +"\n---Против---\n" + str(fight[5])

        await bot_memb.send_message(message.from_user.id, text=s)
    await view_select(message, state)