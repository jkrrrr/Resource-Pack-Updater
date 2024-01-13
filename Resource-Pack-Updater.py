import zipfile
import shutil
import os
from os import listdir
from os.path import isfile, join
import sys
import json

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Dictionary of versions - update when needed
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

# Current working directory
currentDir = os.getcwd()

def get_key_by_value(value):
    """
    Retrieves the key for a given value

    :param value: The value of the key to retrieve
    :type value: str
    """
    for key, val in versions.items():
        if val == value:
            return key
    return None

def update(pack, version):
    """
    Updates the version of a resource pack

    :param pack: The name of the resource pack to update
    :type pack: str

    :param version: The version to replace it with
    :type  version: str
    """
    print("Processing resource pack " + pack + " to version " + version)
    packPath_zip = os.path.join(currentDir, pack + ".zip")
    packPath = os.path.join(currentDir, pack)

    # Check if pack exists
    if not os.path.exists(packPath_zip):
        print("Resource pack does not exist!")
        sys.exit()

    # Extract pack
    with zipfile.ZipFile(packPath_zip, 'r') as zip_ref:
        zip_ref.extractall(packPath)
        
    # Open file and load JSON
    targetPath = os.path.join(currentDir, pack, "pack.mcmeta")
    file = open(targetPath)
    data = json.load(file)

    print("Current version is " + versions.get(data["pack"]["pack_format"]))

    # Update the version
    with open(os.path.join(packPath, "pack.mcmeta"), 'w') as file:
        data["pack"]["pack_format"] = get_key_by_value(version)

        file.seek(0)
        json.dump(data, file, indent=4)

    file.close()

    # Repack as new zip
    shutil.make_archive(pack, 'zip', packPath)
    shutil.rmtree(packPath)

def main():
    # Get only get only .zips, and remove the .zip
    dirFiles = [file[:-4] for file in listdir(currentDir) if isfile(join(currentDir, file)) and file.endswith('.zip')]
    completers = dirFiles
    completers.extend("all")
    completer = WordCompleter(completers)
    session = PromptSession(completer=completer)

    name = session.prompt("Input name of resource pack:\n")
    version = session.prompt("Input new version:\n")

    # Test for valid version
    if not version in versions.values():
        print("Invalid version.\nCheck the list of formats at https://minecraft.wiki/w/Pack_format")
        sys.exit()

    # To do all packs
    if name == "all":
        # Update each one
        for pack in dirFiles:
            try:
                update(pack, version)
            except:
                print("Unable to process " + pack)
    else: # Single pack
        update(name, version)

    print("Complete!")


main()



