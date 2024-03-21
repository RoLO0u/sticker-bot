SELECT userid, packs, username, language, additional_info FROM public.users
    WHERE username = %s;