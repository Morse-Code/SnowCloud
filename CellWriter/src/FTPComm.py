# FTPComm
# 12/15/12

__author__ = 'Christopher Morse'

import time

import serial
import re


class ATCommands:
    """"""

    def __init__(self):
        """Constructor for """
        self.newLine = ('\r\n')

    def initModem(self, port='/dev/tty.usbserial-A9014MJT',
                  baudrate=115200,
                  timeout=1):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        while (self.sendCommand('') != 'OK'):
            time.sleep(.5)
        time.sleep(1)
        while (self.sendCommand('E0') != 'OK'):
            time.sleep(.5)
        return 1

    def checkSignal(self):
        command = '+CSQ'
        s = re.compile('\s*(.*:)*\s*(?P<signal>[0-9]+),.*')
        response = self.sendCommand(command)
        m = s.match(response)
        signal = m.group('signal')
        print(signal)
        return signal

    def sendCommand(self, command, getline=True):
        self.ser.write('AT' + command + '\r')
        data = ''
        if getline:
            data = self.ReadLine()
        return data

    def ReadLine(self):
        data = self.ser.read(256)
        print(data.split())
        data = data.strip()
        r = re.compile("\s*((?P<type>.+):)*\s*(?P<value>.+),*.*")
        m = r.match(data)
        responseType = m.group('type')
        responseValue = m.group('value')
        print(data)
        self.ser.flush()
        return data

    def closeConn(self):
        self.ser.close()


def main():
    modem = ATCommands()
    modem.initModem()
    print("Thats all folks")
    time.sleep(.5)
    modem.checkSignal()


if __name__ == "__main__":
    #noinspection PyArgumentList
    main()
    exit(0)