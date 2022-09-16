from zipfile import ZipFile
import os

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

            if file_name.endswith('.pdf'):

                zip_object.extract(file_name, end_path)

        zip_object.close()

        # os.remove(zip_name)
        
def loop():
    
    for x in os.listdir('depth_grader/media/sequences'):

        path = 'depth_grader/media/sequences/' + x

        if path == 'depth_grader/media/sequences/.DS_Store':

            os.remove(path)

        else:

            for x in os.listdir(path):

                new_path = path + "/" + x

                if new_path == path + "/.DS_Store":

                    os.remove(new_path)

                else:

                    compression_factor(new_path)

                    unzip(new_path)