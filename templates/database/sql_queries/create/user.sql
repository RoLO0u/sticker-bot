INSERT INTO public.users
    (userid, packs, username, language, name, title, emoji, stickers, emojis, sticker, images)
	VALUES
    (%s, ARRAY []::VARCHAR [], %s, 'en', NULL, NULL, NULL, ARRAY []::VARCHAR [], ARRAY []::VARCHAR [], NULL, ARRAY []::VARCHAR []);