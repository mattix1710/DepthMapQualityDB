import os
import pathlib
import shutil
import subprocess
from importlib.resources import path
from zipfile import ZipFile
import re

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
        print(file_size, 'MB')
        zip_object = ZipFile(file_name, 'r')
        size = sum([zinfo.file_size for zinfo in zip_object.filelist])
        archive_size = round((size / 1048576), 2)
        print(archive_size, 'MB')
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

FUNCTIONS_PATH = str(pathlib.Path(__file__).parent)

MAIN_PATH = str(pathlib.Path(__file__).parent.parent.parent)

# MATEUSZ
def batchSynthesis(object):
    # running BATCH file
    batchPATH = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_"))
    print(batchPATH)
    # won't work for 1 sequence
    # subprocess.call(batchPATH)    
    
# WOJCIECH (listowanie po folderze; wyznaczanie wartości: min, max, avg)
# MATEUSZ (dostosowanie do ścieżek absolutnych; wyszukiwanie określonego pliku; pobieranie wartości za pomocą REGEX; zapis do tabeli)
def processPSNR(object, location):
    # /media/sequences/ absolute path - works properly
    absPATH = pathlib.Path(MEDIA_PATH, pathlib.Path(location).parent)
    
    # .parts[-2] indicates currents sequence folder name, i.e. with path: "sequences/abc/abc.zip" -> "abc"
    seqName = pathlib.PurePath(location).parts[-2]
    
    for fileName in os.listdir(absPATH):
        if fileName.startswith('ivpsnr_SL_' + seqName):
            # opening a file through its absolute path
            file = open(pathlib.Path(absPATH, fileName))
            
            psnrValues = []
            
            for line in file:
                if line.startswith('IVPSNR'):
                    psnrValues.append(float(re.findall('[0-9]+\.[0-9]+', line)[0]))
            
            if psnrValues:      # if psnrValues list isn't empty
                maxValue = max(psnrValues)
                minValue = min(psnrValues)
                avgValue = round((sum(psnrValues) / len(psnrValues)), 4)
                # TODO: update SequenceModels object
                object.quality = avgValue
                # INFO: .update method doesn't work on single objects
                # object.update(quality=avgValue)
                print("AVG_DATA:", avgValue)
                object.save(update_fields=['quality'])
                
##############################################
# multicolumn

# MATEUSZ - wyciąganie map głębi dla wielu sekwencji i restrukturyzacja kodu
# WOJCIECH - pierwotny zamysł
# DONE: zipUnpack [multicolumn]
def zipUnpack_m(location):
    absPATH = MEDIA_PATH + str(pathlib.Path(location).parent)
    file_name = str(pathlib.PurePath(location).stem) + '.zip'
    if file_name in os.listdir(absPATH):
        file_path = absPATH + "\\" + file_name
        zip_obj = ZipFile(file_path, 'r')
        zip_obj.extractall(file_path.replace('.zip', ''))       # extracts all files from archive to new subfolder named the same as archive
        zip_obj.close()
        
# MATEUSZ
# DONE: probably - batchSynthesis
def batchSynthesis_m(object):
    # running BATCH file
    batchPATH_Poznan_10 = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_") + " PoznanFencing 10")
    
    batchPATH_Poznan_30 = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_") + " PoznanFencing 30")
    
    batchPATH_Poznan_raw = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_") + " PoznanFencing raw")
    
    batchPATH_Carpark_10 = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_") + " Carpark 10")
    
    batchPATH_Carpark_30 = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_") + " Carpark 30")
    
    batchPATH_Carpark_raw = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(object.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(object.src)).parent) + " " + str(object.title).lower().replace(" ", "_") + " Carpark raw")
    
    # subprocess.call(batchPATH)        - old/deprecated
    # PROCESSING PoznanFencing (10/30/raw depth_QP)
    subprocess.run(batchPATH_Poznan_10)
    subprocess.run(batchPATH_Poznan_30)
    subprocess.run(batchPATH_Poznan_raw)
    
    # PROCESSING Carpark (10/30/raw depth_QP)
    subprocess.run(batchPATH_Carpark_10)
    subprocess.run(batchPATH_Carpark_30)
    subprocess.run(batchPATH_Carpark_raw)
    
    # delete folder with unpacked depths
    rmPATH = pathlib.Path(MEDIA_PATH, str(object.src).replace('.zip', ''))
    shutil.rmtree(rmPATH)
    print("PROCESSING_{}: REMOVING auxilliary folder of {}".format(str(object.title), str(object.title)))

    
    
def processPSNR_m(object, location):
    print("NOTHING") 
    # TODO: PSNR for multiple depths