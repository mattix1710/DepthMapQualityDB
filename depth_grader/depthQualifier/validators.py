def validate_archive_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]       # [0] returns path+filename
    validExtensions = ['.zip']
    if not ext.lower() in validExtensions:
        raise ValidationError('Unsupported file extension.')

def validate_file_exist(value):                 # TODO: check validation "Storage"
    import os
    from django.core.exceptions import ValidationError
    from django.core.files.storage import Storage
    print(Storage.exists(value.name))

