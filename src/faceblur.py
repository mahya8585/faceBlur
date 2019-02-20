from PIL import Image, ImageFilter
import os
import requests


def create_blur_img(src_img, face_rectangle, blur_ratio):
    top = face_rectangle['top']
    left = face_rectangle['left']

    # crop image(target face)
    src_crop = src_img.crop((left, top, left + face_rectangle['width'], top + face_rectangle['height']))

    # blur for crop image
    crop_blur = src_crop.filter(ImageFilter.GaussianBlur(blur_ratio))
    # overwrite
    src_img.paste(crop_blur, (left, top))

    return src_img


def get_face_rectangle(img, key):
    url = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/detect'
    header = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': key
    }

    res = requests.post(url, headers=header, data=open(img, 'rb'))
    res_json = res.json()
    print(res_json)

    return res_json


def main():
    base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'img')
    # target image directory path
    img_dir = os.path.join(base_dir, 'target')
    # response image directory path
    output_dir = os.path.join(base_dir, 'result')
    # Face API key
    face_key = 'xxxxxx'
    # blur ratio(float)
    ratio = 15.0

    # loop: all images
    for image in os.listdir(img_dir):
        if image == '__init__.py' or image == '.DS_Store':
            continue

        # get image
        img_path = os.path.join(img_dir, image)
        im = Image.open(img_path)

        # send face api (get face rectangle etc.)
        rectangles = get_face_rectangle(img_path, face_key)

        # blur
        blur_img = im
        for rectangle in rectangles:
            blur_img = create_blur_img(blur_img, rectangle['faceRectangle'], 15.0)

        # write image
        blur_img.save(os.path.join(output_dir, image), quality=100)


if __name__ == "__main__":
    main()
