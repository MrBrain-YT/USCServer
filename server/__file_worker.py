# app - copy class Flask

import configparser
import os
import tarfile
import shutil

from flask import request, send_file

def file_worker(app):

    @app.route('/package', methods = ['POST'])
    def send_package():
        info = request.form
        files_path = os.path.dirname(os.path.abspath(__file__))
        # for filename in files_path:
        #     print(filename)
        #     file_path = os.path.join(files_path, filename)
        #     os.remove(file_path)
            
        with tarfile.open(f"{files_path}/archives/{info.get("package_name")}.tar.gz", "w:gz") as tar:
            source_dir = f"{files_path}/packages/{info.get("package_name")}"
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        
        return send_file(f"{files_path}/archives/{info.get("package_name")}.tar.gz", as_attachment=True)
    
    @app.route('/', methods = ['GET'])
    def home():
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/src/home.html") as home:
            return home.read()
    
    @app.route('/add', methods = ['GET'])
    def add_package():
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/src/add.html") as add:
            return add.read()
        
    @app.route('/list', methods = ['GET'])
    def list():
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/src/list.html") as list:
            return list.read()
        
    @app.route('/upload', methods=['POST'])
    def upload_file():
        uploaded_file = request.files['file']
        # save file
        tar_file_path = f"{os.path.dirname(os.path.abspath(__file__))}/archives/{uploaded_file.filename}"
        uploaded_file.save(tar_file_path)
        
        # extrcting tar file for check
        dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/temp"
        file = tarfile.open(tar_file_path) 
        file.extractall(dir_path) 
        file.close()
        
        # Check package
        if os.path.exists(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}/package.ini"):
            config = configparser.ConfigParser()
            config.read(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}/package.ini")
            package_name = config["INFO"].get("name")
            package_version = config["INFO"].get("version")
            print(package_name, package_version)
            if package_name and package_version != None:
                # add package to list
                config_file = f"{os.path.dirname(os.path.abspath(__file__))}/packages/packages.ini"
                packages_config = configparser.ConfigParser()
                packages_config.read(config_file)
                packages_config[package_name] = {
                    "name" : package_name,
                    "version" : package_version
                }
                with open(config_file, 'w') as configfile:
                    packages_config.write(configfile)
                
                # extrcting tar file to packages
                new_dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/packages"
                file = tarfile.open(tar_file_path)
                file.extractall(new_dir_path)
                file.close()
                os.remove(tar_file_path)
                shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
            else:
                os.remove(tar_file_path)
                shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
        else:
            os.remove(tar_file_path)
            shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
        
        return 'File uploaded successfully'