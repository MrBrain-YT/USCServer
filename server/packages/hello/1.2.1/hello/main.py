from flask import Flask


def main(app:Flask):

    @app.route('/hello/', methods = ['GET'], endpoint='hello_home_page')
    def home_page():
        return "Home page for hello package"