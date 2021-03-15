Findclone API by vypivshiy<br>
Installation:<br>
`pip install findclone_api`<br>
Requirements:<br>
```
requests
aiohttp
PIL
```
Examples:

```python
# sync findclone example
from Findclone import findclone
from io import BytesIO

if __name__ == '__main__':
    phone = "+123456172"
    password = "foobar"
    f = findclone.FindcloneApi()
    f.login(phone, password)
    session = f.get_session # get session for authorisation
    f2 = findclone.FindcloneApi()
    f2.login(session_key=session["session-key"], userid=session["user-id"])
    print(f2)
    print(f)  # get account information or call f.info
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
case if detect 2 or more faces:<br>
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
finally, retry upload request:
```python
...
face_box_id = 0
profiles = f.upload("test.jpg", face_box_id=face_box_id)
for profile in profiles:
    print(profile)
``` 
