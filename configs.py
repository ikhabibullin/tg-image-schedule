import os

import deta

ENV = os.getenv('ENV', 'local')

TOKEN = os.getenv('TOKEN')
WEBHOOK_PATH = f'/bot/{TOKEN}'
WEBHOOK_URL = os.getenv('WEBHOOK_HOST') + WEBHOOK_PATH
ALLOW_IDS = set(map(int, os.getenv('ALLOW_IDS').split(' '))) if os.getenv('ALLOW_IDS') is not None else set()
SENTRY_DSN = os.getenv('SENTRY_DSN')

deta = deta.Deta(os.getenv('DETA_PROJECT_KEY'))
photo_drive = deta.Drive('photos')
chats = deta.Base('chats')
