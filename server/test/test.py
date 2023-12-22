import requests
import os
import zipfile

data = {
    "package_name" : "test"
}

file = requests.post(url="http://127.0.0.1:5000/package", data=data).text
print(file, file.encode())

with open(f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}.zip", "w", encoding="utf-8") as new_package:
    new_package.write(file)
    
    
dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}"
os.makedirs(dir_path)
print(f"{dir_path}.zip")
with zipfile.ZipFile(f"{dir_path}.zip", 'r') as zip_ref:
    zip_ref.extractall(dir_path)