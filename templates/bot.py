import telebot
import json

from templates.funcs import reg_user, load_db, upload_db, is_emoji, resize_image, PM # Private Messages
from templates.markups import start_button, start_button_exception1, cancel_button

with open("token.txt", "r") as raw_token:
    token = raw_token.readlines()[0]

with open("texts.json", "r", encoding="utf-8") as raw_texts:
    texts = json.load(raw_texts)

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"], func=PM)
def start(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    db = reg_user(user_id, username)
    user_lang = db["users"][user_id]["language"]
    
    if username is None:
        db["users"][user_id]["status"] = "start_exception_1"
        bot.send_message(message.chat.id, texts["start_exception_1"][user_lang], parse_mode="HTML", \
            reply_markup=start_button_exception1( texts["start_button_exception_1"][user_lang] ))

    else:
        db["users"][user_id]["status"] = "start"
        bot.send_message(message.chat.id, texts["start"][user_lang], parse_mode="HTML", \
            reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

    upload_db(db)

@bot.message_handler(content_types=["text", "photo"], func=PM)
def text_processing(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username

    db = reg_user(user_id, username)
    user_lang = db["users"][user_id]["language"]
    status = db["users"][user_id]["status"]

    match status:

        case "start":

            answers = list(zip(*texts["start_buttons"].values())) + [texts["change_lang_buttons"]] # -> [('Join pack', 'Приєднатись до пакунку'), ('Create pack', 'Створити пакунок'), ('Add sticker', 'Додати наліпку'), ["Change language to 🇬🇧 (English)", "Змінити мову на 🇺🇦 (Українську)"]]

            class Answers:
                join_btn_en, join_btn_ua = answers[0]
                create_btn_en, create_btn_ua = answers[1]
                man_btn_en, man_btn_ua = answers[2]
                ch_lan_en, ch_lan_ua = answers[3]

            # TODO: make match case better. More: README.md

            match message.text:

                case Answers.join_btn_en|Answers.join_btn_ua:

                    # db["users"][user_id]["status"] = "start" # useless
                    bot.send_message(message.chat.id, texts["joined"][user_lang], \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                case Answers.create_btn_en|Answers.create_btn_ua:
                    
                    db["users"][user_id]["status"] = "creating"

                    bot.send_message(message.chat.id, texts["creating1"][user_lang], \
                        reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                case Answers.man_btn_en|Answers.man_btn_ua:
                    
                    # db["users"][user_id]["status"] = "start" # useless
                    bot.send_message(message.chat.id, texts["added"][user_lang], \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                case Answers.ch_lan_en|Answers.ch_lan_ua:

                    db["users"][user_id]["language"] = "en" if Answers.ch_lan_en == message.text else "ua"

                    user_lang = db["users"][user_id]["language"]

                    bot.send_message(message.chat.id, texts["lan_changed"][user_lang], \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                case _:

                    bot.send_message(message.chat.id, texts["unknown_exception_2"][user_lang])

        case "start_exception_1":

            if message.text in texts["start_button_exception_1"].values():
                
                if username is None:
                    db["users"][user_id]["status"] = "start_exception_1"
                    bot.send_message(message.chat.id, texts["start_exception_1"][user_lang], \
                        reply_markup=start_button_exception1( texts["start_button_exception_1"][user_lang] ))

                else:
                    db["users"][user_id]["status"] = "start"
                    bot.send_message(message.chat.id, texts["start"][user_lang], parse_mode="HTML", \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
        
        case "creating":

            class Answers:
                create_btn_en, create_btn_ua = texts["cancel_button"].values()

            match message.text:

                case Answers.create_btn_en|Answers.create_btn_ua:

                    db["users"][user_id]["status"] = "start"

                    bot.send_message(message.chat.id, texts["start"][user_lang], parse_mode="HTML", \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                case _ if len(message.text) <= 64:
                    
                    db["packs"].append({"title": message.text, "adm": user_id, "members": [user_id], "stickers": [], "status": "making"})
                    db["users"][user_id]["packs"].append(len(db["packs"])-1)
                    db["users"][user_id]["status"] = "creating2"

                    bot.send_message(message.chat.id, texts["creating2"][user_lang], \
                        reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                case _:
                    
                    bot.send_message(message.chat.id, texts["creating1_e1"][user_lang], \
                        reply_markup=cancel_button(texts["cancel_button"][user_lang]))

        case "creating2":

            class Answers:
                create_btn_en, create_btn_ua = texts["cancel_button"].values()

            match message.text:

                case Answers.create_btn_en|Answers.create_btn_ua:

                    db["users"][user_id]["status"] = "start"
                    db["packs"].pop( db["users"][user_id]["packs"].pop() )

                    bot.send_message(message.chat.id, texts["start"][user_lang], parse_mode="HTML", \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                case None:

                    if is_emoji(message.caption):

                        # TODO: make multiple emoji possible
                        # TODO: make webm and tgs possible
                        pack_id = db["users"][user_id]["packs"][-1]
                        pack_name = "p{}_by_paces_bot".format(pack_id)

                        photo = resize_image( bot.download_file( bot.get_file( message.photo[len(message.photo)-1].file_id ).file_path ) )

                        if bot.create_new_sticker_set(int(user_id), pack_name, \
                            db["packs"][pack_id]["title"], message.caption, png_sticker=photo):

                            db["users"][user_id]["status"] = "start"
                            db["packs"][pack_id]["status"] = "maked"

                            bot.send_message(message.chat.id, texts["created"][user_lang] + "t.me/addstickers/" + pack_name, \
                                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

                        else:

                            bot.send_message(message.chat.id, texts["unknown_exception_1"][user_lang]+'2')
                        
                    else:

                        bot.send_message(message.chat.id, texts["creating2_e2"][user_lang], \
                            reply_markup=cancel_button(texts["cancel_button"][user_lang]))
                
                case _:

                    bot.send_message(message.chat.id, texts["creating2_e1"][user_lang], \
                        reply_markup=cancel_button(texts["cancel_button"][user_lang]))

        case _:

            bot.send_message(message.chat.id, texts["unknown_exception_1"][user_lang]+'1')
        
    upload_db(db)

def run(non_stop: bool) -> None:

    bot.polling(non_stop=non_stop)