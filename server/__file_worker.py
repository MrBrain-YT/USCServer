# app - copy class Flask

import configparser
import os
import tarfile
import re
import shutil
import stat
from subprocess import call

import git
import requests
from flask import request, send_file, jsonify, render_template

from __list_work import ListWorker

ListWorker = ListWorker()

def file_worker(app):

    @app.route('/package', methods = ['POST'])
    def send_package():
        info = request.form
        package_name = info.get("package_name")
        files_path = os.path.dirname(os.path.abspath(__file__))
        if ListWorker.check_exits(name=package_name):
            with tarfile.open(f"{files_path}/archives/{package_name}.tar.gz", "w:gz") as tar:
                source_dir = f"{files_path}/packages/{package_name}"
                tar.add(source_dir, arcname=os.path.basename(source_dir))
            
            return send_file(f"{files_path}/archives/{package_name}.tar.gz", as_attachment=True)
        else:
            return "error", 500
    
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
            package_config = configparser.ConfigParser()
            package_config.read(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}/package.ini")
            package_name = package_config["INFO"].get("name")
            package_version = package_config["INFO"].get("version")
            if package_name and package_version != None:
                pattern = r"[!@#$%^&*(),?\":{}|<>]"
                if re.search(pattern, package_name) or re.search(pattern, package_version):
                    os.remove(tar_file_path)
                    shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
                else:
                    # add package to list
                    if not ListWorker.check_exits(package_name):
                        ListWorker.add_package_to_list(package_config=package_config)
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
                    else:
                        os.remove(tar_file_path)
                        shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
                        pass
            else:
                os.remove(tar_file_path)
                shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
                pass
        else:
            os.remove(tar_file_path)
            shutil.rmtree(f"{dir_path}/{uploaded_file.filename.replace(".tar.gz", "")}")
            pass


        return 'File uploaded successfully'
    
    @app.route('/delete', methods=['POST'])
    def delete_item():
        data = request.json
        dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/packages"
        package_name = data.get('itemName').lower()
        if ListWorker.check_exits(package_name):
            # remove package from list
            shutil.rmtree(f"{dir_path}/{package_name}")
            ListWorker.remove_package_from_list(package_name)
        else:
            pass
        return jsonify({'message': f'Deleted item: {package_name}'}), 200
    
    
    
    def on_rm_error(func, path, exc_info):
        #from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)


    @app.route('/from_repo', methods=['POST'])
    def from_repo():
        # set global variables
        error = False
        package_name = ""
        
        # get url
        data = request.get_json()
        url = data.get('url')
        dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/temp/git"
        

        # Проверяем, что URL является ссылкой на GitHub
        github_url_pattern = r'^https?://github\.com/.+/.+\.git$'
        if not re.match(github_url_pattern, url):
            return jsonify({'error': 'Invalid GitHub repository URL'}), 400

        code = requests.get(url).status_code
        if code == 200:
            # Клонируем репозиторий по указанному URL
            git.Repo.clone_from(url, dir_path)
            
            # Check package
            package_dir_path = f"{dir_path}/{[folder for folder in os.listdir(dir_path) if os.path.isdir(f"{dir_path}/{folder}")][1]}"
            if os.path.exists(f"{package_dir_path}/package.ini"):
                config = configparser.ConfigParser()
                config.read(f"{package_dir_path}/package.ini")
                package_name = config["INFO"].get("name")
                package_version = config["INFO"].get("version")
                if package_name and package_version != None:
                    pattern = r"[!@#$%^&*(),?\":{}|<>]"
                    if re.search(pattern, package_name) or re.search(pattern, package_version):
                        error = True
                    else:
                        # add package to list
                        config_file = f"{os.path.dirname(os.path.abspath(__file__))}/packages/packages.ini"
                        packages_config = configparser.ConfigParser()
                        packages_config.read(config_file)
                        if not ListWorker.check_exits(package_name):
                            packages_config[package_name] = {
                                "name" : package_name,
                                "version" : package_version
                            }
                            with open(config_file, 'w') as configfile:
                                packages_config.write(configfile)
                            
                            # move dir to packages
                            shutil.move(package_dir_path, f"{os.path.dirname(os.path.abspath(__file__))}/packages")
                        else:
                            error = True            
                else:
                    error = True
            else:
                error = True
        else:
            error = True

        # delete .git folder
        for i in os.listdir(dir_path):
            if i.endswith('git'):
                tmp = os.path.join(dir_path, i)
                # We want to unhide the .git folder before unlinking it.
                while True:
                    call(['attrib', '-H', tmp])
                    break
                shutil.rmtree(tmp, onerror=on_rm_error)
        # delete git folder
        shutil.rmtree(dir_path)
        if not error:
            return jsonify({'message': f'Added item: {package_name}'}), 200
        else:
            return jsonify({'message': "error"}), 500
            
        