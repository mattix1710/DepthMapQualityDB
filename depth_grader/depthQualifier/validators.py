from django.core.exceptions import ValidationError
import zipfile
import os

# (only USERS) file list that is expected to be available in uploaded ZIP file
FILE_DEPTH_METHOD_LIST = {'PoznanFencing/', 'PoznanFencing/v0_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v1_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v2_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v3_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v4_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v5_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v6_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v7_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v8_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v9_depth_1920x1080_yuv400p16le.yuv', 'Carpark/', 'Carpark/v0_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v1_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v2_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v3_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v4_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v5_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v6_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v7_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v8_depth_1920x1088_yuv400p16le.yuv'}

# (only ADMIN use) file list that is expected to be available in uploaded ZIP file
FILE_SEQUENCE_POZNANFENCING = {'PoznanFencing/', 'PoznanFencing/v0_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v1_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v2_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v3_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v4_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v5_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v6_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v7_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v8_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v9_texture_1920x1080_yuv420p8le.yuv'}
FILE_SEQUENCE_CARPARK = {'Carpark/', 'Carpark/v0_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v1_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v2_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v3_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v4_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v5_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v6_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v7_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v8_texture_1920x1088_yuv420p8le.yuv'}
FILE_SEQUENCE_ALL = {'Carpark/', 'Carpark/v0_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v1_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v2_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v3_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v4_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v5_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v6_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v7_texture_1920x1088_yuv420p8le.yuv', 'Carpark/v8_texture_1920x1088_yuv420p8le.yuv', 'PoznanFencing/', 'PoznanFencing/v0_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v1_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v2_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v3_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v4_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v5_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v6_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v7_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v8_texture_1920x1080_yuv420p8le.yuv', 'PoznanFencing/v9_texture_1920x1080_yuv420p8le.yuv'}

FILE_SEQUENCE_LIST = {'all': FILE_SEQUENCE_ALL,
                    'PoznanFencing' : FILE_SEQUENCE_POZNANFENCING,
                    'Carpark' : FILE_SEQUENCE_CARPARK}

# uploaded_file - file uploaded through a method upload form
def validate_archive_method(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1]       # [0] returns path+filename
    validExtensions = ['.zip']
    if not ext.lower() in validExtensions:
        raise ValidationError('Unsupported file extension. Use ZIP archive!')
    
    #################################
    
    file_path = uploaded_file._get_file().temporary_file_path()
    
    try:
        with zipfile.ZipFile(file_path, mode='r') as archive:
            archive_list = archive.namelist()
            if FILE_DEPTH_METHOD_LIST != set(archive_list):
                if len(FILE_DEPTH_METHOD_LIST) != len(archive_list):
                    print("WRONG FILE UPLOAD: some files are missing!")
                    raise ValidationError("ERROR: some files are missing!\nCheck if contents match the file hierarchy shown next to the form.")
                else:
                    print("WRONG FILE UPLOAD: some files or folders are incorrectly named!")
                    raise ValidationError("ERROR: some files or folders are incorrectly named!\nCheck if contents match the file hierarchy shown next to the form.")
    # exception thrown if uploaded file doesn't match ZIP file coding 
    # (i.e. file was secretly .7z archive, but had .zip extension instead)
    except zipfile.BadZipFile:
        raise ValidationError("ERROR: file is not a ZIP file!")
    finally:
        archive.close()
    
# uploaded_file - file uploaded through admin page
def validate_archive_sequence(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1]       # [0] returns path+filename
    validExtensions = ['.zip']
    if not ext.lower() in validExtensions:
        raise ValidationError('Unsupported file extension. Use ZIP archive!')
    
    #################################
    
    file_path = uploaded_file._get_file().temporary_file_path()
    
    try:
        with zipfile.ZipFile(file_path, mode='r') as archive:
            archive_list = archive.namelist()
            for file in FILE_SEQUENCE_LIST:
                if FILE_SEQUENCE_LIST[file] != set(archive_list):
                    if len(FILE_SEQUENCE_LIST[file]) != len(archive_list):
                        print("WRONG FILE UPLOAD: some files are missing!")
                        raise ValidationError("ERROR: some files are missing!")
                    else:
                        print("WRONG FILE UPLOAD: some files or folders are incorrectly named!")
                        raise ValidationError("ERROR: some files or folders are incorrectly named!")
    # exception thrown if uploaded file doesn't match ZIP file coding 
    # (i.e. file was secretly .7z archive, but had .zip extension instead)
    except zipfile.BadZipFile:
        raise ValidationError("ERROR: file is not a ZIP file!")
    finally:
        archive.close()