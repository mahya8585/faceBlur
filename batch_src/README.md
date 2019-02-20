# 利用までの道のり
## pythonの準備
- Python3.7をインストールして使えるようにする
  - [https://www.python.org/](https://www.python.org/)
  - ターミナルで `python -V` してみて3.7が返ってきたらOK

## Azureの準備
- Azure Cognitive Service の Face APIを使えるようにする
  - [https://azure.microsoft.com/ja-jp/services/cognitive-services/face/](https://azure.microsoft.com/ja-jp/services/cognitive-services/face/)
  - subscription key を控えておく

## ソースコードの準備
- 本ディレクトリ([/py/pillowLab/blur](https://github.com/mahya8585/toolbox/tree/master/py/pillowLab/blur))を自分のPCに入れておく
  - ターミナルで本ディレクトリに移動
  - [py/pillowLab/blur/target](https://github.com/mahya8585/toolbox/tree/master/py/pillowLab/blur/target) に加工したい画像を投入
- [faceblur.py](https://github.com/mahya8585/toolbox/blob/master/py/pillowLab/blur/faceblur.py)の `def main()` 内 `face_key` にFace APIのsubscription keyを設定する
- `pip install -r requirements.txt` をターミナルで実行
- `python blur.py` をターミナルで実行
- [py/pillowLab/blur/result](https://github.com/mahya8585/toolbox/tree/master/py/pillowLab/blur/result) に加工済みデータが出力されていれば成功～
