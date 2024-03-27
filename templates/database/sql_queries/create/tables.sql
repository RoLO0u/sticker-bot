CREATE TABLE IF NOT EXISTS public.users (
	"userid" varchar(16) NOT NULL,
    "packs" varchar(10) [],
    "username" varchar(64),
    "language" varchar(4) NOT NULL,
    "name" character varying(255),
    "title" character varying(64),
    "emoji" character varying(255),
	PRIMARY KEY ("userid")
);

CREATE TABLE IF NOT EXISTS public.packs (
    "packid" varchar(10) NOT NULL,
	"title" varchar(64) NOT NULL,
    "adm" varchar(16) NOT NULL,
    "members" varchar(16) [],
    "status" varchar(8) NOT NULL,
    "password" varchar(10) NOT NULL,
    PRIMARY KEY ("packid")
);