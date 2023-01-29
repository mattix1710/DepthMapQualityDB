import os
import sys
import pathlib2

FILES_PATH = pathlib2.Path(sys.argv[1])
SEQ_NAME = sys.argv[2]
METHOD_NAME = sys.argv[3]
QP_SET = sys.argv[4]

ROOT_PATH_FILE = pathlib2.PurePath(FILES_PATH.parent.parent, 'bitrate_' + METHOD_NAME + '.txt')

total_bytes = 0
counter = 0

for file in os.listdir(FILES_PATH):
    if file.__contains__('synth_COMPRESSED.mp4'):                          # if "synth_COMPRESSED.mp4"
        FILE_PATH = pathlib2.PurePath(FILES_PATH, file)
        total_bytes += os.path.getsize(FILE_PATH)
        counter += 1
        
MEGABITS = 10**6

# /5 * 25 * 8 = *40 <- five frames of video with framerate of 25fps in bits (1 byte = 8 bits) gives multiplication of 40
bitrate_number = round((total_bytes * 40 / (counter * MEGABITS)), 2)
bitrate_string = SEQ_NAME + "_" + QP_SET + ": " + str(bitrate_number) + " [Mb/s]"

with open(ROOT_PATH_FILE,'a') as file:
    file.write(bitrate_string + '\n')
    file.close()
    print("BITRATE data successfully written!")