from __future__ import annotations
from typing import Dict, List
import json


Texts = Dict[str, Dict[str, str]]
TextsButtons = Dict[str, Dict[str, List[str]]]

with open("texts.json", "r", encoding="utf-8") as raw:
    texts: Texts = json.load(raw)
with open("texts_buttons.json", "r", encoding="utf-8") as raw:
    texts_buttons: TextsButtons = json.load(raw)
    
class Answers:
    
    def __init__(self, user_lang: str) -> None:
        self.user_lang = user_lang
        
    def get_cancel_btn(self) -> Answers:
        self.cancel_btn = texts_buttons["cancel"][self.user_lang][0]
        return self
    def get_back_btns(self) -> Answers:
        self.back_btn_en, self.back_btn_ua = texts["back"].values()
        return self
    def get_confirming(self) -> Answers:
        self.confirming = texts["confirming"][self.user_lang]
        return self
    def get_delete_sticker_confirming(self) -> Answers:
        self.delete_sticker_confirming = texts_buttons["managing_del_conf"][self.user_lang][0]
        return self
    def get_menu_btns(self) -> Answers:
        self.add_btn = texts_buttons["managing_2"][self.user_lang][0]
        self.del_stick_btn = texts_buttons["managing_2"][self.user_lang][1]
        self.edit_emoji_btn = texts_buttons["managing_2"][self.user_lang][2]
        self.generate_password = texts_buttons["managing_2"][self.user_lang][3]
        self.invite_btn = texts_buttons["managing_2"][self.user_lang][4]
        self.kick_btn = texts_buttons["managing_2"][self.user_lang][5]
        self.del_pack_btn = texts_buttons["managing_2"][self.user_lang][6]
        self.set_pack_title = texts_buttons["managing_2"][self.user_lang][7]
        self.show_btn = texts_buttons["managing_2"][self.user_lang][8]
        self.back_btn = texts_buttons["managing_2"][self.user_lang][9]
        return self
    def get_start_btns(self) -> Answers:
        self.join_btn = texts_buttons["start"][self.user_lang][0]
        self.create_btn = texts_buttons["start"][self.user_lang][1]
        self.man_btn = texts_buttons["start"][self.user_lang][2]
        self.ch_lan_en = texts_buttons["change_lang"]['en'][0]
        self.ch_lan_ua = texts_buttons["change_lang"]['ua'][0]
        return self
    def get_start_opts_btns(self) -> Answers:
        self.from_scratch = texts_buttons["start_opts"][self.user_lang][0]
        self.copy = texts_buttons["start_opts"][self.user_lang][1]
        self.cancel_btn = texts_buttons["start_opts"][self.user_lang][2]
        return self