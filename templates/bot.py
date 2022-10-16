import logging
import json
import os

from aiogram import Bot, Dispatcher, executor, types, utils

from templates.funcs import reg_user, load_db, upload_db, is_emoji, resize_image, \
    pack_availability, random_string, user_packs # Private Messages
from templates.markups import start_button, start_button_exception1, cancel_button, \
    managing_button, pack_link_button, managing_button_2, managing_button_inline

logging.basicConfig(level=logging.INFO)

token = os.getenv("BOT_TOKEN")

with open("texts.json", "r", encoding="utf-8") as raw_texts:
    texts = json.load(raw_texts)

bot = Bot(token)
dp = Dispatcher(bot)

WATERMARK = "_by_paces_bot"

# TODO correction of status

@dp.message_handler(commands=["start"], chat_type="private")
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    db = reg_user(user_id, username)
    user_lang = db["users"][user_id]["language"]
    
    if username is None:
        db["users"][user_id]["status"] = "start_exception_1"
        await message.answer(texts["start_exception_1"][user_lang], parse_mode="HTML", \
            reply_markup=start_button_exception1( texts["start_button_exception_1"][user_lang] ))

    else:
        db["users"][user_id]["status"] = "start"
        await message.answer(texts["start"][user_lang], parse_mode="HTML", \
            reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

    upload_db(db)

@dp.message_handler(commands=["test"], chat_type="private")
async def test_func(message: types.Message):
    if message.from_user.id == 602197013:
        to_check = 0
        match to_check:
            case 0:
                # if pack_availability(bot.get_sticker_set, \
                #         telebot.apihelper.ApiTelegramException, message.text[6:]):
                await bot.get_sticker_set(message.get_args())
                print(1)
                # else:
                #     print(0)
            case 1:
                await bot.send_sticker(message.chat.id, \
                    await bot.download_file( bot.get_file(bot.get_sticker_set("hxxhzkhRpq_by_paces_bot").stickers[0].file_id).file_path))
            case 2:
                await bot.send_sticker(chat_id=message.chat.id, sticker=bot.get_sticker_set("hxxhzkhRpq_by_paces_bot").stickers[0].file_id)
            case 3:
                await bot.send_sticker(chat_id=message.chat.id, sticker="CAACAgIAAxUAAWMtsh1VasOoVWxE67jLt5UBaQkNAAIqIQACF7xxSVCXRGA5ki1uKQQ")

@dp.message_handler(content_types=["text", "photo", "sticker"], chat_type="private")
async def text_processing(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username

    db = reg_user(user_id, username)
    user_lang = db["users"][user_id]["language"]
    status = db["users"][user_id]["status"]

    # TODO move all things doing here in another file

    match message.content_type:

        case "text":

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

                        # TODO check packs availibility

                        case Answers.join_btn_en|Answers.join_btn_ua:

                            # db["users"][user_id]["status"] = "start" # useless
                            await message.answer(texts["joined"][user_lang], \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                        case Answers.create_btn_en|Answers.create_btn_ua:
                            
                            db["users"][user_id]["status"] = "creating"

                            await message.answer(texts["creating1"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                        case Answers.man_btn_en|Answers.man_btn_ua:

                            db["users"][user_id]["status"] = "managing"
                            await message.answer(texts["managing0"][user_lang], \
                                reply_markup=managing_button(texts["back"][user_lang]))
                            
                            # packs_to_check = [(userpack, db["packs"][userpack]) for userpack in db["users"][user_lang]["packs"]]

                            to_pop = []
                            for pname in db["users"][user_id]["packs"]:
                                if not await pack_availability(bot.get_sticker_set, \
                                    utils.exceptions.InvalidStickersSet, pname + WATERMARK) or not db["packs"][pname]["stickers"]:
                                    to_pop.append(pname)
                            for pname in to_pop:
                                db["packs"].pop(pname)
                                db["users"][user_id]["packs"].remove(pname)

                            # user have packs
                            if db["users"][user_id]["packs"]:
                                await message.answer(texts["managing"][user_lang], \
                                    reply_markup=managing_button_inline(user_packs(db["packs"], \
                                    db["users"][user_id]["packs"])))
                            
                            else:
                                await message.answer(texts["managing_e"][user_lang])

                        case Answers.ch_lan_en|Answers.ch_lan_ua:

                            db["users"][user_id]["language"] = "en" if Answers.ch_lan_en == message.text else "ua"

                            user_lang = db["users"][user_id]["language"]

                            await message.answer(texts["lan_changed"][user_lang], \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                        case _:
                            await message.answer(texts["unknown_exception_2"][user_lang])

                case "start_exception_1":

                    if message.text in texts["start_button_exception_1"].values():
                        
                        if username is None:
                            db["users"][user_id]["status"] = "start_exception_1"
                            await message.answer(texts["start_exception_1"][user_lang], \
                                reply_markup=start_button_exception1( texts["start_button_exception_1"][user_lang] ))

                        else:
                            db["users"][user_id]["status"] = "start"
                            await message.answer(texts["start"][user_lang], parse_mode="HTML", \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
                
                case "creating":

                    class Answers:
                        create_btn_en, create_btn_ua = texts["cancel_button"].values()

                    match message.text:

                        case Answers.create_btn_en|Answers.create_btn_ua:

                            db["users"][user_id]["status"] = "start"

                            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                        case _ if len(message.text) <= 64:

                            name = random_string()

                            while name in db["packs"].keys():
                                name = random_string()
                            
                            db["packs"][name] = {"title": message.text, "adm": user_id, "members": [user_id], "stickers": [], "status": "making"}
                            db["users"][user_id]["packs"].append(name)
                            db["users"][user_id]["status"] = "creating2"

                            await message.answer(texts["creating2"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                        case _:
                            await message.answer(texts["creating1_e1"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                case "creating2":

                    class Answers:
                        create_btn_en, create_btn_ua = texts["cancel_button"].values()

                    match message.text:

                        case Answers.create_btn_en|Answers.create_btn_ua:

                            db["users"][user_id]["status"] = "start"
                            db["packs"].pop( db["users"][user_id]["packs"].pop() )

                            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
                        
                        case _:

                            if is_emoji(message.text):

                                db["users"][user_id]["additional_info"] = message.text
                                db["users"][user_id]["status"] = "creating3"

                                await message.answer(texts["creating3"][user_lang], \
                                    reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                            else:
                                await message.answer(texts["emoji_only_e"][user_lang], \
                                    reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                case "creating3":

                    class Answers:
                        cancel_btn_en, cancel_btn_ua = texts["cancel_button"].values()

                    match message.text:

                        case Answers.cancel_btn_en|Answers.cancel_btn_ua:

                            db["users"][user_id]["status"] = "start"
                            db["users"][user_id]["additional_info"] = None
                            db["packs"].pop( db["users"][user_id]["packs"].pop() )

                            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
                        
                        case _:
                            await message.answer(texts["image_only_e"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))
                    
                case "managing":

                    class Answers:
                        back_btn_en, back_btn_ua = texts["back"].values()

                    match message.text:

                        case Answers.back_btn_en | Answers.back_btn_ua:

                            db["users"][user_id]["status"] = "start"

                            await message.answer(texts["backed"][user_lang],\
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
                            
                        case _:
                            await message.answer(texts["managing_exception_1"][user_lang])
                
                case "managing2":

                    packs = user_packs(db["packs"], db["users"][user_id]["packs"])
                    
                    # TODO create inline sticker pick like in @Stickers bot

                    class Answers:
                        back_btn = texts["managing_buttons_2"][user_lang][-1]
                        add_btn = texts["managing_buttons_2"][user_lang][0]
                        del_stick_btn = texts["managing_buttons_2"][user_lang][1]
                        del_pack_btn = texts["managing_buttons_2"][user_lang][-4]
                        show_btn = texts["managing_buttons_2"][user_lang][-2]

                    match message.text:
                        
                        case Answers.back_btn:
                            db["users"][user_id]["status"] = "managing"
                            await message.answer(texts["managing0"][user_lang], \
                                reply_markup=managing_button(texts["back"][user_lang]))

                            to_pop = []
                            for pname in db["users"][user_id]["packs"]:
                                if not await pack_availability(bot.get_sticker_set, \
                                        utils.exceptions.InvalidStickersSet, pname + WATERMARK):
                                    to_pop.append(pname)
                            for pname in to_pop:
                                db["packs"].pop(pname)
                                db["users"][user_id]["packs"].remove(pname)
                        
                            await message.answer(texts["managing"][user_lang], \
                                reply_markup=managing_button_inline(user_packs(db["packs"], \
                                db["users"][user_id]["packs"])))

                        case Answers.add_btn:
                            db["users"][user_id]["status"] = "managing_add_1"
                            await message.answer(texts["managing_add_1"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                        case Answers.del_stick_btn:
                            db["users"][user_id]["status"] = "managing_del_1"
                            await message.answer(texts["managing_del_1"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))
                        
                        case Answers.del_pack_btn:
                            db["users"][user_id]["status"] = "managing_del2_1"
                            await message.answer(texts["managing_del2_1"][user_lang], parse_mode="markdown", \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                        case Answers.show_btn:
                            sticker = await bot.get_sticker_set(db["users"][user_id]["additional_info"]+WATERMARK)
                            await bot.send_sticker(message.chat.id, \
                                sticker=sticker.stickers[0].file_id)

                        # TODO this is temporary case                
                        case _:
                            msg = {"en": "Sorry, we don't have this function now. Use @Stickers to solve problem", \
                                "ua": "Вибачте, ми не маєм цієї функції наразі. Скористуйтесь @Stickers, щоб вирішити вашу проблему"}
                            await message.answer(msg[user_lang])
                
                case "managing_add_1":
                    
                    class Answers:
                        cancel_btn = texts["cancel_button"][user_lang]

                    match message.text:

                        case Answers.cancel_btn:
                            db["users"][user_id]["status"] = "managing2"
                            await message.answer(texts["managing2"][user_lang], \
                                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

                        case _:

                            if is_emoji(message.text):

                                db["users"][user_id]["status"] = "managing_add_2"
                                db["users"][user_id]["additional_info"] += f"-{message.text}"
                                await message.answer(texts["managing_add_2"][user_lang], \
                                    reply_markup=cancel_button(texts["cancel_button"][user_lang]))
                        
                            else:
                                await message.answer(texts["emoji_only_e"][user_lang])
                
                case "managing_add_2":

                    class Answers:
                        cancel_btn = texts["cancel_button"][user_lang]

                    match message.text:

                        case Answers.cancel_btn:
                            db["users"][user_id]["status"] = "managing2"
                            await message.answer(texts["managing2"][user_lang], \
                                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

                        case _:
                            await message.answer(texts["image_only_e"][user_lang])
                
                # TODO delete set from his members also

                case "managing_del_1":

                    class Answers:
                        cancel_btn = texts["cancel_button"][user_lang]

                    match message.text:

                        case Answers.cancel_btn:
                            db["users"][user_id]["status"] = "managing2"
                            await message.answer(texts["managing2"][user_lang], \
                                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

                        case _:
                            await message.answer(texts["sticker_only_e"][user_lang])
                
                case "managing_del2_1":

                    class Answers:
                        cancel_btn = texts["cancel_button"][user_lang]
                        confirming = texts["confirming"][user_lang]

                    match message.text:

                        case Answers.cancel_btn:
                            db["users"][user_id]["status"] = "managing2"
                            await message.answer(texts["managing2"][user_lang], \
                                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

                        case Answers.confirming:
                            db["users"][user_id]["status"] = "start"
                            set_name = db["users"][user_id]["additional_info"]
                            db["users"][user_id]["packs"].remove(set_name)
                            db["packs"].pop(set_name)
                            sticker_set = await bot.get_sticker_set(set_name+WATERMARK)
                            for sticker in sticker_set.stickers:
                                await bot.delete_sticker_from_set(sticker.file_id)
                            db["users"][user_id]["additional_info"] = None
                            await message.answer(texts["pack_deleted"][user_lang], \
                                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

                        case _:
                            await message.answer(texts["unknown_exception_1"][user_lang])

                case _:
                    await message.answer(texts["unknown_exception_1"][user_lang]+'1')

    
        case "photo":

            match status:

                case "creating3":

                    # TODO: make multiple emojis to sticker possible
                    # TODO: make webm and tgs image format possible

                    pack_name = db["users"][user_id]["packs"][-1]
                    pack_name_plus = pack_name + WATERMARK
                    raw_file = await bot.get_file(message.photo[len(message.photo)-1].file_id)
                    photo = resize_image(await bot.download_file(raw_file.file_path), user_id )
                    
                    try:
                        if await bot.create_new_sticker_set(int(user_id), pack_name_plus, \
                            db["packs"][pack_name]["title"], db["users"][user_id]["additional_info"], png_sticker=photo):

                            db["users"][user_id]["status"] = "start"
                            db["users"][user_id]["additional_info"] = None
                            db["packs"][pack_name]["status"] = "maked"
                            created_pack = await bot.get_sticker_set(pack_name_plus)
                            db["packs"][pack_name]["stickers"] = [created_pack.stickers[0].file_unique_id]

                            await message.answer(texts["created1"][user_lang], \
                                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + WATERMARK))
                            await message.answer(texts["created2"][user_lang], \
                                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

                        else:
                            await message.answer(texts["unknown_exception_1"][user_lang]+'2')

                    except utils.exceptions.InvalidStickersSet as e:
                        await message.answer(texts["known_e_1"][user_lang]+str(e).split()[-1])
                
                case "managing_add_2":

                    pack_name, emojis = db["users"][user_id]["additional_info"].split("-")
                    pack_name_plus = pack_name + WATERMARK
                    file_raw = await bot.get_file(message.photo[len(message.photo)-1].file_id)
                    file_raw = await bot.download_file(file_raw.file_path)
                    photo = resize_image(file_raw, user_id )
                    
                    try:
                        
                        if await bot.add_sticker_to_set(int(user_id), pack_name_plus, \
                            emojis, png_sticker=photo):
                            db["users"][user_id]["status"] = "start"
                            db["users"][user_id]["additional_info"] = None
                            sticker_set = await bot.get_sticker_set(pack_name_plus)
                            db["packs"][pack_name]["stickers"] = [sticker.file_unique_id for sticker in sticker_set.stickers]

                            await message.answer(texts["added1"][user_lang], \
                                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + WATERMARK))
                            await message.answer(texts["created2"][user_lang], \
                                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))
                    
                    except utils.exceptions.InvalidStickersSet:
                        db["users"][user_id]["status"] = "start"
                        db["packs"].pop(pack_name)
                        db["users"][user_id]["additional_info"] = None
                        db["users"][user_id]["packs"].remove(pack_name)
                        await message.answer(texts["managing_add_e"][user_lang], \
                            reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))
                        
                case _:
                    await message.answer(texts["unknown_exception_3"][user_lang])
        
        case "sticker":

            match status:

                case "managing_del_1":

                    db["users"][user_id]["status"] = "start"

                    sticker_id = message.sticker.file_id
                    unique_id = message.sticker.file_unique_id

                    # TODO: make warning message if it's last sticker

                    # checking if sticker in user stickerpack
                    if unique_id in db["packs"][db["users"][user_id]["additional_info"]]["stickers"]:

                        db["packs"][db["users"][user_id]["additional_info"]]["stickers"].remove(unique_id)

                        await bot.delete_sticker_from_set(sticker_id)

                        await message.answer(texts["deleted"][user_lang], \
                            reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))
                    
                    else:
                        await message.answer(texts["managing_del_e"][user_lang])

                case _:
                    await message.answer(texts["unknown_exception_3"][user_lang])
        
    upload_db(db)

@dp.callback_query_handler(lambda call: True and call.message)
async def callhandler(call):

    user_id = str(call.from_user.id)
    username = call.from_user.username

    db = reg_user(user_id, username)
    user_lang = db["users"][user_id]["language"]
    status = db["users"][user_id]["status"]

    # it's managing case 👇
    
    if status == "managing":
        
        db["users"][user_id]["status"] = "managing2"
        db["users"][user_id]["additional_info"] = call.data

        await call.message.answer(texts["managing2"][user_lang], \
            reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

    else:
        await call.message.answer(texts["managing_call_e"][user_lang])

    upload_db(db)

def run() -> None:
    executor.start_polling(dp, skip_updates=True)