SELECT userid, packs, username, language, name, title, emoji FROM public.users
    WHERE userid = %s;