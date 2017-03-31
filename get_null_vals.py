import sys
from optparse import OptionParser
import numpy as np
from pymoduleconnector import ModuleConnector

__version__ = 2

def reset(device_name):
    from time import sleep
    mc = ModuleConnector(device_name)
    r = mc.get_xep()
    r.module_reset()
    mc.close()
    sleep(3)

def simple_xep_plot(device_name, bb = True):

    FPS = 10

    reset(device_name)
    mc = ModuleConnector(device_name)
    r = mc.get_xep()
    # Set DAC range
    r.x4driver_set_dac_min(900)
    r.x4driver_set_dac_max(1150)

    # Set integration
    r.x4driver_set_iterations(16)
    r.x4driver_set_pulses_per_step(26)

    if bb:
        r.x4driver_set_downconversion(1)

    # Start streaming of data
    r.x4driver_set_fps(FPS)

    def clear_buffer():
        """Clears the frame buffer"""
        while r.peek_message_data_float():
            _=r.read_message_data_float()

    def read_frame():
        """Gets frame data from module"""
        d = r.read_message_data_float()
        frame = np.array(d.data)
         # Convert the resulting frame to a complex array if downconversion is enabled
        if bb:
            n=len(frame)
            frame = frame[:n/2] + 1j*frame[n/2:]

        return frame

    clear_buffer()

    absFrame = abs(read_frame())
    print "["
    for x in range(absFrame.shape[0]):
        print absFrame[x],
        print ",",

    print "]"


    # Stop streaming of data
    r.x4driver_set_fps(0)



def main():
    parser = OptionParser()
    parser.add_option(
        "-d",
        "--device",
        dest="device_name",
        help="device file to use",
        metavar="FILE")
    parser.add_option(
        "-b",
        "--baseband",
        action="store_true",
        default=True,
        dest="baseband",
        help="Enable baseband, rf data is default",
        metavar="FILE")


    (options, args) = parser.parse_args()

    if not options.device_name:
        print "you have to specify device, e.g.: python record.py -d /dev/ttyACM0"
        sys.exit(1)

    simple_xep_plot(options.device_name, bb = options.baseband)


if __name__ == "__main__":
    main()


