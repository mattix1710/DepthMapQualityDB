"""
    * functions.py
    * File containing various methods used in methods from tasks.py or used freely
"""

import os
import pathlib2 as pathlib
import shutil
import subprocess
from zipfile import ZipFile
import re

# from parent location
from ..models import *

MEDIA_PATH = str(pathlib.Path(__file__).parent.parent.parent) + '/media/'
    
# MATEUSZ
def delete_method(method):
    folder_path = os.path.dirname(str(method.src))
    full_folder_path = MEDIA_PATH + folder_path
    
    # remove folder and its contents
    shutil.rmtree(full_folder_path)

# WOJCIECH - nigdzie nie używana
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

FUNCTIONS_PATH = str(pathlib.Path(__file__).parent)

MAIN_PATH = str(pathlib.Path(__file__).parent.parent.parent)  

# MATEUSZ - wyciąganie map głębi dla wielu sekwencji i restrukturyzacja kodu
# WOJCIECH - pierwotny zamysł
# TODO: add try/catch FILE NOT EXISTS ERROR
def mul_zip_unpack(location):
    absPATH = MEDIA_PATH + str(pathlib.Path(location).parent)
    file_name = str(pathlib.PurePath(location).stem) + '.zip'
    if file_name in os.listdir(absPATH):
        file_path = absPATH + "\\" + file_name
        with ZipFile(file_path, 'r') as zip_obj:
            zip_obj.extractall(file_path.replace('.zip', ''))       # extracts all files from archive to new subfolder named the same as archive
            zip_obj.close()
        
# MATEUSZ
def mul_batch_synthesis(method):
    # running BATCH file
    batchPATH_Poznan_10 = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(method.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(method.src)).parent) + " " + str(method.method_name).lower().replace(" ", "_") + " PoznanFencing 10")
    
    batchPATH_Poznan_30 = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(method.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(method.src)).parent) + " " + str(method.method_name).lower().replace(" ", "_") + " PoznanFencing 30")
    
    batchPATH_Poznan_raw = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(method.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(method.src)).parent) + " " + str(method.method_name).lower().replace(" ", "_") + " PoznanFencing raw")
    
    batchPATH_Carpark_10 = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(method.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(method.src)).parent) + " " + str(method.method_name).lower().replace(" ", "_") + " Carpark 10")
    
    batchPATH_Carpark_30 = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(method.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(method.src)).parent) + " " + str(method.method_name).lower().replace(" ", "_") + " Carpark 30")
    
    batchPATH_Carpark_raw = os.path.abspath(FUNCTIONS_PATH + '/synthSequence.bat ' + str(method.src).replace('.zip', '') 
        + " " + MAIN_PATH + " " + str(pathlib.Path(str(method.src)).parent) + " " + str(method.method_name).lower().replace(" ", "_") + " Carpark raw")
    
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
    rmPATH = pathlib.Path(MEDIA_PATH, str(method.src).replace('.zip', ''))
    shutil.rmtree(rmPATH)
    print("PROCESSING_{}: REMOVING auxilliary folder of {}".format(str(method.method_name), str(method.method_name)))

# WOJCIECH po wielkich męczarniach
# process calculated data: PSNR & bitrate (found in txt files in objects location)
def mul_process_data(method, location):
    
    SEQUENCE_POZNAN_FENCING = Sequence.objects.get(seq_name = 'PoznanFencing')
    SEQUENCE_CARPARK = Sequence.objects.get(seq_name = 'Carpark')

    metoda = method

    ideal_path = pathlib.Path(MEDIA_PATH, pathlib.Path(location).parent)
    
    Carpark_10 = ['Carpark_10', 0, 0]
    Carpark_30 = ['Carpark_30', 0, 0]
    Carpark_raw = ['Carpark_raw', 0, 0]
    Fencing_10 = ['Fencing_10', 0, 0]
    Fencing_30 = ['Fencing_30', 0, 0]
    Fencing_raw = ['Fencing_raw', 0, 0]

    for fileName in os.listdir(ideal_path):
            if fileName.startswith('ivpsnr_SL_'):

                file = open(pathlib.Path(ideal_path, fileName))

                psnrValues = []
                
                for line in file:
                    if line.startswith('IVPSNR'):
                        psnrValues.append(float(re.findall('[0-9]+\.[0-9]+', line)[0]))
                        avgValue = round((sum(psnrValues) / len(psnrValues)), 4)
                if('Carpark_10' in fileName):
                    Carpark_10[1] = (avgValue)
                
                if('Carpark_30' in fileName):
                    Carpark_30[1] = (avgValue)

                if('Carpark_raw' in fileName):
                    Carpark_raw[1] = (avgValue)

                if('Fencing_10' in fileName):
                    Fencing_10[1] = (avgValue)

                if('Fencing_30' in fileName):
                    Fencing_30[1] = (avgValue)

                if('Fencing_raw' in fileName):
                    Fencing_raw[1] = (avgValue)

            elif fileName.startswith('bitrate'):

                file = open(pathlib.Path(ideal_path, fileName))
                
                for line in file:
                    if(line.startswith('Carpark_10')):
                        Carpark_10[2] = (float(re.findall('[0-9]+\.[0-9]+', line)[0]))

                    if(line.startswith('Carpark_30')):
                        Carpark_30[2] = (float(re.findall('[0-9]+\.[0-9]+', line)[0]))

                    if(line.startswith('Carpark_raw')):
                        Carpark_raw[2] = (float(re.findall('[0-9]+\.[0-9]+', line)[0]))

                    if(line.startswith('PoznanFencing_10')):
                        Fencing_10[2] = (float(re.findall('[0-9]+\.[0-9]+', line)[0]))

                    if(line.startswith('PoznanFencing_30')):
                        Fencing_30[2] = (float(re.findall('[0-9]+\.[0-9]+', line)[0]))

                    if(line.startswith('PoznanFencing_raw')):
                        Fencing_raw[2] = (float(re.findall('[0-9]+\.[0-9]+', line)[0]))

    print(Carpark_10)
    print(Carpark_30)
    print(Carpark_raw)
    print(Fencing_10)
    print(Fencing_30)
    print(Fencing_raw)

    results1 = SeqDepthResult.objects.get(method_id = metoda, seq_id = SEQUENCE_CARPARK)
    results1.synth_PSNR_1018 = Carpark_10[1]
    results1.synth_PSNR_3042 = Carpark_30[1]
    results1.synth_PSNR_none = Carpark_raw[1]
    results1.synth_bitrate_1018 = Carpark_10[2]
    results1.synth_bitrate_3042 = Carpark_30[2]
    results1.synth_bitrate_none = Carpark_raw[2]
    results1.save()

    results2 = SeqDepthResult.objects.get(method_id = metoda, seq_id = SEQUENCE_POZNAN_FENCING)
    results2.synth_PSNR_1018 = Fencing_10[1]
    results2.synth_PSNR_3042 = Fencing_30[1]
    results2.synth_PSNR_none = Fencing_raw[1]
    results2.synth_bitrate_1018 = Fencing_10[2]
    results2.synth_bitrate_3042 = Fencing_30[2]
    results2.synth_bitrate_none = Fencing_raw[2]
    results2.save()