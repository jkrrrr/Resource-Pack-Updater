import zipfile
import shutil
import os
from os import listdir
from os.path import isfile, join
import sys
import json


versions = {
    1 : "1.6.1",
    2 : "1.9",
    3 : "1.11",
    4 : "1.13",
    5 : "1.15",
    6 : "1.16.2",
    7 : "1.17",
    8 : "1.18",
    9 : "1.19",
    11 : "22w42a",
    12 : "1.19.3",
    13 : "1.19.4",
    14 : "23w14a",
    15 : "23w17a",
    16 : "23w31a",
    17 : "23w32a",
    18 : "1.20.2"
}

currentDir = os.getcwd()

def get_key_by_value(value):
    for key, val in versions.items():
        if val == value:
            return key
    return None

def update(pack, version):
    print("Processing resource pack " + pack + " to version " + version)
    packPath_zip = os.path.join(currentDir, pack + ".zip")
    packPath = os.path.join(currentDir, pack)

    if not os.path.exists(packPath_zip):
        print("Resource pack does not exist!")
        sys.exit()

    with zipfile.ZipFile(packPath_zip, 'r') as zip_ref:
        zip_ref.extractall(packPath)
        
    targetPath = os.path.join(currentDir, pack, "pack.mcmeta")
    file = open(targetPath)
    data = json.load(file)

    print("Current version is " + versions.get(data["pack"]["pack_format"]))

    with open(os.path.join(packPath, "pack.mcmeta"), 'w') as file:
        data["pack"]["pack_format"] = get_key_by_value(version)

        file.seek(0)
        json.dump(data, file, indent=4)

    file.close()

    shutil.make_archive(pack, 'zip', packPath)
    shutil.rmtree(packPath)

def main():
    name = input("Input name of resource pack:\n")
    version = input("Input new version:\n")

    if name == "all":
        dirFiles = [file[:-4] for file in listdir(currentDir) if isfile(join(currentDir, file)) and file.endswith('.zip')]
        for pack in dirFiles:
            update(pack, version)
    else:
        update(name, version)

    print("Complete!")


main()



