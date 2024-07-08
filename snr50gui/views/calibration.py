""" Calibration dialog class

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Import system packages
import os


#########
# BEGIN #
#########
class CalibrationDialog(tk.Toplevel):
    """ Dialog for calibration
    """
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        # Window setup
        self.withdraw()
        self.focus()
        self.title("Calibration")
        self.grab_set()

        # Create display
        self._build()

        # Enabled last used calibration method
        self._set_cal_val()

        # Center calibration window dialog
        self.center_window()


    def _build(self):
        """ Create form widgets 
        """
        # Options for label frames
        options = {'padx':10, 'pady':10}
        options_small = {'padx':2.5, 'pady':2.5}


        #################
        # Create frames #
        #################
        # Choose calibration stimulus controls
        lf_load = ttk.LabelFrame(self, text="Choose Calibration Stimulus")
        lf_load.grid(column=5, columnspan=10, row=5, **options)

        # Calibration presentation controls
        lf_present = ttk.Labelframe(self, text='Play Calibration Stimulus')
        lf_present.grid(column=5, row=10, **options, sticky='w')

        # SLM reading controls
        lf_record = ttk.Labelframe(self, text='Sound Level Meter')
        lf_record.grid(column=10, row=10, **options, sticky='e')


        ##################################
        # Calibration selection controls #
        ##################################
        # Define variables for file path and radio button value
        self.cal_path = tk.StringVar(value='Please choose a calibration stimulus file')
        self.cal_var = tk.StringVar()
        
        # Default white noise stimulus radio button
        rad_wgn = ttk.Radiobutton(lf_load, text="White Noise", takefocus=0,
            variable=self.cal_var, value='wgn', command=self._cal_type)
        rad_wgn.grid(column=5, row=0, columnspan=10, sticky='w', 
            **options_small)

        # Custom calibration stimulus radio button
        rad_custom = ttk.Radiobutton(lf_load, text="Custom File", takefocus=0,
            variable=self.cal_var, value='custom', command=self._cal_type)
        rad_custom.grid(column=5, row=1, columnspan=10, sticky='w', 
            **options_small)

        # Get calibration file path
        self.lbl_calfile1 = ttk.Label(lf_load, text='File:', state='disabled')
        self.lbl_calfile1.grid(column=5, row=5, sticky='w', **options_small)
        self.lbl_calfile2 = ttk.Label(lf_load, textvariable=self.cal_path, borderwidth=2, 
            relief="solid", width=60, state='disabled')
        self.lbl_calfile2.grid(column=10, row=5, sticky='w', **options_small)

        # Browse button
        self.btn_browse = ttk.Button(lf_load, text="Browse", state='disabled',
            takefocus=0, command=self._load_cal)
        self.btn_browse.grid(column=10, row=10, sticky='w', 
            **options_small)


        #####################################
        # Calibration presentation controls #
        #####################################
        # Raw level entry
        ttk.Label(lf_present, text="Raw Level (dB FS):").grid(
            column=5, row=5, sticky='e', **options_small)
        ent_slm = ttk.Entry(lf_present, textvariable=self.sessionpars['raw_lvl'],
            width=6)
        ent_slm.grid(column=10, row=5, sticky='w', **options_small)
 
        # Play calibration stimulus
        ttk.Label(lf_present, text="Calibration Stimulus:").grid(
            column=5, row=10, sticky='e', **options_small)
        btn_play = ttk.Button(lf_present, text="Play", command=self._on_play)
        btn_play.grid(column=10, row=10, sticky='w', **options_small)
        btn_play.focus()


        ########################
        # SLM reading controls #
        ########################
        # SLM reading entry box
        ttk.Label(lf_record, text="SLM Reading (dB):").grid(
            column=5, row=15, sticky='e', **options_small)
        self.ent_slm = ttk.Entry(lf_record, textvariable=self.sessionpars['slm_cal_value'],
            width=6, state='disabled')
        self.ent_slm.grid(column=10, row=15, sticky='w', **options_small)

        # Submit button
        self.btn_submit = ttk.Button(lf_record, text="Submit", 
            command=self._on_submit, state='disabled')
        self.btn_submit.grid(column=5, columnspan=10, row=20, **options_small)


    #############
    # FUNCTIONS #
    #############
    def _set_cal_val(self):
        """ Enable calibration controls for last method used 
            (i.e., wgn or custom file)
        """
        if self.sessionpars['Calibration File'].get() == 'cal_stim.wav':
            self.cal_var.set('wgn')
            self._set_custom_cntrls_status('disabled')
        else:
            self.cal_var.set('custom')
            self.cal_path.set(os.path.basename(
                self.sessionpars['Calibration File'].get()))
            self._set_custom_cntrls_status('enabled')


    def center_window(self):
        """ Center window based on new size
        """
        self.update_idletasks()
        #root.attributes('-topmost',1)
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.deiconify()


    def _set_custom_cntrls_status(self, state):
        """ Enable or disable custom cal file controls
        """
        self.lbl_calfile1.config(state=state)
        self.lbl_calfile2.config(state=state)
        self.btn_browse.config(state=state)


    def _cal_type(self):
        """ Radio button functions for choosing cal type
        """
        # Custom calibration file
        if self.cal_var.get() == 'custom':
            # Enable file browsing controls
            self._set_custom_cntrls_status('enabled')

        # Default white noise
        elif self.cal_var.get() == 'wgn':
            # Assign default cal file
            self.sessionpars['Calibration File'].set('cal_stim.wav')
            # Update path text
            self.cal_path.set('Please choose a calibration stimulus file')
            # Disable custom file controls
            self._set_custom_cntrls_status('disabled')

        print(f"Cal file from cal dialog: {self.sessionpars['Calibration File'].get()}")


    def _load_cal(self):
        """ File dialog for custom calibration file
        """
        self.sessionpars['Calibration File'].set(filedialog.askopenfilename())
        self.cal_path.set(
            os.path.basename(self.sessionpars['Calibration File'].get()))


    def _on_play(self):
        """ Send play event to controller and enable SLM value 
            entry controls
        """
        print(f"Using calibration file: " +
            f"{self.sessionpars['Calibration File'].get()}")
        self.parent.event_generate('<<PlayCalStim>>')
        self.btn_submit.config(state='enabled')
        self.ent_slm.config(state='enabled')


    def _on_submit(self):
        """ Send save SLM value event to controller
        """
        print("\nViews_Cal_210: Sending save calibration event...")
        self.parent.event_generate('<<CalibrationSubmit>>')
        self.destroy()
