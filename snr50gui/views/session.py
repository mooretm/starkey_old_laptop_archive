""" Session parameters dialog
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


#########
# BEGIN #
#########
class SessionDialog(tk.Toplevel):
    """ Dialog for setting session parameters
    """
    def __init__(self, parent, sessionpars, sessionmodel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars
        self.sessionmodel = sessionmodel

        # Window setup
        self.withdraw()
        self.title("Session")
        self.grab_set()

        # Shared display settings
        options = {'padx':5, 'pady':5}

        #################
        # Create frames #
        #################
        # Session info frame
        frm_session = ttk.Labelframe(self, text='Session Information')
        frm_session.grid(column=0, row=5, padx=10, pady=10, sticky='nsew')

        # Audio file browser frame
        frm_audiopath = ttk.Labelframe(self, text="Audio File Directory")
        frm_audiopath.grid(column=0, row=10, padx=10, pady=10, ipadx=5, ipady=5)

        # Sentence file browser frame
        frm_sentencepath = ttk.Labelframe(self, text='Sentence File Directory')
        frm_sentencepath.grid(column=0, row=15, padx=10, pady=10, ipadx=5, ipady=5)


        #######################
        # Create view widgets #
        #######################
        # Subject
        ttk.Label(frm_session, text="Subject:"
            ).grid(row=2, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['Subject']
            ).grid(row=2, column=1, sticky='w')
        
        # Condition
        ttk.Label(frm_session, text="Condition:"
            ).grid(row=3, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['Condition']
            ).grid(row=3, column=1, sticky='w')

        # List
        ttk.Label(frm_session, text="List(s):"
            ).grid(row=4, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['List Number']
            ).grid(row=4, column=1, sticky='w')

        # Level
        ttk.Label(frm_session, text="Level (dB):"
            ).grid(row=5, column=0, sticky='e', **options)
        ttk.Entry(frm_session, width=20, 
            textvariable=self.sessionpars['Presentation Level']
            ).grid(row=5, column=1, sticky='w')

        # Audio directory
        ttk.Label(frm_audiopath, text="Path:"
            ).grid(row=6, column=0, sticky='e', **options)
        ttk.Label(frm_audiopath, textvariable=self.sessionpars['Audio Files Path'], 
            borderwidth=2, relief="solid", width=60
            ).grid(row=6, column=1, sticky='w')
        ttk.Button(frm_audiopath, text="Browse", command=self._get_audio_directory
            ).grid(row=7, column=1, sticky='w', pady=(0, 10))

        # Sentence directory
        ttk.Label(frm_sentencepath, text="Path:"
            ).grid(row=9, column=0, sticky='e', **options)
        ttk.Label(frm_sentencepath, textvariable=self.sessionpars['Sentence File Path'], 
            borderwidth=2, relief="solid", width=60
            ).grid(row=9, column=1, sticky='w')
        ttk.Button(frm_sentencepath, text="Browse", command=self._get_sentence_directory
            ).grid(row=10, column=1, sticky='w', pady=(0, 5))

        # Submit button
        btn_submit = ttk.Button(self, text="Submit", command=self._on_submit)
        btn_submit.grid(column=0, columnspan=2, row=20, pady=(0,10))

        # Center the session dialog window
        self.center_window()


    #############
    # Functions #
    #############
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


    def _get_audio_directory(self):
        """ Ask user to specify audio files directory and 
            store it in sessionpars
        """
        self.sessionpars['Audio Files Path'].set(
            filedialog.askdirectory(title="Audio File Directory"))


    def _get_sentence_directory(self):
        """ Ask user to specify sentence file and store
            it in sessionpars
        """
        self.sessionpars['Sentence File Path'].set(
            filedialog.askdirectory(title="Sentence File Directory"))


    def _on_submit(self):
        """ Set new_db_lvl to specified presentation level.
            Send event to controller to write sessionpars data to file
        """
        self.sessionpars['new_db_lvl'].set(self.sessionpars['Presentation Level'].get())
        print("\nViews_Session_140: Sending save event to controller...")
        self.parent.event_generate('<<SessionSubmit>>')
        self.destroy()
