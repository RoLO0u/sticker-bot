INSERT INTO public.packs(packid, title, adm, members, status, password)
	VALUES (%s, %s, %s, %s, %s, %s);

UPDATE public.users SET packs = %s WHERE userid = %s;