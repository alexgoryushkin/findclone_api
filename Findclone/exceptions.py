from requests import Response


class FindcloneError(Exception):
    pass


def error_handler(response: Response):
    if response.status_code == 400 or response.status_code == 401 or response.json().get("Error"):
        raise FindcloneError(response.json()["Error"])
    else:
        return True
