# **Speech Task Controller**

Graphical user interface (GUI) for presenting and scoring speech tasks.

- Written by: **Travis M. Moore**
- Latest version: **Version 2.1.1**
- Last edited: **December 02, 2022**
<br>
<br>

---

## Description
- This GUI was developed to provide an easy method for presenting speech tasks
at various presentation levels, including adaptive changes in presentation 
level, without having to recalibrate each time the level changes. 

- This GUI also offers point-and-click scoring and provides session 
data at the end in .csv format. This avoids data entry errors (e.g., transferring 
paper scores into a spreadsheet), as well as provides a common format for storing
scores (e.g., for use with automated data entry scripts). 
<br>
<br>

---

## Getting Started

### Dependencies

- Windows 10 or greater (not compatible with Mac OS)

### Installing

- This is a compiled app; the executable file is stored on Starfile at: \\starfile\Public\Temp\MooreT\Custom Software
- Simply copy the executable file and paste to a location on the local machine
- Double click to start the app

### First Use
- Double-click to start the application for the first time.
- Go to **File-->Session** to provide file paths to stimulus files, as 
well as enter session information 
- Go to **Tools-->Audio** Settings to enter a valid audio device ID.
- Go to **Tools-->Calibration** to calibrate using a sound level meter.
- Click the START button on the main screen to begin.
<br>
<br>

---

## Session Details
The Speech Task Controller requires several pieces of session information. Navigate to **File-->Session** to open the Session window (see image below).

<!-- <img src="./assets/images/session_info_window.png" alt="Session Info Window image" width="600"/> -->
<img src="session_info_window.png" alt="Session Info Window image" width="600"/>

### Session Information
The first section of the Session window asks for the following information:

- Subject: The participant ID number. Can be alphanumeric. 
- Condition: A custom name for the current condition. Use underscores to add additional descriptors. For example: `quiet_highpass_unaided`.
- List(s): Specify the list you would like to present from the speech test/corpus. Enter additional list numbers separated by spaces to present multiple lists. For example: `1 2 5`. Lists do not have to be in sequential order. 
- Level (dB): Enter the desired presentation level, using up to one decimal place For example: `65.5`.

### Stimulus Directories
Provide the Speech Task Controller with the file paths to your stimuli. 

- Click the BROWSE button in the "Audio File Directory" section and navigate to the folder containing your audio files.
- Click the BROWSE button in the "Sentence File Directory" section and navigate to the folder containing your .csv file of sentence text.
<br>
<br>

---

## Stimulus Requirements

### Audio Files

- All audio files must be in .wav format. 
- Each sentence from the speech task/corpus must exist in its own .wav file. 
That is, if there are 500 sentences you wish to use from a particular corpus, 
there should be 500 .wav files in the audio directory. 
- Audio files should be named using integers. Example: `1.wav, 2.wav, 3.wav`.

### Sentence List

-   A single list of sentences must be provided in .csv format.
-   The sentence list should contain 3 columns
    1.  **sentence**: each sentence in its own row
    2.  **list_num**: the list each sentence belongs to
    3.  **sentence_num**: integer identifiers, starting at 1.<br>
    NOTE: *sentence_num values must correspond to the audio file names!*
-   Any key words must be CAPITALIZED. The Speech Task Controller identifies key words based on capitalization.

<!-- ![Sentence List Format image](./assets/images/sentence_list.png "Sentence List Format")
<img src="./assets/images/sentence_list.png" alt="Sentence List image" width="600"/> -->
<img src="sentence_list.png" alt="Sentence List image" width="600"/>
<br>
<br>

---

## Channel Routing and Audio Device Selection
The Speech Task Controller has audio routing capability thanks to the *sounddevice* Python library. Navigate to **Tools-->Audio Settings** to open the Audio Settings window to assign an audio channel and device (see image below). 

<!-- <img src="./assets/images/audio_settings_window.png" alt="Audio Settings Window image" width="600"/> -->
<img src="audio_settings_window.png" alt="Audio Settings Window image" width="600"/>

### Choose a Speaker
The Speech Task Controller is able to route a single channel of audio to a 
specified speaker. Simply type the speaker number in the "Output Speaker" 
text entry box.<br>
NOTE: The speaker number refers to the channel assigned to a speaker by the soundcard. Check the speaker routing to identify its number.

### Choose an Audio Device
The Audio Settings window will display a list of available audio devices in 
tabular format.

1. Use the "name" column to find the desired audio device (often 
the Hammerfall ASIO device in the clinical research labs). 
2. Ensure that the number of channels out in the "chans_out" column is not 0, 
and is sufficient for the desired number of audio channels/speakers. For example, to present audio from speaker 5, there must be at least 5 channels in the "chans_out" column.
3. After you have identified the appropriate audio device, enter its ID number 
from the "device_id" column into the "Audio Device ID" text entry box. 
4. Finally, click the SUBMIT button to save your selections. 
<br>
<br>

---

## Calibration
Before actual use in an experiment, the Speech Task Controller must be calibrated using a sound level meter (SLM). Use the menu to navigate to **Tools-->Calibration** to open the calibration window (see image below).

<!-- <img src="./assets/images/calibration_window.png" alt="Calibration Window image" width="600"/> -->
<img src="calibration_window.png" alt="Calibration Window image" width="600"/>

### Choose Calibration Stimulus
There are two options when calibrating.

1. The Speech Task Controller contains its own white noise stimulus for general calibration. Select the "White Noise" button to use this stimulus.
2. The "Custom File" button allows for an existing calibration file to be loaded. For example, to present IEEE sentences, load in the IEEE calibration file. 

### Play Calibration Stimulus
Clicking the PLAY button will present the calibration stimulus. You can set the level of the calibration stimulus using the "Raw Level (dB FS)" text entry box. A level of -30 dB FS is relatively safe, and is the default value. Making the Raw Level more negative will decrease the presentation level. Making the Raw Level more positive will increase the presentation level. It is not recommended to make this level more positive to avoid damaging the speakers. 

### Sound Level Meter
After you have loaded a calibration file and set up the SLM, press the PLAY button (Note: Make sure you have the SLM set to the proper speed and weighting [e.g., slow, dBA]). Enter the value from the SLM into the "SLM Reading (dB)" text entry box. Click the SUBMIT button to save the SLM value. 
<br>
<br>

---

## Fixed and Adaptive Presentation Levels
The Speech Task Controller can present audio at a fixed level, or can change 
the level adaptively. For a fixed presentation level, simply enter a value 
of 0 in each text entry box labeled **Step (dB)** on the main screen (see red 
rectangle in the image below). 

To change the level adaptively, enter non-zero values in the text entry boxes. The value given for the RIGHT button will *decrease* the level by that amount. The value given for the WRONG button will *increase* the level by that amount.<br>
Note: Step sizes are in decibels.

<!-- <img src="./assets/images/step_size.png" alt="Step Size image" width="600"/> -->
<img src="step_size.png" alt="Step Size image" width="600"/>
<br>
<br>

---

## Scoring
Sentences will be presented one-by-one from the list(s) entered in the Session window. The sentence text will be displayed in the "Sentence" section of the main screen. Check boxes will appear beneath each key word in the sentence. Click the check box if the participant correctly identified the word, otherwise leave the checkbox blank.

<!-- <img src="./assets/images/scoring.png" alt="Scoring image" width="600"/> -->
<img src="scoring.png" alt="Scoring image" width="600"/>

After selecting the appropriate check boxes, click either the RIGHT or WRONG button. You are free to click whichever button you wish without defining any special scoring criteria. A running count of each time the RIGHT and WRONG buttons is pressed is kept and recorded for scoring. This record is displayed as the percent correct in a message box once the task has finished, labeled as **Percent Correct (Custom)**.

In addition to scoring based on the number of right/wrong responses, the Speech Task Controller also tracks the percent correct based on the overall number of key words. This score is also provided in the message box at the end of the task, labeled **Percent Correct (Word)**.

Finally, the mean level is also displayed at the end of the task in the message box, labeled as **Mean Level**. 

<!-- <img src="./assets/images/summary.png" alt="Summary image" width="300"/> -->
<img src="summary.png" alt="Summary image" width="300"/>
<br>
<br>

---

## Data Output
Each time you click the RIGHT or WRONG button, session data are written as a new line to the data .csv file. This file serves as a record of the session and can be used to calculate scores for later analysis. The file appears in the same directory as the Speech Task Controller app, with a naming convention of: `year_month_day_time_condition_subject.csv`. This ensures previous records are not overridden, even if you need to repeat the same condition. 

The data .csv file stores the following information on each trial: 

- Subject: taken from the Session window
- Condition: taken from the Session window
- List Number: taken from the Session window
- Presentation Level: the starting level, taken from the Session window
- raw_lvl: hard-coded starting level in dB FS
- slm_cal_val: the SLM value entered in the Calibration window
- slm_offset: calculated as `SLM Calibration Value - Raw Level`
- new_db_lvl: calculated on each trial using values in the "Step (dB)" text entry boxes on the main screen
- new_raw_lvl: calculated as `new_db_lvl - slm_offset`
- Words Correct: a space-separated list of the words marked correct
- Num Words Correct: the number of words marked correct
- Words Incorrect: a space-separated list of the words marked incorrect
- Outcome: a `1` or `0` based on whether the RIGHT or WRONG button was clicked, respectively
- Trial: a counter starting at 1 and increasing with each presentation
<br>
<br>

---

## Rebuilding from Source
```
pyinstaller --noconfirm --onefile --windowed --add-data "C:/Users/MooTra/Code/Python/speech_task_gui/assets/cal_stim.wav;." --add-data "C:/Users/MooTra/Code/Python/speech_task_gui/assets/README;README/"  "C:/Users/MooTra/Code/Python/speech_task_gui/controller.py"
```
<br>
<br>

---

## Contact
Please use the contact information below to submit bug reports, feature requests and any other feedback. Thank you for using the Speech Task Controller!

- Travis M. Moore: travis_moore@starkey.com
