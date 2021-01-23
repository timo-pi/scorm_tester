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

"""def zipScorm(filePaths, zip_filename):
    print("zip_filename: " + str(zip_filename))
    # writing files to a zipfile
    zip_file = zipfile.ZipFile(zip_filename, 'w')
    with zip_file:
        # writing each file one by one
        for file in filePaths:
            zip_file.write(file)
    print(zip_filename + ' file is created successfully!')
    zip_file.close()"""

def zipDir(dir_name, out_filename):
    print("def zipDir2: ")
    print(Path(dir_name).parent.parent)
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


"""def createZipPath():
    filename = os.path.basename(zip_file)
    dirname = os.path.dirname(zip_file)
    extract_path = os.path.join(dirname, 'temp', filename)
    extracted_scorm_path = extract_path[:-4]"""



