ALTER TABLE IF EXISTS public.users
    ADD COLUMN name character varying(255),
    ADD COLUMN title character varying(64),
    ADD COLUMN emoji character varying(255),
    DROP COLUMN additional_info;