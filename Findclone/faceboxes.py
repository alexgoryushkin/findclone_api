from .utils import paint_boxes

if __name__ == '__main__':
    boxes = {
        "Rotation": 0,
        "faceBoxes": [{
            "h": 133.1,
            "i": 0,
            "l": 335.34999999999997,
            "t": 210.64999999999998,
            "w": 133.1
        }, {
            "h": 127.4,
            "i": 1,
            "l": 497.90000000000003,
            "t": 204.7,
            "w": 127.4
        }],
        "height": 674,
        "width": 1012
    }
    img = paint_boxes("test.jpg", boxes)
    with open("test_rt.jpg", "wb") as f:
        f.write(img)
