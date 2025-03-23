INSERT INTO public.users
    (userid, packs, username, language, name, title, emoji, stickers, emojis, sticker, image, first_name)
	VALUES
    (%s, ARRAY []::VARCHAR [], %s, 'en', NULL, NULL, NULL, ARRAY []::VARCHAR [], ARRAY []::VARCHAR [], NULL, NULL, %s);