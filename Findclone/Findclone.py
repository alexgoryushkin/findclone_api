from requests import Session
from requests_toolbelt import MultipartEncoder

from .exceptions import *
from .utils import *
from .models import Response


class FindcloneApi:
    def __init__(self):
        self.session = Session()
        self.session.headers.update({'User-Agent': 'findclone-api/0.31'})
        self.session_key = None
        self.userid = None
        self.last_check = None
        self.builder = Response().build_response

    def login(self, login=None, password=None, session_key=None, userid=None):
        '''Авторизация на Findclone по сессии или логину и паролю'''
        if session_key and userid:
            self.session.headers.update({"session-key": session_key, "user-id":str(userid)})
            response = self.session.post("https://findclone.ru/profile")
            self.session_key = session_key
            error_handler(response)
            return True
        elif login and password:
            fields = {"phone": login, "password": password}
            multipart_str = multipart_string()
            payload = MultipartEncoder(fields=fields, boundary=f"----{multipart_str}")
            response = self.session.post("https://findclone.ru/login", data=payload,
                                         headers=multipart_headers(multipart_str))

            error_handler(response)
            self.session_key = response.json()["session_key"]
            self.userid = response.json()["userid"]
            self.session.headers.update({'session-key': self.session_key, 'user-id': str(self.userid)})
            return True
        else:
            raise FindcloneError("Need login and password or session-key and userid")

    @property
    def info(self):
        response = self.session.get("https://findclone.ru/profile")
        info = self.builder(response)
        return info

    def upload(self, file, face_box_id=None, timeout=180):
        '''file like url or filename'''

        if file.startswith("http"):
            file = self.session.get(file).content
            fields = {"uploaded_photo": (f"{random_string()}.png", file, "image/png")}
        else:
            fields = {"uploaded_photo": (f"{random_string()}.png", open(file, 'rb'), "image/png")}

        multipart_str = multipart_string()
        payload = MultipartEncoder(fields=fields, boundary=f"----{multipart_str}")
        response = self.session.post("https://findclone.ru/upload2", data=payload, timeout=timeout,
                                     headers=multipart_headers(multipart_str))

        if response.json().get("faceBoxes"):
            if face_box_id is not None:
                response = self.session.get("https://findclone.ru/upload3", params={"id": face_box_id})
            else:
                img_bytes = paint_boxes(file, response.json())  # return bytes IO object
                return img_bytes
        self.last_check = response.json()
        response = self.builder(response)
        return response

    def history(self, offset=0, count=100):
        response = self.session.get("https://findclone.ru/hist", params={"start": offset, "count": count})
        response = self.builder(response)
        return response

    def search(self, search_id, count=128):
        """выдача результата по id из истории"""
        response = self.session.get("https://findclone.ru/search", params={"id":search_id, "count":count})
        response = self.builder(response)
        return response

    @property
    def get_session(self):
        _session = {"session-key": self.session_key, "user-id": self.userid}
        return _session

    def __str__(self):
        response = self.info
        return response.__str__()

