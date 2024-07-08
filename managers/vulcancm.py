""" Vulcan OOP approach test script
"""

###########
# Imports #
###########
# Import system packages
import os
import time
import sys

# Import custom modules
os.sys.path.append('C:/Program Files (x86)/Starkey Hearing Technologies/FWE/Vulcan/Bin')
import clr
clr.AddReference("Starkey.FWE.Vulcan")
from Starkey.FWE.Vulcan import Vulcan





# # Import managers
# from managers.printcm import SuppressPrint

# import requests
# import logging

# logging.basicConfig()
# #logging.getLogger('requests').setLevel(logging.ERROR)

# from contextlib import contextmanager

# @contextmanager
# def suppress_stdout():
#     with open(os.devnull, "w") as devnull:
#         old_stdout = sys.stdout
#         sys.stdout = devnull
#         try:
#             yield
#         finally:
#             sys.stdout = old_stdout

# import io

# text_trap = io.StringIO()
# sys.stdout = text_trap



#########
# BEGIN #
#########
class VulcanSessionManager:
    """ Context manager for Vulcan sessions. This ensures connecting and 
        disconnecting are always carried out without the user having 
        to remember.
    """
    def __init__(self):
        """ Detect and connect to programmer and instruments
        """
        # List of snapshots
        self.AS = ['Invalid', 'MLR', 'QRS', 'LRS', 'TRS', 'TRN', 'DHL', 'DLL', 'WND']


    def __enter__(self):
        print('--------------------------------     Starting Vulcan Session     ------------------------------------------')
        #with SuppressPrint():
        #with suppress_stdout():
        # Create the session as global to all consumers of this module access
        self.vulcanSession = Vulcan.CreateInstance()
        print("InstrumentConfig.py - Session created")

        # Know what we are working against
        print("InstrumentConfig.py - Vulcan Version: " + str(self.vulcanSession.Version))

        # Connecting to first programmer found
        self.vulcanSession.DetectProgrammers()

        # Define the accessed programmer globally for consumer access
        self.programmer = self.vulcanSession.DetectedProgrammers[0]

        # NOTE: because we are connecting we need to "Disconnect", and that falls on the module consumer
        self.programmer.Connect()

        # Connecting to first instrument found
        self.programmer.DetectInstruments()

        # Define the accessed instrument globally for consumer access
        self.instrument_left = self.programmer.DetectedInstruments[0]
        self.instrument_right = self.programmer.DetectedInstruments[1]

        self.instrument_left.Connect()
        self.instrument_right.Connect()

        programmingModeResponse_left = self.instrument_left.AdjustProgrammingMode(True)
        programmingModeResponse_right = self.instrument_right.AdjustProgrammingMode(True)

        if (programmingModeResponse_left.Succeeded == False):
            print("Failed to start programming mode on Left: " + str(programmingModeResponse_left.ResponseMessage))

        if (programmingModeResponse_right.Succeeded == False):
            print("Failed to start programming mode on Right: " + str(programmingModeResponse_right.ResponseMessage))

        print('--------------------------------     Connection Established     -------------------------------------------')

        return (self.instrument_left, self.instrument_right)


    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('---------------------------------     Ending Vulcan Session     -------------------------------------------')
        if self.instrument_left or self.instrument_right is None:
            print("InstrumentConfig.py - Clean up called but no instrument was ever initialized.")
        else:
            programmingModeResponse_left = self.instrument_left.AdjustProgrammingMode(False)
            programmingModeResponse_right = self.instrument_right.AdjustProgrammingMode(False)
            if (programmingModeResponse_left.Succeeded == False):
                print("Failed to end programming mode on Left: " + programmingModeResponse_left.ResponseMessage)
            if (programmingModeResponse_right.Succeeded == False):
                print("Failed to start programming mode on Right: " + programmingModeResponse_right.ResponseMessage)
            self.instrument_left.Disconnect()
            self.instrument_right.Disconnect()
        if self.programmer is None:
            print("InstrumentConfig.py - Clean up called but no programmer was ever initialized.")
        else:
            self.programmer.Disconnect()
        print('----------------------------------   Instrument Disconnected    -------------------------------------------')
