# FTPComm
# 12/15/12
import sys
import io

__author__ = 'Christopher Morse'

import serial

serialPort = serial.Serial(port='/dev/tty.Bluetooth-PDA-Sync',
                           baudrate=115200,
                           timeout=0, rtscts=True,
                           xonxoff=False)


def sendatcmd(cmd):
    serialPort.write('at' + cmd + '\r')


print 'Loading profile...',
sendatcmd('+npsda=0,2')


def main():
    sendatcmd("cmd")
    sendatcmd("hello")
    print("hello")


if __name__ == "__main__":
    #noinspection PyArgumentList
    main()
    exit(0)