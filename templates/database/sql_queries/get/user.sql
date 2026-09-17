SELECT userid, packs, username, language, name, title, emoji, stickers, emojis, sticker, image, first_name, email FROM public.users
    WHERE userid = %s;