from Findclone import Findclone

'''пример получения информации по фотографии'''

if __name__ == '__main__':
    phone = "123123123123"
    password = "foobar"
    # Или авторизация по сессии
    userid = 1337133755
    session_key = "li7p5u5tkdyi4ie5wn5w43nezctw5pfmueep4l5khvjgppo4voawkl7y5lmbt2vp"
    findclone = Findclone.FindcloneApi()
    # настройка объекта сессии из requests.Session()
    findclone.session.headers.update({"foo":"bar"})
    findclone.session.verify = False
    findclone.login(session_key=session_key, userid=userid)
    findclone.login(phone, password)
    auth_session = findclone.get_session  # получение данных сессии для авторизации
    print(findclone)  # получение информации об аккаунте
    # Загрузка фотографии на Findclone. Поддерживает файл изображения или ссылку на него
    response = findclone.upload("test.jpg")  # Или f.upload("https://mysitefoobar.com/test.jpg")
    # при обнаружение более 2х лиц необходимо добавить проверку условия, сохранить фотографию и отправить дополнительно face_box_id
    if isinstance(response, list):
        for profile in response.profiles_list:  # парсинг данных с помощью встроенных функций
            print(profile)
    else:
        # сохранения изображения с отрисованными квадратами и нумерацией лиц
        with open("img.jpg", "wb") as file:
            file.write(response.getvalue())
    face_id = input("face_id ->")
    response = findclone.upload("test.jpg", face_box_id=face_id)
    for profile in response.profiles_list:  # парсинг данных с помощью встроенных функций
        print(profile)
        print(profile.url, profile.city, profile.score)
