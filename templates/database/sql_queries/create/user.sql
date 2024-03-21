INSERT INTO public.users
    (userid, packs, username, language, additional_info)
	VALUES
    (%s, ARRAY []::VARCHAR [], %s, 'en', '{"emoji": null, "name": null, "title": null}');