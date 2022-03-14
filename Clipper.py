from PIL import Image, ImageFont, ImageDraw
import PIL
import numpy as np
import os
import datetime

IMPORT_DIR = "raw_bg/"
EXPORT_DIR = "bgs/"
valid_images = [".jpg", ".jpeg", ".gif", ".png", ".tga"]
crop_area = (0, 0, 1000, 120)

inputs = [f for f in os.listdir(IMPORT_DIR) if not f.startswith('.')]
for bg in inputs:
    ext = os.path.splitext(bg)[1]
    if ext.lower() not in valid_images:
        continue
    else:
        try:
            im = Image.open(IMPORT_DIR + bg)
        except PIL.UnidentifiedImageError:
            continue
        draw = ImageDraw.Draw(im, "RGBA")
        if np.random.random() < 0.5:
            draw.rectangle(crop_area, fill=(255, 255, 255, 120))
            if im.size[0] >= 1000 and im.size[1] >= 120:
                cropped_im = im.crop(crop_area)
                cropped_im.save(EXPORT_DIR + "img_" + str(datetime.datetime.now()).replace("/", "")
                                .replace("-", "")
                                .replace(" ", "")
                                .replace(":", "")
                                .replace(".", "") + "_w" + ".jpg")
        else:
            draw.rectangle(crop_area, fill=(0, 0, 0, 120))
            if im.size[0] >= 1000 and im.size[1] >= 120:
                cropped_im = im.crop(crop_area)
                cropped_im.save(EXPORT_DIR + "img_" + str(datetime.datetime.now()).replace("/", "")
                                .replace("-", "")
                                .replace(" ", "")
                                .replace(":", "")
                                .replace(".", "") + "_b" + ".jpg")
