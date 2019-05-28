from PIL import Image, ImageFilter
import os
import requests


"""
顔にモザイクをかける処理 with faceAPI
モザイクがかかっていてもメガネしている人を判別しよう
"""


def create_blur_img_using_attr(src_img, face_rectangle, blur_ratio, face_attr):
    """ブラー効果を付与した画像を作成します
    :param src_img: 元画像
    :param face_rectangle: ブラー効果をかけたいエリアのtop, left, width, height のディクショナリ
    :param blur_ratio: blur率(float)
    :param face_attr: 顔属性オブジェクト
    :return:
    """
    top = face_rectangle['top']
    left = face_rectangle['left']
    width = face_rectangle['width']
    height = face_rectangle['height']

    # ブラー効果させたい部分を切り抜く
    src_crop = src_img.crop((left, top, left + width, top + height))

    # TODO メガネをしている場合は色付きblur, 素顔の人はノーマルblur
    if face_attr['glasses'] != 'NoGlasses':
        crop_color = Image.new('RGB', (face_rectangle['width'], face_rectangle['height']), (41, 115, 198))
        crop = Image.blend(src_crop, crop_color, 0.5)
        src_img.paste(crop, (left, top))

    else:
        crop = src_crop

    # 切り抜いた画像をブラー化する
    crop_blur = crop.filter(ImageFilter.GaussianBlur(blur_ratio))
    # 元画像にブラー化した画像を張り付ける
    src_img.paste(crop_blur, (left, top))

    return src_img


def get_face_rectangle_with_attr(img, key):
    """Azure Cognitive Service face APIを呼び出し、顔の位置を取得する。FaceAttributeオブジェクトも取得する
    :param img: 対象の画像
    :param key: face api の subscription key
    :return:
    """
    # TODO メガネ判定を利用する
    url = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=glasses'
    header = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': key
    }

    res = requests.post(url, headers=header, data=open(img, 'rb'))
    res_json = res.json()

    return res_json


def main():
    """ディレクトリ内すべての画像に処理をします
    :return:
    """
    # 作業ベースディレクトリ
    base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    # モザイクをかけたい画像が入っているディレクトリ
    img_dir = os.path.join(base_dir, 'target')
    # モザイク加工済み画像が出力されるディレクトリ
    output_dir = os.path.join(base_dir, 'result')
    # Face API サブスクリプションkey
    face_key = 'xxxxx'
    # blur 効果のratio(float)
    ratio = 15.0

    # モザイクをかけたい画像が入ってるディレクトリ内すべてのファイルに処理をします
    for image in os.listdir(img_dir):
        if image == '__init__.py':
            continue

        # imageの取得
        img_path = os.path.join(img_dir, image)
        im = Image.open(img_path)

        # 顔位置の特定
        rectangles = get_face_rectangle_with_attr(img_path, face_key)
        print(rectangles)

        # blur処理(1枚に複数の顔があったら全部にblur処理かけるよ～）
        blur_img = im
        for rectangle in rectangles:
            blur_img = create_blur_img_using_attr(blur_img, rectangle['faceRectangle'], ratio, rectangle['faceAttributes'])

        # ファイルの書き出し
        blur_img.save(os.path.join(output_dir, image), quality=100)


if __name__ == "__main__":
    main()
