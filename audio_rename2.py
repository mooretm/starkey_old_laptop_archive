
import os
import tkinter as tk
from tkinter import filedialog

#To rename the IEEE audio files for sorting
dir_name = filedialog.askdirectory()
print(dir_name)

names = os.listdir(dir_name)
names = [x[:-4] for x in names]
names = sorted(names, key = int) # sort strings as int
names = [x+'.wav' for x in names]
print(names)

for idx, file in enumerate(names, start=1):
    old_path = os.path.join(dir_name, file)
    new_path = os.path.join(dir_name, file[:-4] + "_" + str(idx) + ".wav")
    os.rename(old_path, new_path)


# for filename in os.listdir('.\\audio\\IEEE'):
#     filename = myPath + filename
#     sep = ' '
#     clipped = filename.split(sep,1)[0]
#     just_nums = clipped[2:]
#     os.rename(filename, just_nums)


# for filename in os.listdir('.\\audio\\IEEE'):
#     os.rename(r'.\\audio\\IEEE\\'+filename,r'.\\audio\\IEEE\\'+filename[2:]+'.wav')


"""
Works for slicing and ordering file names, 
but doesn't actually change them.
sep = ' ' 
clipped = [x.split(sep,1)[0] for x in fileList]
just_nums = [x[2:] for x in clipped]
fileList = sorted(just_nums, key = int)
#print(fileList)
"""