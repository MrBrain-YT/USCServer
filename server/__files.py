import os

from flask import send_file

def files(app):
    @app.route('/templates/img/<img>', methods = ['GET'])
    def USCServerImg(img):
        return send_file(f"{os.path.dirname(os.path.abspath(__file__))}/templates/img/{img}")
