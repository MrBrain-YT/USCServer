from flask import Flask


def main(app:Flask):

    @app.route('/help/', methods = ['GET'], endpoint='help_home_page')
    def home_page():
        return "Home page for help package"