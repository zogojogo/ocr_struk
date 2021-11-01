import numpy as np
import cv2, re
from re import search
# from .item import find_item, is_address, is_phone, is_item

def sort_lines(txt_file):
    newlist = []
    f = open(txt_file)
    for line in f.readlines():
        newlist.append([int(line.split(',')[1]),line])
    sortedlines = sorted(newlist, key=(lambda x: x[0]))
    new_txt = []
    for line in sortedlines:
        new_txt.append(line[1])
    return new_txt

def flatten(lst):
    """
    Only works if it's a 2D list
    """
    if len(lst) == 0:
        return []
    return [i for x in lst for i in x]

def sort_lines(txt_file):
    newlist = []
    f = open(txt_file)
    for line in f.readlines():
        newlist.append([int(line.split(',')[1]),line])
    sortedlines = sorted(newlist, key=(lambda x: x[0]))
    new_txt = []
    for line in sortedlines:
        new_txt.append(line[1])
    return new_txt

def sort_x(paired):
    for i, pairs in enumerate(paired):
        paired[i] = sorted(pairs, key=(lambda x: x[0]))
    return paired

def concat_imgs(imgs:list, vertical=False, interpolation = cv2.INTER_CUBIC):
    if vertical:
        imgs = [np.array(pil_image)[:, :, ::-1].copy() for pil_image in imgs]
        return cv2.vconcat(imgs)
    else :
        return cv2.hconcat(imgs)

def is_address(s):
    keywords = ["jl"]
    return any(search(key, s.lower()) for key in keywords)

def is_phone(s):
    pattern = '\+?([ -]?\d+)+|\(\d+\)([ -]\d+)'
    phone = False
    if re.search(pattern, s):
        phone = True
    return phone

def is_item(s):
    qty_duluan = "^[0-9]([a-zA-Z0-9 ]* )[ 0-9]*"
    nama_duluan = "(.+?) [0-9] [0-9]*"
    check_1 = True if re.search(nama_duluan, s) else False
    check_2 = True if re.search(qty_duluan, s) else False
    if check_1:
        return "nama_duluan"
    elif check_2:
        return "qty_duluan"
    return "bukan_item"

def is_prices(s):
    pattern = "^([a-zA-Z:]*) (\d*)"
    prices = False
    if re.search(pattern, s):
        prices = True
    return prices

def remove_punc(s, puncs=":", replace=" "):
    pattern = "[{}]+\ *".format(puncs)
    clean = re.sub(pattern.encode('unicode-escape').decode().replace('\\\\', '\\'), replace, s)
    # clean = re.sub(r"[.,]+\ *", "", clean)
    return clean

def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
      textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=scale/10, thickness=2)
      new_width = textSize[0][0]
      #print(new_width)
      if (new_width <= width):
          return scale/10
    
    return 1