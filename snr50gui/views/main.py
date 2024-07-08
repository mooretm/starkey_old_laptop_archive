""" Main view for speech task controller.

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Import data science packages
import numpy as np

# Import text packages
import string # for creating alphabet list

# Import custom modules
from models import audiomodel as a


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, scoremodel, sessionpars, listmodel, 
    *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Initialize
        self.scoremodel = scoremodel
        self.sessionpars = sessionpars
        self.listmodel = listmodel
        self.counter = 0
        self.outcome = None

        # Set widget display options
        self.myFont = tk.font.nametofont('TkDefaultFont').configure(size=10)
        options = {'padx':10, 'pady':10}

        style = ttk.Style()
        style.configure('Start.TButton', 
            font=('TkDefaultFont', 10, 'bold'), 
            foreground='green',
            background='black')


        #################
        # Create frames #
        #################
        # Main content frame
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, sticky='nsew')

        # Words and checkbuttons frame
        self.frm_sentence = ttk.LabelFrame(frm_main, text='Sentence:', 
            padding=8, width=500, height=80)
        self.frm_sentence.grid(column=5, columnspan=15, row=5, sticky='nsew', 
            **options)
        self.frm_sentence.grid_propagate(0)

        # Vertical separator for session info
        sep = ttk.Separator(frm_main, orient='vertical')
        sep.grid(column=20, row=5, rowspan=50, sticky='ns')

        # Session info frame
        self.frm_params = ttk.LabelFrame(frm_main, text="Session Info")
        self.frm_params.grid(column=25, row=5, rowspan=15, sticky='n',
            **options, ipadx=5, ipady=5)


        #######################
        # Session info labels #
        #######################
        # Create session info label textvariables for updating
        self.subject_var = tk.StringVar(value="Subject:")
        self.condition_var = tk.StringVar(value="Condition:")
        self.level_var = tk.StringVar(value="Level:")
        self.list_var = tk.StringVar(value="List:")
        self.speaker_var = tk.StringVar(value="Speaker:")
        self.trial_var = tk.StringVar(value="Trial:")

        # Plot session info labels
        # Subject
        ttk.Label(self.frm_params, 
            textvariable=self.subject_var).grid(sticky='w')
        # Condition
        ttk.Label(self.frm_params, 
            textvariable=self.condition_var).grid(sticky='w')
        # Speaker number
        ttk.Label(self.frm_params, 
           textvariable=self.speaker_var).grid(sticky='w')
         # List number(s)  
        ttk.Label(self.frm_params, 
            textvariable=self.list_var).grid(sticky='w')
        # Level
        ttk.Label(self.frm_params, 
           textvariable=self.level_var).grid(sticky='w')
        # Trial number
        ttk.Label(self.frm_params, 
            textvariable=self.trial_var).grid(sticky='w')


        #################
        # User controls #
        #################
        # "Start" button
        self.btn_start = ttk.Button(frm_main, text='Start',
            command=self._on_start, style='Start.TButton')
        self.btn_start.grid(column=7, row=15, rowspan=6, 
            sticky='nsew', pady=(0,10))

        # "Right" button
        self.btn_right = ttk.Button(frm_main, text='Right', state='disabled', 
            command=self._on_right)
        self.btn_right.grid(column=5, row=15, pady=(0,10))

        # "Wrong" button
        self.btn_wrong = ttk.Button(frm_main, text='Wrong', state='disabled',
            command=self._on_wrong)
        self.btn_wrong.grid(column=5, row=20, pady=(0,10))

        # "Right" step size entry
        #self.right_var = tk.DoubleVar()
        self.right_var = tk.StringVar()
        ent_right = ttk.Entry(frm_main, textvariable=self.right_var, width=5)
        ent_right.grid(column=6, row=15, sticky='w', pady=(0,10))

        # "Wrong" step size entry
        #self.wrong_var = tk.DoubleVar()
        self.wrong_var = tk.StringVar()
        ent_wrong = ttk.Entry(frm_main, textvariable=self.wrong_var, width=5)
        ent_wrong.grid(column=6, row=20, sticky='w', pady=(0,10))

        # Level step size label
        ttk.Label(frm_main, text='Step (dB)').grid(column=6, row=10, 
            sticky='w')


        ##########################
        # Words and checkbuttons #
        ##########################
        # Create list of labels for displaying words
        self.text_vars = list(string.ascii_lowercase)
        self.word_labels = []
        for idx, letter in enumerate(self.text_vars):
            self.text_vars[idx] = tk.StringVar(value='')
            self.lbl_word = ttk.Label(self.frm_sentence, 
                textvariable=self.text_vars[idx], font=self.myFont)
            self.lbl_word.grid(column=idx, row=0)
            self.word_labels.append(self.lbl_word)

        # Set temporary instructions text in the first word label
        self.text_vars[0].set("Click the START button to begin.")

        # Create list of checkbuttons for displaying beneath key words
        self.chk_vars = list(string.ascii_uppercase)
        self.word_chks = []
        for idx in range(0, len(self.text_vars)):
            self.chk_vars[idx] = tk.IntVar(value=0)
            self.chk_word = ttk.Checkbutton(self.frm_sentence, 
                text='', takefocus=0, variable=self.chk_vars[idx])
            self.word_chks.append(self.chk_word)


        #####################
        # Check for stimuli #
        #####################
        # Load stimuli from listmodel
        self._load_listmodel()


    #####################
    # General functions #
    #####################
    def _load_listmodel(self):
        """ Load in current stimulus lists from listmodel
        """
        try:
            self.audio_df = self.listmodel.audio_df
            self.sentence_df = self.listmodel.sentence_df
            self.text_vars[0].set("Click the START button to begin.")
        except AttributeError:
            print("Views_Main_178: Problem loading stimuli!")
            #messagebox.showerror(title="Restart Required",
            #    message="Go to File -> Session to provide valid paths " + 
            #    "to stimuli\n " + "then close and restart the application.")
            # Provide instructions to give path and restart in sentence label
            self._reset()
            self.text_vars[0].set("Stimuli not found!\nGo to File-->Session to provide stimulus paths.")

            # Open session dialog for user
            self.event_generate('<<FileSession>>')


    def _update_labels(self, *_):
        """ Update session info labels
        """
        try:
            self.subject_var.set(f"Subject: {self.sessionpars['Subject'].get()}")
            self.condition_var.set(f"Condition: {self.sessionpars['Condition'].get()}")
            self.speaker_var.set(f"Speaker: {self.sessionpars['Speaker Number'].get()}")
            self.list_var.set(f"List(s): {self.sessionpars['List Number'].get()}")
            self.level_var.set(f"Level: {self.sessionpars['new_db_lvl'].get()}")
            self.trial_var.set(f"Trial: {self.counter+1} of {len(self.sentence_df)}")
        except AttributeError:
            print("Views_Main_189: Cannot calculate trials data: stimuli not yet loaded!")


    ####################
    # Button functions #
    ####################
    def _on_start(self):
        """ Display/present first trial
        """
        # Check for step size values
        if not self.right_var.get() or not self.wrong_var.get():
            messagebox.showerror(title="Invalid Step Size",
                message="Please enter right/wrong step sizes to continue!\n\n" +
                    "Note: Enter zeros for a fixed presentation level.")
            return

        # Calculate new dB FS level from current 
        # new_db_lvl value in sessionpars
        self._get_level()

        # Send event to controller to disable session menu
        # once task has started
        self.event_generate('<<MainStart>>')

        # Clean up buttons
        self.btn_start.grid_remove()
        self.btn_right.config(state='enabled')
        self.btn_wrong.config(state='enabled')

        # Reset trial counter to 0
        self.counter = 0

        # Load stimulus lists again
        # Required if no stimuli were available on init
        self._load_listmodel()

        # Load starting level based on value specified in session dialog.
        self.sessionpars['new_db_lvl'].set(
            self.sessionpars['Presentation Level'].get())

        # Update session info labels after loading listmodel
        self._update_labels()

        # Display first sentence and present first audio file
        self._display()
        self._play()


    def _on_wrong(self):
        """ Update outcome to incorrect. 
            Call remaining task functions. 
        """
        # Set response outcome to incorrect (0)
        # Based on "wrong" button click
        self.outcome = 0

        # Call series of task functions (same as _on_right)
        self._next()


    def _on_right(self):
        """ Update outcome to correct.
            Call remaining task functions. 
        """
        # Set response outcome to correct (1)
        # Based on "right" button click
        self.outcome = 1

        # Call series of task functions (same as _on_wrong)
        self._next()


    ###########################
    # Task process controller #
    ###########################
    def _next(self):
        """ Control the order of operations after right/wrong 
            buttons have assigned response outcome.
        """
        # Score responses
        self._score()
        # Reset word labels and checkbuttons
        self._reset()
        # Set new level based on right/wrong step size
        self._adjust_level()
        # Calculate raw value to achieve new level
        self._get_level()
        # Update trial counter
        self.counter += 1
        # Update trial label
        self.trial_var.set(f"Trial: {self.counter+1} of {len(self.sentence_df)}")
        # Start next trial: display new word labels and checkbuttons
        self._display()
        self._play()


    ###################
    # Audio functions #
    ###################
    def _adjust_level(self):
        """ Apply right/wrong step size to presentation level
            based on response outcome.
        """
        if self.outcome == 1:
            # Apply step size offset to presentation level
            self.sessionpars['new_db_lvl'].set(
                self.sessionpars['new_db_lvl'].get() - float(self.right_var.get())
            )
        elif self.outcome == 0:
            # Apply step size offset to presentation level
            self.sessionpars['new_db_lvl'].set(
                self.sessionpars['new_db_lvl'].get() + float(self.wrong_var.get())
            )
        else:
            messagebox.showerror(
                title="Uh oh!",
                message="Cannot calculate new level with invalid score!\n" + 
                    "Aborting!\n\nError: Views_Main_294"
            )
            self.quit()


    def _get_level(self):
        """ Send event to controller to calculate new 
            raw level for the updated presentation level.
        """
        self.event_generate('<<GetLevel>>')


    def _enable_btns(self):
        """ Set right/wrong button state to ENABLED
            Set right/wrong text to right/wrong
        """
        self.btn_right.config(state='enabled')
        self.btn_wrong.config(state='enabled')
        self.btn_right.config(text="Right")
        self.btn_wrong.config(text="Wrong")


    def _disable_btns(self, btntext):
        """ Set right/wrong button state to DISABLED
            Set right/wrong text to: Presenting
        """
        self.btn_right.config(state='disabled')
        self.btn_wrong.config(state='disabled')
        self.btn_right.config(text=btntext)
        self.btn_wrong.config(text=btntext)


    def _play(self):
        """ Load next audio file and present it.
        """
        try:
            # Create audio object
            print(f"Views_Main_363: Raw level sent to audio object: " +
                f"{self.sessionpars['new_raw_lvl'].get()}")
            audio = a.Audio(self.audio_df.iloc[self.counter]['path'], 
                self.sessionpars['new_raw_lvl'].get())

            # Disable right/wrong buttons to prevent multiple clicks
            self._disable_btns("Presenting")
            # Update tasks is required before playing audio
            # for _disable_btns to update the GUI
            self.update()

            # Present audio
            try:
                audio.play(
                    device_id=self.sessionpars['Audio Device ID'].get(),
                    channels=self.sessionpars['Speaker Number'].get()
                    )
            except ValueError:
                # Show error messagebox
                messagebox.showerror(title="Invalid Audio Device",
                    message="Please provide a valid audio device ID!")
                # Give instructions in sentence label
                self._reset()
                self.text_vars[0].set("Please restart the application " +
                    "to apply changes.")
                # Open audio device dialog for user
                self.event_generate('<<ToolsAudioSettings>>')
                # Disable right/wrong buttons
                self._disable_btns("Ready")
                # Restore START button
                self.btn_start.grid(column=7, row=15, rowspan=6, 
                    sticky='nsew', pady=(0,10))
                return

            # Re-enable buttons after audio has finished playing
            # NOTE: .after expects an integer duration in ms
            self.after((int(np.ceil(audio.dur)))*1000, self._enable_btns)
        except KeyError:
            messagebox.showerror(title="Cannot Find File",
                message="Requested audio file does not exist!")
            print("Views_Main_354: Audio file does not exist!")
            return


    ##################################
    # Display words and checkbuttons #
    ##################################
    def _display(self):
        """ Display each word. Display checkbutton beneath 
            each key word (capitalized). Underline each 
            key word.
        """
        try:
            # Get next sentence and split into a list of words
            self.words = self.sentence_df.loc[
                self.counter, 'sentence'].split()
            # Remove period from last word
            if self.words[-1][-1] == '.':
                self.words[-1] = self.words[-1][:-1]

            # Display words and checkboxes
            for idx, word in enumerate(self.words):
                if word.isupper() and word != 'A':
                    # Words
                    self.text_vars[idx].set(word)
                    self.word_labels[idx].config(
                        font=('TkDefaultFont 10 underline'))
                    # Checkboxes
                    self.word_chks[idx].grid(column=idx, row=1)
                else:
                    # Words
                    self.text_vars[idx].set(word)
        except KeyError:
            print("Out of sentences!")
            self.text_vars[0].set("Done!")
            self.trial_var.set(f"Trial {len(self.sentence_df)} of " +
                f"{len(self.sentence_df)}")
            self.btn_right.config(state='disabled')
            self.btn_wrong.config(state='disabled')
            self.event_generate('<<MainDone>>')
            return


    ################################
    # Store correct response words #
    ################################
    def _score(self):
        """ Get words marked correct and incorrect, update 
            scoremodel, and send event to controller.
        """
        # Get correct words
        correct = []
        for idx, value in enumerate(self.chk_vars):
            if value.get() != 0:
                correct.append(self.words[idx])

        # Get incorrect words
        # Exclude correct words from list of words
        incorrect = list(set(self.words).difference(correct))
        # Only take capitalized words
        incorrect = [word for word in incorrect if word.isupper()]
        # Remove 'A' if it exists (never a key word, but can be capital)
        try:
            incorrect.remove('A')
        except ValueError:
            # There was no 'A' in the list
            pass

        # Update scoremodel with values
        self.scoremodel.fields['Words Correct'] = ' '.join(correct)
        self.scoremodel.fields['Num Words Correct'] = len(
            self.scoremodel.fields['Words Correct'].split())
        self.scoremodel.fields['Words Incorrect'] = ' '.join(incorrect)
        self.scoremodel.fields['Trial'] = self.counter + 1
        self.scoremodel.fields['Outcome'] = self.outcome

        # Send event to controller to write response to file
        self.event_generate('<<SubmitResponse>>')


    #####################################
    # Reset all labels and checkbuttons #
    #####################################
    def _reset(self):
        """ Reset all word labels and checkbuttons to default 
            values for next trial.
        """
        # Reset word label text
        for val in self.text_vars:
            val.set('')
        # Reset word label font
        for lbl in self.word_labels:
            lbl.config(font=('TkDefaultFont 10'))
        # Hide checkbuttons
        for chk in self.word_chks:
            chk.grid_remove()
        # Reset checkbutton values to 0
        for val in self.chk_vars:
            val.set(0)
