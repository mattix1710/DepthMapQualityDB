import zipfile
import os

def deleteFile(fileObject):
    folder_path = os.path.dirname(str(fileObject.src))
    index = os.path.abspath(folder_path).find('\sequences')
    folder_path = os.path.abspath(folder_path)[:index] + '\media' + os.path.abspath(folder_path)[index:]

    # removing all files in sequeunce directory
    for file in os.listdir(folder_path):
        os.remove(os.path.join(folder_path, file))

    # removing folder itself
    os.rmdir(folder_path)