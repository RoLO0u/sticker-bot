SELECT userid, packs, username, language, additional_info FROM public.users
    WHERE userid = %s;