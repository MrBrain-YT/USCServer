from flask import Flask, render_template

def main(app:Flask):
    
    @app.route('/test/', methods = ['GET'], endpoint='test_home_page')
    def home_page():
        return render_template("test/test.html")
    
