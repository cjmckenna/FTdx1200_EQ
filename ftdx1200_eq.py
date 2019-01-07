from tkinter import *
import tkinter.ttk as ttk
import serial
import sys
import glob
import time

ser = serial.Serial(timeout=.01)

reverse_eq1_frequency_cat_values = {'00': '00', '01': '100', '02': '200', '03': '300',
                            '04': '400', '05': '500', '06': '600', '07': '700'}

reverse_eq_level_cat_values = {'-20': '-20', '-19': '-19', '-18': '-18', '-17': '-17', '-16': '-16', '-15': '-15',
                       '-14': '-14', '-13': '-13', '-12': '-12', '-11': '-11', '-10': '-10', '-09': '-9',
                       '-08': '-8', '-07': '-7', '-06': '-6', '-05': '-5', '-04': '-4', '-03': '-3',
                       '-02': '-2', '-01': '-1', '+00': '0', '+01': '1', '+02': '2', '+03': '3', '+04': '4',
                       '+05': '5', '+06': '6', '+07': '7', '+08': '8', '+09': '9', '+10': '10'}

reverse_eq2_frequency_cat_values = {'00': '00', '01': '700', '02': '800', '03': '900', '04': '1000',
                            '05': '11', '06': '1200', '07': '1300', '08': '1400', '09': '1500'}

reverse_eq3_frequency_cat_values = {'00': '00', '01': '1500', '02': '1600', '03': '1700', '04': '1800',
                            '05': '1900', '06': '2000', '07': '2100', '08': '2200', '09': '2300',
                            '10': '2400', '11': '2500', '12': '2600', '13': '2700', '14': '2800',
                            '15': '2900', '16': '3000', '17': '3100', '18': '3200'}

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    print("I am running on:", sys.platform)
    if sys.platform.startswith('win32'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def com_on_select(event=None):
    # get selection from event
    print("event.widget:", event.widget.get())

    # or get selection directly from combobox
    print("com port: ", cbcom.get())
    ser.port = cbcom.get()
    print("What I set as a com port: ", ser.port)


def baud_on_select(event=None):
    # get selection from event
    print("event.widget:", event.widget.get())

    # or get selection directly from combobox
    print("baudrate: ", cbbaud.get())
    ser.baudrate = cbbaud.get()
    print("What I set as a baud: ", ser.baudrate)


def open_serial():
    ser.open()
    print(ser.is_open)
    print("I am opening the port")

    #########################################################################
    # now we have to actually test that we can talk to the radio
    ser.write('FA;'.encode())
    readret = (ser.read(1).decode('utf-8', 'ignore'))
    print("Return Value", readret)

    if readret != 'F':
        print("Oh Crap!")
        ser.close()
    else:

        amiopen = str(ser.is_open)
        print(amiopen)
        if amiopen == "True":
            print('Yep... its open')
            radio_connect_button.config(highlightbackground='#4ca64c')
            radio_connect_button.config(text='Connected')
            loadcurrents()
        else:
            print('something went wrong')


def close_serial():
    ser.close()  # close port
    print(ser.is_open)
    radio_connect_button.config(highlightbackground='#db3328')
    radio_connect_button.config(text='Connect')

######################################################################################################
# This section will hopefully get the current values for the EQ settings in the radio
#

def loadcurrents():
    endtoend_start_time = time.time()
    print("I am running loadcurrents")
    ser.flushInput()
    ser.flushOutput()
    #time.sleep(10)

    ## PROC OFF CURRENT SETTINGS READ
    ###################################################################################################
    # Proc Off EQ1 Frequency
    start_time = time.time()
    print("Proc Off EQ1 Frequency Start")
    ser.write('EX159;'.encode())
    pofffeq1ret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX159').rstrip(';'))
    # print("POFF EQ1 Frequency Return Value", pofffeq1ret)
    # print("This is from the dictionary: ", reverse_eq1_frequency_cat_values[pofffeq1ret])
    poff_eq1_frequency.set(reverse_eq1_frequency_cat_values[pofffeq1ret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ1 Frequency END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc Off EQ1 Level
    start_time = time.time()
    ser.write('EX160;'.encode())
    poffeq1levelret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX160').rstrip(';'))
    intlevel = int(poffeq1levelret)
    # print("this is level set as an integer", intlevel)
    # print("POFF EQ1 Level Return Value", poffeq1levelret)
    # print("This is from the dictionary for EQ1 Level:", reverse_eq_level_cat_values[poffeq1levelret])
    poff_eq1_level.set(reverse_eq_level_cat_values[poffeq1levelret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ1 Level END Elapsed Time", elapsed_time)


    ###################################################################################################
    # Proc Off EQ1 Bandwidth
    start_time = time.time()
    ser.write('EX161;'.encode())
    poffeq1bwret = int((ser.read_until(';').decode('utf-8', 'ignore').strip('EX161').rstrip(';')))
    # print("POFF EQ1 Bandwidth Return Value", poffeq1bwret)
    poff_eq1_bandw.set(poffeq1bwret)
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ1 BW END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc Off EQ2 Frequency
    start_time = time.time()
    ser.write('EX162;'.encode())
    poffeq2ret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX162').rstrip(';'))
    # print("POFF EQ2 Frequency Return Value", poffeq2ret)
    # print("This is from the dictionary: ", reverse_eq2_frequency_cat_values[pofffeq1ret])
    poff_eq2_frequency.set(reverse_eq2_frequency_cat_values[poffeq2ret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ2 Frequency END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc Off EQ2 Level
    start_time = time.time()
    ser.write('EX163;'.encode())
    poffeq2levelret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX163').rstrip(';'))
    # print("POFF EQ2 Level Return Value", poffeq2levelret)
    # print("This is from the dictionary for EQ2 Level:", reverse_eq_level_cat_values[poffeq2levelret])
    poff_eq2_level.set(reverse_eq_level_cat_values[poffeq2levelret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ2 Level END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc Off EQ2 Bandwidth
    start_time = time.time()
    ser.write('EX164;'.encode())
    poffeq2bwret = int((ser.read_until(';').decode('utf-8', 'ignore').strip('EX164').rstrip(';')))
    # print("POFF EQ2 Bandwidth Return Value", poffeq2bwret)
    poff_eq2_bandw.set(poffeq2bwret)
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ2 BW END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc Off EQ3 Frequency
    start_time = time.time()
    ser.write('EX165;'.encode())
    poffeq3ret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX165').rstrip(';'))
    print("POFF EQ3 Frequency Return Value", poffeq3ret)
    print("This is from the dictionary for POFFEQ3 Freq: ", reverse_eq3_frequency_cat_values[pofffeq1ret])
    poff_eq3_frequency.set(reverse_eq3_frequency_cat_values[poffeq3ret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ3 Frequency END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc Off EQ3 Level
    start_time = time.time()
    ser.write('EX166;'.encode())
    poffeq3levelret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX166').rstrip(';'))
    # print("POFF EQ3 Level Return Value", poffeq3levelret)
    # print("This is from the dictionary for EQ3 Level:", reverse_eq_level_cat_values[poffeq3levelret])
    poff_eq3_level.set(reverse_eq_level_cat_values[poffeq3levelret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ3 Level END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc Off EQ3 Bandwidth
    start_time = time.time()
    ser.write('EX167;'.encode())
    poffeq3bwret = int((ser.read_until(';').decode('utf-8', 'ignore').strip('EX167').rstrip(';')))
    # print("POFF EQ3 Bandwidth Return Value", poffeq3bwret)
    poff_eq3_bandw.set(poffeq3bwret)
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc Off EQ3 BW END Elapsed Time", elapsed_time)

    ## PROC ON CURRENT SETTINGS READ
    ###################################################################################################
    # Proc ON EQ1 Frequency
    start_time = time.time()
    ser.write('EX168;'.encode())
    ponfeq1ret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX168').rstrip(';'))
    # print("PON EQ1 Frequency Return Value", ponfeq1ret)
    # print("This is from the dictionary: ", reverse_eq1_frequency_cat_values[ponfeq1ret])
    pon_eq1_frequency.set(reverse_eq1_frequency_cat_values[ponfeq1ret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc On EQ1 Frequency END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc ON EQ1 Level
    start_time = time.time()
    ser.write('EX169;'.encode())
    poneq1levelret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX169').rstrip(';'))
    intlevel = int(poneq1levelret)
    # print("this is level set as an integer", intlevel)
    # print("PON EQ1 Level Return Value", poneq1levelret)
    # print("This is from the dictionary for EQ1 Level:", reverse_eq_level_cat_values[poneq1levelret])
    pon_eq1_level.set(reverse_eq_level_cat_values[poneq1levelret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc On EQ1 Level END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc Off EQ1 Bandwidth
    start_time = time.time()
    ser.write('EX170;'.encode())
    poneq1bwret = int((ser.read_until(';').decode('utf-8', 'ignore').strip('EX170').rstrip(';')))
    # print("PON EQ1 Bandwidth Return Value", poneq1bwret)
    pon_eq1_bandw.set(poneq1bwret)
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc On EQ1 BW END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc ON EQ2 Frequency
    start_time = time.time()
    ser.write('EX171;'.encode())
    poneq2ret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX171').rstrip(';'))
    # print("PON EQ2 Frequency Return Value", poneq2ret)
    # print("This is from the dictionary: ", reverse_eq2_frequency_cat_values[poneq2ret])
    pon_eq2_frequency.set(reverse_eq2_frequency_cat_values[poneq2ret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc On EQ2 Frequency END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc ON EQ2 Level
    start_time = time.time()
    ser.write('EX172;'.encode())
    poneq2levelret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX172').rstrip(';'))
    # print("PON EQ2 Level Return Value", poneq2levelret)
    # print("This is from the dictionary for EQ2 Level:", reverse_eq_level_cat_values[poneq2levelret])
    pon_eq2_level.set(reverse_eq_level_cat_values[poneq2levelret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc On EQ2 Level END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc ON EQ2 Bandwidth
    start_time = time.time()
    ser.write('EX173;'.encode())
    poneq2bwret = int((ser.read_until(';').decode('utf-8', 'ignore').strip('EX173').rstrip(';')))
    # print("PON EQ2 Bandwidth Return Value", poneq2bwret)
    pon_eq2_bandw.set(poneq2bwret)
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc On EQ2 Frequency END Elapsed Time", elapsed_time)

    endtoend_elapsed_time = time.time() - endtoend_start_time
    print("End to End time", endtoend_elapsed_time)

    ###################################################################################################
    # Proc Off EQ3 Frequency
    start_time = time.time()
    ser.write('EX174;'.encode())
    poneq3ret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX174').rstrip(';'))
    print("PON EQ3 Frequency Return Value", poneq3ret)
    print("This is from the dictionary for PONEQ3 Freq: ", reverse_eq3_frequency_cat_values[poneq3ret])
    pon_eq3_frequency.set(reverse_eq3_frequency_cat_values[poneq3ret])
    ser.flushInput()
    ser.flushOutput()
    elapsed_time = time.time() - start_time
    print("Proc ON EQ3 Frequency END Elapsed Time", elapsed_time)

    ###################################################################################################
    # Proc ON EQ3 Level
    ser.write('EX175;'.encode())
    poneq3levelret = (ser.read_until(';').decode('utf-8', 'ignore').strip('EX175').rstrip(';'))
    print("PON EQ3 Level Return Value", poneq3levelret)
    print("This is from the dictionary for EQ3 Level:", reverse_eq_level_cat_values[poneq3levelret])
    pon_eq3_level.set(reverse_eq_level_cat_values[poneq3levelret])

    ###################################################################################################
    # Proc ON EQ3 Bandwidth
    ser.write('EX176;'.encode())
    poneq3bwret = int((ser.read_until(';').decode('utf-8', 'ignore').strip('EX176').rstrip(';')))
    print("PON EQ3 BW Return Value", poffeq3ret)
    print("This is from the dictionary for PONEQ3 BW: ", reverse_eq3_frequency_cat_values[pofffeq1ret])
    pon_eq3_bandw.set(poneq3bwret)

######################################################################################################



######################################################################################################
freqDefault = 0


# setup the dictionaries for the values that we will need to pass to the CAT control.  We only need a dictionary
# for the frequency and level because they are not contiguous values.  The bandwidth runs continuous from 01 to 10
# so we can just use the slider value straight from the output.

# because of the differences in the frequencies we need a dictionary for each EQ.  The level is the same across each EQ
# so we only need one dictionary


eq1_frequency_cat_values = {'00': '00', '100': '01', '200': '02', '300': '03',
                            '400': '04', '500': '05', '600': '06', '700': '07'}

eq2_frequency_cat_values = {'00': '00', '700': '01', '800': '02', '900': '03', '1000': '04',
                            '1100': '05', '1200': '06', '1300': '07', '1400': '08', '1500': '09'}

eq3_frequency_cat_values = {'00': '00', '1500': '01', '1600': '02', '1700': '03', '1800': '04',
                            '1900': '05', '2000': '06', '2100': '07', '2200': '08', '2300': '09',
                            '2400': '10', '2500': '11', '2600': '12', '2700': '13', '2800': '14',
                            '2900': '15', '3000': '16', '3100': '17', '3200': '18'}

# For the level values, I can probably replace the dictionary below with an if statement.
# The only reason I am using the dictionary
# is because the 00 has to be either -00 or +00 and I can't get that from the slider.  Look in to something like
# if value is 00 make it +00 else use the slider value.  I'm tired right now and don't want to try it

eq_level_cat_values = {'-20': '-20', '-19': '-19', '-18': '-18', '-17': '-17', '-16': '-16', '-15': '-15',
                       '-14': '-14', '-13': '-13', '-12': '-12', '-11': '-11', '-10': '-10', '-9': '-09',
                       '-8': '-08', '-7': '-07', '-6': '-06', '-5': '-05', '-4': '-04', '-3': '-03',
                       '-2': '-02', '-1': '-01', '00': '+00', '01': '+01', '02': '+02', '03': '+03', '04': '+04',
                       '05': '+05', '06': '+06', '07': '+07', '08': '+08', '09': '+09', '10': '+10'}

# this will assign the values for the frequency sliders for each EQ because of the jump from
# zero to the first value makes it so we can't just assign the values in the slider itself.
# No need to do this for the level or bandwidth sliders because we can
# just set the min and max property of the slider directly because they run from 01 to 10 and -20 to +10.
# We can put that right in the sliders.

eq1_frequency_slider_values = [0, 100, 200, 300, 400, 500, 600, 700]
eq2_frequency_slider_values = [0, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
eq3_frequency_slider_values = [0, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600,
                               2700, 2800, 2900, 3000, 3100, 3200]



# Below are the functions to update the radio.

# update the settings for each EQ for the processor off. Menu items 159 to 167

def poff_set_eq1_frequency(value):
    poff_eq1_frequency_newval = min(eq1_frequency_slider_values, key=lambda x: abs(x - float(value)))
    poff_eq1_frequency.set(poff_eq1_frequency_newval)
    txt = str(poff_eq1_frequency.get())
    newval = txt.zfill(2)
    print("What is the new value: ", newval)
    print("Slider Value: ", txt, "New Value: ", eq1_frequency_cat_values[newval])
    concatval = 'EX159' + eq1_frequency_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def poff_set_eq1_level(value):
    txt = str(poff_eq1_level.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq_level_cat_values[newval])
    concatval = 'EX160' + eq_level_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def poff_set_eq1_bandw(value):
    txt = str(poff_eq1_bandw.get())
    newval = txt.zfill(2)
    print(newval)
    concatval = 'EX161' + newval + ';'
    ser.write(concatval.encode())
    print(concatval)


def poff_set_eq2_frequency(value):
    poff_eq2_frequency_newval = min(eq2_frequency_slider_values, key=lambda x: abs(x - float(value)))
    poff_eq2_frequency.set(poff_eq2_frequency_newval)
    txt = str(poff_eq2_frequency.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq2_frequency_cat_values[newval])
    concatval = 'EX162' + eq2_frequency_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def poff_set_eq2_level(value):
    txt = str(poff_eq2_level.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq_level_cat_values[newval])
    concatval = 'EX163' + eq_level_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def poff_set_eq2_bandw(value):
    txt = str(poff_eq2_bandw.get())
    newval = txt.zfill(2)
    print(newval)
    concatval = 'EX164' + newval + ';'
    ser.write(concatval.encode())
    print(concatval)


def poff_set_eq3_frequency(value):
    poff_eq3_frequency_newval = min(eq3_frequency_slider_values, key=lambda x: abs(x - float(value)))
    poff_eq3_frequency.set(poff_eq3_frequency_newval)
    txt = str(poff_eq3_frequency.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq3_frequency_cat_values[newval])
    concatval = 'EX165' + eq3_frequency_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def poff_set_eq3_level(value):
    txt = str(poff_eq3_level.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq_level_cat_values[newval])
    concatval = 'EX166' + eq_level_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def poff_set_eq3_bandw(value):
    txt = str(poff_eq3_bandw.get())
    newval = txt.zfill(2)
    print(newval)
    concatval = 'EX167' + newval + ';'
    ser.write(concatval.encode())
    print(concatval)


# update the settings for each EQ for the processor ON. Menu items 168 to 176

def pon_set_eq1_frequency(value):
    pon_eq1_frequency_newval = min(eq1_frequency_slider_values, key=lambda x: abs(x - float(value)))
    pon_eq1_frequency.set(pon_eq1_frequency_newval)
    txt = str(pon_eq1_frequency.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq1_frequency_cat_values[newval])
    concatval = 'EX168' + eq1_frequency_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def pon_set_eq1_level(value):
    txt = str(pon_eq1_level.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq_level_cat_values[newval])
    concatval = 'EX169' + eq_level_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def pon_set_eq1_bandw(value):
    txt = str(pon_eq1_bandw.get())
    newval = txt.zfill(2)
    print(newval)
    concatval = 'EX170' + newval + ';'
    ser.write(concatval.encode())
    print(concatval)


def pon_set_eq2_frequency(value):
    pon_eq2_frequency_newval = min(eq2_frequency_slider_values, key=lambda x: abs(x - float(value)))
    pon_eq2_frequency.set(pon_eq2_frequency_newval)
    txt = str(pon_eq2_frequency.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq2_frequency_cat_values[newval])
    concatval = 'EX171' + eq2_frequency_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def pon_set_eq2_level(value):
    txt = str(pon_eq2_level.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq_level_cat_values[newval])
    concatval = 'EX172' + eq_level_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def pon_set_eq2_bandw(value):
    txt = str(pon_eq2_bandw.get())
    newval = txt.zfill(2)
    print(newval)
    concatval = 'EX173' + newval + ';'
    ser.write(concatval.encode())
    print(concatval)


def pon_set_eq3_frequency(value):
    pon_eq3_frequency_newval = min(eq3_frequency_slider_values, key=lambda x: abs(x - float(value)))
    pon_eq3_frequency.set(pon_eq3_frequency_newval)
    txt = str(pon_eq3_frequency.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq3_frequency_cat_values[newval])
    concatval = 'EX174' + eq3_frequency_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def pon_set_eq3_level(value):
    txt = str(pon_eq3_level.get())
    newval = txt.zfill(2)
    print("Slider Value: ", txt, "New Value: ", eq_level_cat_values[newval])
    concatval = 'EX175' + eq_level_cat_values[newval] + ';'
    ser.write(concatval.encode())
    print(concatval)


def pon_set_eq3_bandw(value):
    txt = str(pon_eq3_bandw.get())
    newval = txt.zfill(2)
    print(newval)
    concatval = 'EX176' + newval + ';'
    ser.write(concatval.encode())
    print(concatval)


# commands to turn proc on and off
def proc_on():
    print("PROC ON")
    proc_off_button.config(text='Turn Proc Off')
    proc_off_button.config(highlightbackground='#FFFFFF')
    proc_on_button.config(highlightbackground='#4ca64c')
    proc_on_button.config(text='PROC IS ON')
    ser.write(b'pr01;')


def proc_off():
    print("PROC OFF")
    proc_off_button.config(text='Proc is OFF')
    proc_off_button.config(highlightbackground='#4ca64c')
    proc_on_button.config(highlightbackground='#FFFFFF')
    proc_on_button.config(text='TURN PROC ON')
    ser.write(b'pr00;')


# commands to turn the EQ on and off

def eq_on():
    print("EQ ON")
    eq_on_button.config(highlightbackground='#4ca64c')
    eq_on_button.config(text='EQ IS ON')
    ser.write(b'pr11;')


def eq_off():
    print("EQ OFF")
    eq_on_button.config(highlightbackground='#FFFFFF')
    eq_on_button.config(text='TURN EQ ON')
    ser.write(b'pr10;')


master = Tk()

master.title("Yaesu FTdx-1200 EQ Utility")

textbox = LabelFrame(master, text=" Yaesu FTdx-1200 EQ Utility ", font=('courier', 15, 'bold'))
textbox.grid(row=0, column=20)

S = Scrollbar(textbox)
T = Text(textbox, height=10, width=50, wrap=WORD)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = """This utility is used to easily setup the EQ settings on the FTdx-1200 without having to constantly
work your way through the menu settings.

Settings are provided for the EQ when the voice processor is on or off.  Additionally, controls are provided for
turning the proc and the EQ on and off for making the setting changes as well as hearing the differences.

Use the radio connection buttons to establish the serial CAT connection to the radio"""
T.insert(END, quote)

# This section is for the settings when the proc is OFF....

noproc = LabelFrame(master, text=" Settings for EQ when the Processor is 'OFF' ", font=('courier', 15, 'bold'))
noproc.grid(row=0, column=0, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

poffeq1 = LabelFrame(noproc, text=" Parametric EQ 1 ")
poffeq1.grid(row=0, column=0, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

Label(poffeq1, text="Frequency").grid(row=1, column=0)
Label(poffeq1, text="Level").grid(row=1, column=1)
Label(poffeq1, text="Bandwidth").grid(row=1, column=2)

poff_eq1_frequency = Scale(poffeq1, orient='vertical', resolution=100, command=poff_set_eq1_frequency,
                           from_=max(eq1_frequency_slider_values), to=min(eq1_frequency_slider_values))
# poff_eq1_frequency.set(freqDefault)
poff_eq1_frequency.grid(row=0, column=0)

poff_eq1_level = Scale(poffeq1, orient='vertical', digits=2, resolution=1, from_=10, to=-20, command=poff_set_eq1_level)
#poff_eq1_level.set(freqDefault)
poff_eq1_level.grid(row=0, column=1)

poff_eq1_bandw = Scale(poffeq1, orient='vertical', digits=2, from_=10, to=1, command=poff_set_eq1_bandw)
#poff_eq1_bandw.set(freqDefault)
poff_eq1_bandw.grid(row=0, column=2)

poff_eq2_label = LabelFrame(noproc, text=" Parametric EQ 2 ")
poff_eq2_label.grid(row=0, column=3, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

Label(poff_eq2_label, text="Frequency").grid(row=1, column=0)
Label(poff_eq2_label, text="Level").grid(row=1, column=1)
Label(poff_eq2_label, text="Bandwidth").grid(row=1, column=2)

poff_eq2_frequency = Scale(poff_eq2_label, orient='vertical', resolution=100, command=poff_set_eq2_frequency,
                           from_=max(eq2_frequency_slider_values), to=min(eq2_frequency_slider_values))
#poff_eq2_frequency.set(freqDefault)
poff_eq2_frequency.grid(row=0, column=0)

poff_eq2_level = Scale(poff_eq2_label, orient='vertical', digits=2, resolution=1, from_=10, to=-20,
                       command=poff_set_eq2_level)
#poff_eq2_level.set(freqDefault)
poff_eq2_level.grid(row=0, column=1)

poff_eq2_bandw = Scale(poff_eq2_label, orient='vertical', digits=2, from_=10, to=1, command=poff_set_eq2_bandw)
#poff_eq2_bandw.set(freqDefault)
poff_eq2_bandw.grid(row=0, column=2)

poff_eq3_label = LabelFrame(noproc, text=" Parametric EQ 3 ")
poff_eq3_label.grid(row=0, column=6, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

Label(poff_eq3_label, text="Frequency").grid(row=1, column=0)
Label(poff_eq3_label, text="Level").grid(row=1, column=1)
Label(poff_eq3_label, text="Bandwidth").grid(row=1, column=2)

poff_eq3_frequency = Scale(poff_eq3_label, orient='vertical', resolution=100, command=poff_set_eq3_frequency,
                           from_=max(eq3_frequency_slider_values), to=min(eq3_frequency_slider_values))
#poff_eq3_frequency.set(freqDefault)
poff_eq3_frequency.grid(row=0, column=0)

poff_eq3_level = Scale(poff_eq3_label, orient='vertical', digits=2, resolution=1, from_=10, to=-20,
                       command=poff_set_eq3_level)
#poff_eq3_level.set(freqDefault)
poff_eq3_level.grid(row=0, column=1)

poff_eq3_bandw = Scale(poff_eq3_label, orient='vertical', digits=2, from_=10, to=1, command=poff_set_eq3_bandw)
#poff_eq3_bandw.set(freqDefault)
poff_eq3_bandw.grid(row=0, column=2)

# This section is for the settings when the proc is on....

procon = LabelFrame(master, text=" Settings for EQ when the Processor is 'ON' ", font=('courier', 15, 'bold'))
procon.grid(row=10, column=0, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

pon_eq1 = LabelFrame(procon, text=" Parametric EQ 1 ")
pon_eq1.grid(row=0, column=0, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

Label(pon_eq1, text="Frequency").grid(row=1, column=0)
Label(pon_eq1, text="Level").grid(row=1, column=1)
Label(pon_eq1, text="Bandwidth").grid(row=1, column=2)

pon_eq1_frequency = Scale(pon_eq1, orient='vertical', resolution=100, command=pon_set_eq1_frequency,
                          from_=max(eq1_frequency_slider_values), to=min(eq1_frequency_slider_values))
#pon_eq1_frequency.set(freqDefault)
pon_eq1_frequency.grid(row=0, column=0)

pon_eq1_level = Scale(pon_eq1, orient='vertical', digits=2, resolution=1, from_=10, to=-20, command=pon_set_eq1_level)
pon_eq1_level.set(freqDefault)
pon_eq1_level.grid(row=0, column=1)

pon_eq1_bandw = Scale(pon_eq1, orient='vertical', digits=2, from_=10, to=1, command=pon_set_eq1_bandw)
#pon_eq1_bandw.set(freqDefault)
pon_eq1_bandw.grid(row=0, column=2)

pon_eq2_label = LabelFrame(procon, text=" Parametric EQ 2 ")
pon_eq2_label.grid(row=0, column=3, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

Label(pon_eq2_label, text="Frequency").grid(row=1, column=0)
Label(pon_eq2_label, text="Level").grid(row=1, column=1)
Label(pon_eq2_label, text="Bandwidth").grid(row=1, column=2)

pon_eq2_frequency = Scale(pon_eq2_label, orient='vertical', resolution=100, command=pon_set_eq2_frequency,
                          from_=max(eq2_frequency_slider_values), to=min(eq2_frequency_slider_values))
#pon_eq2_frequency.set(freqDefault)
pon_eq2_frequency.grid(row=0, column=0)

pon_eq2_level = Scale(pon_eq2_label, orient='vertical', digits=2, resolution=1, from_=10, to=-20,
                      command=pon_set_eq2_level)
#pon_eq2_level.set(freqDefault)
pon_eq2_level.grid(row=0, column=1)

pon_eq2_bandw = Scale(pon_eq2_label, orient='vertical', digits=2, from_=10, to=1, command=pon_set_eq2_bandw)
#pon_eq2_bandw.set(freqDefault)
pon_eq2_bandw.grid(row=0, column=2)

pon_eq3_label = LabelFrame(procon, text=" Parametric EQ 3 ")
pon_eq3_label.grid(row=0, column=6, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)

Label(pon_eq3_label, text="Frequency").grid(row=1, column=0)
Label(pon_eq3_label, text="Level").grid(row=1, column=1)
Label(pon_eq3_label, text="Bandwidth").grid(row=1, column=2)

pon_eq3_frequency = Scale(pon_eq3_label, orient='vertical', resolution=100, command=pon_set_eq3_frequency,
                          from_=max(eq3_frequency_slider_values), to=min(eq3_frequency_slider_values))
#pon_eq3_frequency.set(freqDefault)
pon_eq3_frequency.grid(row=0, column=0)

pon_eq3_level = Scale(pon_eq3_label, orient='vertical', digits=2, resolution=1, from_=10, to=-20,
                      command=pon_set_eq3_level)
#pon_eq3_level.set(freqDefault)
pon_eq3_level.grid(row=0, column=1)

pon_eq3_bandw = Scale(pon_eq3_label, orient='vertical', digits=2, from_=10, to=1, command=pon_set_eq3_bandw)
#pon_eq3_bandw.set(freqDefault)
pon_eq3_bandw.grid(row=0, column=2)

# This section is to have a set of buttons that will turn the proc and the EQ on and off....

eq_control_frame = LabelFrame(master, text=" Mic EQ On/Off ", font=('courier', 15, 'bold'))
eq_control_frame.grid(row=20, column=0, columnspan=1, rowspan=8, sticky='EW', padx=5, pady=5)

eq_off_button = Button(eq_control_frame, text="TURN EQ OFF", command=eq_off)
eq_off_button.grid(row=0, column=0)

eq_on_button = Button(eq_control_frame, text="TURN EQ ON", command=eq_on)
eq_on_button.grid(row=0, column=1)

proc_control_frame = LabelFrame(master, text=" Processor On/Off ", font=('courier', 15, 'bold'))
proc_control_frame.grid(row=20, column=1, columnspan=1, rowspan=8, sticky='EW', padx=5, pady=5)

proc_off_button = Button(proc_control_frame, text="TURN PROC OFF", command=proc_off)
proc_off_button.grid(row=0, column=0)

proc_on_button = Button(proc_control_frame, text="TURN PROC ON", command=proc_on)
proc_on_button.grid(row=0, column=1)

###############################
# Com Port Stuff

radio_connect_frame = LabelFrame(master, text=" Radio Connection ", font=('courier', 15, 'bold'))
radio_connect_frame.grid(row=30, column=0, columnspan=1, rowspan=8, sticky='EW', padx=5, pady=5)

radio_connect_button = Button(radio_connect_frame, text="Connect", state='normal', highlightbackground='#db3328',
                              command=open_serial)
radio_connect_button.grid(row=0, column=0)

radio_disconnect_button = Button(radio_connect_frame, text="Disconnect", command=close_serial)
radio_disconnect_button.grid(row=0, column=1)

comport_frame = LabelFrame(master, text=" Com Port Selection ", font=('courier', 15, 'bold'))
comport_frame.grid(row=30, column=1, columnspan=1, rowspan=8, sticky='EW', padx=5, pady=5)

cbcom = ttk.Combobox(comport_frame, text="Select COM", values=serial_ports())
cbcom.grid(row=1, column=0)

cbbaud = ttk.Combobox(comport_frame, text="Select Baud Rate", values=["4800", "9600", "19200", "38400"])
cbbaud.grid(row=1, column=1)

# assign function to comboboxs
cbcom.bind('<<ComboboxSelected>>', com_on_select)

cbbaud.bind('<<ComboboxSelected>>', baud_on_select)

mainloop()
