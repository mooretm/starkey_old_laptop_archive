""" Model to write data to .csv
"""

############
# IMPORTS  #
############
import tkinter
from tkinter import messagebox

# Import system packages
import csv
from pathlib import Path
from datetime import datetime
import os


#########
# MODEL #
#########
class CSVModel:
    """ Write provided dictionary to .csv
    """
    def __init__(self, sessionpars):
        self.sessionpars = sessionpars

        # Generate date stamp
        self.datestamp = datetime.now().strftime("%Y_%b_%d_%H%M")


    def save_record(self, data):
        """ Save a dictionary of data to .csv file 
        """
        # Create file name and path
        filename = f"{self.datestamp}_{self.sessionpars['Condition'].get()}_{self.sessionpars['Subject'].get()}.csv"
        self.file = Path(filename)

        # Check for write access to store csv
        file_exists = os.access(self.file, os.F_OK)
        parent_writable = os.access(self.file.parent, os.W_OK)
        file_writable = os.access(self.file, os.W_OK)
        if (
            (not file_exists and not parent_writable) or
            (file_exists and not file_writable)
        ):
            msg = f"Permission denied accessing file: {filename}"
            raise PermissionError(msg)

        # Write data to file
        newfile = not self.file.exists()
        with open(self.file, 'a', newline='') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
        print("Models_csvmodel_52:Record successfully saved!")
