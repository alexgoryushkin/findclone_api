from requests import Session

from .exceptions import FindcloneError, error_handler
from .utils import random_string, paint_boxes
from .models import get_builder, Account, Profiles, Histories
from io import BufferedReader, BytesIO


class FindcloneApi:
    """sync findclone api class
    Attributes:
        session: Session() - requests.Session() object"""
    def __init__(self):
        self.session = Session()
        self.session.headers.update({'User-Agent': 'findclone-api/1.0'})
        self._session_key = None
        self._userid = None

        self.__builder = get_builder().build_response

    def login(self, login: [str, None] = None, password: [str, None] = None, session_key: [str, None] = None,
              userid: [int, str, None] = None) -> bool:
        """
        Findclone authorisation
        :param login:
        :param password:
        :param session_key:
        :param userid:
        :return:
        """
        if session_key and userid:
            self.session.headers.update({"session-key": session_key, "user-id": str(userid)})
            response = self.session.get("https://findclone.ru/profile")
            self._session_key = session_key
            error_handler(response)
            return True
        elif login and password:
            response = self.session.post("https://findclone.ru/login",
                                         data={"phone": login, "password": password})
            error_handler(response)
            self._session_key = response.json()["session_key"]
            self._userid = response.json()["userid"]
            self.session.headers.update({'session-key': self._session_key, 'user-id': str(self._userid)})
            return True
        else:
            raise FindcloneError("Need login and password or session-key and userid")

    @property
    def info(self) -> Account:
        """
        return Account object
        :return Account:
        :type Account:
        """
        response = self.session.get("https://findclone.ru/profile")
        info = self.__builder(response)
        return info

    def upload(self, file: [str, BufferedReader], face_box_id: [None, int] = None,
               timeout: [float] = 30) -> [Profiles, BytesIO]:
        """
        upload file on read file or url and return Profiles object if founded 1 face else return BytesIO object
        :param file: url or file bytes object
        :param face_box_id: int
        :param timeout: float
        :return:
        """
        if file.startswith("http"):
            file = self.session.get(file).content
            fields = {"uploaded_photo": (f"{random_string()}.png", file, "image/png")}
        else:
            fields = {"uploaded_photo": (f"{random_string()}.png", open(file, 'rb'), "image/png")}

        response = self.session.post("https://findclone.ru/upload2", files=fields, timeout=timeout)

        if response.json().get("faceBoxes"):
            if face_box_id is not None:
                response = self.session.get("https://findclone.ru/upload3", params={"id": face_box_id})
            else:
                img_bytes: BytesIO = paint_boxes(file, response.json())  # return bytes IO object
                return img_bytes
        profiles: Profiles = self.__builder(response)
        return profiles  # return Profiles Object

    def history(self, offset: int = 0, count: int = 100) -> Histories:
        """
        return history search for account
        :param offset: int
        :param count: int
        :return:
        """
        response = self.session.get("https://findclone.ru/hist", params={"start": offset, "count": count})
        history = self.__builder(response)
        return history

    def search(self, search_id: [int, str], count: int = 128) -> Profiles:
        """
        return profiles for history search results
        :param search_id: [int, str]
        :param count: int
        :return:
        """
        response = self.session.get("https://findclone.ru/search", params={"id": search_id, "count": count})
        search_result = self.__builder(response)
        return search_result

    @property
    def get_session(self) -> dict:
        """
        return session-key and userid account
        :return:  {'session-key': key, "user-id": userid}
        """
        _session = {'session-key': self._session_key, "user-id": self._userid}
        return _session

    def __str__(self):
        """
        return account information
        :return self.info:
        """
        response = self.info
        return response.__str__()
