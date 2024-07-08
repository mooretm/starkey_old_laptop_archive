import pandas as pd
import numpy as np

import tkinter as tk
from tkinter import filedialog


#_path = filedialog.askopenfilename(
#    filetypes=[("All files", "*.*")])
#print(_path)

_path = 'C:/Users/MooTra/OneDrive - Starkey/Desktop/SNR50_Stimuli/IEEE_Sentences/IEEE_snr50.csv'
x = pd.read_csv(_path)
nums = np.repeat(x['list_num'].unique(), 11)
nums = nums[0:len(x['list_num'])]

print(f"The highest list number is: {np.max(nums)}")
print(f"{np.max(nums)} occurs {list(nums).count(np.max(nums))} times")
if list(nums).count(np.max(nums)) != 11:
    print(f"Removing {np.max(nums)}")
    nums = nums[0:-list(nums).count(np.max(nums))]
    print(f"The new highest value is: {np.max(nums)}")
    print(f"{np.max(nums)} occurs {list(nums).count(np.max(nums))} times")
print(f"")

x = x.iloc[0:len(nums), :]
x['list_num'] = nums

x.to_csv('IEEE_snr50.csv')

