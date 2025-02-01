import asyncio

from aiogram.filters import CommandStart, Command
from aiogram.types import Message, URLInputFile, FSInputFile, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F, Bot
from aiogram.enums import ParseMode
from config import BOT_TOKEN, RAPIDAPI_TOKEN

import requests
import texts
import database
import keyboard as kb

database.create_table_users()
database.create_table_convertations()

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
router = Router()


class Soc(StatesGroup):
    start = State()
    denied = State()
    tiktok = State()
    likee = State()
    pinterest = State()
    pin_video = State()
    pin_photo = State()
    soundcloud = State()


async def check_subscription(user_id):
    channel_id = '@gossip_fm'
    chat_member = await bot.get_chat_member(channel_id, user_id)

    if chat_member.status not in ['member', 'administrator', 'creator']:
        return False
    return True


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if not await check_subscription(message.from_user.id):
        await message.answer(texts.NOT_SUBSCRIBED_TEXT, reply_markup=kb.sub_keyboard)
        await state.set_state(Soc.denied)
        return
    await message.answer_animation(texts.START_GIF)
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}!"
        f"\nПривет! я бот-загрузчик видео из TikTok, Likee, Pinterest без водяных знаков,"
        f" а еще я научился скачивать песни из SoundCloud!",
        reply_markup=kb.start_kb)
    await state.set_state(Soc.start)
    database.add_user(message.from_user.id, message.from_user.username)


@router.callback_query(F.data == 'subscribed')
async def process_callback_kb1btn1(callback: CallbackQuery, state: FSMContext):
    if not await check_subscription(callback.from_user.id):
        await bot.send_message(chat_id=callback.from_user.id, text='Тебя все еще нет в подписчиках😓\n'
                                                                   'Попробуй еще разок нажать на "подписаться"',
                               reply_markup=kb.sub_keyboard)
        await state.set_state(Soc.denied)
        return
    await state.set_state(Soc.start)
    await callback.message.answer('Спасибо за подписку🩵\nМожешь выбрать команду👇', reply_markup=kb.start_kb)


@router.message(F.text == '🎥VIDEO🎥')
async def video_choice(message: Message, state: FSMContext) -> None:
    if not await check_subscription(message.from_user.id):
        await message.answer(texts.NOT_SUBSCRIBED_TEXT, reply_markup=kb.sub_keyboard)
        await state.set_state(Soc.denied)
        return
    await message.answer('Команды видео:', reply_markup=kb.video_kb)


@router.message(F.text == '🎼AUDIO🎼')
async def video_choice(message: Message, state: FSMContext) -> None:
    if not await check_subscription(message.from_user.id):
        await message.answer(texts.NOT_SUBSCRIBED_TEXT, reply_markup=kb.sub_keyboard)
        await state.set_state(Soc.denied)
        return
    await message.answer('Команды аудио:', reply_markup=kb.audio_kb)


@router.message(F.text == '🎧TikTok🎧')
async def tiktok(message: Message, state: FSMContext) -> None:
    if not await check_subscription(message.from_user.id):
        await message.answer(texts.NOT_SUBSCRIBED_TEXT, reply_markup=kb.sub_keyboard)
        await state.set_state(Soc.denied)
        return
    await state.set_state(Soc.tiktok)
    await message.answer('Супер! Просто отправь мне ссылку на видео', reply_markup=kb.cancel_keyboard)


@router.message(Soc.tiktok)
async def tiktok_sender(message: Message, state: FSMContext):
    link = message.text

    msg = await message.answer("Пожалуйста подождите, мы обрабатываем ваш запрос")
    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

    querystring = {"url": link, "hd": "1"}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_TOKEN,
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    try:
        video_link = response.json()['data']['play']
    except KeyError:
        await msg.edit_text('Ссылка оказалась неверная. Введи корректную ссылку на видео в TikTok',
                            reply_markup=kb.cancel_keyboard)
        database.add_convertation(message.from_user.id, 'Failed')
        return

    await msg.edit_text("📲Отправляем видео📲\nСекундочку...")
    await asyncio.sleep(6)
    await msg.delete()
    await message.answer_video(URLInputFile(video_link), reply_markup=kb.start_kb)
    database.add_convertation(message.from_user.id, 'Done')
    await state.clear()


@router.message(F.text == '🩷Likee🩷')
async def tiktok(message: Message, state: FSMContext) -> None:
    if not await check_subscription(message.from_user.id):
        await message.answer(texts.NOT_SUBSCRIBED_TEXT, reply_markup=kb.sub_keyboard)
        await state.set_state(Soc.denied)
        return
    await state.set_state(Soc.likee)
    await message.answer('Супер! Просто отправь мне ссылку на видео в Likee', reply_markup=kb.cancel_keyboard)


@router.message(Soc.likee)
async def likee_sender(message: Message, state: FSMContext):
    link = message.text

    msg = await message.answer("Пожалуйста подождите, мы обрабатываем ваш запрос")
    url = 'https://likee-downloader-download-likee-videos.p.rapidapi.com/process'
    querystring = {"url": link, "hd": "1"}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_TOKEN,
        "X-RapidAPI-Host": "likee-downloader-download-likee-videos.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    try:
        video_link = response.json()['withoutWater']
        video_width = response.json()['video_width']
        video_height = response.json()['video_height']
    except KeyError:
        await msg.edit_text('Ссылка оказалась неверная. Введи корректную ссылку на видео в Likee',
                            reply_markup=kb.cancel_keyboard)
        database.add_convertation(message.from_user.id, 'Failed')
        return

    await msg.edit_text("📲Отправляем видео📲\nСекундочку...")
    await asyncio.sleep(5)
    try:
        await msg.delete()
    except Exception:
        pass
    await message.answer_video(URLInputFile(video_link), width=video_width,
                               height=video_height, reply_markup=kb.start_kb)
    database.add_convertation(message.from_user.id, 'Done')
    await state.clear()


@router.callback_query(F.data == 'cancel')
async def process_callback_kb1btn1(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Soc.start)
    await callback.message.answer('Ты вернулся в начало.\nМожешь выбрать команду👇', reply_markup=kb.start_kb)


@router.message(F.text == '💋Pinterest💋')
async def tiktok(message: Message, state: FSMContext) -> None:
    if not await check_subscription(message.from_user.id):
        await message.answer(texts.NOT_SUBSCRIBED_TEXT, reply_markup=kb.sub_keyboard)
        await state.set_state(Soc.denied)
        return
    await state.set_state(Soc.pinterest)
    await message.answer('Выбери что нужно скачать👇', reply_markup=kb.PIN_KB)


@router.message(F.text == '🎞️Видео Pinterest🎞️')
async def pin_video(message: Message, state: FSMContext):
    await state.set_state(Soc.pin_video)
    await message.answer('Супер! Просто отправь мне ссылку на видео в Pinterest', reply_markup=kb.cancel_keyboard)


@router.message(F.text == '🖼️Картинка Pinterest🖼️')
async def pin_video(message: Message, state: FSMContext):
    await state.set_state(Soc.pin_photo)
    await message.answer('Супер! Просто отправь мне ссылку на пикчу в Pinterest', reply_markup=kb.cancel_keyboard)


@router.message(Soc.pin_photo)
async def likee_sender(message: Message, state: FSMContext):
    link = message.text

    msg = await message.answer("Пожалуйста подождите, мы обрабатываем ваш запрос")
    url = "https://pinterest-downloader-download-pinterest-image-video-and-reels.p.rapidapi.com/api/pins"

    querystring = {"url": link}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_TOKEN,
        "X-RapidAPI-Host": "pinterest-downloader-download-pinterest-image-video-and-reels.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        photo_link = f"{response.json()['media']['items']['orig']['url']}"
    except KeyError:
        await msg.edit_text('Ссылка оказалась неверная. Введи корректную ссылку на видео в Pinterest',
                            reply_markup=kb.cancel_keyboard)
        database.add_convertation(message.from_user.id, 'Failed')
        return

    await msg.edit_text("📲Отправляем картинку📲\nСекундочку...")
    await asyncio.sleep(2)
    try:
        await msg.delete()
    except Exception:
        pass
    await message.answer_photo(URLInputFile(photo_link), reply_markup=kb.start_kb)
    database.add_convertation(message.from_user.id, 'Done')
    await state.clear()
    # await bot.send_message(text='', reply_markup=kb.start_kb)


@router.message(Soc.pin_video)
async def likee_sender(message: Message, state: FSMContext):
    link = message.text

    msg = await message.answer("Пожалуйста подождите, мы обрабатываем ваш запрос")
    url = "https://pinterest-downloader-download-pinterest-image-video-and-reels.p.rapidapi.com/api/pins"

    querystring = {"url": link}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_TOKEN,
        "X-RapidAPI-Host": "pinterest-downloader-download-pinterest-image-video-and-reels.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        video_link = f"{response.json()['media']['items']['V_HLSV3_MOBILE']['url']}"
    except KeyError:
        await msg.edit_text('Ссылка оказалась неверная. Введи корректную ссылку на видео в Pinterest',
                            reply_markup=kb.cancel_keyboard)
        database.add_convertation(message.from_user.id, 'Failed')
        return

    await msg.edit_text("📲Отправляем видео📲\nСекундочку...")
    await asyncio.sleep(6)
    try:
        await msg.delete()
    except Exception:
        pass
    await message.answer_video(URLInputFile(video_link), reply_markup=kb.start_kb)
    database.add_convertation(message.from_user.id, 'Done')
    await state.clear()


@router.message(F.text == '🎸SoundCloud🎶')
async def soundcloud(message: Message, state: FSMContext) -> None:
    if not await check_subscription(message.from_user.id):
        await message.answer(texts.NOT_SUBSCRIBED_TEXT, reply_markup=kb.sub_keyboard)
        await state.set_state(Soc.denied)
        return
    await state.set_state(Soc.soundcloud)
    await message.answer('Супер! Просто отправь мне ссылку на песню в SoundCloud', reply_markup=kb.cancel_keyboard)


@router.message(Soc.soundcloud)
async def soundcloud_sender(message: Message, state: FSMContext):
    link = message.text

    msg = await message.answer("Пожалуйста подождите, мы обрабатываем ваш запрос")
    url = "https://soundcloud-scraper.p.rapidapi.com/v1/track/metadata"

    querystring = {"track": link}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_TOKEN,
        "X-RapidAPI-Host": "soundcloud-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    try:
        audio_link = f"{response.json()['audio'][0]['url']}"
    except KeyError:
        await msg.edit_text('Ссылка оказалась неверная. Введи корректную ссылку на песню в SoundCloud',
                            reply_markup=kb.cancel_keyboard)
        database.add_convertation(message.from_user.id, 'Failed')
        return
    except Exception as e:
        await msg.answer('error', reply_markup=kb.start_kb)
        return

    await msg.edit_text("📲Отправляем песню📲\nСекундочку...")
    await asyncio.sleep(6)
    try:
        await msg.delete()
    except Exception:
        pass
    await message.answer(text=f'{response.json()["title"]}', reply_markup=kb.start_kb)
    await message.answer_audio(URLInputFile(audio_link), reply_markup=kb.start_kb)
    database.add_convertation(message.from_user.id, 'Done')
    await state.clear()
    # await state.clear()


@router.message(F.text == 'Вернуться в начало')
async def to_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Soc.start)
    await message.answer(text='Ты вернулся в начало', reply_markup=kb.start_kb)


# команда для проверки админом данных
@router.message(Command('admin_show'))
async def command_start_handler(message: Message) -> None:
    users = database.get_users()
    convertations = database.get_convertations()
    with open('info.txt', 'w') as file:
        file.write(f'USERS\n{users}\nCONVERTATIONS\n{convertations}')

    await message.answer_document(document=FSInputFile('info.txt'))


@router.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer_animation(texts.TEXT_ERROR_GIF)
    await message.answer("Извини, я не ChatGpt, я пока не умею общаться\n"
                         "Выбери команду на клавиатуре кнопок, я делал их для твоего удобства.")
