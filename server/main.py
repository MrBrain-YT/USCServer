""" main server """
from flask import Flask

import __files as files
import __file_worker as file_worker

app = Flask(__name__)

file_worker.file_worker(app=app)
files.files(app=app)


if __name__ ==  "__main__":
    app.run()