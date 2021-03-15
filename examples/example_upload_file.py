from Findclone import findclone

if __name__ == '__main__':
    login = "123123123"
    password = "foobar"
    file_url = "https://example.com/rick_astley_never_give_u_up.jpg"
    f = findclone.FindcloneApi()
    f.login(login, password)
    result = f.upload(file_url)
    # check if is really Profiles object else write file with painted rectangles
    if isinstance(result, list):
        for profile in result:
            print(profile.raw_data)
    else:
        with open("foobar.jpg", "wb") as file:
            file.write(result.getvalue())
