# FTdx1200_EQ
This utility is designed to allow easy configuration of the EQ setting on the Yaesu FTdx-1200 radio.  It allows for realtime updates to the settings so that the user can monitor the effects while updating.

Controls are provided for both sets of EQ (proc on and proc off) and the user can selectivly turn the proc and EQ on and off to gauge the impact of the changes.

Currently there is no user interface to change the COM port so the user MUST edit the file and put the appropriate comport and baud rate in for their particular configuration.

This should run on both Windows and MAC OSX and I have tested on both of them.

This utility requires python 3.x with pyserial and tkinter.

Currently it is just the script but I hope to deliver both a Windows and Mac compiled executable soon.  Till then you will need to have python installed on your computer.
