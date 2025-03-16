SELECT userid, packs, username, language, name, title, emoji, stickers, emojis, sticker, image FROM public.users
    WHERE username = %s;