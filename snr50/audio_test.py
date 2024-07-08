# Import published modules
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from scipy.io import wavfile
import sounddevice as sd


sys.path.append('.\\lib') # Point to custom library file
import tmsignals as ts # Custom library
import importlib 
importlib.reload(ts) # Reload custom module on every run

fs, s235 = wavfile.read('.\\audio\\IEEE\\235.wav')

sig = ts.doNormalize(s235)
sig = ts.setRMS(s235,-50)
sd.play(sig,fs)
sd.wait(len(sig)/fs)

print("end")
