from setuptools import setup

setup(
    name='findclone_api',
    license="MIT",
    description='Findclone API for humans',
    author='Vypivshiy',
    url='https://github.com/vypivshiy',
    version='0.31',
    packages=['Findclone', "examples"],
    install_requires=["requests", "requests_toolbelt", "PIL", "aiohttp"],
    author_email="bomb3r98@gmail.com"
)
