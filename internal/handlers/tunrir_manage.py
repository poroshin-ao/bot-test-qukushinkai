from aiogram import types, Dispatcher, Router, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from internal.server.bot_init import bot, bot_memb
from internal.logics.get_turnir import get_turnir_name_date, get_id_tur_by_num
import datetime
from aiogram.filters import Command
from internal.handlers.start_handler import menu_command
from internal.logics.get_turnir import get_path_setki, get_turnir_data_by_id
from internal.logics.delete_turnir import delete_tur_by_id
from internal.logics.get_fight import get_spisok_to_win
from internal.logics.set_turnir import set_winner_db
from internal.logics.get_fight import get_last_2_and_5_fight
from internal.logics.get_member import get_tel_id_by_m_id


router = Router()

class FSMTurManage(StatesGroup):
    turnirs = State()
    tur_manage = State()
    tur_delete = State()
    set_winer = State()
    
@router.message(Command("Турниры"))
async def select_turnir(message: types.Message, state: FSMContext):
    tur_data = get_turnir_name_date()
    buttons = []
    keyboard = []
    for i in range(len(tur_data)):
        s = str(i+1)+". "+ str(tur_data[i][0])+"\n"
        s = s + str(tur_data[i][1]) + "\n"
        s = s + str(tur_data[i][2]) 
        await bot.send_message(message.from_user.id, s)

        buttons.append(KeyboardButton(text=str(i+1)))

    for i in range(0,len(buttons),4):
        r = []
        for j in range(i,min(len(buttons),i+4)):
            r.append(buttons[j])
        keyboard.append(r)
    otmena = KeyboardButton(text="Отмена") 
    keyboard.append([otmena])
    tur_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)
    await state.set_state(FSMTurManage.turnirs)
    await bot.send_message(message.from_user.id, "Выберите турнир", reply_markup=tur_keyboard)


@router.message(
    FSMTurManage.turnirs,
    F.text.lower() == "отмена"
)
async def tur_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await menu_command(message)


@router.message(
    FSMTurManage.turnirs
)
async def tur_manage(message: types.Message, state: FSMContext):
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

    button_photo = KeyboardButton(text = "Турнирные сетки")
    button_make_winer = KeyboardButton(text = "Выбрать победителей боёв")
    button_delete_tur = KeyboardButton(text = "Удалить турнир")
    button_otmena = KeyboardButton(text = "Отмена")

    await state.update_data(f_num = 0)

    keyboard = [[button_photo], [button_make_winer], [button_delete_tur], [button_otmena]]
    tur_manage_keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False) 
    await state.set_state(FSMTurManage.tur_manage)
    await message.answer("Инструменты для работы с "+str(id)+" турниром", reply_markup=tur_manage_keyboard)


@router.message(
    FSMTurManage.tur_manage,
    F.text.lower() == "отмена"
)
async def tur_manage_cancel(message: types.Message, state: FSMContext):
    await select_turnir(message, state)


@router.message(
    FSMTurManage.tur_manage,
    F.text.lower() == "турнирные сетки"
)
async def tur_setki(message: types.Message, state: FSMContext):
    data = await state.get_data()
    img_paths = get_path_setki(data["tur_id"])
    for img in img_paths:
        photo = FSInputFile(".\storage\img_setka\setka_"+img+".jpg")
        await bot.send_photo(message.from_user.id, photo=photo)


@router.message(
    FSMTurManage.tur_manage,
    F.text.lower() == "удалить турнир"
)
async def proof_del_turnir(message: types.Message, state: FSMContext):
    button_ok = KeyboardButton(text = "Удалить")
    button_otmena = KeyboardButton(text = "Отмена")
    del_keyboard = ReplyKeyboardMarkup(keyboard=[[button_ok],[button_otmena]], resize_keyboard=True, one_time_keyboard=True)
    id = (await state.get_data())["tur_id"]
    tur = get_turnir_data_by_id(id)
    s = str(tur[0])+"\n"+str(tur[1])+"\n"+str(tur[2])
    await state.set_state(FSMTurManage.tur_delete)
    await message.answer("Вы точно хотите удалить турнир?\n"+s, reply_markup=del_keyboard)


@router.message(
    FSMTurManage.tur_delete,
    F.text.lower() == "отмена"
)
async def not_delete_tur(message: types.Message, state: FSMContext):
    await tur_manage(message, state)


@router.message(
    FSMTurManage.tur_delete,
    F.text.lower() == "удалить"
)
async def delete_tur(message: types.Message, state: FSMContext):
    id = (await state.get_data())["tur_id"]
    delete_tur_by_id(id)
    await message.answer("Турнир удалён")
    await select_turnir(message, state)


@router.message(
    FSMTurManage.tur_manage,
    F.text.lower() == "выбрать победителей боёв"
)
async def set_winner(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id = data["tur_id"]
    f_num = data["f_num"]
    data_win = get_spisok_to_win(id, f_num)
    if data_win is None:
        await message.answer("Все бои были проведены")
        await tur_manage(message, state)
        return
    await state.update_data(d = data_win)
    s = "Выберите победителя\n"
    s = s + "Бой "+str(data_win[1])+"\n\n"
    s = s + "1. " + str(data_win[3])+"\n"
    s = s + "2. " + str(data_win[5])+"\n"

    button1 = KeyboardButton(text = "1 участник")
    button2 = KeyboardButton(text = "2 участник")
    button_sled = KeyboardButton(text = "Следующий")
    button_otmena = KeyboardButton(text = "Отмена")

    keyboard = ReplyKeyboardMarkup(keyboard = [[button1,button2],[button_sled, button_otmena]], resize_keyboard = True, one_time_keyboard=True)

    await state.set_state(FSMTurManage.set_winer)
    await message.answer(s, reply_markup = keyboard)

@router.message(
    FSMTurManage.set_winer,
    F.text.lower() == "1 участник"
)
async def make_winner_1(message: types.Message, state: FSMContext):
    data = (await state.get_data())["d"]
    tur_id = (await state.get_data())["tur_id"]
    img_path = set_winner_db(data[0], data[2], tur_id)
    photo = FSInputFile(".\storage\img_setka\setka_"+img_path)

    l25 = get_last_2_and_5_fight(tur_id)

    if not l25 is None:
        if not l25[0] is None:
            l2 = l25[0]
            
            for mid in l2:
                tel_m1 = get_tel_id_by_m_id(mid[0])

                for tel_id in tel_m1:
                    await bot_memb.send_message(tel_id[0],"Готовтесь!\n\n Через 2 боя начнется ваш бой")


        if not l25[1] is None: 
            l5 = l25[1]
            
            for mid in l5:
                tel_m1 = get_tel_id_by_m_id(mid[0])
            
                for tel_id in tel_m1:
                    await bot_memb.send_message(tel_id[0],"Готовтесь!\n\n Через 5 боёв начнется ваш бой")

    await message.answer_photo(photo=photo)
    await set_winner(message, state)


@router.message(
    FSMTurManage.set_winer,
    F.text.lower() == "2 участник"
)
async def make_winner_2(message: types.Message, state: FSMContext):
    data = (await state.get_data())["d"]
    tur_id = (await state.get_data())["tur_id"]
    img_path = set_winner_db(data[0], data[4], tur_id)
    photo = FSInputFile(".\storage\img_setka\setka_"+img_path)

    l25 = get_last_2_and_5_fight(tur_id)

    if not l25 is None:
        if not l25[0] is None:
            l2 = l25[0]
            
            for mid in l2:
                tel_m1 = get_tel_id_by_m_id(mid[0])
                print(tel_m1)
                for tel_id in tel_m1:
                    await bot_memb.send_message(tel_id[0],"Готовтесь!\n\n Через 2 боя начнется ваш бой")


        if not l25[1] is None: 
            l5 = l25[1]
            
            for mid in l5:
                tel_m1 = get_tel_id_by_m_id(mid[0])
                for tel_id in tel_m1:
                    await bot_memb.send_message(tel_id[0],"Готовтесь!\n\n Через 5 боёв начнется ваш бой")

    await message.answer_photo(photo=photo)
    await set_winner(message, state)

@router.message(
    FSMTurManage.set_winer,
    F.text.lower() == "следующий"
)
async def sled_winner(message: types.Message, state: FSMContext):
    f_num = await state.get_data()
    await state.update_data(f_num = (f_num["f_num"]+1))
    await set_winner(message, state)

@router.message(
    FSMTurManage.set_winer,
    F.text.lower() == "отмена"
)
async def otmena_winner(message: types.Message, state: FSMContext):
    await state.update_data(f_num = 0)
    await tur_manage(message, state)