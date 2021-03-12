import asyncio
from aiohttp import ClientSession, MultipartWriter
from Findclone.utils import *
from .models import *


class FindcloneAio:
    def __init__(self, session: ClientSession):
        self.session = session

    async def login(self, login, password, **kwargs):
        pass

    async def upload(self):
        pass


async def main():
    pass

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

