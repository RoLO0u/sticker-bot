import telebot
import json

from templates.funcs import reg_user, load_db, upload_db, is_emoji, resize_image, pack_availability, random_string, PM # Private Messages
from templates.markups import start_button, start_button_exception1, cancel_button, managing_button

with open("token.txt", "r") as raw_token:
    token = raw_token.readlines()[0]

with open("texts.json", "r", encoding="utf-8") as raw_texts:
    texts = json.load(raw_texts)

bot = telebot.TeleBot(token)

WATERMARK = "_by_paces_bot"

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

@bot.message_handler(commands=["test"], func=PM)
def test_func(message):
    if message.from_user.id == 602197013:
        if pack_availability(bot.get_sticker_set, \
                telebot.apihelper.ApiTelegramException, message.text[6:]):
            print(1)
        else:
            print(0)

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
                    
                    db["users"][user_id]["status"] = "managing"
                    bot.send_message(message.chat.id, texts["managing"][user_lang], \
                        reply_markup=managing_button( texts["cancel"][user_lang], ) )

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

                    bot.send_message(message.chat.id, texts["cancel"][user_lang], parse_mode="HTML", \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                case _ if len(message.text) <= 64:

                    name = random_string()

                    while name in db["packs"].keys():
                        name = random_string()
                    
                    db["packs"][name] = {"title": message.text, "adm": user_id, "members": [user_id], "stickers": [], "status": "making"}
                    db["users"][user_id]["packs"].append(name)
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

                    bot.send_message(message.chat.id, texts["cancel"][user_lang], parse_mode="HTML", \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
                
                case _:

                    if is_emoji(message.text):

                        db["users"][user_id]["additional_info"] = message.text
                        db["users"][user_id]["status"] = "creating3"

                        bot.send_message(message.chat.id, texts["creating3"][user_lang], \
                            reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                    else:

                        bot.send_message(message.chat.id, texts["creating2_e1"][user_lang], \
                            reply_markup=cancel_button(texts["cancel_button"][user_lang]))

        case "creating3":

            class Answers:
                create_btn_en, create_btn_ua = texts["cancel_button"].values()

            match message.text:

                case Answers.create_btn_en|Answers.create_btn_ua:

                    db["users"][user_id]["status"] = "start"
                    db["users"][user_id]["additional_info"] = None
                    db["packs"].pop( db["users"][user_id]["packs"].pop() )

                    bot.send_message(message.chat.id, texts["cancel"][user_lang], parse_mode="HTML", \
                        reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                case None:

                        # TODO: make multiple emojis to sticker possible
                        # TODO: make webm and tgs image format possible

                        pack_name = db["users"][user_id]["packs"][-1]
                        photo = resize_image( bot.download_file( bot.get_file( message.photo[len(message.photo)-1].file_id ).file_path ) )

                        if bot.create_new_sticker_set(int(user_id), pack_name + WATERMARK, \
                            db["packs"][pack_name]["title"], db["users"][user_id]["additional_info"], png_sticker=photo):

                            db["users"][user_id]["status"] = "start"
                            db["users"][user_id]["additional_info"] = None
                            db["packs"][pack_name]["status"] = "maked"

                            bot.send_message(message.chat.id, texts["created"][user_lang] + "t.me/addstickers/" + pack_name + WATERMARK, \
                                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

                        else:

                            bot.send_message(message.chat.id, texts["unknown_exception_1"][user_lang]+'2')
                
                case _:

                    bot.send_message(message.chat.id, texts["creating3_e1"][user_lang], \
                        reply_markup=cancel_button(texts["cancel_button"][user_lang]))

        case "managing":

            bot.send_message(message.chat.id, texts["managing"][user_lang], \
                reply_markup=managing_button())

        case _:

            bot.send_message(message.chat.id, texts["unknown_exception_1"][user_lang]+'1')
        
    upload_db(db)

def run(non_stop: bool) -> None:

    bot.polling(non_stop=non_stop)
    # bot.infinity_polling()