""" Class for storing session parameters 
"""

############
# IMPORTS  #
############
# Import system packages
from pathlib import Path

# Import data handling packages
import json
from glob import glob


#########
# BEGIN #
#########
class SessionParsModel:
    # Define dictionary items
    fields = {
        'Subject': {'type': 'str', 'value': '999'},
        'Condition': {'type': 'str', 'value': 'Quiet'},
        'List Number': {'type': 'str', 'value': '1'},
        'Presentation Level': {'type': 'float', 'value': 65},
        'Speaker Number': {'type': 'int', 'value': 1},
        'Audio Files Path': {'type': 'str', 'value': 'Please select a path'},
        'Sentence File Path': {'type': 'str', 'value': 'Please select a path'},
        'Audio Device ID': {'type': 'int', 'value': None},
        'raw_lvl': {'type': 'float', 'value': -30},
        'slm_cal_value': {'type': 'float', 'value': 65},
        'slm_offset': {'type': 'float', 'value': 95.0},
        'new_raw_lvl': {'type': 'float', 'value': -30},
        'new_db_lvl': {'type': 'float', 'value': 65},
        'Calibration File': {'type': 'str', 'value': 'cal_stim.wav'}
    }

    def __init__(self):
        # Create session parameters file
        filename = 'snr50_pars.json'

        # Store settings file in user's home directory
        self.filepath = Path.home() / filename

        # Load settings file
        self.load()


    def load(self):
        """ Load session parameters from file
        """
        # If the file doesn't exist, abort
        print("\nModels_Session_54: Checking for parameter file...")
        if not self.filepath.exists():
            return

        # Open the file and read in the raw values
        print("Models_Session_59: File found - reading raw values from " +
            "parameter file...")
        with open(self.filepath, 'r') as fh:
            raw_values = json.load(fh)

        # Don't implicitly trust the raw values: only get known keys
        print("Models_Session_65: Loading vals into sessionpars model " +
            "if they match model keys")
        # Populate session parameter dictionary
        for key in self.fields:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.fields[key]['value'] = raw_value


    def save(self):
        """ Save current session parameters to file 
        """
        # Write to JSON file
        print("Models_Session_78: Writing session pars from model to file...")
        with open(self.filepath, 'w') as fh:
            json.dump(self.fields, fh)


    def set(self, key, value):
        """ Set a variable value """
        print("Models_Session_85: Setting sessionpars model " +
            "fields with running vals...")
        if (
            key in self.fields and 
            type(value).__name__ == self.fields[key]['type']
        ):
            self.fields[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")
