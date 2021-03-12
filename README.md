Findclone API by vypivshiy
Findclone API requests for humans(c)
установка:
прописать в консоли:
`pip install findclone_api`
requirements:
```
requests
requests_toolbelt
```
Quick start:
```python
from Findclone import Findclone

'''пример получения информации по фотографии'''

if __name__ == '__main__':
    phone = "ТЕЛЕФОН ДЛЯ АВТОРИЗАЦИИ В FINDCLONE"
    password = "ПАРОЛЬ ДЛЯ АВТОРИЗАЦИИ В FINDCLONE"
    f = Findclone.Findclone()
    f.login(phone, password)
    print(f.info)  # получение информации об аккаунте
    print(f.periods)  # перевод секунд в сутки активной подписки
    print(f.quantity)  # получение попыток оставшихся проверок
    # Загрузка фотографии на Findclone
    f.upload("test2.jpg")
    # Или f.upload("прямая ссылка на фотографию")
    # получение результата обработки (весь запрос)
    print(f.profiles)
    # парсинг данных с помощью встроенных функций
    for profile in f.profiles:
        print(f.firstname(profile), f.vk_url(profile), f.city(profile), f.score(profile), f.age(profile), f.photo_list(profile))
```
запланированный TODO list что добавить и исправить:
* Допилить методы по истории проверок
* Отловить и исправить баги
* Придумать алгоритм дейстий при нахождении более 1 лица
* asyncio версия библиотеки
* Рефакторинг, оптимизация кода