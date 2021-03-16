import asyncio
import aiohttp
from Findclone import FindcloneAsync


async def main(login, password):
    async with aiohttp.ClientSession() as session:
        findclone = FindcloneAsync(session)
        await findclone.login(login=login, password=password)
        print(await findclone.info)
        histories = await findclone.history()
        # get history search
        for history in histories:
            h_id = history.id
            profiles = await findclone.search(h_id)
            for profile in profiles:
                print(profile.raw_data)


if __name__ == '__main__':
    login = "123123123"
    password = "foobar"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(login, password))