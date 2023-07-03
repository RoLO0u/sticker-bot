DO $$
BEGIN
	IF EXISTS 
		(SELECT user_id FROM public.state
			WHERE user_id=%s)
	THEN
		UPDATE public.state SET state = %s WHERE user_id = %s;
	ELSE
		INSERT INTO public.state (user_id, state) VALUES (%s, %s);
	END IF;
END
$$