from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from services.logicWrapper import *
from messages import *
from random import randint
from services.apiWrapper import *


class AdminChangeParameter(StatesGroup):
    value = State()
class dannie_pay(StatesGroup):
    people=State()

class UserCreateRequest(StatesGroup):
    name = State()
    area = State()
    wifi = State()
    internal_model = State()
    external_model = State()
    wall_material = State()
    comments = State()
    plan = State()
    email = State()


class AdminChangeText(StatesGroup):
    value = State()


class AdminFinishWork(StatesGroup):
    ceiling_ar = State()
    wall_ar = State()
    omni_ar = State()
    sector_ar = State()
    result = State()


class AdminNews(StatesGroup):
    buttons = State()
    text = State()


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def get_markup(text):
    text = text.replace("\\n", "\n")
    markup = types.InlineKeyboardMarkup()
    for line in text.split("\n"):
        buttons = line.split("|")
        button_obj = []
        for button in buttons:
            name, value = button.split("](")
            name = name[1:]
            value = value[:-1]
            if "http" in value:
                button_obj.append(types.InlineKeyboardButton(name, url=value))
            else:
                button_obj.append(types.InlineKeyboardButton(name, callback_data=value))
        markup.add(*button_obj)
    return markup


async def send_support(chat_id):
    msg = get_text(47)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(get_text(48), get_setting(19)))
    await bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)


async def send_information(chat_id):
    await send_main_keyboard(chat_id, get_text(15))


async def send_admin_texts(chat_id, page_index, msg_id=None):
    texts = get_texts()
    need_texts = texts[page_index * MAX_ELS_IN_PAGE:(page_index + 1) * MAX_ELS_IN_PAGE]
    next_texts = texts[(page_index + 1) * MAX_ELS_IN_PAGE:(page_index + 2) * MAX_ELS_IN_PAGE]
    msg = "Текста:\n\n"
    markup = types.InlineKeyboardMarkup()
    for text in need_texts:
        msg += f"<b>{text[1]}:</b>\n{text[2]}\n\n"
        markup.add(types.InlineKeyboardButton(f"Сменить '{text[1]}'", callback_data=f"admin_changetext_{text[0]}"))
    buttons = []
    if page_index != 0:
        buttons.append(types.InlineKeyboardButton(LEFT, callback_data=f"admin_texts_{page_index - 1}"))
    if len(next_texts) > 0:
        buttons.append(types.InlineKeyboardButton(RIGHT, callback_data=f"admin_texts_{page_index + 1}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton(RETURN_BUTTON, callback_data=f"admin_return"))
    await bot.edit_message_text(msg, chat_id, msg_id, reply_markup=markup, parse_mode="HTML")


async def send_admin_users(chat_id, page_index, msg_id=None):
    users = get_all_users()
    need_users = users[page_index * MAX_ELS_IN_PAGE:(page_index + 1) * MAX_ELS_IN_PAGE]
    next_users = users[(page_index + 1) * MAX_ELS_IN_PAGE:(page_index + 2) * MAX_ELS_IN_PAGE]
    count = page_index * MAX_ELS_IN_PAGE
    msg = "Пользователи:\n\n"
    markup = types.InlineKeyboardMarkup()
    for user in need_users:
        count += 1
        msg += f"{count}) @{user[2]} ({user[1]})\n"
    buttons = []
    if page_index != 0:
        buttons.append(types.InlineKeyboardButton(LEFT, callback_data=f"admin_users_{page_index - 1}"))
    if len(next_users) > 0:
        buttons.append(types.InlineKeyboardButton(RIGHT, callback_data=f"admin_users_{page_index + 1}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton(RETURN_BUTTON, callback_data=f"admin_return"))
    await bot.edit_message_text(msg, chat_id, msg_id, reply_markup=markup, parse_mode="HTML")


async def send_request_check_to_admin(request_id, msg_id=None):
    request = get_request_by_id(request_id)
    user = get_user_by_id(request[1])
    msg = get_text(32)
    if request[13] not in [None, 'None', '']:
        msg = f"{msg}\n{get_text(36)}"
        try:
            manager = get_user_by_id(request[13])
            msg = msg.replace('{MANAGER_ID}', str(manager[1]))
            msg = msg.replace('{MANAGER_USERNAME}', str(manager[2]))
        except Exception:
            pass
    if request[15] not in [None, 'None', '']:

        msg = f"{msg}\n{get_text(40)}"
        msg = msg.replace('{RESULT}', str(request[15]))
    msg = msg.replace('{USER_ID}', str(user[1]))
    msg = msg.replace('{USERNAME}', str(user[2]))
    msg = msg.replace('{REQUEST_ID}', str(request_id))
    msg = msg.replace('{NAME}', str(request[2]))
    msg = msg.replace('{AREA}', str(request[3]))
    msg = msg.replace('{INTERNAL_MODEL}', str(request[4]))
    msg = msg.replace('{EXTERNAL_MODEL}', str(request[5]))
    msg = msg.replace('{WALL_MATERIAL}', str(request[6]))
    msg = msg.replace('{COMMENTS}', str(request[7]))
    msg = msg.replace('{PLAN}', str(request[8]))
    msg = msg.replace('{PRICE}', str(request[9]))
    msg = msg.replace('{EMAIL}', str(request[10]))
    msg = msg.replace("{WIFI}", str(request[17]))
    markup = types.InlineKeyboardMarkup()
    if request[16] == 0:
        msg = msg.replace('{STATUS}', get_text(33))
        markup.add(types.InlineKeyboardButton(get_text(37), callback_data=f"takework_{request_id}"))
    elif request[16] == 1:
        msg = msg.replace('{STATUS}', get_text(34))
        markup.add(types.InlineKeyboardButton(get_text(38), callback_data=f"finishwork_{request_id}"))
    elif request[16] == 2:
        msg = msg.replace('{STATUS}', get_text(35))
    if msg_id is None:
        msg = await bot.send_message(get_setting(18), msg, parse_mode="HTML", reply_markup=markup)
        change_request_parametr(request_id, 'manager_msg_id', msg.message_id)
    else:
        await bot.edit_message_text(msg, get_setting(18), msg_id, parse_mode="HTML", reply_markup=markup)


async def send_request_check(chat_id, request_id):
    request = get_request_by_id(request_id)
    msg = get_text(24)
    msg = msg.replace('{NAME}', str(request[2]))
    msg = msg.replace('{AREA}', str(request[3]))
    msg = msg.replace('{INTERNAL_MODEL}', str(request[4]))
    msg = msg.replace('{EXTERNAL_MODEL}', str(request[5]))
    msg = msg.replace('{WALL_MATERIAL}', str(request[6]))
    msg = msg.replace('{COMMENTS}', str(request[7]))
    msg = msg.replace('{PLAN}', str(request[8]))
    msg = msg.replace('{PRICE}', str(request[9]))
    msg = msg.replace('{EMAIL}', str(request[10]))
    msg = msg.replace("{WIFI}", str(request[17]))

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(get_text(49), callback_data=f"acceptpay_{request_id}"))
    markup.add(types.InlineKeyboardButton(get_text(29), callback_data=f"cancelpay_{request_id}"))
    await bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=markup)


async def send_admin_parameters(chat_id, page_index, msg_id=None):
    parameters = get_parameters()
    need_parameters = parameters[page_index * MAX_ELS_IN_PAGE:(page_index + 1) * MAX_ELS_IN_PAGE]
    next_parameters = parameters[(page_index + 1) * MAX_ELS_IN_PAGE:(page_index + 2) * MAX_ELS_IN_PAGE]
    msg = "Параметры:\n\n"
    markup = types.InlineKeyboardMarkup()
    for parameter in need_parameters:
        msg += f"{parameter[1]}: {parameter[3]} (тип: {parameter[2]})\n"
        markup.add(types.InlineKeyboardButton(f"Сменить '{parameter[1]}'",
                                              callback_data=f"admin_changeparameter_{parameter[0]}"))
    buttons = []
    if page_index != 0:
        buttons.append(types.InlineKeyboardButton(LEFT, callback_data=f"admin_parameters_{page_index - 1}"))
    if len(next_parameters) > 0:
        buttons.append(types.InlineKeyboardButton(RIGHT, callback_data=f"admin_parameters_{page_index + 1}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton(RETURN_BUTTON, callback_data=f"admin_return"))
    await bot.edit_message_text(msg, chat_id, msg_id, reply_markup=markup)


@dp.message_handler(state=AdminChangeParameter.value,
                    content_types=['text', 'photo', 'video', 'voice', 'document', 'animation'])
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    if text == REJECT_BUTTON:
        await send_main_keyboard(chat_id, ACTION_REJECTED)
        await state.finish()
        return
    async with state.proxy() as state_data:
        parameter_id = state_data["parameter_id"]
    parameter = get_parameter_obj(parameter_id)
    parameter_type = parameter[2]
    if parameter_type == 'text':
        if message.content_type == 'text':
            value = text
        else:
            await bot.send_message(chat_id, "Неправильный формат сообщения! Пришлите текст!")
            return
    elif parameter_type == 'photo':
        if message.content_type == 'photo':
            value = message.photo[-1].file_id
        else:
            await bot.send_message(chat_id, "Неправильный формат сообщения! Пришлите фото!")
            return
    elif parameter_type == 'video':
        if message.content_type == 'video':
            value = message.video.file_id
        else:
            await bot.send_message(chat_id, "Неправильный формат сообщения! Пришлите видео!")
            return
    elif parameter_type == 'document':
        if message.content_type == 'document':
            value = message.document.file_id
        else:
            await bot.send_message(chat_id, "Неправильный формат сообщения! Пришлите документ!")
            return
    elif parameter_type == 'animation':
        if message.content_type == 'animation':
            value = message.animation.file_id
        else:
            await bot.send_message(chat_id, "Неправильный формат сообщения! Пришлите гиф!")
            return
    elif parameter_type == 'integer':
        try:
            value = int(text)
        except Exception:
            await bot.send_message(chat_id, "Неправильный формат сообщения! Пришлите число!")
            return
    elif parameter_type == 'float':
        try:
            value = float(text)
        except Exception:
            await bot.send_message(chat_id, "Неправильный формат сообщения! Пришлите дробное число!")
            return
    elif parameter_type == 'attachment':
        if message.content_type == 'photo':
            value = f"photo {message.photo[-1].file_id}"
        elif message.content_type == 'video':
            value = f"video {message.video.file_id}"
        elif message.content_type == 'voice':
            value = f"voice {message.voice.file_id}"
        else:
            await bot.send_message(chat_id, "Неправильный формат сообщения! Пришлите приложение!")
            return
    else:
        value = text
    if set_setting(parameter_id, value):
        await bot.send_message(chat_id, f"Парамтер обновлён!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(state=AdminChangeText.value)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == REJECT_BUTTON:
        await bot.send_message(chat_id, ACTION_REJECTED)
        await state.finish()
        return
    async with state.proxy() as state_data:
        text_id = state_data["text_id"]
    if set_text(text_id, text):
        await bot.send_message(chat_id, f"Текст обновлён!")
    await state.finish()


@dp.message_handler(state=AdminFinishWork.ceiling_ar)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    async with state.proxy() as state_data:
        state_data["ceiling_ar"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(52), parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
    await AdminFinishWork.wall_ar.set()


@dp.message_handler(state=AdminFinishWork.wall_ar)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    async with state.proxy() as state_data:
        state_data["wall_ar"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(53), parse_mode="HTML")
    await AdminFinishWork.omni_ar.set()


@dp.message_handler(state=AdminFinishWork.omni_ar)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    async with state.proxy() as state_data:
        state_data["omni_ar"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(54), parse_mode="HTML")
    await AdminFinishWork.sector_ar.set()


@dp.message_handler(state=AdminFinishWork.sector_ar)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    async with state.proxy() as state_data:
        state_data["sector_ar"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(39), parse_mode="HTML")
    await AdminFinishWork.result.set()


@dp.message_handler(state=AdminFinishWork.result)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    async with state.proxy() as state_data:
        state_data["result"] = message.text
    async with state.proxy() as state_data:
        request_id = state_data["request_id"]
        ceiling_ar = state_data["ceiling_ar"]
        wall_ar = state_data["wall_ar"]
        sector_ar = state_data["sector_ar"]
        result = state_data["result"]
        omni_ar = state_data["omni_ar"]

    change_request_parametr(request_id, 'status', 2)
    change_request_parametr(request_id, 'result', result)
    change_request_parametr(request_id, 'ceiling_ar', ceiling_ar)
    change_request_parametr(request_id, 'wall_ar', wall_ar)
    change_request_parametr(request_id, 'sector_ar', sector_ar)
    change_request_parametr(request_id, 'omni', omni_ar)
    await state.finish()
    request = get_request_by_id(request_id)
    msg = get_text(41)
    msg = msg.replace('{number}', str(request[0]))
    msg = msg.replace('{ceiling_ar}', str(request[18]))
    msg = msg.replace('{wall_ar}', str(request[19]))
    msg = msg.replace('{omni}', str(request[20]))
    msg = msg.replace('{sector_ar}', str(request[21]))
    msg = msg.replace('{RESULT}', str(request[15]))
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Все верно отправить заказчику", callback_data=f"acceptsend_{request_id}"))
    markup.add(types.InlineKeyboardButton("Отмена", callback_data=f"cancellsend_{request_id}"))
    await bot.send_message(chat_id, f"{msg}\n Все верно?", reply_markup=markup)


@dp.message_handler(state=UserCreateRequest.name)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == get_text(17):
        await send_main_keyboard(chat_id, get_text(1))
        await state.finish()
        return
    async with state.proxy() as state_data:
        state_data["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(18), reply_markup=keyboard, parse_mode="HTML")
    await UserCreateRequest.area.set()


@dp.message_handler(state=UserCreateRequest.area)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == get_text(17):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(45), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.name.set()
        return
    try:
        area = int(message.text)
    except Exception:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(23), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.area.set()
        return
    if area < 0:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(23), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.area.set()
        return
    async with state.proxy() as state_data:
        state_data["area"] = area
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(50), reply_markup=keyboard, parse_mode="HTML")
    await UserCreateRequest.wifi.set()


@dp.message_handler(state=UserCreateRequest.wifi)
async def agent_registration_wifi(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text

    if text == get_text(17):
        print(text)
        print("if")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(20), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.plan.set()
        return
    elif text == "Да" or text == "да":

        async with state.proxy() as state_data:
            state_data["wifi"] = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(19), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.internal_model.set()
    elif text == "Нет" or text == "нет":

        async with state.proxy() as state_data:
            state_data["wifi"] = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(19), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.internal_model.set()
    else:

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(56), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.wifi.set()
        return


@dp.message_handler(state=UserCreateRequest.internal_model)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == get_text(17):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(18), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.area.set()
        return
    async with state.proxy() as state_data:
        state_data["internal_model"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(44), reply_markup=keyboard, parse_mode="HTML")
    await UserCreateRequest.external_model.set()


@dp.message_handler(state=UserCreateRequest.external_model)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == get_text(17):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(19), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.internal_model.set()
        return
    async with state.proxy() as state_data:
        state_data["external_model"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(20), reply_markup=keyboard, parse_mode="HTML")
    await UserCreateRequest.wall_material.set()


@dp.message_handler(state=UserCreateRequest.wall_material)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == get_text(17):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(44), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.external_model.set()
        return
    async with state.proxy() as state_data:
        state_data["wall_material"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(21), reply_markup=keyboard, parse_mode="HTML")
    await UserCreateRequest.comments.set()


@dp.message_handler(state=UserCreateRequest.comments)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == get_text(17):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(20), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.wall_material.set()
        return
    async with state.proxy() as state_data:
        state_data["comments"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(22), reply_markup=keyboard, parse_mode="HTML")
    await UserCreateRequest.plan.set()


@dp.message_handler(state=UserCreateRequest.plan)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == get_text(17):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(21), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.comments.set()
        return
    async with state.proxy() as state_data:
        state_data["plan"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(26), reply_markup=keyboard, parse_mode="HTML")
    await UserCreateRequest.email.set()


@dp.message_handler(state=UserCreateRequest.email)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    if text == get_text(17):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(21), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.comments.set()
        return
    email = message.text.replace("'", '`')
    if "" not in email or '' not in email:  # убрал проверку емейла
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(27), reply_markup=keyboard, parse_mode="HTML")
        return
    async with state.proxy() as state_data:
        name = state_data["name"].replace("'", '`')
        area = state_data["area"]
        wifi = state_data["wifi"].replace("'", '`')
        internal_model = state_data["internal_model"].replace("'", '`')
        external_model = state_data["external_model"].replace("'", '`')
        wall_material = state_data["wall_material"].replace("'", '`')
        comments = state_data["comments"].replace("'", '`')
        plan = state_data["plan"].replace("'", '`')
    request_id = create_request(chat_id, name, area, wifi, internal_model, external_model, wall_material, comments,
                                plan, email)
    price = get_price(area, wifi)
    change_request_parametr(request_id, 'price', price)
    # zyookassa_id, yookassa_link = create_payment_link(price, email)
    # change_request_parametr(request_id, 'yookassa_id', yookassa_id)
    # change_request_parametr(request_id, 'yookassa_link', yookassa_link)
    await send_request_check(chat_id, request_id)
    await state.finish()


@dp.message_handler(state=AdminNews.buttons)
async def send(message: types.Message, state: FSMContext):
    if message.text == REJECT_BUTTON:
        await send_main_keyboard(message.chat.id, ACTION_REJECTED)
        await state.finish()
        return
    if message.text == SKIP_BUTTON:
        markup = types.InlineKeyboardMarkup()
        user_markup = types.InlineKeyboardMarkup()
    else:
        try:
            markup = get_markup(message.text)
            user_markup = get_markup(message.text)
        except Exception as e:
            markup = types.InlineKeyboardMarkup()
            user_markup = types.InlineKeyboardMarkup()
    async with state.proxy() as state_data:
        state_data["markup"] = markup
        state_data["user_markup"] = user_markup
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(REJECT_BUTTON)
    await bot.send_message(message.chat.id, "Введите сообщение:", reply_markup=keyboard)
    await AdminNews.text.set()

@dp.message_handler(state=dannie_pay.people)
async def agent_registration_fio(message: types.Message, state: FSMContext):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.html_text
    async with state.proxy() as state_data:
        state_data["people"] = message.text
    async with state.proxy() as state_data:
        request_id = state_data["request_id"]
        people = state_data["people"]
    change_request_parametr(request_id, 'who_pay', people)
    request = get_request_by_id(request_id)
    msg = get_text(59)
    msg = msg.replace('{number}', str(request[0]))
    msg = msg.replace('{PRICE}', str(request[9]))
    msg = msg.replace('{who_pay}', str(request[22]))
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перевод получен", callback_data=f"acceptitogpay_{request_id}"))
    await bot.send_message(chat_id, "Проверяем оплату")
    await bot.send_message(get_setting(18), msg, reply_markup=markup, parse_mode="HTML")
    await state.finish()


@dp.message_handler(state=AdminNews.text, content_types=["text", "photo", "video", "animation", 'voice', 'video_note'])
async def send(message: types.Message, state: FSMContext):
    try:
        if message.text == REJECT_BUTTON:
            await send_main_keyboard(message.chat.id, ACTION_REJECTED)
            await state.finish()
            return
    except Exception:
        pass
    async with state.proxy() as state_data:
        user_markup = state_data["user_markup"]
        admin_markup = state_data["markup"]
    users = get_all_users()
    keyboard = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, "Рассылка начата!", reply_markup=keyboard)
    await state.finish()
    news_id = randint(1, 1000000)
    count = 0
    admin_markup.add(types.InlineKeyboardButton("Удалить сообщения", callback_data=f"admindeletenews_{news_id}"))
    for user in users:
        try:
            if int(user[1]) == ADMIN_IDS[0]:
                markup = admin_markup
            else:
                markup = user_markup
            if message.content_type == "text":
                msg = await bot.send_message(user[1], message.html_text, parse_mode="HTML", reply_markup=markup)
            elif message.content_type == "photo":
                if message.caption is not None:
                    msg = await bot.send_photo(user[1], message.photo[-1].file_id, caption=message.html_text,
                                               parse_mode="HTML", reply_markup=markup)
                else:
                    msg = await bot.send_photo(user[1], message.photo[-1].file_id)
            elif message.content_type == "video":
                if message.caption is not None:
                    msg = await bot.send_video(user[1], message.video.file_id, caption=message.html_text,
                                               parse_mode="HTML",
                                               reply_markup=markup)
                else:
                    msg = await bot.send_video(user[1], message.video.file_id, parse_mode="HTML", reply_markup=markup)
            elif message.content_type == "animation":
                if message.caption is not None:
                    msg = await bot.send_animation(user[1], message.animation.file_id, caption=message.html_text,
                                                   parse_mode="HTML", reply_markup=markup)
                else:
                    msg = await bot.send_animation(user[1], message.animation.file_id, parse_mode="HTML",
                                                   reply_markup=markup)
            elif message.content_type == 'voice':
                msg = await bot.send_voice(user[1], message.voice.file_id)
            elif message.content_type == 'video_note':
                msg = await bot.send_voice(user[1], message.video_note.file_id)
            count += 1
            add_news(news_id, user[1], msg.message_id)
        except Exception:
            pass
    await bot.send_message(message.chat.id, f"Рассылка закончена! Рассылку получили {count} человек!")


async def send_main_keyboard(chat_id, text=MAIN_MENU_MESSAGE):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(get_text(16))
    keyboard.add(get_text(14), get_text(46))
    await bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='HTML')


async def send_admin_keyboard(chat_id, msg_id=None):
    if chat_id in ADMIN_IDS:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Параметры", callback_data=f"admin_parameters_0"))
        markup.add(types.InlineKeyboardButton("Текста", callback_data=f"admin_texts_0"))
        markup.add(types.InlineKeyboardButton("Cтатистика", callback_data='admin_stat'))
        markup.add(types.InlineKeyboardButton("Пользователи", callback_data='admin_users_0'))
        markup.add(types.InlineKeyboardButton("Рассылка", callback_data='admin_news'))
        if msg_id is None:
            await bot.send_message(chat_id, "Админ-панель:", reply_markup=markup)
        else:
            await bot.edit_message_text("Админ-панель:", chat_id, msg_id, reply_markup=markup)


@dp.callback_query_handler()
async def query_show_list(call: types.CallbackQuery, state: FSMContext):
    logging_message(call.from_user.id, call.from_user.username, call.data)
    chat_id, username, data = call.from_user.id, call.from_user.username, call.data
    if data == "admin_return":
        await send_admin_keyboard(chat_id, call.message.message_id)
    elif "admindeletenews_" in data:
        news_id = int(data.split("_")[1])
        messages = get_news_messages(news_id)
        await bot.send_message(chat_id, "Начинаю удалять рассылку!")
        for message in messages:
            try:
                await bot.delete_message(message[2], message[3])
            except Exception as e:
                print(str(e))
        await bot.send_message(chat_id, "Рассылка удалена!")
    elif "admin_changeparameter_" in data:
        parameter_id = data.split("_")[2]
        parameter = get_parameter(parameter_id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(REJECT_BUTTON)
        await AdminChangeParameter.value.set()
        await bot.send_message(chat_id, f"Введите новое значение параметра '{parameter[1]}':", reply_markup=keyboard)
        async with state.proxy() as state_data:
            state_data["parameter_id"] = parameter_id
    elif "admin_texts_" in data:
        page_index = int(data.split("_")[2])
        await send_admin_texts(chat_id, page_index, call.message.message_id)
    elif "admin_parameters_" in data:
        page_index = int(data.split("_")[2])
        await send_admin_parameters(chat_id, page_index, call.message.message_id)
    elif "admin_users_" in data:
        page_index = int(data.split("_")[2])
        await send_admin_users(chat_id, page_index, call.message.message_id)
    elif "admin_changetext_" in data:
        text_id = data.split("_")[2]
        text = get_text_obj(text_id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(REJECT_BUTTON)
        await AdminChangeText.value.set()
        await bot.send_message(chat_id,
                               f"Введите новое значение текста '{text[1]}'\n\n<b>Действующий текст</b>:\n{text[2]}",
                               reply_markup=keyboard, parse_mode="HTML")
        async with state.proxy() as state_data:
            state_data["text_id"] = text_id
    elif data == "admin_stat":
        users = get_all_users()
        await bot.send_message(chat_id, f"Статистика:\n\nКоличество пользователей - {len(users)}")
    elif data == "admin_news":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(REJECT_BUTTON, SKIP_BUTTON)
        await bot.send_message(chat_id, "Введите клавиатуру:", reply_markup=keyboard)
        await AdminNews.buttons.set()
    elif "cancelpay_" in data:
        request_id = int(data.split("_")[1])
        print(request_id)
        change_request_parametr(request_id, 'status', -1)
        await bot.delete_message(chat_id, call.message.message_id)
        await send_main_keyboard(chat_id, get_text(30))
    elif "acceptpay_" in data:
        request_id = int(data.split("_")[1])
        async with state.proxy() as state_data:
            state_data["request_id"] = request_id
        request = get_request_by_id(request_id)
        await send_main_keyboard(chat_id, get_text(43))
        await bot.delete_message(chat_id, call.message.message_id)
        print("dota")
        await send_request_check_to_admin(request_id)
        print("dota")

        msg = get_text(62)
        msg = msg.replace('{area}', str(request[3]))
        price_area = msg
        price_area = math.ceil(int(price_area) / 1000)
        price_area = price_area * 15

        msg = get_text(63)
        msg = msg.replace('{WIFI}', str(request[17]))
        price_wifi = msg
        if price_wifi == "Да" or price_wifi == "да":
            price_wifi = 15
        else:
            price_wifi = 0
        print(price_wifi)
        print(price_area)
        print("SOVA")
        msg = get_text(57)
        msg = msg.replace('{number}', str(request[0]))
        msg = msg.replace('{area}', str(request[3]))
        msg = msg.replace('{NAME}', str(request[2]))
        msg = msg.replace('{price_area}', str(price_area))
        msg = msg.replace('{price_wifi}', str(price_wifi))
        msg = msg.replace('{PRICE}', str(request[9]))
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Оплатил✅", callback_data=f"acceptcheckpaytwo_{request_id}"))
        await bot.send_message(chat_id, msg, reply_markup=markup, parse_mode='HTML')
        # await bot.send_message(chat_id, "🔗<b> Сеть TRC20</b>", parse_mode='HTML')
        # await bot.send_message(chat_id, "TY2L2hKrjpporWDUeDxUmuXHyKFC2UEXHX")
        # await bot.send_message(chat_id, "🔗<b>Сеть TON</b>", parse_mode='HTML')
        # await bot.send_message(chat_id, "UQC6HSSd17-126M3EwHYVo-STS2gUDjtSCWh7UIUdDVu6KUi")

    elif "acceptcheckpaytwo_" in data:
        request_id = int(data.split("_")[1])
        async with state.proxy() as state_data:
            state_data["request_id"] = request_id
        request = get_request_by_id(request_id)
        await bot.send_message(chat_id,"Введите телеграм аккаунт с которого была выполнена оплата USDT")
        await dannie_pay.people.set()








    elif "acceptcheckpay_" in data:
        request_id = int(data.split("_")[1])
        async with state.proxy() as state_data:
            state_data["request_id"] = request_id
        request = get_request_by_id(request_id)
        await bot.delete_message(chat_id, call.message.message_id)

        msg = get_text(59)
        msg = msg.replace('{number}', str(request[0]))
        msg = msg.replace('{PRICE}', str(request[9]))
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Перевод получен", callback_data=f"acceptitogpay_{request_id}"))
        await bot.send_message(chat_id, "Проверяем оплату")
        await bot.send_message(get_setting(18), msg, reply_markup=markup, parse_mode="HTML")
    elif "acceptitogpay" in data:
        request_id = int(data.split("_")[1])
        async with state.proxy() as state_data:
            state_data["request_id"] = request_id
        request = get_request_by_id(request_id)
        msg = get_text(60)
        msg = msg.replace('{number}', str(request[0]))  ###########################
        await send_main_keyboard(request[1], msg)
        await bot.delete_message(chat_id, call.message.message_id)





    ##############оплату убрали###############
    # elif "checkpay_" in data:
    # request_id = int(data.split("_")[1])
    # request = get_request_by_id(request_id)
    # if check_payment(request[11]):
    # await send_main_keyboard(chat_id, get_text(43))
    # await bot.delete_message(chat_id, call.message.message_id)
    # await send_request_check_to_admin(request_id)
    # else:
    # await send_main_keyboard(chat_id, get_text(31))
    elif "takework_" in data:
        request_id = int(data.split("_")[1])
        change_request_parametr(request_id, 'status', 1)
        change_request_parametr(request_id, 'manager_id', call.from_user.id)
        await send_request_check_to_admin(request_id, call.message.message_id, )
        await send_main_keyboard(chat_id, get_text(42))

    elif "finishwork_" in data:
        request_id = int(data.split("_")[1])
        async with state.proxy() as state_data:
            state_data["request_id"] = request_id
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(get_setting(18), get_text(51), reply_markup=types.ReplyKeyboardRemove())
        await AdminFinishWork.ceiling_ar.set()

    elif "cancellsend_" in data:
        request_id = int(data.split("_")[1])
        print(request_id)
        async with state.proxy() as state_data:
            state_data["request_id"] = request_id
        request = get_request_by_id(request_id)
        user_id = call.from_user.id
        delete_dannie(user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Заполнить заново", callback_data=f"finishwork_{request_id}"))
        await bot.send_message(get_setting(18), "Заполните данные заново", reply_markup=markup)

    elif "acceptsend_" in data:
        request_id = int(data.split("_")[1])
        print(request_id)
        async with state.proxy() as state_data:
            state_data["request_id"] = request_id
        request = get_request_by_id(request_id)

        msg = get_text(41)
        msg = msg.replace('{number}', str(request[0]))
        msg = msg.replace('{ceiling_ar}', str(request[18]))
        msg = msg.replace('{wall_ar}', str(request[19]))
        msg = msg.replace('{omni}', str(request[20]))
        msg = msg.replace('{sector_ar}', str(request[21]))
        msg = msg.replace('{RESULT}', str(request[15]))
        await send_main_keyboard(request[1], msg)
        msg = get_text(55)
        msg = msg.replace('{number}', str(request[0]))
        today = date.today()

        await bot.send_message(get_setting(18), f"{msg}\nДата:{today}")


@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    if chat_id in ADMIN_IDS:
        await send_admin_keyboard(chat_id)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    if message.chat.id < 0:
        return
    if not check_user_presence(chat_id):
        create_user(chat_id, username)
    await send_main_keyboard(chat_id, get_text(1))


@dp.message_handler(commands=['order'])
async def send_welcome(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(get_text(17))
    await bot.send_message(chat_id, get_text(45), reply_markup=keyboard, parse_mode="HTML")
    await UserCreateRequest.name.set()


@dp.message_handler(commands=['support'])
async def send_welcome(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    await send_support(chat_id)


@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    await send_information(chat_id)


@dp.message_handler(commands=['pay'])
async def send_welcome(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    msg = get_text(61)
    await bot.send_message(chat_id, msg, parse_mode="HTML")


@dp.message_handler()
async def echo(message: types.Message):
    logging_message(message.chat.id, message.from_user.username, message.text)
    chat_id, username, text = message.chat.id, message.from_user.username, message.text
    if message.chat.id < 0:
        return
    if text == get_text(14):
        await send_information(chat_id)
    elif text == get_text(46):
        await send_support(chat_id)
    elif text == get_text(16):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(get_text(17))
        await bot.send_message(chat_id, get_text(45), reply_markup=keyboard, parse_mode="HTML")
        await UserCreateRequest.name.set()
    else:
        await send_main_keyboard(chat_id, get_text(1))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
