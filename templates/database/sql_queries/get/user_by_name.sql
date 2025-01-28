SELECT userid, packs, username, language, name, title, emoji, stickers, emojis, sticker, images FROM public.users
    WHERE username = %s;