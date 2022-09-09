import os
import zipfile
from pathlib import Path
import shutil

# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
    # setup file paths variable
    filePaths = []

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)

    # return all paths
    return filePaths

def zipDir(dir_name, out_filename):
    print("Creating new SCORM package in directory " + str(Path(dir_name).parent.parent) + "...")
    #print(Path(dir_name).parent.parent)
    current_cwd = os.getcwd()
    os.chdir(Path(dir_name).parent.parent)
    shutil.make_archive(out_filename, 'zip', dir_name)
    os.chdir(current_cwd)

def extractScorm(zip_file):
    # btn_select.config(state="disabled")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:

        # create /temp folder
        filename = os.path.basename(zip_file)
        dirname = os.path.dirname(zip_file)
        extract_path = os.path.join(dirname, 'temp', filename).replace('\\', '/')
        extracted_scorm_path = extract_path[:-4]

        zip_ref.extractall(extracted_scorm_path)
        print("extracted_scorm_path: " + extracted_scorm_path + "/imsmanifest.xml")
        return extracted_scorm_path

"""def deleteUnpackedScorm(dirName):
    # NOT WORKING YET
    for root, directories, files in os.walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            filePath = os.path.join(root, filename)
            os.remove(filePath)"""


