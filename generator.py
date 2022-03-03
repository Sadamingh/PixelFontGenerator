from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os


FONT_DIR_EN = "en_fonts/"
FONT_DIR_JP = "jp_fonts/"
BG_DIR = "bgs"


def get_background():
    r = np.random.randint(0, 255)
    g = np.random.randint(0, 255)
    b = np.random.randint(0, 255)
    a = np.random.randint(0, 100)
    im = Image.new('RGBA', (400, 200), (r, g, b, a))
    return im


def get_random_font(directory: str):
    font_list = os.listdir(directory)
    font = np.random.choice(font_list)
    print("[DEBUG] Font name: " + font)
    return font


def get_random_text(directory: str):
    if directory == FONT_DIR_EN:
        return np.random.choice(["hello", "TesT", "0t1Vck3z"])
    elif directory == FONT_DIR_JP:
        return np.random.choice(["トラック", "くるま", "乗り物"])
    else:
        raise ValueError("Can't recognize dir name.")


def generate_image_plain(directory: str):

    im = get_background()
    draw = ImageDraw.Draw(im)
    font_name = directory + get_random_font(directory)
    font = ImageFont.truetype(font_name, 50)
    text_value = get_random_text(directory)
    draw.text((10, 25), text_value, font=font)
    im.show()


def main():
    generate_image_plain(FONT_DIR_EN)
    generate_image_plain(FONT_DIR_JP)


if __name__ == '__main__':
    main()
