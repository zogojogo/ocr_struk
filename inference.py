"""
This is prolly for the main pipeline
"""
from PaddleOCR.tools.infer.predict_det import TextDetector, check_and_read_gif, get_logger, utility
from PaddleOCR.tools.infer.predict_rec import TextRecognizer, traceback
from entity.tuls import sort_lines
from config import parse_args
import numpy as np
import os, cv2, time, json


logger = get_logger()
def detection(args, text_detector):
    img_file = args.image_path
    draw_img_save = args.image_save

    if args.warmup:
        img = np.random.uniform(0, 255, [640, 640, 3]).astype(np.uint8)
        for i in range(2):
            res = text_detector(img)
    
    if not os.path.exists(draw_img_save):
        os.makedirs(draw_img_save)
    
    # save_results=[]

    img, flag = check_and_read_gif(img_file)
    if not flag:
        img = cv2.imread(img_file)
    if img is None:
        logger.info("error in loading image:{}".format(img_file))

    st = time.time()
    dt_boxes, _ = text_detector(img)
    elapse = time.time() - st

    # logger.info(save_pred)
    logger.info("The predict time of {}: {}".format(img_file, elapse))
    src_img = utility.draw_text_det_res(dt_boxes, img_file)

    img_name_pure = os.path.split(img_file)[-1]
    img_path = os.path.join(draw_img_save,
                            "det_res.jpg")
    
    cv2.imwrite(img_path, src_img)
    logger.info("The visualized image saved in {}".format(img_path))

    # save_pred = os.path.basename(img_file) + "\t" + str(
    #         json.dumps(np.array(dt_boxes).astype(np.int32).tolist())) + "\n"
    save_pred = []
    for box in dt_boxes:
        line = ",".join([str(int(i)) for x in box for i in x])
        save_pred.append(line)

    with open(os.path.join(draw_img_save, "det_results.txt"), 'w') as f:
        f.write('\n'.join(save_pred))
        f.close()

def crop_img(img, box):
    # Crop image
    ## Find bbox rect
    # print(box)
    rect = cv2.boundingRect(box)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()

    # ## mask
    # box = box - box.min(axis=0)
    # mask = np.zeros(croped.shape[:2], np.uint8)
    # cv2.drawContours(mask, [box], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # ## bit-op
    # dst = cv2.bitwise_and(croped, croped, mask=mask)

    # ## add the white background
    # bg = np.ones_like(croped, np.uint8)*255
    # cv2.bitwise_not(bg,bg, mask=mask)
    # dst2 = bg+ dst

    return croped

def recognition(args, text_recognizer):
    img_file = args.image_path
    draw_img_save = args.image_save
    label_path = os.path.join(draw_img_save, "det_results.txt")
    txt = sort_lines(label_path)
    # print(txt)
    img_list = []

    # if args.warmup:
    #     img = np.random.uniform(0, 255, [32, 320, 3]).astype(np.uint8)
    #     for i in range(2):
    #         res = text_recognizer([img] * int(args.rec_batch_num))
    
    img, flag = check_and_read_gif(img_file)
    if not flag:
        img = cv2.imread(img_file)
    if img is None:
        logger.info("error in loading image:{}".format(img_file))

    for line in txt:
        box = np.array(line.split(","), dtype=int).reshape(-1, 2)
        croped = crop_img(img, box)
        img_list.append(croped)
    
    try:
        rec_res, _ = text_recognizer(img_list)
    except Exception as E:
        logger.info(traceback.format_exc())
        logger.info(E)
        exit()

    with open(os.path.join(draw_img_save, "rec_result.txt"), "w") as f:
        f.write('\n'.join(list(["{}".format(res[0]) for res in rec_res])))
        f.close()


if __name__ == "__main__":
    args = parse_args()
    detector = TextDetector(args)
    recognizer = TextRecognizer(args)
    # print(recognizer.postprocess_op.character)
    detection(args, detector)
    recognition(args, recognizer)
