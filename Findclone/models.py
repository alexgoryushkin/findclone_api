from requests import Response as _Response
from datetime import datetime


class Response:
    '''Класс построения объектов ответа'''

    def __init__(self):
        pass

    @staticmethod
    def build_response(response: _Response):
        # Объект информации об аккаунте
        if response.url.endswith("profile"):
            account = Account()
            response = response.json()
            account.info = response
            account.quantity = response["Quantity"]
            account.period = response["Period"]
            account.typename = response["TypeName"]
            account.userid = response["userid"]
            return account
        # Объект информации истории поиска
        elif response.url.split("?")[0].endswith("hist"):
            histories = Histories()
            response = response.json()[0]
            histories.histories = response
            histories.prettify()
            return histories
        # Объект информации о найденных профилях
        elif response.url.split("?")[0].endswith("search"):
            profiles = Profiles()
            response = response.json()
            profiles.profiles = response["data"]
            profiles.total = response["Total"]
            profiles.prettify()
            return profiles
        elif response.url.split("?")[0].endswith("upload2") or response.url.split("?")[0].endswith("upload3") \
                or response.url.split("?")[0].endswith("upload"):
            profiles = Profiles()
            response = response.json()
            profiles.profiles = response["data"]
            profiles.total = response["Total"]
            profiles.prettify()
            return profiles


class Account:
    '''класс информации об аккаунте findclone'''

    def __init__(self):
        self.info = None  # полный json ответ
        self.quantity = None  # количество запросов
        self.period = None  # срок подписки, в секундах
        self.typename = None  # тип подписки
        self.history = None  # история поиска, первые 12 аккаунтов
        self.userid = None  # id аккаунта

    def __str__(self):
        return f"quantity: {self.quantity} period: {self.period_days} type: {self.typename}"

    def __repr__(self):
        return self.info

    @property
    def period_days(self):
        """Конвертирование секунд в дни"""
        return int(round(self.period / 60 / 60 / 24, 0)) - 1


class Histories:
    '''класс объекта истории поиска'''

    def __init__(self):
        self.histories = None
        self.history_list = list()

    def prettify(self):
        for _history in self.histories:
            history = History()
            history.data = _history
            history.date = _history["date"]
            history.id = _history["id"]
            history.thumbnail = _history["thumbnail"]
            self.history_list.append(history)

    def __repr__(self):
        return self.histories

    def __str__(self):
        return str(len(self.histories))


class History:
    def __init__(self):
        self.data = None
        self.date = None
        self.id = None
        self.thumbnail = None

    def unix_to_date(self, format_time='%Y-%m-%d %H:%M:%S'):
        return datetime.utcfromtimestamp(int(self.date)).strftime(format_time)

    def __str__(self):
        return f"{self.unix_to_date()} {self.id}"

    def __repr__(self):
        return self.data


class Profiles:
    '''класс объекта профилей из поиска'''

    def __init__(self):
        self.profiles = None
        self.total = None
        self.thumbnail = None
        self.profiles_list = list()

    def prettify(self):
        for _profile in self.profiles:
            profile = Profile()
            age = _profile["Age"] if _profile.get("Age") else None
            city = _profile["city"] if _profile.get("city") else None
            details = _profile["details"]
            firstname = _profile["firstname"]
            score = _profile["score"]
            url = "https://vk.com/id" + str(_profile['userid'])

            profile.profile = _profile
            profile.age = age
            profile.city = city
            profile.details = details
            profile.firstname = firstname
            profile.score = score
            profile.url = url
            self.profiles_list.append(profile)

    def __repr__(self):
        return self.profiles


class Profile:
    """класс объекта профиля"""

    def __init__(self):
        self.profile = None
        self.age = None
        self.city = None
        self.details = None
        self.firstname = None
        self.score = None
        self.url = None

    def __str__(self):
        return f"{self.url} {self.firstname} {self.score} {self.city} {self.age}"

    def __repr__(self):
        return self.profile


