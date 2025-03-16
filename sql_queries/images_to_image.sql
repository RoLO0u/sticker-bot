ALTER TABLE IF EXISTS public.users
    DROP COLUMN images,
    ADD COLUMN image character varying(255);