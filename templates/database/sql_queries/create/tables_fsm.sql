CREATE TABLE IF NOT EXISTS public.data (
	"user_id" varchar(16) NOT NULL,
    "data" json,
	PRIMARY KEY ("user_id")
);

CREATE TABLE IF NOT EXISTS public.state (
    "user_id" varchar(16) NOT NULL,
	"state" varchar(64),
    PRIMARY KEY ("user_id")
);