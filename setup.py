from setuptools import setup
from Findclone import __version__ as version

setup(
    name='findclone_api',
    license="MIT",
    description='Findclone API for humans',
    author='Vypivshiy',
    url='https://github.com/vypivshiy',
    version=version,
    packages=['Findclone', "examples"],
    install_requires=["requests",
                      "aiohttp",
                      "Pillow"],
    python_requires=">=3.6",
    author_email="bomb3r98@gmail.com"
)
