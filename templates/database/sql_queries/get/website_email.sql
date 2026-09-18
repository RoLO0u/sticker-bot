SELECT email, banned, telegram FROM public.user
    WHERE email = %s;