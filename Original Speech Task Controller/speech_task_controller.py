# tk inter imports
import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter import font
from tkinter import Menu
from tkinter.messagebox import askyesno
from tkinter.messagebox import showinfo
from tkinter.messagebox import showwarning

# system imports
import os
import sys
import csv
from datetime import datetime
import time

# data science imports
import numpy as np
import pandas as pd
from pandastable import Table

# audio imports
from scipy.io import wavfile
import sounddevice as sd
#import warnings
#warnings.filterwarnings("ignore", message="Chunk (non-data) not understood ")

# import my library
sys.path.append('.\\lib') # Point to custom library file
import tmsignals as ts # Custom library
import importlib 
importlib.reload(ts) # Reload custom module on every run


#######################################
#### FOLDER AND STARTUP MANAGEMENT ####
#######################################
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Check for existing etc folder
if os.path.isdir(_thisDir + os.sep + 'etc' + os.sep):
    print("Found etc folder.")
else:
    print("No etc folder found; creating one.")
    os.mkdir(_thisDir + os.sep + 'etc' + os.sep)
    isdir = os.path.isdir(_thisDir + os.sep + 'etc' + os.sep)
    if isdir:
        print("Etc folder created successfully.")
    else:
        print("Problem creating etc folder.")

# Check for existing data folder
if os.path.isdir(_thisDir + os.sep + 'data' + os.sep):
    print("Found data folder.")
else:
    print("No data folder found; creating one.")
    os.mkdir(_thisDir + os.sep + 'data' + os.sep)
    isdir = os.path.isdir(_thisDir + os.sep + 'data' + os.sep)
    if isdir:
        print("Data folder created successfully.")
    else:
        print("Problem creating data folder.")

# Look for previous parameters file
try:
    df = pd.read_csv('.\\etc\\lastParams.csv',
        header=None, index_col=0)
    expInfo = df.to_dict()
    expInfo = expInfo[1] # to_dict returns a list, so grab first one
    # Set data types
    expInfo['level'] = float(expInfo['level'])
    expInfo['speaker'] = int(expInfo['speaker'])
    print("Loaded previous parameters from file")
except:
    expInfo = {'subject':'999', 'condition':'quiet', 'speaker':int(1), 'level':float(65), 'lists':'5'}
    print('Using default dictionary')

# Get current date/time
now = datetime.now()
expInfo['stamp'] = now.strftime("%Y_%b_%d_%H%M")


def import_stim_file(file_name):
    """ Select file using system file dialog 
        and read it into a dictionary.
    """
    global audio_dtype
    global audio_file
    global wav_dict
    # Dictionary of data types and ranges
    wav_dict = {
        'float32': (-1.0, 1.0),
        'int32': (-2147483648, 2147483647),
        'int16': (-32768, 32767),
        'uint8': (0, 255)
    }

    #file_name = filedialog.askopenfilename(initialdir=_thisDir)
    fs, audio_file = wavfile.read(file_name)
    audio_dtype = np.dtype(audio_file[0])
    print(f"Incoming data type: {audio_dtype}")

    # Immediately convert to float64 for manipulating
    if audio_dtype == 'float64':
        pass
    else:
        # 1. Convert to float64
        audio_file = audio_file.astype(np.float64)
        forced_audio_type = np.dtype(audio_file[0])
        print(f"Forced audio data type: {forced_audio_type}")
        # 2. Divide by original dtype max val
        audio_file = audio_file / wav_dict[str(audio_dtype)][1]

    return fs, audio_file, file_name


#####################
#### GLOBAL VARS ####
#####################
# Increment sentence/audio numbers
global list_counter
list_counter = 0
# Score function globals
global words
global nums
global newWords
global vals
global chkbox_dict
global theWords
global aCheckButton
# Score tracking
global cor_count
cor_count = 0
global incor_count
incor_count = 0
#global img
#img = ".\\assets\\temp.ico"
global REF_LEVEL
REF_LEVEL = -30.0
global SLM_Reading
global STARTING_LEVEL
global sndDevice
global level_tracker
level_tracker = []
global TASK_MODE
TASK_MODE = 'adaptive'


#########################
#### STARTUP WINDOW  ####
#########################
# Make params window
winStartParams = tk.Tk()
winStartParams.title('Session Parameters')
winStartParams.withdraw()
#winStartParams.wm_iconbitmap(img)

# Create startup parameters frames
frmStartup = ttk.Frame(winStartParams)
frmStartup.grid(column=0,row=0,sticky='NSEW', padx=10, pady=10)
frmStartup.columnconfigure(0, weight=1)
frmStartup.rowconfigure(0, weight=1)

frmStartup2 = ttk.Frame(winStartParams)
frmStartup2.grid(column=0,row=1,sticky='NSEW', padx=10, pady=10)
frmStartup2.columnconfigure(0, weight=1)
frmStartup2.rowconfigure(0, weight=1)

# Create labels and entries for startup params
# Values filled from params file or default dict
entries = []
text = tk.StringVar()
for idx, key in enumerate(expInfo):
    # Labels
    ttk.Label(frmStartup,text=str(key).capitalize() + ': ').grid(column=0,row=idx,sticky='E')
    # Entry boxes
    text = tk.StringVar()
    myEntry = ttk.Entry(frmStartup,textvariable=text)
    text = str(expInfo[key])
    myEntry.insert(0,text)
    #print(myEntry.get())
    if key == 'stamp':
        myEntry.config(state = 'disabled')
    myEntry.grid(column=1,row=idx,sticky='W')
    entries.append(myEntry)

# Write startup params to lastParams.csv
def startup_params():
    global sentences
    """ Collect param values and write to file.
    """
    keys = list(expInfo.keys())
    with open('.\\etc\\lastParams.csv', 'w', newline='') as f:
        for idx, entry in enumerate(entries):
            #print(entry.get())
            writer = csv.writer(f)
            writer.writerow([keys[idx], entry.get()])

    winStartParams.destroy()

# Save button
btnSave = ttk.Button(frmStartup2,text="Save",command=startup_params)
#btnSave.bind('<Return>', startup_params)
btnSave.focus()
btnSave.grid(column=0,row=len(expInfo)+1)

# Cancel without saving button
ttk.Button(frmStartup2,text="Cancel",command=lambda: quit()).grid(column=1,
    row=len(expInfo)+1)

# Center winStartParams  based on new size
winStartParams.update_idletasks()
#root.attributes('-topmost',1)
window_width = winStartParams.winfo_width()
window_height = winStartParams.winfo_height()
# get the screen dimension
screen_width = winStartParams.winfo_screenwidth()
screen_height = winStartParams.winfo_screenheight()
# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
# set the position of the window to the center of the screen
winStartParams.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
winStartParams.resizable(False, False)
winStartParams.deiconify()

winStartParams.mainloop()


#######################################
#### READ/WRITE VALUES BEFORE MAIN #### 
#######################################
# Reread expInfo to get updated values 
# entered in startup window
df = pd.read_csv('.\\etc\\lastParams.csv',
    header=None, index_col=0)
expInfo = df.to_dict()
expInfo = expInfo[1] # to_dict returns a list
expInfo['level'] = float(expInfo['level'])
expInfo['speaker'] = int(expInfo['speaker'])

# Get lists of written sentences
# based on values entered in startup
# window
df = pd.read_csv('.\\sentences\\IEEE-DF.csv')
lists = expInfo['lists'].split()
lists = [int(x) for x in lists]
sentences = df.loc[df['list_num'].isin(lists), 'ieee_text']
#print(sentences)

# Get audio files
# NOTE: files must be renamed as increasing
# integer values (e.g., 1, 2, 3...)
fileList = os.listdir('.\\audio\\IEEE')
x = [x[:-4] for x in fileList] # strip off '.wav'
fileList = sorted(x, key = int) # sort strings as int
fileList = [x+'.wav' for x in fileList] # add '.wav' back
sentence_nums = df.loc[df['list_num'].isin(lists), 'sentence_num']
sentence_nums = np.array(sentence_nums)
fileList = np.array(fileList)
fileList = fileList[sentence_nums]
#print(fileList)

# make a text file to save data
dataFile = _thisDir + os.sep + 'data' + os.sep + '%s_%s_%s' % (expInfo['subject'], expInfo['condition'], expInfo['stamp'] + '.csv')
with open(dataFile, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['subject','condition','lists','wrds_wrong','wrds_corr','num_words_corr','percent_cor','slm_cal_reading','raw_level','slm_offset','new_raw_lvl','new_db_lvl'])


########################
#### MENU FUNCTIONS ####
########################
def list_audio_devs():
    """ Return a table with the available audio devices.
    """
    global sndDevice
    audDev_win = Toplevel(root)
    audDev_win.title('Audio Device List')
    audDev_win.withdraw()
    #audDev_win.wm_iconbitmap(img)

    def doDevID():
        try:
            sndDevice = int(entDeviceID.get())
            sd.default.device = sndDevice
            # make a text file to save data
            dataFile = _thisDir + os.sep + 'etc' + os.sep + 'Sound_Device.csv'
            with open(dataFile, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([str(sndDevice)])

            audDev_win.destroy()
        except:
            showwarning(title='Oops!', message="Not a valid selection!\nPlease select another device!")

    options = {'padx':10, 'pady':10}
    options_small = {'padx':5, 'pady':5}
    frmID = ttk.Frame(audDev_win)
    frmID.grid(column=0, row=0, **options)

    frmTable = ttk.Frame(audDev_win)
    frmTable.grid(column=0, row=1, **options)

    lblInstr = ttk.Label(frmID, text="Enter the audio device ID:")
    lblInstr.grid(column=0, row=0, sticky='e', **options_small)
   
    entDeviceID = ttk.Entry(frmID)
    entDeviceID.grid(column=1, row=0, sticky='w', ** options_small)
    entDeviceID.focus()

    btnDeviceID = ttk.Button(frmID, text="Submit", command=doDevID)
    btnDeviceID.grid(column=0, row=1, sticky='w', **options_small)

    deviceList = sd.query_devices()
    names = [deviceList[x]['name'] for x in np.arange(0,len(deviceList))]
    chans_in =  [deviceList[x]['max_input_channels'] for x in np.arange(0,len(deviceList))]
    ids = np.arange(0,len(deviceList))
    df = pd.DataFrame({"device_id": ids, "name": names,"chans_in": chans_in})

    pt = Table(frmTable,dataframe=df, showtoolbar=True, showstatusbar=True)
    table = pt = Table(frmTable, dataframe=df)
    table.grid(column=0, row=0)
    pt.show()

    # Center root based on new size
    audDev_win.update_idletasks()
    #root.attributes('-topmost',1)
    window_width = audDev_win.winfo_width()
    window_height = audDev_win.winfo_height()
    # get the screen dimension
    screen_width = audDev_win.winfo_screenwidth()
    screen_height = audDev_win.winfo_screenheight()
    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    # set the position of the window to the center of the screen
    audDev_win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    audDev_win.resizable(False, False)
    audDev_win.deiconify()

    audDev_win.mainloop()


def mnuCalibrate():
    """ Calibration routine. Plays calibration file for speech 
        test and creates a correction factor based off the 
        entered SLM reading.
    """
    device_check()
    def playCalStim():
        # Calibration file location
        cal_file = ('.\\calibration\\IEEE_cal.wav')
        # Import audio and convert data type
        fs, myTarget, file_name = import_stim_file(cal_file)
        myTarget = ts.setRMS(myTarget,REF_LEVEL,eq='n')
        sigdur = len(myTarget) / fs
        sd.wait(sigdur)
        sd.play(myTarget,fs,mapping=[int(expInfo['speaker'])])


    def doWriteCal():
        global SLM_Reading
        global STARTING_LEVEL
        global SLM_OFFSET
        SLM_Reading = entSLMinput.get()
        print(SLM_Reading)
        # make a text file to save data
        dataFile = _thisDir + os.sep + 'etc' + os.sep + 'SLM_Reading.csv'
        with open(dataFile, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([str(SLM_Reading)])

        SLM_OFFSET = float(SLM_Reading) - float(REF_LEVEL)
        STARTING_LEVEL = float(expInfo['level']) - float(SLM_OFFSET)
        print("\n")
        print("SLM OUTPUT: " + str(SLM_Reading))
        print("-")
        print("REF LEVEL: " + str(REF_LEVEL))
        print("=")
        print("SLM OFFSET: " + str(SLM_OFFSET))
        print("\n")
        print("Desired starting level: " + str(expInfo['level']))
        print("-")
        print("SLM OFFSET: " + str(SLM_OFFSET))
        print("=")
        print("STARTING LEVEL: " + str(STARTING_LEVEL))
        print("\n")

        cal_win.destroy()


    # Create window
    cal_win = Toplevel(root)
    cal_win.withdraw()
    cal_win.title('Calibration')

    frame_options = {'padx':10, 'pady':10}
    options = {'padx':5, 'pady':5}
    
    # Frames
    frmLeft = ttk.Frame(cal_win)
    frmLeft.grid(column=0, row=0, sticky='e', **frame_options)

    frmRight = ttk.Frame(cal_win)
    frmRight.grid(column=1, row=0, sticky='w', **frame_options)

    frmBottom = ttk.Frame(cal_win)
    frmBottom.grid(column=0, row=1, **frame_options)

    # Widgets
    lblStartCal = ttk.Label(frmLeft, text="Present Stimulus:")
    lblStartCal.grid(column=0, row=0, sticky='e', **options)
    btnStartCal = ttk.Button(frmRight,text="Play", command=playCalStim)
    btnStartCal.grid(column=0, row=0, sticky='w', **options)
    btnStartCal.focus()

    lblSLMinput = ttk.Label(frmLeft, text="SLM Reading:")
    lblSLMinput.grid(column=0,row=1, sticky='e', **options)
    entSLMinput = ttk.Entry(frmRight)
    entSLMinput.grid(column=0,row=1, sticky='w', **options)

    btnSubmitCal = ttk.Button(frmBottom,text='Submit',command=doWriteCal)
    btnSubmitCal.grid(column=0,row=0)

    # Center root window based on new size
    cal_win.update_idletasks()
    window_width = cal_win.winfo_width()
    window_height = cal_win.winfo_height()
    screen_width = cal_win.winfo_screenwidth()
    screen_height = cal_win.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    cal_win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    cal_win.resizable(False, False)
    cal_win.deiconify()

    cal_win.mainloop()


def mnuAbout2():
    showinfo(
        title='About Speech Task Controller',
        message="Version: 1.2.1\nWritten by: Travis M. Moore\nCreated: 06/02/2022\nLast Updated: 06/23/2022")


def mnuHelp():
    showwarning(
        title='Help',
        message="Not yet available!\nGo find Travis! (Unless he's cranky...)"
    )


######################
#### ROOT WINDOW  ####
######################
# Initialize root window
root = tk.Tk()
root.title("Speech Task Controller")
root.withdraw()
#root.wm_iconbitmap(img)

# Menu
def confirm_exit():
    answer = askyesno(title='Really?',
        message='Are you sure you want to quit?')
    if answer:
        root.destroy()

# create a menubar
menubar = Menu(root)
root.config(menu=menubar)
# create the File menu
file_menu = Menu(menubar, tearoff=False)
# add menu items to the File menu
file_menu.add_command(
    label="Adaptive",
    command=lambda: [frmBtn.grid_forget(), frmBtnAdapt.grid(column=0, row=1, sticky="sw", **options), root.geometry("642x236")]
    #command=lambda: [frmBtn.destroy(), frmBtnAdapt.grid(column=0, row=1, sticky="sw", **options), root.geometry("642x236")]
)
file_menu.add_command(
    label="Fixed",
    command=lambda: [frmBtnAdapt.grid_forget(), frmBtn.grid(column=0, row=1, sticky="sw", **options), root.geometry("642x186")]
)
file_menu.add_separator()
file_menu.add_command(
    label='Exit',
    command=confirm_exit
)
# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)
# Create Tools menu
tools_menu = Menu(
    menubar,
    tearoff=0
)
# Add items to the Tools menu
tools_menu.add_command(
    label='Audio Devices',
    command=list_audio_devs)
tools_menu.add_command(
    label='Calibrate',
    command=mnuCalibrate)
# Add Tools menu to the menubar
menubar.add_cascade(
    label="Tools",
    menu=tools_menu
)
# create the help menu
help_menu = Menu(
    menubar,
    tearoff=0
)
# add items to the Help menu
help_menu.add_command(
    label='Help',
    command=mnuHelp)
help_menu.add_command(
    label='About',
    command=mnuAbout2
)
# add the Help menu to the menubar
menubar.add_cascade(
    label="Help",
    menu=help_menu
)

# Set widget display options
myFont = font.nametofont('TkDefaultFont').configure(size=10)
options = {'padx':10, 'pady':10}
#options_word = {'padx':0, 'pady':0}

frmSentence = ttk.LabelFrame(root, text='Sentence:', width=500, height=60)
frmSentence.grid(column=0, columnspan=2, row=0, sticky='nsew', **options, ipady=10)
frmSentence.grid_propagate(0)

frmBtnAdapt = ttk.Frame(root)
frmBtnAdapt.grid(column=0, row=1, sticky="sw", **options)

frmBtn = ttk.Frame(root)
#frmBtn.grid(column=0, row=1, sticky="sw", **options)

frmScore = ttk.Frame(root)
frmScore.grid(column=1, row=2, sticky="e")

sep = ttk.Separator(root, orient='vertical')
sep.grid(column=2, row=0, rowspan=12, sticky='ns')

frmParams = ttk.LabelFrame(root, text="Parameters")
frmParams.grid(column=3, row=0, rowspan=2, sticky='n',**options)

frmTrials = ttk.Frame(root)
frmTrials.grid(column=0, row=2, sticky='w',  **options)

# Display parameters in parameter frame
keys = list(expInfo.keys())
param_lbl_list = []
for idx, param in enumerate(expInfo):
    if param == 'stamp':
        pass
    else:
        lblLabel = ttk.Label(frmParams, text=keys[idx].capitalize() + ': ' + str(expInfo[param]))
        param_lbl_list.append(lblLabel)
        lblLabel.grid(column=0, row=idx, sticky='w')

# Display trial number
lblTrial = ttk.Label(frmTrials, text='Trial 0 of 0')
lblTrial.grid(column=0, row=0)

# Display presentation status
#status = tk.StringVar()
#status.set("Ready")
#lblStatus = ttk.Label(frmStatus, textvariable=status, anchor="center", width=10, borderwidth=1, relief="groove")
#lblStatus.config(font=('TkDefaultFont', 14))
#lblStatus.grid(column=0, row=0, sticky="n", ipadx=5, ipady=5)

score_text = tk.StringVar()
lblScore = ttk.Label(frmScore, textvariable=score_text, font=myFont) # padding=10
lblScore.grid(column=0, row=0, sticky="e", **options)
score_text.set('0 of 0 = 0.0% correct')


def play_audio():
    """ Presents current audio file.
    """
    # Define next audio file path
    audio_path = ('.\\audio\\IEEE\\')
    myFile = fileList[list_counter]
    myFilePath = audio_path + myFile
    # Import audio and convert data type
    fs, myTarget, file_name = import_stim_file(myFilePath)
    #[fs, myTarget] = wavfile.read(myFilePath)
    #myTarget = ts.doNormalize(myTarget,48000)
    myTarget = ts.setRMS(myTarget,STARTING_LEVEL,eq='n')
    sigdur = len(myTarget) / fs
    sd.wait(sigdur)
    sd.play(myTarget,fs,mapping=[int(expInfo['speaker'])])


theScores = []
def score(resp_val):
    # Process current sentence for presentation
    # and scoring.
    # Embarrassing list of globals...
    global cor_count
    global incor_count
    global list_counter
    global words
    global nums
    global newWords
    global vals
    global chkbox_dict
    global theWords
    global aCheckButton
    global list_of_lbls
    global list_of_chkboxes
    global SLM_OFFSET
    global SLM_Reading
    global STARTING_LEVEL

    try: 
        STARTING_LEVEL = STARTING_LEVEL
    except:
        print("Retrieving starting level...")
        device_check()
        cal_check()
        print(f"Found start level of: {round(STARTING_LEVEL,2)}")

    # Try scoring if there has been a response
    try:
        theScores = []
        words_cor = []
        words_incor = []
        for key, value in chkbox_dict.items():
            state = value.get()
            if state != 0:
                #print('Correct! ' + key[:-1])
                theScores.append(1)
                words_cor.append(key[:-1])
                chkbox_dict[key].set(0)
            else:
                if key.isupper() and key[:-1] != 'A':
                    #print('Wrong! ' + key[:-1])
                    theScores.append(0)
                    words_incor.append(key[:-1])
                    chkbox_dict[key].set(0)

        cor_vals = [
            x
            for x in theScores
            if x == 1
        ]

        num_corr = len(cor_vals)

        # Mark correct or incorrect
        # Criterion: all keywords must have been correctly identified
        if all(ele > 0 for ele in theScores):
            cor_count += 1
            #level_tracker.append(SLM_OFFSET+STARTING_LEVEL) # only averaging correct levels is incorrect!
            print(f"Correct! Adding {SLM_OFFSET+STARTING_LEVEL} to average")
        else:
            incor_count += 1

        # Store all levels for averaging 
        # to calculate SNR50 speech level
        level_tracker.append(SLM_OFFSET+STARTING_LEVEL)

        total_count = cor_count + incor_count
        try:
            percent_cor = cor_count/total_count*100
        except:
            percent_cor = 0

        score_text.set(f'{cor_count} of {total_count} = {round(percent_cor,1)}% correct')
        lblTrial.config(text=f'Trial {total_count} of {len(fileList)}')
        #print(theScores)
        print("Try: Scored Responses")
    except:
        print("Except: Couldn't score because there were no values yet")
        # No values to score, which means this is the first iteration

    # Destroy labels and checkboxes, if they exist
    try:
        list_of_lbls = list(filter(None, list_of_lbls))
        list_of_chkboxes = list(filter(None, list_of_chkboxes))

        for widget in list_of_chkboxes:
            widget.destroy()

        for widget in list_of_lbls:
            widget.destroy()

        # Increment list counter to move to next list
        list_counter += 1
        print("Try: Destroyed checkboxes and labels")
    except:
        print("Except: Nothing to destroy on first iteration")
        pass

    # Write data to file BEFORE loading sentences at end of list
    try:
        with open(dataFile, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([str(expInfo['subject']), 
                str(expInfo['condition']), str(expInfo['lists']),
                str(words_incor), str(words_cor), str(num_corr),
                str(round(percent_cor,2)), str(SLM_Reading), 
                str(REF_LEVEL), str(SLM_OFFSET), str(STARTING_LEVEL),
                str(SLM_OFFSET+STARTING_LEVEL)])
        print("Wrote data to file")
        print(f"Wrote level: {round(STARTING_LEVEL,2)}")

        # Display data to user after final iteration
        if list_counter > len(sentences)-1:
            print("That was the last trial!")
            if TASK_MODE == 'adaptive':
                showinfo(title="Task complete!", 
                    #message="Final score: " + str(percent_cor) + "%")
                    message="SNR50: " + str(np.mean(level_tracker)) + " dB")
            elif TASK_MODE == 'fixed':
                showinfo(title="Task complete!", 
                    message="Final score: " + str(percent_cor) + "%")
                    #message="SNR50: " + str(np.mean(level_tracker)) + " dB")
    except: 
        pass
    # Quit doesn't seem to work inside the try/except test,
    # so I'm putting it on its own. 
    if list_counter > len(sentences)-1:
        print("Using second quit")
        quit()

    # Update STARTING_LEVEL based on button click
    if btn_right.cget('text') == "Start":
        print(f"Running with original level: {round(STARTING_LEVEL,2)}")
    else:
        print("Updating level...")
        if resp_val == "right":
            print(f'Try: previous level: {round(STARTING_LEVEL,2)}')
            STARTING_LEVEL = float(STARTING_LEVEL) - float(ent_right.get())
            print(f'Try: adjusted level: {round(STARTING_LEVEL,2)}')
        elif resp_val == "wrong":
            print(f'Try: previous level: {round(STARTING_LEVEL,2)}')
            STARTING_LEVEL = float(STARTING_LEVEL) + float(ent_wrong.get())
            print(f'Try: adjusted level: {round(STARTING_LEVEL,2)}')
        elif resp_val == "fixed":
            pass

    # Update start button text as a flat the first iteration 
    # has occurred
    btn_right.config(text="Right")

    #### Text and checkbox display ####
    print("Adding labels and checkboxes")
    theText = ''.join(sentences.iloc[list_counter]) # using pandas, ['the dog is fast']
    words = theText.split() # ['the' 'dog' 'is' 'fast']
    nums = np.arange(0,len(words)) # index to ensure each word is a unique key
    nums = [str(x) for x in nums] # turn into strings
    # Append nums to words to ensure each word is a unique dict key
    newWords = []
    for i, word in enumerate(words):
        word = word + str(i)
        newWords.append(word)
    # Prepopulate checkboxes to "off"
    vals = np.zeros(len(words),dtype=int)
    chkbox_dict = dict(zip(newWords,vals))

    # Instantiate and display words and checkboxes
    list_of_chkboxes = [] # Store boxes in list
    list_of_lbls = [] # Store word labels in list
    for counter, key in enumerate(chkbox_dict,start=0):
        chkbox_dict[key] = tk.IntVar()
        if key.isupper() and key[:-1] != 'A': # Have to strip trailing numeral
            theWords = ttk.Label(frmSentence,text=newWords[counter][:-1])
            theWords.config(font=('TkDefaultFont 10 underline'))
            theWords.grid(column=counter,row=0)
            aCheckButton = ttk.Checkbutton(frmSentence,text='',takefocus=0,variable=chkbox_dict[key])
            aCheckButton.grid(column=counter,row=1)
            list_of_chkboxes.append(aCheckButton)
            list_of_lbls.append(theWords)
        else:
            aCheckButton = ttk.Checkbutton(frmSentence,text='',takefocus=0,variable=chkbox_dict[key])
            #aCheckButton.grid(column=counter,row=4) # Do not display these checkboxes
            theWords = ttk.Label(frmSentence,text=newWords[counter][:-1])
            theWords.grid(column=counter,row=0)
            #list_of_chkboxes.append(aCheckButton)
            list_of_lbls.append(theWords)

    # Present the current audio file
    print(f"Playing audio at {round(STARTING_LEVEL,2)}")
    param_lbl_list[3].config(text="Level: " + str(SLM_OFFSET+STARTING_LEVEL))

    # btn_right.config(state='disabled')
    # btn_right.update()
    # btn_wrong.config(state='disabled')
    # btn_wrong.update()
    # btnNext.config(state='disabled')
    # btnNext.update()

    play_audio()

    # btn_right.config(state='enabled')
    # btn_right.update()
    # btn_wrong.config(state='enabled')
    # btn_wrong.update()
    # btnNext.config(state='enabled')
    # btnNext.update()

    print("End of iteration\n")


def do_right():
    global TASK_MODE
    device_check()
    btn_wrong.config(state='enabled')
    TASK_MODE='adaptive'
    score("right")


def do_wrong():
    global TASK_MODE
    TASK_MODE='adaptive'
    score("wrong")


def do_fixed():
    device_check()
    #wait_var.set(1)
    global TASK_MODE
    TASK_MODE='fixed'
    btnNext.config(text="Next")
    score("fixed")


# Buttons
# Adaptive task buttons
btn_right = ttk.Button(frmBtnAdapt, text="Start", state='enabled', command=do_right)
btn_right.grid(column=0, row=1)
btn_wrong = ttk.Button(frmBtnAdapt, text="Wrong", state='disabled', command=do_wrong)
btn_wrong.grid(column=0, row=2)

ent_right = ttk.Entry(frmBtnAdapt, width=5)
ent_right.grid(column=1,row=1)
ent_right.insert(0,str(10))
ent_wrong = ttk.Entry(frmBtnAdapt, width=5)
ent_wrong.grid(column=1,row=2)
ent_wrong.insert(0,str(5))

lbl_step = ttk.Label(frmBtnAdapt, text="Step Size")
lbl_step.grid(column=1, row=0)

# Fixed task buttons
wait_var = tk.IntVar()
btnNext = ttk.Button(frmBtn, text="Start", command=do_fixed)
btnNext.grid(column=0, row=0, sticky="w")


# Center root based on new size
root.update_idletasks()
#root.attributes('-topmost',1)
window_width = root.winfo_width()
window_height = root.winfo_height()
#window_width = 600
#window_height=200
# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.deiconify()


############################
#### SOUND DEVICE CHECK ####
############################
def device_check():
    try:
        sndDevice = pd.read_csv('.\\etc\\Sound_Device.csv')
        sndDevice = int(sndDevice.columns[0])
        sd.default.device = sndDevice
    except:
        showwarning(title="Whoa!!", message="No sound device selected!!\nPlease select a sound device before continuing!")
        list_audio_devs()


###########################
#### CALIBRATION CHECK ####
###########################
def cal_check():
    global STARTING_LEVEL
    global SLM_Reading
    global SLM_OFFSET
    try:
        SLM_Reading = pd.read_csv('.\\etc\\SLM_Reading.csv')
        SLM_Reading = float(SLM_Reading.columns[0])
        SLM_OFFSET = float(SLM_Reading) - float(REF_LEVEL)
        STARTING_LEVEL = float(expInfo['level']) - float(SLM_OFFSET)
        if SLM_Reading < 0:
            showwarning(title="Whoa!!", message="Invalid calibration value found! Please recalibrate before continuing!!")
            mnuCalibrate()
    except:
        showwarning(title="Whoa!!", message="No calibration value found! Please calibrate before continuing!!")
        mnuCalibrate()

root.mainloop()
