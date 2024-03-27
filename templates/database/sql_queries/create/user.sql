INSERT INTO public.users
    (userid, packs, username, language, name, title, emoji)
	VALUES
    (%s, ARRAY []::VARCHAR [], %s, 'en', NULL, NULL, NULL);