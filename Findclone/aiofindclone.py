from aiohttp import ClientSession, FormData

from .models import *
from .utils import random_string, paint_boxes
from .exceptions import a_error_handler, FindcloneError
from io import BufferedReader


class FindcloneAio:
    """async findclone api class
    Attributes:
        headers : dict - set requests headers
    """
    def __init__(self, session: ClientSession):
        self._session = session
        self.headers = {"User-Agent": "findclone-api/1.0"}
        self.__builder = Factory().build_aio_response
        self.session_key = None
        self.userid = None
        self.__info = None

    async def login(self, login: [str, None] = None, password: [str, None] = None, session_key: [str, None] = None,
                    userid: [str, int, None] = None) -> bool:
        """
        Findclone authorisation
        :param login:
        :param password:
        :param session_key:
        :param userid:
        :return:
        """
        if login and password:
            async with self._session.post("https://findclone.ru/login", data={"phone": login,
                                                                             "password": password}) as response:
                await a_error_handler(response)
                resp = await response.json()
                self.__info = await self.__builder(response)
                self.session_key = resp["session_key"]
                self.userid = resp["userid"]
                self.headers.update({'session-key': self.session_key, 'user-id': str(self.userid)})
                return True
        elif session_key and userid:
            self.headers.update({"session-key": session_key, "user-id": str(userid)})
            async with self._session.get("https://findclone.ru/profile", headers=self.headers) as response:
                await a_error_handler(response)
                self.__info = await self.__builder(response)
                self.session_key = session_key
                self.userid = userid
                return True
        else:
            raise FindcloneError("Need login and password or session-key and userid")

    @property
    async def info(self) -> Account:
        """
        return account information
        :return:
        """
        async with self._session.get("https://findclone.ru/profile", headers=self.headers) as response:
            info = await self.__builder(response)
            self.__info = info
        return info

    async def upload(self, file: [str, BufferedReader], face_box_id: int = None,
                     timeout: float = 180) -> [Profiles, BytesIO]:
        """
        upload image or image url and return Profiles object or BytesIO object
        :param file:
        :param face_box_id:
        :param timeout:
        :return:
        """
        data = FormData()
        if file.startswith("http"):
            async with self._session.get(file, headers=self.headers) as response:
                file = await response.read()
                data.add_field("uploaded_photo", file, filename=f"{random_string()}.png", content_type="image/png")
        else:
            data.add_field("uploaded_photo", open(file, "rb"), filename=f"{random_string()}.png", content_type="image/png")

        async with self._session.post("https://findclone.ru/upload2", data=data, headers=self.headers,
                                      timeout=timeout) as response:
            resp = await response.json()
            if resp.get("faceBoxes"):
                if face_box_id is not None:
                    async with self._session.get("https://findclone.ru/upload3", params={"id": face_box_id},
                                                 headers=self.headers) as response2:
                        resp = await self.__builder(response2)
                        return resp
                else:
                    img_bytes = paint_boxes(file, resp) # return bytesIO object
                    return img_bytes
            resp = await self.__builder(response)
            return resp

    async def history(self, offset: int = 0, count: int = 100) -> Histories:
        """
        return object history search for account
        :param offset: int
        :param count: int
        :return:
        """
        async with self._session.get("https://findclone.ru/hist", params={"offset":offset, "count": count},
                                     headers=self.headers) as response:
            history = await self.__builder(response)
        return history

    async def search(self, search_id: [int, str], count: int = 128) -> Profiles:
        """
        return Profiles object
        :param search_id: [int, str]
        :param count: [int]
        :return:
        """
        async with self._session.get("https://findclone.ru/search", params={"id": search_id, "count": count},
                                     headers=self.headers) as response:
            search_result = await self.__builder(response)
        return search_result

    @property
    def get_session(self) -> dict:
        """
        return session-key and userid account
        :return: {"session-key": session_key, "user-id": userid}
        """
        _session = {"session-key": self.session_key, "user-id": self.userid}
        return _session

    def __str__(self):
        return self.__info.__str__()
