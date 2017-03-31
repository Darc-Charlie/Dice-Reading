import sys
from optparse import OptionParser
import numpy as np
from pymoduleconnector import ModuleConnector
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)                #set mode of gpio to use board numbers
GPIO.setup(15, GPIO.IN, GPIO.PUD_DOWN)  #set mode of pin 15 to an input pin

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
    data_log = open('xethruData.dat','w')
    reset(device_name)
    mc = ModuleConnector(device_name)
    r = mc.get_xep()
    # Set DAC range
    r.x4driver_set_dac_min(900)
    r.x4driver_set_dac_max(1150)

    # Set integration
    r.x4driver_set_iterations(16)
    r.x4driver_set_pulses_per_step(26)

    defArray = np.array([1.71766245732 , 1.33376367685 , 0.812835983414 , 0.804757654989 , 0.696728880331 , 0.603134053569 , 0.388225223077 , 0.121377225643 , 0.0523278424259 , 0.0829639190341 , 0.0373298312747 , 0.0470495846549 , 0.0919810905222 , 0.108570369162 , 0.0614378272901 , 0.0264122795212 , 0.0338875862593 , 0.0188069953999 , 0.0381272538132 , 0.0521902867476 , 0.0387276501028 , 0.0168732815946 , 0.00781831594333 , 0.0123205264851 , 0.0212964171893 , 0.0225971961546 , 0.0205349306615 , 0.015673871026 , 0.0113001123674 , 0.0130202237048 , 0.00680364633844 , 0.00103544257327 , 0.00573072949922 , 0.0104509984507 , 0.00869035783507 , 0.00416269003841 , 0.00802805775349 , 0.0115015819054 , 0.0139124437395 , 0.0143847259023 , 0.0126674295647 , 0.0171529418329 , 0.0203039230479 , 0.0139951677793 , 0.00430691715701 , 0.00101243540393 , 0.00370630543599 , 0.00522211151922 , 0.00386195175237 , 0.00210642330596 , 0.00135419747492 , 0.0019448048384 , 0.00262631091817 , 0.00213745858429 , 0.002642793381 , 0.00631597788749 , 0.00537551103048 , 0.00954176581709 , 0.0115430146989 , 0.00656553983417 , 0.00243403099474 , 0.00995741909614 , 0.00965675631359 , 0.00244886633016 , 0.00532211702783 , 0.00420443822581 , 0.00369168640776 , 0.00649265277976 , 0.0100664612483 , 0.0140825412986 , 0.015093453513 , 0.0124673518561 , 0.00761470529102 , 0.00471235961056 , 0.00510928447451 , 0.00380444588441 , 0.00369516318064 , 0.00548376224017 , 0.0059736614595 , 0.00678695180239 , 0.0132160005703 , 0.0161282831091 , 0.0109076683949 , 0.00690549691019 , 0.00757329577067 , 0.00791437901582 , 0.00619512614966 , 0.00361618001092 , 0.00226444052001 , 0.00251087233416 , 0.00364076105634 , 0.00440695048909 , 0.00374027344895 , 0.00301864342063 , 0.00364262945643 , 0.0049681037367 , 0.00401365230618 , 0.00279794003853 , 0.00328324054684 , 0.00302377169527 , 0.00197571850795 , 0.00320632133446 , 0.00254457809543 , 0.000952269392357 , 0.00113000170016 , 0.000911554873974 , 0.00265909535249 , 0.00393204729337 , 0.00328292629763 , 0.00449144932375 , 0.00745833590317 , 0.00698310014148 , 0.00556051521308 , 0.00330700340232 , 0.0028264167969 , 0.00450360203048 , 0.00438371978743 , 0.00461981125789 , 0.0036826210197 , 0.00137544207157 , 0.00271125463942 , 0.00381352047966 , 0.00331657039666 , 0.00135912019 , 0.000206742393165 , 0.00130842539046 , 0.00261725955246 , 0.00238893024359 , 0.00198996189865 , 0.00149521444805 , 0.000611071915771 , 0.00028000784323 , 0.000299522849017 , 0.00124919925103 , 0.00180529545337 , 0.000811367795703 , 0.000422020222233 , 0.00207079633271 , 0.00416827805608 , 0.00444198824321 , 0.00388245370834 , 0.00340853149415 , 0.00332784985996 , 0.00311053251753 , 0.00305088761996 , 0.00268822931698 , 0.00148972850404 , 0.000333826298157 , 0.000679961544195 , 0.000865732868698 , 0.00156257084811 , 0.00183678777054 , 0.00101291367587 , 0.000882768911587 , 0.00243680797166 , 0.00318300818911 , 0.00294107022348 , 0.00219054955048 , 0.000995247933737 , 0.00130351467388 , 0.0014905223939 , 0.000294416961478 , 0.000631521237715 , 0.00107062674016 , 0.00210991664369 , 0.00231756298685 , 0.00157161887478 , 0.000823251456692 , 0.000536609310573 , 0.00141192417378 , 0.00294634543308 , 0.00231946335472 , 0.000305520985118 , 0.000736987601132 , 0.00062378600629 , 0.000520922236433 , 0.000843446826988 , 0.000626753992536 , 0.000748974053109 , 0.00161082146902 , 0.0025275076983 , 0.00240893174696 , 0.00125419587456 , 0.000584903231703 , 0.000628733326367 , 0.00100186606529 , 0.00504230403063 , 0.0144768420296])

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
    count = 0
    field = []
    field.append("s")
    readCell = False
    
    while (count != 48):
        readCell = GPIO.input(15)
        #raw_input("Press Enter to continue...")
        
        if (readCell):
            count = count+1
            absFrame = abs(read_frame())

            for x in range(absFrame.shape[0]):
                absFrame[x] = absFrame[x]-defArray[x]
            maxVal = 0
            for y in range(11):
                if absFrame[y] > maxVal:
                    maxVal = absFrame[y]

            if maxVal > 0.07:
                field.append(0)
            else:
                field.append(1)

    for i in range(len(field)):
        if i%7 is 0 and i != 0:
            data_log.write("\n")
        
        data_log.write(str(field[i]) + " ")

    data_log.close()
    # Stop streaming of data
    r.x4driver_set_fps(0)



def main():
    #pin 33 from arduino
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


