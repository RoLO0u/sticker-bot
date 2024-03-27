SELECT userid, packs, username, language, name, title, emoji, stickers, emojis, sticker FROM public.users
    WHERE username = %s;