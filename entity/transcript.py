import cv2
from PIL import Image, ImageDraw, ImageFont
from .tuls import remove_punc

def clean_transcripts(transcripts):
    for i,transcript in enumerate(transcripts):
        if not transcript[0].isalnum():
            transcripts[i] = transcript[1:-1]
        else:
            transcripts[i] = transcript[:-1]
    return transcripts

def write_transcript(image, coords, transcripts):
    font = cv2.FONT_HERSHEY_SIMPLEX
    imageHeight, imageWidth = image.shape[:-1]
    fontScale = (imageWidth * imageHeight) / (500**2)
    color = (0, 0, 250)
    thickness = 1
    for coord, transcript in zip(coords, transcripts):
        org = tuple(coord[-2:])
        image = cv2.putText(image, transcript, org, font,
                            fontScale, color, thickness, cv2.LINE_AA)
    return image

def vis_text(levels, transcripts, height,width, fontsize=12):
    result = []
    imgs = []

    for level in levels:
        line = " ".join(transcripts[i] for i in level)
        result.append(line)

    h = height//len(result)
    w = width

    for i,res in enumerate(result):
        img = Image.new('RGB', (w, h), color='#FFFFFF')
        font = ImageFont.truetype('Roboto-Black.ttf', size=fontsize)
        canvas = ImageDraw.Draw(img)
        res = remove_punc(res)
        canvas.text((1,1), str(i+1) + "." + res, font=font, fill='#000000')
        imgs.append(img)
    
    return result, imgs