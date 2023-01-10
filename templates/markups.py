# -*- coding: utf-8 -*-

from typing import Dict, List, Tuple

import random

from templates.const import CAPTCHA_CAPTIONS

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def start_button(start_buttons: list, change_lang_buttons: list) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=change_lang_buttons[0]), KeyboardButton(text=change_lang_buttons[1])],
        [KeyboardButton(text=start_buttons[0]), KeyboardButton(text=start_buttons[1] )],
        [KeyboardButton(text=start_buttons[2])]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    
def single_button(caption: str) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=caption)]]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def managing_button_inline(packs: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    """:param packs: packs => [{"name": "title"}, {"name1": "title1"}]"""
    packs: List[Tuple] = [list(pack.items())[0] for pack in packs]
    keyboard = [InlineKeyboardButton(text=pack[1], callback_data=pack[0]) for pack in packs]
    splited_keyboard = []
    for i in range(0, len(keyboard), 2):
        splited_keyboard.append(keyboard[i:i+2])
    return InlineKeyboardMarkup(inline_keyboard=splited_keyboard)

def managing_button_2(captions: list|tuple) -> ReplyKeyboardMarkup:
    keyboard = list()
    for num in range(0, len(captions)-1, 3):
        keyboard.append([KeyboardButton(text=capt) for capt in captions[num:num+3]])
    keyboard.append([KeyboardButton(text=captions[-1])])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def pack_link_button(caption: str, url: str) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=caption, url=url)]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def captcha_inline() -> InlineKeyboardMarkup:
    random_capts = [(key, CAPTCHA_CAPTIONS[key]) for key in list(CAPTCHA_CAPTIONS.keys())]
    random.shuffle(random_capts)
    random_capts = dict(random_capts)
    listed_markup = [InlineKeyboardButton(text=capt, callback_data=random_capts[capt]) for capt in random_capts]
    listed_markup = [listed_markup[:3], listed_markup[3:]]
    return InlineKeyboardMarkup(row_width=3, inline_keyboard=listed_markup)