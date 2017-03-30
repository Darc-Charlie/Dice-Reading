import sys
from optparse import OptionParser
import numpy as np
from pymoduleconnector import ModuleConnector
import time

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

    defArray = np.array([1.76256894715 , 1.78936439048 , 1.46481661239 , 0.885794704476 , 0.467862110317 , 0.277090653321 , 0.158559293792 , 0.0852799201875 , 0.0710036611872 , 0.080788534533 , 0.0872443142989 , 0.0855755365231 , 0.0791982070525 , 0.0645761042075 , 0.0484659286997 , 0.0358667740008 , 0.0249812852657 , 0.016924000282 , 0.0140094235166 , 0.0134958582114 , 0.0191459262445 , 0.0458953790776 , 0.074260334003 , 0.0742149026753 , 0.0437136411526 , 0.0116809849234 , 0.0126678134071 , 0.0111888565057 , 0.00453271517805 , 0.00370491049932 , 0.00250467443573 , 0.00971752750542 , 0.010879719485 , 0.00441182394503 , 0.0050235685031 , 0.0102334577239 , 0.0133007847681 , 0.0108231231529 , 0.00510209029097 , 0.0028703452202 , 0.0108301438094 , 0.0191588401928 , 0.0211987020612 , 0.0149662227096 , 0.0138762737797 , 0.0111413246884 , 0.0054136391096 , 0.00250554238005 , 0.00487377221802 , 0.00568854691149 , 0.00408475813658 , 0.0036237171852 , 0.00308515447175 , 0.00490590103776 , 0.0100498449564 , 0.0131783506955 , 0.0114972702564 , 0.00773870080901 , 0.00740336419089 , 0.0106162728443 , 0.00918110511975 , 0.00410370965791 , 0.00415047760726 , 0.00632975460947 , 0.00662896902187 , 0.00801865729728 , 0.00907293704938 , 0.00827219440954 , 0.00364050100425 , 0.010310127958 , 0.0161916918193 , 0.0157684284024 , 0.0125214922129 , 0.00860937793194 , 0.0055419552596 , 0.0058311891325 , 0.00525400274601 , 0.00521166272589 , 0.00352994978465 , 0.000915316900604 , 0.00562765405747 , 0.00877590294859 , 0.00988393782922 , 0.00980039012453 , 0.00959402763479 , 0.0126062651028 , 0.0184027642543 , 0.0209186532848 , 0.0142483983935 , 0.00437384891065 , 0.0111725035466 , 0.0124112296829 , 0.0095777377534 , 0.0047772418336 , 0.0028760019707 , 0.00570199026778 , 0.00416883430543 , 0.00518456388785 , 0.00636503363082 , 0.0044516103267 , 0.00258490222123 , 0.00315685617121 , 0.00450143613011 , 0.00425804669362 , 0.00185116401827 , 0.00254123244027 , 0.00462917594416 , 0.0039604561004 , 0.00310329374715 , 0.00159285063863 , 0.000632905920959 , 0.000743706757889 , 0.00288389847873 , 0.00585656907547 , 0.00858851348158 , 0.010565766738 , 0.0110642430489 , 0.00871310008512 , 0.00473320691018 , 0.00315085594789 , 0.00480514954595 , 0.00427183547296 , 0.00306597873896 , 0.00186068485696 , 0.00163440029372 , 0.00211365310047 , 0.00254818674613 , 0.00248596691991 , 0.00206814483009 , 0.00284598465445 , 0.00385632117923 , 0.00420981544047 , 0.00308813541808 , 0.000924540822403 , 0.00168591989293 , 0.00148405009783 , 0.000499347144066 , 0.000999914282214 , 0.00177480316806 , 0.00348459391394 , 0.00414456911972 , 0.00337515869381 , 0.00249914916368 , 0.00196793485601 , 0.00162087328104 , 0.00180206631503 , 0.00258322943081 , 0.00312475670722 , 0.00245511198558 , 0.00249395857339 , 0.00423257873249 , 0.0054280853608 , 0.00519257470347 , 0.00366267312197 , 0.000985128077012 , 0.00108171288606 , 0.000965422313757 , 0.00179155790736 , 0.00203106839058 , 0.00161917559719 , 0.00353167448301 , 0.0038009281108 , 0.00317506036455 , 0.00226667345374 , 0.000989582872234 , 0.00132771079964 , 0.00246928414812 , 0.003121750115 , 0.00316872974433 , 0.00333916545628 , 0.00325257767797 , 0.00181886893729 , 0.000738416898294 , 0.00135428644665 , 0.000934436823186 , 0.000312547706746 , 0.000664205742383 , 0.000974862113708 , 0.00167666097617 , 0.00123986094021 , 0.000323185073495 , 8.78349947067e-05 , 0.000253846806352 , 0.000624479350309 , 0.00126360621645 , 0.00199159322199 , 0.00496844379991 , 0.0161165954566])

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

    def animate(i):
        if bb:
            absFrame = abs(read_frame())
            for x in range(absFrame.shape[0]):
                absFrame[x] = absFrame[x]-defArray[x]
            line.set_ydata(absFrame)  # update the data
        else:
            line.set_ydata(read_frame())  # update the data
        return line,


    clear_buffer()

    absFrame = abs(read_frame())
    '''print "["
    for x in range(absFrame.shape[0]):
        print absFrame[x],
        print ",",

    print "]"'''
    

    for x in range(absFrame.shape[0]):
                absFrame[x] = absFrame[x]-defArray[x]
    maxVal = 0
    for y in range(12):
        if absFrame[y] > maxVal:
            maxVal = absFrame[y]

    if maxVal > 0.01:
        print "Foam"
    else:
        print "DeadEnd"

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
    while(True):
        simple_xep_plot(options.device_name, bb = options.baseband)
        time.sleep(1.5)

if __name__ == "__main__":
    main()


