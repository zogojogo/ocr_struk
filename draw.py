import cv2, json, argparse
from entity.pairing import entity_pairing, get_paired, split_pairs, flatten
from entity.item import draw_level, to_json
from entity.transcript import clean_transcripts, vis_text
from entity.tuls import sort_lines, sort_x, concat_imgs

def pair(coord_path, transcript_path):
    # read data
    coords_data = sort_lines(coord_path)
    transcripts = clean_transcripts(open(transcript_path).readlines())

    # Pairing
    coords_data = [list(map(int, line[:].split(",")) )for line in coords_data]
    levels = entity_pairing(coords_data)
    paired = sort_x(get_paired(levels, coords_data, transcripts))

    # get cleaned data
    coords_data, transcripts = split_pairs(paired)
    coords_data = flatten(coords_data)
    transcripts = flatten(transcripts)

    return levels, coords_data, transcripts

def level_to_img(img, levels, coords_data):
    img_c, lev_coords = draw_level(img.copy(), levels, coords_data)
    return img_c, lev_coords

def text_to_img(img, levels, coords_data, transcripts):
    h, w = img.shape[:-1]
    img_c, _ = level_to_img(img, levels, coords_data)

    _, imgs = vis_text(levels, transcripts, h, w)
    img_text = concat_imgs(imgs, vertical=True)

    img_text = cv2.resize(img_text, (w,h))
    full_img = concat_imgs([img, img_c, img_text])
    return full_img

def main(args):
    coord_path = args.coord_path
    transcript_path = args.transcript_path
    img_path = args.img_path
    second = 1000

    img = cv2.imread(img_path)
    levels, coords_data, transcripts = pair(coord_path, transcript_path)
    # img_c, lev_coords = level_to_img(img, levels, coords_data)
    full_img = text_to_img(img, levels, coords_data, transcripts)

    cv2.imwrite("./inference_results/full_img.jpg", full_img)
    # cv2.waitKey(10*second)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--img_path", type=str)
    parser.add_argument("--coord_path", type=str, default="./inference_results/det_results.txt")
    parser.add_argument("--transcript_path", type=str, default="./inference_results/rec_result.txt")

    args = parser.parse_args()

    main(args)