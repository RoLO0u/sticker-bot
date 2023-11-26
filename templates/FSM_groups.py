from aiogram.fsm.state import StatesGroup, State

class StartFSM(StatesGroup):
    start = State()
    exception = State()

class ManagingFSM(StatesGroup):
    choosing_pack = State()
    menu = State()
    collecting_emoji_add = State() # to add
    collecting_photo_add = State() # to add
    collecting_sticker = State() # to delete sticker
    delete_sticker = State() # to make sure to delete sticker
    are_you_sure = State() # to delete pack
    set_title = State()

class ChangeStickerFSM(StatesGroup):
    change_sticker_emoji = State()
    get_emoji_to_change = State()

class CreatingFSM(StatesGroup):
    creating_name = State()
    collecting_emoji = State()
    collecting_photo = State()

class JoiningFSM(StatesGroup):
    kick = State()
    join_pass = State()