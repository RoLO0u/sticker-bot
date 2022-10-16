# -*- coding: utf-8 -*-

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def start_button(start_buttons: list|tuple, change_lang_buttons) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(change_lang_buttons[0]), KeyboardButton(change_lang_buttons[1]))
    markup.add(KeyboardButton(start_buttons[0]), KeyboardButton(start_buttons[1] ))
    markup.add(KeyboardButton(start_buttons[2]))
    return markup
    
def start_button_exception1(start_buttons_exception: str) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton(start_buttons_exception))
    return markup

def cancel_button(caption: str) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(caption))
    return markup

def managing_button(caption: str) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(caption))
    return markup

def managing_button_inline(packs: list|tuple) -> InlineKeyboardMarkup:
    """:param packs: packs => [["title", "name"], ["title1", "name1"]]"""
    markup = InlineKeyboardMarkup(row_width=2)
    packs = [InlineKeyboardButton(capt[0], callback_data=capt[1]) for capt in packs]
    for i in range(0, len(packs), 2):
        markup.add( *packs[i:i+2] )
    return markup

def managing_button_2(captions: list|tuple) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*captions[:3])
    markup.add(*captions[3:6])
    markup.add(*captions[6:])
    # markup.add(captions)
    return markup

def pack_link_button(caption: str, url: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(caption, url=url))
    return markup