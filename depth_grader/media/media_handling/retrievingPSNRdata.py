import re
import os
import statistics as st

filename = 'ivpsnr_SL.txt'

file = open(filename, 'r')
lines = file.readlines()

arr = []

for line in lines:
    if(line.startswith("IVPSNR")):
        print(line)
        data = re.findall("\d+\.\d+", line)
        for value in data:
            arr.append(float(value))

print("mean PSNR: " + str(round(st.mean(arr),2)))

with open('../outPSNR.txt', 'a') as output:
    output.write(str(round(st.mean(arr),2)) + os.linesep)
    # for line in arr:
    #     for val in line:
    #         output.write(str(val) + "\t")
    #     output.write(os.linesep)