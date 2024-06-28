from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton(text='🎥VIDEO🎥')],
    [KeyboardButton(text='🎼AUDIO🎼')]
])


video_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='🎧TikTok🎧')],
    [KeyboardButton(text='🩷Likee🩷'), KeyboardButton(text='💋Pinterest💋')],
    [KeyboardButton(text='Вернуться в начало')]
])

audio_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='🎸SoundCloud🎶')],
    [KeyboardButton(text='Вернуться в начало')]
])

PIN_VIDEO = 'Супер! Просто отправь мне ссылку на видео в Pinterest'

PIN_KB = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text='🎞️Видео Pinterest🎞️')],
    [KeyboardButton(text='🖼️Картинка Pinterest🖼️')],
    [KeyboardButton(text='Вернуться в начало')],
])


kb_c = [
  [
    types.InlineKeyboardButton(text='Вернуться в начало', callback_data='cancel', one_time_keyboard=True)
  ]
]
cancel_keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb_c)

kb_sub = [
  [types.InlineKeyboardButton(text='🎙️Gossip FM🎙️', url='https://t.me/gossip_fm')],
    [types.InlineKeyboardButton(text='Я Подписался', callback_data='subscribed')]
]
sub_keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb_sub)
