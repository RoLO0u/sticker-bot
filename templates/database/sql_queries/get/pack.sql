SELECT packid, title, adm, members, status, password FROM public.packs
    WHERE packid = %s;