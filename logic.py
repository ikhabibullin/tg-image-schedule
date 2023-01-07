import asyncio
from io import BytesIO

from configs import photo_drive, chats


async def save_photo(file_name: str, photo: BytesIO):
    _bytes = photo.read()
    await asyncio.to_thread(photo_drive.put, name=file_name, data=_bytes)
    photo.close()


def get_photo_from_drive(name: str) -> bytes:
    drive_obj = photo_drive.get(name)
    content = drive_obj.read()
    drive_obj.close()
    photo_drive.delete(name)
    return content


async def get_photo() -> bytes:
    images_info: dict = await asyncio.to_thread(photo_drive.list, limit=1)
    try:
        image_name: str = images_info['names'][0]
    except IndexError:
        return

    photo: bytes = await asyncio.to_thread(get_photo_from_drive, image_name)
    return photo


async def save_chat_id(chat_id: str):
    await asyncio.to_thread(chats.put, key=chat_id, data=chat_id)


async def fetch_chats():
    result = await asyncio.to_thread(chats.fetch)
    return [int(d['key']) for d in result.items]
