import cv2
from .tuls import get_optimal_font_scale, is_address, is_phone, is_item, remove_punc

def draw_level(image, levels, coords, scale=1):
    color = (255, 0, 0)
    lev_coords = []
    thickness = 2
    imageHeight, imageWidth = image.shape[:-1]
    # fontScale = (imageWidth * imageHeight) / (factor**2)
    fontScale = min(imageWidth,imageHeight)/(500/scale)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i,level in enumerate(levels):
        if len(level) == 1:
            coord = coords[level[0]]
            start_point = tuple(coord[:2])
            end_point = tuple(coord[4:6])
        else :
            start_point = coords[level[0]][:2]
            end_point = coords[level[-1]][4:6]
        lev_coord = list(start_point) + [end_point[0], start_point[1]] + list(end_point) + [start_point[0],end_point[1]]
        lev_coords.append(lev_coord)
        # fontScale = get_optimal_font_scale(str(i+1), imageWidth)
        image = cv2.rectangle(image, tuple(start_point), tuple(end_point), color, thickness=thickness)
        image = cv2.putText(image, str(i+1), tuple(end_point), font,
                            fontScale, (0,0,255), thickness, cv2.LINE_AA)
    return image, lev_coords


def find_item(level, transcripts):
    qty = None
    name = None
    pprice = None
    price = None

    for lev in level:
        try :
            if transcripts[lev][0].isalpha():
                name = transcripts[lev]
            elif transcripts[lev][0].isnumeric():
                if len(transcripts[lev]) > 1:
                    if len(level) <= 3:
                        prices = transcripts[lev].split(" ")
                        if len(prices) > 1:
                            pprice = prices[0]
                            price = prices[1]
                        else :
                            pprice = prices[0]
                            price = prices[0]
                    else :
                        if not pprice:
                            pprice = transcripts[lev]
                        else:
                            price = transcripts[lev]
                else :
                    qty = transcripts[lev]
        except Exception as e:
            print(e)
            print(lev)

    return qty, name, pprice, price

def to_json(levels, transcripts):
    responses = {"address" : None,
                 "number" : None,
                 "info": [],
                 "item" : []}
    item_keys = ['qty', 'name', 'price', 'total']

    for level in levels:
        info = True
        for lev in level:
            if is_address(transcripts[lev]) and responses["address"] is None:
                responses["address"] = " ".join([transcripts[x] for x in level])
                info = False
            elif is_phone(transcripts[lev]) and responses["number"] is None:
                responses["number"] = " ".join([transcripts[x] for x in level])
                info = False
        if len(level) > 1 and info:
            item = find_item(level, transcripts)
            response = {x:y for x,y in zip(item_keys, item)}
            responses['item'].append(response)
        else :
            info = transcripts[level[0]]
            check = is_item(remove_punc(info, puncs=".,", replace=""))
            barang = info.split(" ")[::-1]
            if check == "nama_duluan" and len(barang) > 4:
                item = barang[:3]
                item.append(" ".join(barang[3:]))
                response = {x:y for x,y in zip(["total","price","qty","name"], item)}
                responses['item'].append(response)
            elif check == "qty_duluan" and len(barang) > 4:
                item = barang[:2]
                item.append(" ".join(barang[2:-1]))
                item.append(barang[-1])
                response = {x:y for x,y in zip(["total","price","name", "qty"], item)}
                responses['item'].append(response)
            else:
                inf = " ".join([transcripts[lev] for lev in level])
                responses["info"].append(inf)