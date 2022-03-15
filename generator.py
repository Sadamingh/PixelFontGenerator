from PIL import Image, ImageFont, ImageDraw
import numpy as np
from bs4 import BeautifulSoup
import os
import sys
import datetime
from tqdm import tqdm

FONT_DIR_EN = "en_fonts/"
FONT_DIR_JP = "jp_fonts/"
BG_DIR = "bgs/"
TEXT_DIR = "text_corpus/wiki_corpus_2.01/"

def random_color(random_type):
    if random_type == "w":
        r = np.random.randint(200, 255)
        g = np.random.randint(200, 255)
        b = np.random.randint(200, 255)
        a = np.random.randint(0, 100)
    else:
        r = np.random.randint(0, 50)
        g = np.random.randint(0, 50)
        b = np.random.randint(0, 50)
        a = np.random.randint(0, 100)
    return r, g, b, a


def get_rand_background():
    if np.random.random() < .1:
        random_type = "w" if np.random.random() < 0.5 else "b"
        r, g, b, a = random_color(random_type)
        im = Image.new('RGBA', (1000, 500), (r, g, b, a))
        bg_type = "plain_" + random_type
    else:
        backgrounds = [f for f in os.listdir(BG_DIR) if not f.startswith('.')]
        background = np.random.choice(backgrounds)
        im = Image.open(BG_DIR + background)
        bg_type = background
    return im, bg_type


def get_random_font(directory: str):
    font_list = [f for f in os.listdir(directory) if not f.startswith('.')]
    font = np.random.choice(font_list)
    return font


def get_random_font_color(bg_type):
    if "b" in bg_type:  # means black bg
        rand = lambda: np.random.randint(200, 255)
        font_color = '#%02X%02X%02X' % (rand(), rand(), rand())
    elif "w" in bg_type:
        rand = lambda: np.random.randint(0, 55)
        font_color = '#%02X%02X%02X' % (rand(), rand(), rand())
    else:
        font_color = ["#000" if np.random.random() < 0.5 else "#fff"][0]
    return font_color


def get_random_text(directory: str):
    rand_folder = np.random.choice(list(os.walk(TEXT_DIR))[0][1])
    rand_dir = TEXT_DIR + rand_folder + "/"
    rand_file = np.random.choice([f for f in os.listdir(rand_dir) if not f.startswith('.')])
    with open(rand_dir + rand_file, 'r', encoding='utf-8') as f:
        data = f.read()
    bs_data = BeautifulSoup(data, 'xml')

    if directory == FONT_DIR_EN:
        b_j = list(bs_data.find_all(attrs={"type": "check", "ver": "1"}))
        b_j = [str(i).replace("<e type=\"check\" ver=\"1\">", "")
                   .replace("</e>", "") for i in b_j]
        text_val = np.random.choice(b_j)

        if len(text_val) <= 60:
            result = text_val
        else:
            i = 60

            while text_val[i - 1] != " ":
                i += 1
                if i > len(text_val):
                    break
            result = text_val[:i] + "\n" + text_val[i:120]
        return result

    elif directory == FONT_DIR_JP:
        b_j = list(bs_data.find_all('j'))
        b_j = [str(i).replace("<j>", "")
                   .replace("</j>", "") for i in b_j]
        text_val = np.random.choice(b_j)
        return text_val[:30] + "\n" + text_val[30:60]
    else:
        raise ValueError("Can't recognize dir name.")


def generate_image(directory: str, export_dir: str, max_text, max_iter=500, boundary=False):
    result = []
    bboxes = []
    iter_num = 0

    im, bg_type = get_rand_background()

    draw = ImageDraw.Draw(im)
    N = np.random.randint(1, max_text + 1)

    while len(result) < N:

        if iter_num > max_iter:
            break

        font_name = directory + get_random_font(directory)
        font_size = np.random.randint(10, 25)
        font = ImageFont.truetype(font_name, font_size)

        text_value = get_random_text(directory)
        font_color = get_random_font_color(bg_type)

        x0 = np.random.randint(im.size[0] * .9)
        y0 = np.random.randint(im.size[1] * .9)

        bbox = draw.textbbox((x0, y0), text_value, font=font)
        if bbox[2] < im.size[0] and bbox[3] < im.size[1]:
            if not is_overlap(bbox, bboxes):
                draw.text((x0, y0), text_value, font=font, fill=font_color)
                if boundary:
                    draw.rectangle(bbox, outline="red")
                result.append((bbox, text_value.replace("\n", "")))
                bboxes.append(bbox)

        iter_num += 1

    if im.mode == "RGBA":
        im = im.convert('RGB')
    filename = export_dir + str(datetime.datetime.now()).replace("/", "") \
        .replace("-", "") \
        .replace(" ", "") \
        .replace(":", "") \
        .replace(".", "") + ".jpg"
    im.save(filename)
    generate_result(filename, export_dir, result)


def generate_result(filename, export_dir, result):
    result_file = open(export_dir.replace("images/", "") + 'result.txt', 'a')
    result_file.write(filename.replace(export_dir.split("/")[0], ".") + " [")
    for i, text_info in enumerate(result):
        result_file.write("{\"translation\":\"" + text_info[1] + "\",")
        result_file.write(f"\"points\":{to_rec(text_info[0])}" + "}")
        if i < len(result) - 1:
            result_file.write(",")
    result_file.write("\"}]\n")
    result_file.close()


def to_rec(bbox):
    x0, y0, x1, y1 = (int(x) for x in bbox)
    return [[x0, y0], [x1, y0], [x0, y1], [x1, y1]]


def is_overlap(current_bbox, bboxes):
    for bbox in bboxes:
        if (current_bbox[0] >= bbox[2]) or (current_bbox[2] <= bbox[0]) \
                or (current_bbox[3] <= bbox[1]) or (current_bbox[1] >= bbox[3]):
            continue
        else:
            return True
    return False


def main():
    if not os.path.exists("en_data/images/"):
        os.makedirs("en_data/images/")

    if not os.path.exists("jp_data/images/"):
        os.makedirs("jp_data/images/")

    for i in tqdm(range(int(sys.argv[1]))):
        generate_image(FONT_DIR_EN, "en_data/images/", int(sys.argv[2]))
        generate_image(FONT_DIR_JP, "jp_data/images/", int(sys.argv[2]))


if __name__ == '__main__':
    main()
