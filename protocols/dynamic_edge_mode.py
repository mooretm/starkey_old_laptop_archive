""" Dynamic Edge Mode setup protocol for use with Vesta. 
"""

###########
# Imports #
###########
# Import system packages
import time

def dem_protocol(self):
    """ Set automatic snapshot switching to max duration. 
        Reinit, reconnect.
        Toggle ODAT.
    """
    start_dem = "*** Starting DEM Procotol ***"
    print(f"\n\nvulcanmodel: {'*' * len(start_dem)}")
    print(f"vulcanmodel: {start_dem}")
    print(f"vulcanmodel: {'*' * len(start_dem)}")

    # Set new snapshot interval (max 255 seconds)
    #print("\nvulcanmodel: Setting snapshot interval to max...")
    timeout = 255
    self.write_parameters("System", "AdaptiveTuningPrivate", 
        "AcousticEnvironmentClassificationInterval", timeout)
    #print("vulcanmodel: Done")
    time.sleep(1)

    # Turn off autosleep
    self.write_parameters("Imu", "ImuFeatures", "AutoSleepEnable", False)
    time.sleep(1)

    # Reinitialize devices
    print("\nvulcanmodel: Reinitializing device(s)...")
    self.reinit()
    time.sleep(5)
    print("vulcanmodel: Done")

    # Reconnect the devices
    print("\nvulcanmodel: Reconnecting device(s)...")
    self._connect_instruments()
    time.sleep(5)
    print("vulcanmodel: Done")

    # Display changed parameters
    self.read_parameters("System", "AdaptiveTuningPrivate",
        "AcousticEnvironmentClassificationInterval")
    time.sleep(1)
    self.read_parameters("Imu", "ImuFeatures", "AutoSleepEnable")
    time.sleep(1)

    # Toggle ODAT
    self.toggle_odat("on")

    end_dem = "*** DEM Procotol Complete ***"
    print(f"\nvulcanmodel: {'*' * len(end_dem)}")
    print(f"vulcanmodel: {end_dem}")
    print(f"vulcanmodel: {'*' * len(end_dem)}\n")
