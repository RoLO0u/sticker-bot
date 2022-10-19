import logging
import json
import os

from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram.utils.markdown import hide_link

from templates import database, Exceptions

from templates.funcs import is_emoji, resize_image, \
    pack_availability, random_string, user_packs # Private Messages
from templates.markups import start_button, start_button_exception1, cancel_button, \
    managing_button, pack_link_button, managing_button_2, managing_button_inline

# TODO move not bot work to other files
# configuring aiogram bot

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if TOKEN == None:
    raise Exceptions.TokenDoesNotDefined()

with open("texts.json", "r", encoding="utf-8") as raw_texts:
    texts = json.load(raw_texts)

bot = Bot(TOKEN)
dp = Dispatcher(bot)

WATERMARK = "_by_paces_bot"

# TODO correction of status

@dp.message_handler(commands=["start"], chat_type="private")
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    user_lang, *_ = database.reg_user(user_id, username)
    
    if username is None:
        database.change_status(user_id, "start_exception_1")
        await message.answer(texts["start_exception_1"][user_lang], parse_mode="HTML", \
            reply_markup=start_button_exception1( texts["start_button_exception_1"][user_lang] ))

    else:
        database.change_status(user_id, "start")
        await message.answer(texts["start"][user_lang], parse_mode="HTML", \
            reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

@dp.message_handler(commands=["help"], chat_type="private")
async def help(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username

    user_lang, *_ = database.reg_user(user_id, username)

    await message.answer(f"{hide_link('https://i.imgur.com/ZRv0bDC.png')}"
        f"{texts['help_1'][user_lang]}", parse_mode="HTML")

@dp.message_handler(commands=["test"], chat_type="private")
async def test_func(message: types.Message):
    if message.from_user.id == 602197013:
        to_check = 7
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
            case 4:
                await message.answer(database.get_user_info(f"{message.from_user.id}"))
            case 5:
                database.change_status(f"{message.from_user.id}", "start")
            case 6:
                database.get_user_packs_name(f"{message.from_user.id}")
            case 7:
                database.get_all_packs()

@dp.message_handler(content_types=["text", "photo", "sticker"], chat_type="private")
async def text_processing(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username

    user_lang, status = database.reg_user(user_id, username)

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
                        ch_lan_en, ch_lan_ua, ch_lan_is = answers[3]

                    # TODO: make match case better. More: README.md

                    match message.text:

                        # TODO check packs availibility

                        case Answers.join_btn_en|Answers.join_btn_ua:

                            await message.answer(texts["joined"][user_lang], \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                        case Answers.create_btn_en|Answers.create_btn_ua:
                            
                            database.change_status(user_id, "creating")

                            await message.answer(texts["creating1"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                        case Answers.man_btn_en|Answers.man_btn_ua:

                            database.change_status(user_id, "managing")
                            await message.answer(texts["managing0"][user_lang], \
                                reply_markup=managing_button(texts["back"][user_lang]))

                            to_pop = []
                            for pname in database.get_user_packs_name(user_id):
                                if not await pack_availability(bot.get_sticker_set, \
                                    utils.exceptions.InvalidStickersSet, pname + WATERMARK) or not database.get_pack(pname)["stickers"]:
                                    to_pop.append(pname)
                            for pname in to_pop:
                                # TODO don't forget to edit when members support added
                                database.delete_pack(user_id, pname)

                            # user have packs
                            if database.get_user_packs_name(user_id):
                                await message.answer(texts["managing"][user_lang], \
                                    reply_markup=managing_button_inline(user_packs(database.get_all_packs(), \
                                    database.get_user_packs_name(user_id))))
                            
                            else:
                                await message.answer(texts["managing_e"][user_lang])

                        case Answers.ch_lan_en|Answers.ch_lan_ua|Answers.ch_lan_is:

                            match message.text:
                                
                                case Answers.ch_lan_en:

                                    change_to = "en"
                                
                                case Answers.ch_lan_ua:

                                    change_to = "ua"

                                case Answers.ch_lan_is:

                                    change_to = "is"

                            database.change_lang(user_id, change_to)

                            user_lang = database.get_user_lang(user_id)

                            await message.answer(texts["lan_changed"][user_lang], \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                        case _:
                            await message.answer(texts["unknown_exception_2"][user_lang])

                case "start_exception_1":

                    if message.text in texts["start_button_exception_1"].values():
                        
                        if username is None:
                            database.change_status(user_id, "start_exception_1")
                            await message.answer(texts["start_exception_1"][user_lang], \
                                reply_markup=start_button_exception1( texts["start_button_exception_1"][user_lang] ))

                        else:
                            database.change_status(user_id, "start")
                            await message.answer(texts["start"][user_lang], parse_mode="HTML", \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
                
                case "creating":

                    class Answers:
                        create_btn_en, create_btn_ua = texts["cancel_button"].values()

                    match message.text:

                        case Answers.create_btn_en|Answers.create_btn_ua:

                            database.change_status(user_id, "start")

                            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))

                        case _ if len(message.text) <= 64:

                            name = random_string()

                            while name in database.get_packs_name():
                                name = random_string()
                            
                            database.create_pack(user_id, name, message.text)
                            database.change_status(user_id, "creating2")
                            database.change_name(user_id, name)

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

                            database.change_status(user_id, "start")
                            database.delete_pack(user_id)
                            database.change_name(user_id, None)

                            await message.answer(texts["cancel"][user_lang], parse_mode="HTML", \
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
                        
                        case _:

                            if is_emoji(message.text):

                                database.change_emoji(user_id, message.text)
                                database.change_status(user_id, "creating3")

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

                            database.change_status(user_id, "start")
                            pack_name = database.get_additional_info(user_id)
                            database.delete_pack(user_id, pack_name["name"])
                            database.change_emoji(user_id, None)
                            database.change_name(user_id, None)

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

                            database.change_status(user_id, "start")

                            await message.answer(texts["backed"][user_lang],\
                                reply_markup=start_button( texts["start_buttons"][user_lang], texts["change_lang_buttons"] ))
                            
                        case _:
                            await message.answer(texts["managing_exception_1"][user_lang])
                
                case "managing2":

                    packs = user_packs(database.get_all_packs(), database.get_user_packs_name(user_id))
                    
                    # TODO create inline sticker pick like in @Stickers bot

                    class Answers:
                        back_btn = texts["managing_buttons_2"][user_lang][-1]
                        add_btn = texts["managing_buttons_2"][user_lang][0]
                        del_stick_btn = texts["managing_buttons_2"][user_lang][1]
                        del_pack_btn = texts["managing_buttons_2"][user_lang][-4]
                        show_btn = texts["managing_buttons_2"][user_lang][-2]

                    match message.text:
                        
                        case Answers.back_btn:
                            database.change_status(user_id, "managing")
                            await message.answer(texts["managing0"][user_lang], \
                                reply_markup=managing_button(texts["back"][user_lang]))

                            to_pop = []
                            for pname in database.get_user_packs_name(user_id):
                                if not await pack_availability(bot.get_sticker_set, \
                                        utils.exceptions.InvalidStickersSet, pname + WATERMARK):
                                    to_pop.append(pname)
                            for pname in to_pop:
                                database.delete_pack(user_id, pname)
                        
                            await message.answer(texts["managing"][user_lang], \
                                reply_markup=managing_button_inline(user_packs(database.get_all_packs(), \
                                database.get_user_packs_name(user_id))))

                        case Answers.add_btn:
                            database.change_status(user_id, "managing_add_1")
                            await message.answer(texts["managing_add_1"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                        case Answers.del_stick_btn:
                            database.change_status(user_id, "managing_del_1")
                            await message.answer(texts["managing_del_1"][user_lang], \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))
                        
                        case Answers.del_pack_btn:
                            database.change_status(user_id, "managing_del2_1")
                            await message.answer(texts["managing_del2_1"][user_lang], parse_mode="markdown", \
                                reply_markup=cancel_button(texts["cancel_button"][user_lang]))

                        case Answers.show_btn:
                            sticker = await bot.get_sticker_set(database.get_additional_info(user_id)["name"]+WATERMARK)
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
                            database.change_status(user_id, "managing2")
                            await message.answer(texts["managing2"][user_lang], \
                                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

                        case _:

                            if is_emoji(message.text):

                                database.change_status(user_id, "managing_add_2")
                                database.change_emoji(user_id, message.text)
                                await message.answer(texts["managing_add_2"][user_lang], \
                                    reply_markup=cancel_button(texts["cancel_button"][user_lang]))
                        
                            else:
                                await message.answer(texts["emoji_only_e"][user_lang])
                
                case "managing_add_2":

                    class Answers:
                        cancel_btn = texts["cancel_button"][user_lang]

                    match message.text:

                        case Answers.cancel_btn:
                            database.change_status(user_id, "managing2")
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
                            database.change_status(user_id, "managing2")
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
                            database.change_status(user_id, "managing2")
                            await message.answer(texts["managing2"][user_lang], \
                                reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

                        case Answers.confirming:
                            database.change_status(user_id, "start")
                            set_name = database.get_additional_info(user_id)["name"]
                            database.delete_pack(user_id, set_name)
                            sticker_set = await bot.get_sticker_set(set_name+WATERMARK)
                            for sticker in sticker_set.stickers:
                                await bot.delete_sticker_from_set(sticker.file_id)
                            database.change_name(user_id, None)
                            await message.answer(texts["pack_deleted"][user_lang], \
                                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

                        case _:
                            await message.answer(texts["unknown_exception_1"][user_lang]+"4")

                case _:
                    await message.answer(texts["unknown_exception_1"][user_lang]+'1')

    
        case "photo":

            match status:

                case "creating3":

                    # TODO: make multiple emojis to sticker possible
                    # TODO: make webm and tgs image format possible

                    additional_info = database.get_additional_info(user_id)
                    pack_name = additional_info["name"]
                    pack_name_plus = pack_name + WATERMARK
                    # print(1, pack_name)
                    raw_file = await bot.get_file(message.photo[len(message.photo)-1].file_id)
                    photo = resize_image(await bot.download_file(raw_file.file_path), user_id )
                    emoji = additional_info["emoji"]
                    
                    try:
                        if await bot.create_new_sticker_set(int(user_id), pack_name_plus, \
                            database.get_pack(pack_name)["title"], emoji, png_sticker=photo):

                            database.change_status(user_id, "start")
                            database.change_name(user_id, None)
                            database.change_emoji(user_id, None)
                            database.change_pack_status(pack_name, "maked")
                            created_pack = await bot.get_sticker_set(pack_name_plus)
                            # print(created_pack.stickers, created_pack.stickers[0].file_unique_id)
                            database.change_pack_stickers(pack_name, [created_pack.stickers[0].file_unique_id])

                            await message.answer(texts["created1"][user_lang], \
                                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + WATERMARK))
                            await message.answer(texts["created2"][user_lang], \
                                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))

                        else:
                            await message.answer(texts["unknown_exception_1"][user_lang]+'2')

                    except utils.exceptions.InvalidStickersSet as e:
                        await message.answer(texts["known_e_1"][user_lang]+str(e).split()[-1])
                
                case "managing_add_2":

                    additional_info = database.get_additional_info(user_id)
                    emoji = additional_info["emoji"]
                    pack_name = additional_info["name"]

                    pack_name_plus = pack_name + WATERMARK
                    file_raw = await bot.get_file(message.photo[len(message.photo)-1].file_id)
                    file_raw = await bot.download_file(file_raw.file_path)
                    photo = resize_image(file_raw, user_id )
                    
                    try:
                        
                        if await bot.add_sticker_to_set(int(user_id), pack_name_plus, \
                            emoji, png_sticker=photo):
                            database.change_status(user_id, "start")
                            database.change_name(user_id, None)
                            database.change_emoji(user_id, None)
                            sticker_set = await bot.get_sticker_set(pack_name_plus)
                            database.change_pack_stickers(pack_name, [sticker.file_unique_id for sticker in sticker_set.stickers])

                            await message.answer(texts["added1"][user_lang], \
                                reply_markup=pack_link_button(texts["created_inline"][user_lang], "https://t.me/addstickers/" + pack_name + WATERMARK))
                            await message.answer(texts["created2"][user_lang], \
                                reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))
                    
                    except utils.exceptions.InvalidStickersSet:
                        database.change_status(user_id, "start")
                        database.change_name(user_id, None)
                        database.change_emoji(user_id, None)
                        database.delete_pack(pack_name)
                        await message.answer(texts["managing_add_e"][user_lang], \
                            reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))
                        
                case _:
                    await message.answer(texts["unknown_exception_3"][user_lang])
        
        case "sticker":

            match status:

                case "managing_del_1":

                    database.change_status(user_id, "start")

                    sticker_id = message.sticker.file_id
                    unique_id = message.sticker.file_unique_id

                    # TODO: make warning message if it's last sticker

                    # checking if sticker in user stickerpack
                    if unique_id in database.get_pack(database.get_additional_info(user_id)["name"])["stickers"]:

                        pack_name = database.get_additional_info(user_id)["name"]

                        database.remove_sticker_from_pack(pack_name, unique_id)

                        await bot.delete_sticker_from_set(sticker_id)

                        await message.answer(texts["deleted"][user_lang], \
                            reply_markup=start_button(texts["start_buttons"][user_lang], texts["change_lang_buttons"]))
                    
                    else:
                        await message.answer(texts["managing_del_e"][user_lang])

                case _:
                    await message.answer(texts["unknown_exception_3"][user_lang])

@dp.callback_query_handler(lambda call: True and call.message)
async def callhandler(call):

    user_id = str(call.from_user.id)
    username = call.from_user.username

    user_lang, status = database.reg_user(user_id, username)

    # it's managing case 👇
    
    if status == "managing":
        
        database.change_status(user_id, "managing2")
        database.change_name(user_id, call.data)

        await call.message.answer(texts["managing2"][user_lang], \
            reply_markup=managing_button_2(texts["managing_buttons_2"][user_lang]))

    else:
        await call.message.answer(texts["managing_call_e"][user_lang])

def run() -> None:
    executor.start_polling(dp, skip_updates=True)