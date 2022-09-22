from importlib.resources import path
from zipfile import ZipFile
import os
import pathlib
import shutil
import subprocess

# from parent location
from ..models import *

MEDIA_PATH = str(pathlib.Path(__file__).parent.parent.parent) + '/media/'

def deleteFile(fileObject):
    folder_path = os.path.dirname(str(fileObject.src))
    seqPath = MEDIA_PATH + folder_path

    # remove folder and its contents
    shutil.rmtree(seqPath)

def compression_factor(x):
    if x.endswith('.zip'):
        file_name = x
        print(file_name)
        file_size = round((os.path.getsize(file_name) / 1048576), 2)
        print(file_size, 'Mb')
        zip_object = ZipFile(file_name, 'r')
        size = sum([zinfo.file_size for zinfo in zip_object.filelist])
        archive_size = round((size / 1048576), 2)
        print(archive_size, 'Mb')
        compression_factor = round((100 * (file_size / archive_size)), 2)
        print('Compression:', compression_factor, '%')


def unzip(x):
    if x.endswith('.zip'):
        file_name = x
        zip_object = ZipFile(file_name, 'r')
        # zip_name = file_name
        file_names = zip_object.namelist()
        end_path = file_name.replace('.zip', '')

        for file_name in file_names:
            if file_name.endswith('.yuv'):
                zip_object.extract(file_name, end_path)

        zip_object.close()
        print(end_path)
        # os.remove(zip_name)
        
def loop():
    # /media/sequences/ path
    absPATH = MEDIA_PATH + 'sequences/'

    for x in os.listdir(absPATH):

        path = absPATH + '/' + x

        if os.path.isdir(path):
            dirName = pathlib.PurePath(path).name

            absInsideFolder = path + "/" + dirName
            if(os.path.isdir(absInsideFolder)):
                print(dirName, "has folder!")
            else:
                for x in os.listdir(path):

                    new_path = path + "/" + x

                    if new_path.endswith('.zip'):
                        compression_factor(new_path)
                        unzip(new_path)

FUNCTIONS_PATH = str(pathlib.Path(__file__).parent)

MAIN_PATH = str(pathlib.Path(__file__).parent.parent.parent)

def batchSynthesis():
    object = SequenceModel.objects.get(id=4)

    # running BATCH file
    batchPATH = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_"))
    print(batchPATH)
    subprocess.call(batchPATH)

def checkPrint():
    print(MAIN_PATH)