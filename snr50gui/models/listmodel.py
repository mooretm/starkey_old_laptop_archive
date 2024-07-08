""" Model for loading and subsetting audio and sentence files.

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import GUI packages
from tkinter import messagebox

# Import data science packages
import pandas as pd

# Import system packages
import os
from glob import glob


#########
# BEGIN #
#########
class StimulusList:
    """ Load audio files and written sentences into dataframes.
        Subset dataframes based on provided list numbers.

        Returns:
            self.audio_df: data frame of audio paths/names
            self.sentence_df: data frame of sentences, indexes
    """

    def __init__(self, sessionpars):
        # Initialize
        self.sessionpars = sessionpars


    def load(self):
        """ Controller to call task functions 
            in the proper order.
        """
        # Retrieve specified list number(s)
        self._get_list_nums()

        try:
            # Load and subset sentences
            # Must occur before audio call
            self._get_sentences()
            # Load and subset audio files
            # Based on sentence call
            self._get_audio_files()
        except FileNotFoundError:
            print("Models_Listmodel_52: Cannot find stimuli!")


    def _get_list_nums(self):
        """ Get list numbers as integers.
        """
        self.lists = self.sessionpars['List Number'].get().split()
        self.lists = [int(val) for val in self.lists]


    #############
    # Sentences #
    #############
    def _get_sentences(self):
        """ Open sentences file and load contents into dataframe. 
            Subset by specified list number(s) from session info.
        """
        # Check whether sentence directory exists
        print("Models_listmodel_66: Checking for sentences dir...")
        if not os.path.exists(self.sessionpars['Sentence File Path'].get()):
            print("Models_listmodel_68: Not a valid 'sentences' file directory!")
            #messagebox.showerror(
            #    title='Directory Not Found!',
            #    message="Cannot find the 'sentence' file directory!\n" + 
            #    "Please choose another file path."
            #)
            raise FileNotFoundError

        # If a valid directory has been given, 
        # get a list of sentence files
        glob_pattern = os.path.join(self.sessionpars['Sentence File Path'].get(), '*.csv')
        sentence_file = glob(glob_pattern)
        # Check to make sure there's only one file in the directory
        if len(sentence_file) > 1:
            messagebox.showwarning(
                title="Too Many Files!",
                message="Multiple sentence files found - taking the first one."
            )
        # Read sentence file into dataframe
        s = pd.read_csv(sentence_file[0])

        # Get sentences for specified list numbers
        self.sentence_df = s.loc[s['list_num'].isin(self.lists)].reset_index()
        print(self.sentence_df)
        print("Models_listmodel_91: Sentence list dataframe loaded into listmodel")


    ###############
    # Audio Files #
    ###############
    def _get_audio_files(self):
        """ Load in files as full paths. Select files based 
            on sentences data frame.
        """
        # Check whether audio directory exists
        print("Models_listmodel_102: Checking for audio files dir...")
        if not os.path.exists(self.sessionpars['Audio Files Path'].get()):
            print("Models_listmodel_104: Not a valid audio files directory!")
            messagebox.showerror(
                title='Directory Not Found!',
                message="Cannot find the audio file directory!\n" +
                "Please choose another file path."
            )

        # If a valid directory has been given, 
        # get the audio file paths and names
        glob_pattern = os.path.join(self.sessionpars['Audio Files Path'].get(), '*.wav')
        # Create audio paths dataframe
        self.audio_df = pd.DataFrame(glob(glob_pattern), columns=['path'])
        # Create new column based on file names (which are numbered)
        self.audio_df['file_num'] = self.audio_df['path'].apply(lambda x: x.split(os.sep)[-1][:-4])
        # Convert to integers
        self.audio_df['file_num'] = self.audio_df['file_num'].astype(int)
        # Sort ascending by new column of integers
        self.audio_df = self.audio_df.sort_values(by=['file_num'])

        # Subset based on sentence dataframe values
        self.audio_df = self.audio_df.loc[self.audio_df['file_num'].isin(self.sentence_df['sentence_num'])]
        print(self.audio_df)
        print("Models_listmodel_126: Audio list dataframe loaded into listmodel")
