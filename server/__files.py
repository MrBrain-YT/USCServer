import os

from flask import send_file

def files(app):
    @app.route('/img/USCServer.png', methods = ['GET'])
    def USCServerImg():
        return send_file(f"{os.path.dirname(os.path.abspath(__file__))}/src/img/USCServer.png")
    
    @app.route('/img/mail.png', methods = ['GET'])
    def MailImg():
        return send_file(f"{os.path.dirname(os.path.abspath(__file__))}/src/img/mail.png")