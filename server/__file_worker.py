# app - copy class Flask

import configparser
import os
import tarfile
import shutil
import time

from flask import request, send_file, jsonify, render_template

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
        return render_template("home.html")
    
    @app.route('/add', methods = ['GET'])
    def add_package():
        return render_template("add.html")
    
    @app.route('/addFromList', methods = ['GET'])
    def addFromList_package():
        return render_template("add_from_list.html")
        
    @app.route('/list', methods = ['GET'])
    def list_site():
        items = []
        config_file = f"{os.path.dirname(os.path.abspath(__file__))}/packages/packages.ini"
        packages_config = configparser.ConfigParser()
        packages_config.read(config_file)
        for package in packages_config.sections():
            package_item = {
                'name': packages_config[package].get("name"),
                'version': packages_config[package].get("version")
            }
            items.append(package_item)

        return render_template("list.html", items=items)
        
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
                old_dirs = [name for name in os.listdir(new_dir_path)]
                file = tarfile.open(tar_file_path)
                file.extractall(new_dir_path)
                file.close()
                new_dirs = [name for name in os.listdir(new_dir_path)]
                foldder_name = set(new_dirs) - set(old_dirs)
                new_folder_name = list(foldder_name)[0]
                os.rename(f"{new_dir_path}/{new_folder_name}", f"{new_dir_path}/{package_name}")
                os.remove(tar_file_path)
                shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
            else:
                os.remove(tar_file_path)
                shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
        else:
            os.remove(tar_file_path)
            shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
        
        return 'File uploaded successfully'
    
    @app.route('/delete', methods=['POST'])
    def delete_item():
        data = request.json
        package_name = data.get('itemName').lower()
        # remove package from list
        config_file = f"{os.path.dirname(os.path.abspath(__file__))}/packages/packages.ini"
        packages_config = configparser.ConfigParser()
        packages_config.read(config_file)
        # remove section
        if packages_config.has_section(package_name):
            packages_config.remove_section(package_name)
        
        package_path = f"{os.path.dirname(os.path.abspath(__file__))}/packages/{package_name}"
        if os.path.exists(package_path):
            shutil.rmtree(package_path)

        with open(config_file, 'w') as config_file:
            packages_config.write(config_file)
        return jsonify({'message': f'Deleted item: {package_name}'}), 200