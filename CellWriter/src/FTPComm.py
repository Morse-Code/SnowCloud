# FTPComm
# 12/15/12

__author__ = 'Christopher Morse'

import time
import serial
import re


class ATCommands:
    """
    AT Command set class. Contains methods to intitialize serial connection
    to ADH8066 modem and issue standard set of commands to establish and
    verify modem data communication.
    """

    def __init__(self):
        """
        Constructor for ATCommands.
        """
        self.newLine = ('\r\n')

    def initModem(self, port='/dev/tty.usbserial-A9014MJT',
                  baudrate=115200,
                  timeout=1):
        """
        Initializes serial connection to modem. Issues 'AT' command to
        verify 'OK' response. Loops until 'OK'.

        Issues 'ATE0' to turn off echo. Loops until 'OK'.

        :type self: FTPComm.ATCommands
        :type port: str
        :type baudrate: int
        :type timeout: int
        """
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        print "AT:\t\t",
        while self.sendCommand('')[2] != 'OK':
            time.sleep(.5)
        time.sleep(1)
        print '\n' + "ATE0:\t",
        while self.sendCommand('E0')[2] != 'OK':
            time.sleep(.5)
        return 1

    def checkSignal(self):
        """
        Issues AT+CSQ command to check signal quality. First value of
        tuple in AT command response has valid range 0-31.

        :type self: FTPComm.ATCommands
        :return: 1 if success, other if error
        :rtype: int
        """
        command = '+CSQ'
        print '\n' + 'AT+CSQ:\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while int(responseValue.split(',')[0]) == 99 or responseConfirm !=\
              'OK':
            time.sleep(1)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print ', Signal: ' + responseValue.split(',')[0]
        return 1

    def sendCommand(self, command, getline=True):
        """
        Sends formatted AT Command over serial connection. Prefixes passed
        command string with 'AT+', and appends '\r' after.

        :type self: FTPComm.ATCommands
        :type command: str
        :type getline: bool
        """
        self.ser.write('AT' + command + '\r')
        if getline:
            return self.ReadLine()

    def ReadLine(self):
        """
        Returns 3-tuple by reading modem output from serial port. Regular
        expressions used to parse responses into tokens

        responseConfirm is the confirmation at the end of a response from
        the modem. Will ususlly be 'OK' or 'ERROR'.

        responseValue if present will be the acutal tuple of values returned
         according to the AT Command issued. ie. signal quality

         responseType is the ususlly the echo of the command issued followed
          by a ':'.
        """
        responseConfirm = ''
        responseValue = ''
        responseType = ''
        data = self.ser.read(256)
        r = re.compile("(\s*((?P<type>\S+):)\s*(?P<value>\S+)"
                       "(,.*)*)*\s*(?P<ok>\S+)\s*")
        m = r.match(data)
        if (m.group('type')):
            responseType = m.group('type')
        if (m.group('value')):
            responseValue = m.group('value')
        if (m.group('ok')):
            responseConfirm = m.group('ok')
            print responseConfirm,
        self.ser.flush()
        return responseType, responseValue, responseConfirm

    def closeConn(self):
        self.ser.close()


def main():
    print '\n\nCmnd | Response'
    modem = ATCommands()
    modem.initModem()
    time.sleep(.5)
    modem.checkSignal()


if __name__ == "__main__":
    #noinspection PyArgumentList
    main()
    exit(0)