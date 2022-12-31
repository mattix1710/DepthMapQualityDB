from django.core.exceptions import ValidationError
import re
import pathlib
import zipfile

# uploaded_file - file uploaded through a method upload form
def validate_archive_extension(uploaded_file):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(uploaded_file.name)[1]       # [0] returns path+filename
    validExtensions = ['.zip']
    if not ext.lower() in validExtensions:
        raise ValidationError('Unsupported file extension. Use ZIP archive!')
    
    #################################
    # file list that is expected to be available in uploaded ZIP file
    file_list = {'PoznanFencing/', 'PoznanFencing/v0_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v1_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v2_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v3_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v4_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v5_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v6_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v7_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v8_depth_1920x1080_yuv400p16le.yuv', 'PoznanFencing/v9_depth_1920x1080_yuv400p16le.yuv', 'Carpark/', 'Carpark/v0_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v1_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v2_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v3_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v4_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v5_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v6_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v7_depth_1920x1088_yuv400p16le.yuv', 'Carpark/v8_depth_1920x1088_yuv400p16le.yuv'}
    
    file_path = uploaded_file._get_file().temporary_file_path()
    
    try:
        with zipfile.ZipFile(file_path, mode='r') as archive:
            archive_list = archive.namelist()
            if file_list != set(archive_list):
                if len(file_list) != len(archive_list):
                    print("WRONG FILE UPLOAD: some files are missing!")
                    raise ValidationError("ERROR: some files are missing!\n Check if contents match the file hierarchy shown next to the form.")
                else:
                    print("WRONG FILE UPLOAD: some files or folders are incorrectly named!")
                    raise ValidationError("ERROR: some files or folders are incorrectly named!\n Check if contents match the file hierarchy shown next to the form.")
            archive.close()
    # exception thrown if uploaded file doesn't match ZIP file coding 
    # (i.e. file was secretly .7z archive, but had .zip extension instead)
    except zipfile.BadZipFile:
        raise ValidationError("ERROR: file is not a ZIP file!")