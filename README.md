<h2>Findclone API by vypivshiy</h2>
<h3>Описание</h3>
findclone-api - это библиотка для взаимодействия с сайтом [Findclone.ru](https://findclone.ru) 
на уровне высокоуровневых запросов.
Присутствет синхронная и __асинхронная__ версии модулей и типизация объектов запросов для более удобной
работы.
<h3>Установка через pip</h3>
`pip install findclone_api`
<h3>Requirements</h3>
```
requests
aiohttp
PIL
```
<h3>Примеры использования:</h3>

```python
# sync findclone example
from Findclone import findclone
from io import BytesIO

if __name__ == '__main__':
    phone = "+123456172"
    password = "foobar"
    f = findclone.FindcloneApi()
    f.login(phone, password)
    print(f) # get account information
    # upload photo
    profiles = f.upload("test.jpg")
    # or send image url
    # profiles = f.upload("https://example.com/image.png")
    # work with return object:
    if isinstance(profiles, BytesIO):  # check return object
        print("write file")
        with open("return_image.jpg", "wb") as file:
            file.write(profiles.getvalue())
    else:
        for profile in profiles:
            print(profile)  # return profile.__str__()
            print(profile.url, profile.score)
    histories = f.history()
    for history in histories:
        print(history)
```

```python
# async findclone example
import asyncio
import aiohttp
from Findclone import aiofindclone
from io import BytesIO

async def main(login, password):
    async with aiohttp.ClientSession() as session:
        f = aiofindclone.FindcloneAio(session)
        await f.login(login, password)
        print(await f.info)
        profiles = await f.upload("file.jpg")
        if isinstance(profiles, BytesIO):
            with open("return_image.jpg", "wb") as file:
                file.write(profiles.getvalue())
        else:
            for profile in profiles:
                print(profile)  # return profile.__str__()
                print(profile.url, profile.score)
        

if __name__ == '__main__':
    login = "123123123"
    password = "foobar"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(login, password))
```
<h3>Кейс если обнаружены на фото 2 и более лиц</h3>
test.jpg:
![img1](https://i.ibb.co/ZN2RM5F/Young-happy-couple-using-two-phones-share-social-media-news-at-home-smiling-husband-and-wife-millenn.jpg)
```python
from Findclone import findclone

if __name__ == '__main__':
    phone = "+123456172"
    password = "foobar"
    f = findclone.FindcloneApi()
    f.login(phone, password)
    profiles = f.upload("test.jpg") 
    # write or send object:
    print("write file")
    with open("out_image.jpg", "wb") as file:
        file.write(profiles.getvalue())
    ...
```
out_image.jpg:
![img2](https://i.ibb.co/SnrGGnD/test-123.png)
Из результата с фотографии, выбираем id лица (указан под квадратом):
```python
...
face_box_id = 0
profiles = f.upload("test.jpg", face_box_id=face_box_id)
for profile in profiles:
    print(profile)
``` 
[Больше примеров](https://github.com/vypivshiy/findclone_api/tree/main/examples)