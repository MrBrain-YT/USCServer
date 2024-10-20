import os
import configparser

class ListWorker():

    def __init__(self) -> None:
        pass
        
        
    def check_exits(self, name:str) -> bool:
        dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/packages"
        config = configparser.ConfigParser()
        config.read(f"{dir_path}/packages.ini")
        if name.lower() in config.sections():
            return True
        else:
            return False

    def add_package_to_list(self, package_config:configparser.ConfigParser) -> None:
        dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/packages"
        package_name = package_config["INFO"].get("name")
        
        # Add package to package list
        config = configparser.ConfigParser()
        config.read(f"{dir_path}/packages.ini")
        if package_name not in config.sections():
            config[package_name.lower()] = {
                "name" : package_name,
            }
            with open(f"{dir_path}/packages.ini", 'w') as configfile:
                config.write(configfile)

    def remove_package_from_list(self, name:str) -> None:
        dir_path = f"{os.path.dirname(os.path.abspath(__file__))}/packages"
        config = configparser.ConfigParser()
        config.read(f"{dir_path}/packages.ini")
        if config.has_section(name):
            config.remove_section(name)
        
        with open(f"{dir_path}/packages.ini", 'w') as configfile:
            config.write(configfile)