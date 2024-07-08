""" Static Edge Mode setup protocol for use with Vesta. 
"""

###########
# Imports #
###########
# Import system packages
import time

def static_edge_mode_protocol(self):
    """ Activate static edge mode. 
    """
    start_protocol = "*** Starting Static Edge Mode Procotol ***"
    print(f"\n\nvulcanmodel: {'*' * len(start_protocol)}")
    print(f"vulcanmodel: {start_protocol}")
    print(f"vulcanmodel: {'*' * len(start_protocol)}")

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
    try:
        if self.prog == 'noahlink':
            self._connect_wireless_instruments(self.sn_dict)
        elif self.prog == 'speedport':
            self._connect_wired_instruments()
    except e.NoDevicesFoundError:
        print('vulcanmodel: No devices found!')
        raise e.NoDevicesFoundError
    time.sleep(5)
    print("vulcanmodel: Done")

    # Display changed parameters
    self.read_parameters("Imu", "ImuFeatures", "AutoSleepEnable")
    time.sleep(1)

    # Toggle ODAT
    self.toggle_odat("on")

    # Change adaptive tuning to static edge mode (default is DEM)
    #self.write_parameters(self, context, parameter_group, Parameter, New_Value)
    #self.write_parameters(self, context, parameter_group, Parameter, New_Value)

    end_protocol = "*** Procotol Complete ***"
    print(f"\nvulcanmodel: {'*' * len(end_protocol)}")
    print(f"vulcanmodel: {end_protocol}")
    print(f"vulcanmodel: {'*' * len(end_protocol)}\n")
