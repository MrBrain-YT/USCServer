import requests
import os
import tarfile

data = {
    "package_name" : "test"
}

responce = requests.post(url="http://127.0.0.1:5000/package", data=data)
print(responce)

# with open(f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}.zip", "w") as new_package:
    # new_package.write(file)
    
with open(f'{data.get("package_name")}.tar.gz', 'wb') as file:
    file.write(responce.content)
    
    
dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}"
os.makedirs(dir_path)
    
file = tarfile.open(f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}.tar.gz") 
# extracting file 
file.extractall(dir_path) 
file.close()
    
os.remove(f"{os.path.dirname(os.path.abspath(__file__))}/{data.get("package_name")}.tar.gz")