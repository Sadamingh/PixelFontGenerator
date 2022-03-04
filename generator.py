from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
import datetime


FONT_DIR_EN = "en_fonts/"
FONT_DIR_JP = "jp_fonts/"
BG_DIR = "bgs/"

def random_color():
    r = np.random.randint(0, 255)
    g = np.random.randint(0, 255)
    b = np.random.randint(0, 255)
    a = np.random.randint(0, 100)
    return r, g, b, a


def get_rand_background():
    if np.random.random() < .1:
        r, g, b, a = random_color()
        im = Image.new('RGBA', (800, 200), (r, g, b, a))
        print("[DEBUG] Background name: plain")
        bg_type = "plain"
    else:
        backgrounds = [f for f in os.listdir(BG_DIR) if not f.startswith('.')]
        background = np.random.choice(backgrounds)
        im = Image.open(BG_DIR + background)
        print("[DEBUG] Background name: " + background + str(im.size))
        bg_type = background
    return im, bg_type


def get_random_font(directory: str):
    font_list = [f for f in os.listdir(directory) if not f.startswith('.')]
    font = np.random.choice(font_list)
    print("[DEBUG] Font name: " + font)
    return font


def get_random_font_color(bg_type):
    if "b" in bg_type:     # means black bg
        font_color = "#fff"
    elif "w" in bg_type:
        font_color = "#000"
    else:
        font_color = ["#000" if np.random.random() < 0.5 else "#fff"][0]
    return font_color


def get_random_text(directory: str):
    if directory == FONT_DIR_EN:
        return np.random.choice(["hello", "TesT", "0t1Vck3z"])
    elif directory == FONT_DIR_JP:
        return np.random.choice(["トラック", "くるま", "乗り物"])
    else:
        raise ValueError("Can't recognize dir name.")


def generate_image(directory: str):

    im, bg_type = get_rand_background()

    draw = ImageDraw.Draw(im)

    font_name = directory + get_random_font(directory)
    font_size = int(im.size[0] * 0.03)
    font = ImageFont.truetype(font_name, font_size)

    text_value = get_random_text(directory)
    font_color = get_random_font_color(bg_type)
    draw.text((im.size[1]*.1, im.size[0]*.01), text_value, font=font, fill=font_color)

    # im.show()

    if im.mode == "RGBA":
        im = im.convert('RGB')
    im.save("data/" + str(datetime.datetime.now()) + ".jpg")


def main():
    for i in range(5):
        generate_image(FONT_DIR_EN)
        generate_image(FONT_DIR_JP)


if __name__ == '__main__':
    main()
