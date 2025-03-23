SELECT userid, packs, username, language, name, title, emoji, stickers, emojis, sticker, image, first_name FROM public.users
    WHERE username = %s;