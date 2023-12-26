""" main server """
import argparse

from flask import Flask

import __files as files
import __file_worker as file_worker




app = Flask(__name__)

file_worker.file_worker(app=app)
files.files(app=app)


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser("server_info")
    parser.add_argument("-i", help="It's server ip argument", type=str)
    parser.add_argument("-p", help="It's server port argument", type=int)
    args = parser.parse_args()
    
    match args._get_kwargs()[0][1]:
        case None:
            host = "localhost"
        case _:
            host = args._get_kwargs()[0][1]
    
    match args._get_kwargs()[1][1]:
        case None:
            port = "5000"
        case _:
            port = args._get_kwargs()[1][1]
            
    app.run(host=host, port=port)