import zipfile
import shutil
import os
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

def get_key_by_value(value):
    for key, val in versions.items():
        if val == value:
            return key
    return None

def main():
    currentDir = os.getcwd()
    name = input("Input name of resource pack:\n")

    packPath_zip = os.path.join(currentDir, name + ".zip")
    packPath = os.path.join(currentDir, name)

    with zipfile.ZipFile(packPath_zip, 'r') as zip_ref:
        print("Extracting zip...")
        zip_ref.extractall(packPath)
        
    targetPath = os.path.join(currentDir, name, "pack.mcmeta")
    file = open(targetPath)
    data = json.load(file)

    print("Current version is " + versions.get(data["pack"]["pack_format"]))

    with open(currentDir+"\\"+name+"\\pack.mcmeta", 'w') as file:
        new = input("Input new version:\n")
        print("Updating value")
        data["pack"]["pack_format"] = get_key_by_value(new)

        file.seek(0)
        json.dump(data, file, indent=4)

    file.close

    print("Creating zip...")
    shutil.make_archive(name, 'zip', packPath_zip)

    print("Removing directory...")
    shutil.rmtree(packPath)

    print("Successfully updated!")


main()



