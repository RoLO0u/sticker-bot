# -*- coding: utf-8 -*-

from typing import Dict, List

import random

from templates.const import CAPTCHA_CAPTIONS

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def start_button(start_buttons: list, change_lang_buttons: list) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=change_lang_buttons[0]), KeyboardButton(text=change_lang_buttons[1]), KeyboardButton(text=change_lang_buttons[2])],
        [KeyboardButton(text=start_buttons[0]), KeyboardButton(text=start_buttons[1] )],
        [KeyboardButton(text=start_buttons[2])]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return markup
    
def start_button_exception1(caption: str) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=caption)]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return markup

def cancel_button(caption: str) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=caption)]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return markup

def managing_button(caption: str) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=caption)]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return markup

def managing_button_inline(packs: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    """:param packs: packs => [["title", "name"], ["title1", "name1"]]"""
    packs = [list(pack.items())[0] for pack in packs]
    keyboard = [InlineKeyboardButton(text=pack[1], callback_data=pack[0]) for pack in packs]
    splited_keyboard = []
    for i in range(0, len(keyboard), 2):
        splited_keyboard.append(keyboard[i:i+2])
    markup = InlineKeyboardMarkup(inline_keyboard=splited_keyboard, row_width=2)
    return markup

def managing_button_2(captions: list|tuple) -> ReplyKeyboardMarkup:
    keyboard = list()
    for num in range(0, len(captions)-1, 3):
        keyboard.append([KeyboardButton(text=capt) for capt in captions[num:num+3]])
    keyboard.append([KeyboardButton(text=captions[-1])])
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return markup

def pack_link_button(caption: str, url: str) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text=caption, url=url)]]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup

def captcha_inline() -> InlineKeyboardMarkup:
    random_capts = [(key, CAPTCHA_CAPTIONS[key]) for key in list(CAPTCHA_CAPTIONS.keys())]
    random.shuffle(random_capts)
    random_capts = dict(random_capts)
    listed_markup = [InlineKeyboardButton(text=capt, callback_data=random_capts[capt]) for capt in random_capts]
    listed_markup = [listed_markup[:3], listed_markup[3:]]
    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=listed_markup)
    return markup