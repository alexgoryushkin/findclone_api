from random import sample
from string import ascii_letters, digits

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO, BufferedReader

# config PIL colours and font
COLOUR_RECTANGLE: tuple = (0, 255, 0, 127)
COLOUR_FONT: tuple = (255, 0, 0, 0)
FONT_FILE: str = "arial.ttf"
FONT_SIZE: int = 24


def paint_boxes(file: BufferedReader, face_boxes: dict, colour_r: tuple = COLOUR_RECTANGLE,
                colour_f: tuple = COLOUR_FONT, font_file: str = FONT_FILE, font_size: int = FONT_SIZE) -> BytesIO:
    """Drawing squares and face number in the image if more than 2 faces are found
    :return: imgByteArr image byte array
    :type: BytesIO
    """
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


def random_string(word: int = 8): return "".join(sample(ascii_letters + digits, word))


