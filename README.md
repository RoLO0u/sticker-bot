# Sticker packs telegram bot

![GitHub](https://img.shields.io/github/license/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub last commit](https://img.shields.io/github/last-commit/RoLO0u/sticker-bot?style=for-the-badge) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/RoLO0u/sticker-bot?style=for-the-badge) ![Python Version](https://img.shields.io/badge/Python-3.13-informational?style=for-the-badge&logo=python) ![GitHub watchers](https://img.shields.io/github/watchers/RoLO0u/sticker-bot?style=for-the-badge)

## Try it right now!

[@paces_bot](https://t.me/paces_bot)

# Installation

Bot simply can be installed by running code on machine using required variables in .env file

> If you're using webhooks, you should set up reverse proxy. You can start with [aiogram documentation](https://docs.aiogram.dev/en/v3.17.0/dispatcher/webhook.html#examples) or [read tutorial on webhooks](https://t.me/aiogram_hent/77) (the tutorial is in ukrainian🇺🇦). Both use nginx and tutorial uses certbot.

## Installation guide step by step

1. Requirements

* [Python >3.10.x](https://www.python.org/)
* [pip](https://pip.pypa.io/en/stable/installation/)
* [postgresql](https://www.postgresql.org/download/)
* [git](https://git-scm.com/downloads)

2. Clone project

```bash
git clone https://github.com/RoLO0u/sticker-bot.git
```

3. Install python requirements

```bash
pip install -r requirements.txt
```

> :warning: **when having problems installing psycopg2**: try running
>
> on debian:
> ```bash
> sudo apt-get install libpq-dev
> ```
> on arch:
> ```bash
> sudo pacman -Sy postgresql-libs
> ```
> [source](https://stackoverflow.com/questions/65821330/how-to-solve-error-failed-building-wheel-for-psycopg2)
> 
> on Amazon Linux:
> ```bash
> sudo yum -y install gcc python-setuptools python-devel postgresql-devel
> ```
> [source](https://stackoverflow.com/questions/42658406/error-installing-psycopg2-on-amazon-linux)
> 
> on MacOS:
> ```bash
> brew install postgresql
> ```


4. Set environment variables

Environment variables can be seen in *Required variables* part or in *.env.example* file

5. Run programm

To run programm use simple command depending on your configuration:

```bash
python main.py
```

If you want to save logs in ```main.log```, you can use ```--log-file``` arg
```bash
python main.py --log-file
```

Or use virtual environment variables AND docker

# Deploying to Heroku

The bot supports Telegram webhooks and long polling. For webhooks on Heroku,
run the `web` process; Heroku supplies the listening port through `PORT`, and
terminates HTTPS before forwarding requests to the dyno.

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
   and log in:

   ```bash
   heroku login
   heroku create your-app-name
   heroku addons:create heroku-postgresql:essential-0 --app your-app-name
   ```

2. Copy the database name, host, port, username, and password from the add-on's
   credentials. This project expects the individual `PG*` variables; it does
   not read Heroku's `DATABASE_URL`.

3. Set the app's config vars (replace the placeholders with your values; don't
   commit credentials):

   ```bash
   heroku config:set \
     BOT_TOKEN=your-telegram-bot-token \
     DEBUG=False \
     WEBHOOK=True \
     BASE_WEBHOOK_URL=https://your-app-name.herokuapp.com \
     WEBHOOK_PATH=/telegram \
     WEBHOOK_SECRET=your-random-webhook-secret \
     SERVER_HOST=0.0.0.0 \
     PGDATABASE=your-database-name \
     PGHOST=your-postgres-host \
     PGPORT=5432 \
     PGUSER=your-postgres-user \
     PGPASSWORD=your-postgres-password \
     PGWEBSITEDATABASE=your-database-name \
     SSLMODE=require \
     --app your-app-name
   ```

   `PGWEBSITEDATABASE` is required. Set it to the same database name if the
   website data should share the bot database, or to the name of a separate
   database if you keep that data separately.

   Use your app's actual HTTPS URL for `BASE_WEBHOOK_URL`, without a trailing
   slash. Generate a unique `WEBHOOK_SECRET`; do not commit it. The app binds
   to Heroku's `PORT` automatically. Do not set `WEBHOOK_SSL_CERT` on Heroku:
   TLS is terminated by the Heroku router.

4. Deploy and start the web dyno:

   ```bash
   git push heroku HEAD:main
   heroku ps:scale web=1 worker=0 --app your-app-name
   heroku logs --tail --app your-app-name
   ```

For long polling instead, set `WEBHOOK=False` and scale `worker=1` with
`web=0`. Heroku config vars are used directly, so a `.env` file should not be
deployed.

# Required variables

## PostgreSQL

* PGDATABASE - database information will be stored in. e.g. aiogram, to create use 
```sql
CREATE DATABASE aiogram; -- or another database name
```
* PGHOST - your address to the postgresql. On local machines should be 127.0.0.1
* PGPORT - port to your postgresql server. Most likely 5432
* PGUSER - user who will be used to execute commands with (e.g. postgres).
* PGPASSWORD - password to user

## Telegram bot configuration

* BOT_TOKEN ─ token bot will use to interact with telegram API
> Use [@BotFather](https://t.me/BotFather) to get bot token

## Debugging

* DEBUG - either `True` or `False`. If `False` only shows `WARNING` level logs.

## Long polling

* WEBHOOK - `False` if you want to use long polling

## Webhook

* WEBHOOK - `True`
* WEBHOOK_SECRET ─ a string of random characters. [Read more here](https://core.telegram.org/bots/api#setwebhook).
* BASE_WEBHOOK_URL ─ an URL to which telegram will send updates to
### Optional
* WEBHOOK_PATH - path to the bot e.g. "telegram-sticker-bot"
* SERVER_HOST - local IPv4 e.g. 127.0.0.1
* SERVER_PORT - local port used e.g. 8080

> If you're encountering issues, read [aiogram documentation](https://docs.aiogram.dev/en/v3.17.0/dispatcher/webhook.html#examples) or [official telegram documentation](https://core.telegram.org/bots/webhooks)

# Migration, database testing, updating

Run db_cli.py script to execute sql from "sql_queries" folder.

When using choose script to execute by entering its number or quit by entering "q"

# Resources

* [aiogram 3 documentation](https://docs.aiogram.dev/en/dev-3.x/)

* [Telegram API](https://core.telegram.org/bots/api)

* [Anti-flood bot](https://github.com/RoLO0u/anti-flood-bot)
