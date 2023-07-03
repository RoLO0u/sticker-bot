DO $$
BEGIN
	IF EXISTS 
		(SELECT user_id FROM public.data
			WHERE user_id=%s)
	THEN
		UPDATE public.data SET data = %s WHERE user_id = %s;
	ELSE
		INSERT INTO public.data (user_id, data) VALUES (%s, %s);
	END IF;
END
$$