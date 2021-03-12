import random, string
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


COLOUR_RECTANGLE = (0, 255, 0, 127)
COLOUR_FONT = (255, 0, 0, 0)
FONT_FILE = "arial.ttf"
FONT_SIZE = 24


def paint_boxes(file, face_boxes: dict, colour_r=COLOUR_RECTANGLE,
                colour_f=COLOUR_FONT, font_file=FONT_FILE, font_size=FONT_SIZE):
    """Отрисовка квадратов и номер лица на изображении если найдено более 2 лиц"""
    img = Image.open(file)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font=font_file, size=font_size)
    for face_box in face_boxes["faceBoxes"]:
        face_number = str(face_box["i"])
        height = face_box["h"]
        l = face_box["l"]
        t = face_box["t"]
        draw.rectangle(((l, t), (l + height, t + height)), outline=colour_r, width=3)
        draw.text(((l*2+height)/2, t+height+5), str(face_number), fill=colour_f, font=font)
    imgByteArr = BytesIO()
    img.save(imgByteArr, format="png")
    return imgByteArr


def random_string(word=8): return "".join(random.sample(string.ascii_letters + string.digits, word))


def multipart_string(): return "WebKitFormBoundary" + random_string(16)


def multipart_headers(string=multipart_string()):
    return {"Content-Type": f"multipart/form-data; boundary=----{string}"}
