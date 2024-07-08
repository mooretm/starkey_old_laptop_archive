# **Change Log**

---

## v2.1.1

Date: Dec 02, 2022

### Minor Bug Fixes
1. Fixed bug where first level presented (in dB FS) was not calculated from the new presentation level specified in the sessionpars view. The displayed level (new_db_lvl) was updated, but the dB FS level was not calculated when the START button was clicked (only when the NEXT button was clicked). 

---

## v2.1.0

Date: 2 Nov, 2022

### Major Features
1. New help file system. The README file is now a markdown file. A new "help" menu option will now convert the README.md file into an html file. The README.html file is then displayed in the default browser.

### Minor Features
1. A message box now alerts the user when data are not successfully saved to file on each occurrence. 
<br>
<br>

---

## v2.0.1  

Date: 31 Oct, 2022 

### Major Bug Fixes
1. Last used level was reloaded as starting level when restarting app without using session dialog (which assigns new_db_lvl according to entered level).

### Minor Features
1. Directory browser dialog title now states the type of path it wants (e.g., "Audio File Directory").
2. Removed messagebox on startup without a saved parameters file. Instead, the sentence label provides instructions.
3. No longer have to restart when stimulus paths and/or audio id weren't given before clicking the START button.
<br>
<br>

---

## v2.0.0

Date: 28 Oct, 2022

### Major Features
1. Complete refactoring of code to OOP. 
2. New logic for handling word display and scoring. 
3. More flexible calibration and session dialogs. 
<br>
<br>

---

## v1.1.1

Date: 08 Jun, 2022

### Major Bug Fixes
1. Corrected issue where presentation level changes lagged behind the user-indicated level while in adaptive mode. 
<br>
<br>

---

## v1.1.0

Date: 07 Jun, 2022

### Major Features
1. Added "audiometer-like" controls that allow for increasing/decreasing level on a per trial basis. Essentially provides manual adaptive functionality. 
<br>
<br>

---

## v1.0.0

Date: 06 Jun, 2022

### Initial Release
1. A GUI-based speech presentation controller with the ability to run the task at a specified presentation level. 
<br>
<br>
