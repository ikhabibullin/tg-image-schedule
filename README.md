# Telegram bot for sending images to channel by schedule

## - Working on Deta(like Heroku and free)
## - stack: fastapi, aiogram

## - Workflow
### 1. Add bot to channel like admin
### 2. In channel: Send msg '/chain', if ok bot send msg 'Channel chained', this means the channel will receive images
### 3. In private chat: send photo for adding to storage

## - Prelude
### 1. Need to register https://www.deta.sh/
### 2. Install client by docs https://docs.deta.sh/docs/micros/getting_started
### 3. Create bot in @BotFather, change access to message in channels, get token
### 4. Set your env variables to .env by .env.example
### 5. update env vars on deta - `deta update --env env_file`
### 6. deploy project - `deta deploy`
### 7. create cron for sending images - `deta cron set "5 hours"`
