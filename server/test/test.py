import requests
import os
import zipfile

data = {
    "package_name" : "test"
}

responce = requests.post(url="http://127.0.0.1:5000/package", data=data)
print(responce)

# with open(f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}.zip", "w") as new_package:
    # new_package.write(file)
    
with open(f'{data.get("package_name")}.zip', 'wb') as file:
    file.write(responce.content)
    
    
dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}"
os.makedirs(dir_path)
with zipfile.ZipFile(f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}.zip", 'r') as zip_ref:
    zip_ref.extractall(dir_path)
    
os.remove(f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}.zip")