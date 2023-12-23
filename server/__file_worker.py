# app - copy class Flask

import shutil
import os

from flask import request, send_file

def file_worker(app):
    
    def reset(tarinfo):
        # Reset info for tar.gz archive
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = "root"
        return tarinfo

    @app.route('/package', methods = ['POST'])
    def send_package():
        info = request.form
        files_path = os.path.dirname(os.path.abspath(__file__))
        # for filename in files_path:
        #     print(filename)
        #     file_path = os.path.join(files_path, filename)
        #     os.remove(file_path)
            
        shutil.make_archive(f"{files_path}/archives/{info.get("package_name")}", 'zip',
                            root_dir=f"{files_path}/packages/{info.get("package_name")}")
        
        return send_file(f"{files_path}/archives/{info.get("package_name")}.zip", as_attachment=True)
        
        