""" Audio dialog for Speech Task Controller

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Import data science packages
import numpy as np
import pandas as pd
from pandastable import Table

# Import audio packages
import sounddevice as sd


#########
# BEGIN #
#########
class AudioDialog(tk.Toplevel):
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, *kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        # Set up window
        self.withdraw()
        self.focus()
        self.title("Audio")
        #self.grab_set() # Disable root window (toplevel as modal window)

        options = {'padx':10, 'pady':10}
        options_small = {'padx':2.5, 'pady':2.5}

        lblfrm_settings = ttk.Labelframe(self, text='Device and Routing')
        lblfrm_settings.grid(column=0, row=0, sticky='nsew', **options)

        frmTable = ttk.Frame(self)
        frmTable.grid(column=0, row=15, **options)

        # Speaker number
        lbl_speaker = ttk.Label(lblfrm_settings, text='Output Speaker:').grid(
            column=5, row=5, sticky='e', **options_small)
        ent_speaker = ttk.Entry(lblfrm_settings, 
            textvariable=self.sessionpars['Speaker Number'], width=6)
        ent_speaker.grid(column=10, row=5, sticky='w', **options_small)

        # Audio device ID
        lbl_device = ttk.Label(lblfrm_settings, text="Audio Device ID:").grid(
            column= 5, row=10, sticky='e', **options_small)
        ent_deviceID = ttk.Entry(lblfrm_settings, 
            textvariable=self.sessionpars['Audio Device ID'], width=6)
        ent_deviceID.grid(column=10, row=10, sticky='w', **options_small)

        # Submit button
        btnDeviceID = ttk.Button(self, text="Submit", 
            command=self._on_submit)
        btnDeviceID.grid(column=0, columnspan=10, row=10, **options_small)

        # Get and display list of audio devices
        deviceList = sd.query_devices()
        names = [deviceList[x]['name'] for x in np.arange(0,len(deviceList))]
        chans_out =  [deviceList[x]['max_output_channels'] for x in np.arange(0,len(deviceList))]
        ids = np.arange(0,len(deviceList))
        df = pd.DataFrame({
            "device_id": ids, 
            "name": names, 
            "chans_out": chans_out})
        pt = Table(frmTable, dataframe=df, showtoolbar=True, showstatusbar=True)
        table = pt = Table(frmTable, dataframe=df)
        table.grid(column=0, row=0)
        pt.show()

        # Center dialog window
        self.center_window()


    def center_window(self):
        """ Center window based on new size
        """
        self.update_idletasks()
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


    def _on_submit(self):
        """ Send event to controller to save entered audio dialog values.
            Close dialog.
        """
        print("\nView_Audio_99: Sending save audio config event...")
        self.parent.event_generate('<<AudioDialogSubmit>>')
        self.destroy()
