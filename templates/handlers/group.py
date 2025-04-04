from aiogram import Router, types, F

router = Router()

@router.message(F.chat.type.in_({"group", "supergroup"}), F.text)
async def group_warning(message: types.Message) -> None:
    
    await message.answer("This bot is not available in groups yet. Please, use it in private chat.")