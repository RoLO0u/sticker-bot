# -*- coding: utf-8 -*-

from telebot.types import KeyboardButton, ReplyKeyboardMarkup

def start_button(start_buttons: list|tuple, change_lang_buttons) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(change_lang_buttons[0]), KeyboardButton(change_lang_buttons[1]))
    markup.add(KeyboardButton(start_buttons[0]), KeyboardButton(start_buttons[1], ))
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

def managing_button(caption: str, packs: list|tuple) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(caption))
    markup.add( KeyboardButton(capt) for capt in packs )
    return markup