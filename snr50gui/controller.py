""" Speech Task Controller is a flexible program for presenting speech
    corpi (e.g., IEEE) and providing word-level and custom scoring ability.

    Simply provide a master list of sentences (with the proper formatting)
    and an audio file directory (with properly-named files) for a given 
    speech corpus. Score using check boxes. Trial data are output as a 
    .csv file. 

    Written by: Travis M. Moore
    Created: 23 Jun, 2022
    Last edited: 2 Nov, 2022
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk

# Import system packages
import os
import sys
from tkinter import messagebox

# Import data science packages
import numpy as np

# Import misc packages
import webbrowser
import markdown

# Import custom modules
# Menu imports
from menus import mainmenu as menu_main
# Model imports
from models import sessionmodel as m_sesspars
from models import audiomodel as m_audio
from models import listmodel as m_list
from models import csvmodel as m_csv
from models import scoremodel as m_score
# View imports
from views import main as v_main
from views import session as v_sess
from views import audio as v_aud
from views import calibration as v_cal


#########
# BEGIN #
#########
class Application(tk.Tk):
    """ Application root window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Root window settings
        self.withdraw() 
        self.title("Speech Task Controller")
        self.resizable(False, False)
        self.grab_set()

        # Dictionary to track values per trial
        # Used to calculate summary stats
        self.tracker = {
            'Level': [], # Adjusted presentation levels
            'PC Word': [], # Number of words correct
            'PC Custom': [], # Outcomes (right/wrong; 1/0)
        }


        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Load session parameters
        self.sessionpars_model = m_sesspars.SessionParsModel()
        self._load_sessionpars()

        # Create CSV writer model
        self.csvmodel = m_csv.CSVModel(self.sessionpars)

        # Create and load list model
        self.listmodel = m_list.StimulusList(self.sessionpars)
        try:
            self.listmodel.load()
        except FileNotFoundError:
            pass

        # Create score model
        self.scoremodel = m_score.ScoreModel()

        # Create main view
        self.main_frame = v_main.MainFrame(self, self.scoremodel, 
            self.sessionpars, self.listmodel)
        self.main_frame.grid()

        # Create menus
        self.menu = menu_main.MainMenu(self)
        self.config(menu=self.menu)

        # Create callback dictionary
        event_callbacks = {
            # File menu
            '<<FileSession>>': lambda _: self._show_session_dialog(),
            '<<FileQuit>>': lambda _: self._quit(),

            # Tools menu
            '<<ToolsAudioSettings>>': lambda _: self._show_audio_dialog(),
            '<<ToolsCalibration>>': lambda _: self._show_calibration_dialog(),

            # Help menu
            '<<Help>>': lambda _: self._show_help(),

            # Session dialog commands
            '<<SessionSubmit>>': lambda _: self._save_sessionpars(),

            # Calibration dialog commands
            '<<PlayCalStim>>': lambda _: self._play_calibration(),
            '<<CalibrationSubmit>>': lambda _: self._calc_level(),

            # Audio dialog commands
            '<<AudioDialogSubmit>>': lambda _: self._save_sessionpars(),

            # Mainframe commands
            '<<SubmitResponse>>': lambda _: self._on_main_submit(),
            '<<MainDone>>': lambda _: self._main_done(),
            '<<GetLevel>>': lambda _: self._calc_level(),
            '<<MainStart>>': lambda _: self._disable_mnu()
        }

        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Center main window
        self.center_window()


    #####################
    # General Functions #
    #####################
    def center_window(self):
        """ Center the root window 
        """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def resource_path(self, relative_path):
        """ Get the absolute path to compiled resources
        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def _quit(self):
        """ Exit the application
        """
        self.destroy()


    #######################
    # Help menu functions #
    #######################
    def _show_help(self):
        """ Create html help file and display in default browser
        """
        print('Looking for help file in compiled version temp location...')
        help_file = self.resource_path('README\\README.html')
        file_exists = os.access(help_file, os.F_OK)
        if not file_exists:
            print('Not found!\nChecking for help file in ' +
                'local script version location')
            # Read markdown file and convert to html
            with open('README.md', 'r') as f:
                text = f.read()
                html = markdown.markdown(text)

            # Create html file for display
            with open('.\\assets\\README\\README.html', 'w') as f:
                f.write(html)

            # Open README in default web browser
            webbrowser.open('.\\assets\\README\\README.html')
        else:
            help_file = self.resource_path('README\\README.html')
            webbrowser.open(help_file)


    ########################
    # Main Frame Functions #
    ########################
    def _disable_mnu(self):
        """ Disable FILE>Session... menu once task has started
        """
        self.menu.file_menu.entryconfig('Session...', state='disabled')


    def _on_main_submit(self):
        """ Display, track and write response data to file
        """
        # Provide feedback to the console
        print(f"\nTrial {self.scoremodel.fields['Trial']}:")
        print(f"Level: {self.sessionpars['new_db_lvl'].get()} (dB)")
        print(f"Correct: {self.scoremodel.fields['Words Correct']}")
        print(f"Incorrect: {self.scoremodel.fields['Words Incorrect']}")
        print(f"Outcome code: {self.scoremodel.fields['Outcome']}\n")

        # Track values for summary at end
        self.tracker['Level'].append(self.sessionpars['new_db_lvl'].get())
        self.tracker['PC Word'].append(self.scoremodel.fields['Num Words Correct'])
        self.tracker['PC Custom'].append(self.scoremodel.fields['Outcome'])

        # Call save function
        self._main_save()
        
        
    def _main_save(self):
        """ Format values and send to csv model
        """
        # Get tk variable values from sessionpars
        data = dict()
        for key in self.sessionpars:
            data[key] = self.sessionpars[key].get()

        # Only write specific sessionpars to file
        drop_list = ['Speaker Number', 'Audio Files Path', 
            'Sentence File Path', 'Audio Device ID', 'Calibration File']
        [data.pop(e) for e in drop_list]

        # Combine sessionpars dict and scoremodel dict for writing
        data.update(self.scoremodel.fields)

        # Save data
        print('App_206: Calling save record function...')
        try:
            self.csvmodel.save_record(data)
        except PermissionError():
            messagebox.showerror(title="Save Failed!",
                message="Could not save data to file!",
                detail="Please make sure the file isn't open and that you " +
                    "have write permission."
            )


    def _main_done(self):
        """ Calculate and display summary stats. Close app.
        """
        # Calculate some descriptive statistics for display
        num_possible_words = len(self.scoremodel.fields['Words Correct'].split()) + len(self.scoremodel.fields['Words Incorrect'].split())
        #print(f'Words per sentence: {num_possible_words}')
        #print(f"Total words correct: {np.sum(self.tracker['PC Word'])}")
        mean_lvl = round(np.mean(self.tracker['Level']), 2)
        print(f"Tracker list of levels: {self.tracker['Level']}")
        pc_word = round((np.sum(self.tracker['PC Word']) / (len(self.tracker['PC Custom'] * num_possible_words))) * 100, 2)
        pc_custom = round((np.sum(self.tracker['PC Custom']) / len(self.tracker['PC Custom'])) * 100, 2)

        # Summary stats messagebox
        messagebox.showinfo(
            title='Done!',
            message='Summary',
            detail=f'Mean Level: {mean_lvl} dB\n' +
                f'Percent Correct (Word): {pc_word}%\n' +
                f'Percent Correct (Custom): {pc_custom}%'
        )

        # Close app when done
        self.quit()


    ############################
    # Session Dialog Functions #
    ############################
    def _show_session_dialog(self):
        """ Show session parameter dialog
        """
        print("\nApp_240: Calling session dialog...")
        v_sess.SessionDialog(self, self.sessionpars, self.sessionpars_model)


    def _load_sessionpars(self):
        """ Load parameters into self.sessionpars dict 
        """
        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create runtime dict from session model fields
        self.sessionpars = dict()
        for key, data in self.sessionpars_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.sessionpars[key] = vartype(value=data['value'])
        print("\nApp_259: Loaded sessionpars model fields into " +
            "running sessionpars dict")


    def _save_sessionpars(self, *_):
        """ Save current runtime parameters to file.
            Update session info labels with new parameters.
        """
        print("\nApp_266: Calling sessionpar model set and save funcs...")
        for key, variable in self.sessionpars.items():
            self.sessionpars_model.set(key, variable.get())
            self.sessionpars_model.save()

        # Update session info labels
        self.listmodel.load()
        self.main_frame._load_listmodel()
        self.main_frame._update_labels()


    ##########################
    # Audio Dialog Functions #
    ##########################
    def _show_audio_dialog(self):
        """ Show audio settings dialog
        """
        print("\nApp_288: Calling audio dialog...")
        v_aud.AudioDialog(self, self.sessionpars)


    ################################
    # Calibration Dialog Functions #
    ################################
    def _show_calibration_dialog(self):
        """ Show calibration dialog
        """
        print("\nApp_296: Calling calibration dialog...")
        v_cal.CalibrationDialog(self, self.sessionpars)


    def _calc_level(self):
        """ Calculate and save adjusted presentation level
        """
        # Calculate SLM offset
        print("\nApp_304: Calculating new presentation level...")
        self.sessionpars['slm_offset'].set(self.sessionpars['slm_cal_value'].get() - self.sessionpars['raw_lvl'].get())
        # Calculate new raw level
        self.sessionpars['new_raw_lvl'].set(
            self.sessionpars['new_db_lvl'].get() - self.sessionpars['slm_offset'].get())
        print(f"New raw level: {self.sessionpars['new_raw_lvl'].get()}")
        # Calculate new corresponding dB level
        self.sessionpars['new_db_lvl'].set(
            self.sessionpars['slm_offset'].get() + self.sessionpars['new_raw_lvl'].get())
        print(f"New level (dB): {self.sessionpars['new_db_lvl'].get()}")

        # Save SLM offset and updated level
        self._save_sessionpars()


    def _play_calibration(self):
        """ Load and present calibration stimulus
        """
        # Check for default calibration stimulus request
        if self.sessionpars['Calibration File'].get() == 'cal_stim.wav':
            # Create calibration audio object
            try:
                # If running from compiled, look in compiled temporary location
                print("Looking for cal file in temp location: compiled version")
                cal_file = self.resource_path('cal_stim.wav')
                cal_stim = m_audio.Audio(cal_file, self.sessionpars['raw_lvl'].get())
            except FileNotFoundError:
                # If running from command line, look in assets folder
                print("Looking for cal file in assets folder: script version")
                cal_file = '.\\assets\\cal_stim.wav'
                try:
                    cal_stim = m_audio.Audio(cal_file, self.sessionpars['raw_lvl'].get())
                except FileNotFoundError:
                    print("Default calibration file not found!")
                    messagebox.showerror(title="File Not Found",
                        message="File not found! Please try again.")
                    return
        else: # Custom calibration file was provided
            print("App_336: Looking for provided custom calibration file...")
            try:
                cal_stim = m_audio.Audio(self.sessionpars['Calibration File'].get(), 
                    self.sessionpars['raw_lvl'].get())
                print("Custom calibration file found!")
            except FileNotFoundError:
                messagebox.showerror(title="File Not Found",
                    message="File not found! Please try again.")
                return

        # Present calibration stimulus
        print("App_341: Attempting to play calibration file...")
        cal_stim.play(device_id=self.sessionpars['Audio Device ID'].get(), 
            channels=self.sessionpars['Speaker Number'].get())


if __name__ == "__main__":
    app = Application()
    app.mainloop()
