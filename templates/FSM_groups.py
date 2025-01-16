from aiogram.fsm.state import StatesGroup, State

class StartFSM(StatesGroup):
    start = State()
    exception = State()

class ManagingFSM(StatesGroup):
    choosing_pack = State()
    menu = State()
    collecting_emoji_add = State()
    collecting_photo_add = State()
    collecting_sticker = State()
    delete_sticker = State()
    are_you_sure = State()
    set_title = State()

class ChangeStickerFSM(StatesGroup):
    change_sticker_emoji = State()
    get_emoji_to_change = State()

class CreatingFSM(StatesGroup):
    choosing_option = State()
    copying_pack = State()
    creating_name = State()
    collecting_emoji = State()
    collecting_photo = State()

class JoiningFSM(StatesGroup):
    kick = State()
    join_pass = State()