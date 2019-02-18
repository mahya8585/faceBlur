import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options, parse_command_line

from src import faceblur

define('port', default=8888, help='run on the given port', type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # 表示対象画像取得
        img_names = []
        img_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'img', 'target')
        for image_name in os.listdir(img_dir):
            if image_name == '__init__.py' or image_name == '.DS_Store':
                continue

            img_names.append(image_name)

        img_names.sort()
        self.render('index.html',
                    image_names=img_names
                    )


class FaceBlurHandler(tornado.web.RequestHandler):
    def post(self):
        faceblur.main()

        # 表示対象画像取得
        result_names = []
        result_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'img', 'result')
        for image_name in os.listdir(result_dir):
            if image_name == '__init__.py' or image_name == '.DS_Store':
                continue

            result_names.append(image_name)

        result_names.sort()
        self.render('result.html',
                    result_names=result_names
                    )


def main():
    parse_command_line()

    # URLマッピング
    application = tornado.web.Application(
        [
            ('/', MainHandler),
            ('/creator', FaceBlurHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'template'),
        static_path=os.path.join(os.path.dirname(__file__), 'static')
    )

    application.listen(options.port)
    print("接続OK")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
