from telethon import TelegramClient

api_id = 17597358
api_hash = '63ec84ff6b319b6fb87da66c5d3d2d29'


client = TelegramClient('anon', api_id, api_hash)

async def main():
    async for message in client.iter_messages('me'):
        print(message.id, message.text)
        if message.photo:
            print('File Name :' + str(message.file.name))
            path = await client.download_media(message.media, "/Users/user/Desktop/Backup")
            print('File saved to', path)  # printed after download is done

with client:
    client.loop.run_until_complete(main())