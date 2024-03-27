SELECT userid, packs, username, language, name, title, emoji, stickers, emojis FROM public.users
    WHERE username = %s;