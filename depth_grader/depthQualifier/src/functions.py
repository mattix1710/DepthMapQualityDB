import os
import pathlib
import shutil
import subprocess
from importlib.resources import path
from zipfile import ZipFile

# from parent location
from ..models import *

MEDIA_PATH = str(pathlib.Path(__file__).parent.parent.parent) + '/media/'

# MATEUSZ
def deleteFile(fileObject):
    folder_path = os.path.dirname(str(fileObject.src))
    seqPath = MEDIA_PATH + folder_path

    # remove folder and its contents
    shutil.rmtree(seqPath)

# WOJCIECH
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

# WOJCIECH & MATEUSZ
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
        
# WOJCIECH & MATEUSZ (korekty co do wyznaczania ścieżki dostępu)
def zipUnpack(location):
    # /media/sequences/ path
    absPATH = MEDIA_PATH + str(pathlib.Path(location).parent)

    for x in os.listdir(absPATH):
        path = absPATH + '/' + x
        
        if path.endswith('.zip'):
            compression_factor(path)
            unzip(path)

    # TODO: probably to remove...
    # for x in os.listdir(absPATH):

    #     path = absPATH + '/' + x

    #     if os.path.isdir(path):
    #         dirName = pathlib.PurePath(path).name

    #         absInsideFolder = path + "/" + dirName
    #         if(os.path.isdir(absInsideFolder)):
    #             print(dirName, "has folder!")
    #         else:
    #             for x in os.listdir(path):

    #                 new_path = path + "/" + x

    #                 if new_path.endswith('.zip'):
    #                     compression_factor(new_path)
    #                     unzip(new_path)

# WOJCIECH (podstawa - wyznaczanie PSNRu) / MATEUSZ (dostosowanie do aktualnego kodu/podłączenie do modelu)
def read_psnr():                # TODO: pass object model ID as an argument
    out = []

    for file_name in os.listdir():

        if file_name == 'ivpsnr_SL.txt':

            f = open(file_name)

            for line in f:

                if line.startswith('IVPSNR'):

                    psnr = str(line.strip())

                    psnr = psnr.replace('IVPSNR', '').replace('dB', '').replace(' ', '')

                    psnr = float(psnr)

                    psnr = round(psnr, 2)

                    out.append(psnr)

        max_value = max(out)
        min_value = min(out)
        avg_value = 0 if len(out) == 0 else sum(out) / len(out)
        avg_value = round(avg_value, 2)

        max_PSNR = "Maximum PSNR: " + str(max_value) + '\n'
        min_PSNR = "Maximum PSNR: " + str(min_value) + '\n'
        avg_PSNR = "Average PSNR: " + str(avg_value) + '\n'
        
        # TODO: saving PSNR values to the model...

        # x = open('psnr.txt', "w+")
        # x.write(max)
        # x.write(min)
        # x.write(avg)


FUNCTIONS_PATH = str(pathlib.Path(__file__).parent)

MAIN_PATH = str(pathlib.Path(__file__).parent.parent.parent)

# MATEUSZ
def batchSynthesis(object):
    # running BATCH file
    batchPATH = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_"))
    print(batchPATH)
    subprocess.call(batchPATH)