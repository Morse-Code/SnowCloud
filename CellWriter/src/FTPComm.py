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
        self.newLine = '\r\n'

    def initModem(self,
                  port='/dev/ttyUSB0',
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
        print "ATE0\t\t",
        responseConfirm = self.sendCommand('E0')[2]
        while responseConfirm != 'OK':
            time.sleep(.5)
            responseConfirm = self.sendCommand('E0')[2]
        print responseConfirm
        print "AT\t\t",
        responseConfirm = self.sendCommand('')[2]
        while responseConfirm != 'OK':
            time.sleep(.5)
            responseConfirm = self.sendCommand('')[2]
        print responseConfirm
        time.sleep(1)
        return

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
        :type self: FTPComm.ATCommands
          by a ':'.
        """
        responseConfirm = ''
        responseValue = ''
        responseType = ''
        data = ''
        data = self.ser.read(256)
        while data == '':
            time.sleep(1)
            data = self.ser.read(512)
        r = re.compile("(\s*((?P<type>\S+):)\s*(?P<value>\S+.+)"
                       "*)*\s*[\n\r]+(?P<ok>OK)*")
        m = r.match(data)
        if m.group('type'):
            responseType = m.group('type')
        if m.group('value'):
            responseValue = m.group('value').strip()
        if m.group('ok'):
            responseConfirm = m.group('ok').strip()
        self.ser.flush()
        return responseType, responseValue, responseConfirm

    def closeConn(self):
        """
        """
        self.ser.close()

    def checkSignal(self):
        """
        Issues AT+CSQ command to check signal quality. First value of
        tuple in AT command response has valid range 0-31.

        :type self: FTPComm.ATCommands
        :return: 1 if success, other if error
        :rtype: int
        """
        command = '+CSQ'
        print command + '\t\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while (int(responseValue.split(',')[0]) == 99 or responseConfirm !=
               'OK'):
            time.sleep(1)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print responseConfirm + '\t\t\t',
        print 'Signal: ' + responseValue.split(',')[0]
        return 1

    def checkSIM(self):
        """Check to make sure the SIM card is ready.

        :type self: FTPComm.ATCommands
        :return: 1 if success; otherwise != 1
        :rtype: int
        """
        command = '+CPIN?'
        print command + '\t\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while responseValue != 'READY' or responseConfirm != 'OK':
            time.sleep(.5)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print responseConfirm + '\t\t\t',
        print 'SIM: ' + responseValue
        return 1

    def attachNetwork(self):
        """
        :type self: FTPComm.ATCommands
        """
        command = '+AIPDCONT="Embeddedworks.globalm2m.net"'
        print '+AIPDCONT' + '\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while responseValue.split(',')[0] != '"Embeddedworks.globalm2m.net"'\
        or responseConfirm != 'OK':
            time.sleep(.5)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print responseConfirm + '\t\t\t',
        print 'APN: ' + responseValue.split(',')[0]
        return 1

    def activateGPRS(self):
        """
        Activate GPRS data connection.
        :type self: FTPComm.ATCommands
        :return:
        :rtype:
        """
        command = '+AIPA=1'
        print command + '\t\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while responseConfirm != 'OK':
            time.sleep(.5)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print responseConfirm + '\t\t\t',
        print 'GPRS: ' + responseValue.split(',')[1]
        return 1

    def setAutoQuality(self):
        """
        :type self: FTPComm.ATCommands
        """
        command = '+AIPQREQ=0,0,0,0,0'
        print command[:8] + '\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while responseConfirm != 'OK':
            time.sleep(.5)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print responseConfirm + '\t\t\t',
        print 'AIPQREQ: ' + responseValue
        return 1

    #noinspection PyTypeChecker
    def FTPconnect(self,
                   IP='174.63.100.132',
                   port=21,
                   user='morsecp',
                   pw='!1Morsecp'):
        """
        :type self: FTPComm.ATCommands
        :type IP: str
        :type port: int
        :type user: str
        :type pw: str
        """
        command = '+AFTPO="%(ip)s",%(p)d,"%(u)s","%(pw)s"' % {'ip': IP, 'p': port,
                                                          'u': user, 'pw': pw}
        #print '\n' + command
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while responseValue != 'Login On':
            print command[:6] + '\t\t',
            print responseConfirm + '\t\t\t',
            print 'AFTPO: ' + responseValue
            time.sleep(.5)
            self.activateGPRS()
            time.sleep(.5)
            #            print command
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print command[:6] + '\t\t',
        print responseConfirm + '\t\t\t',
        print 'AFTPO: ' + responseValue
        pass

    def FTPclose(self):
        """
        :return:
        :rtype:
        """
        command = '+AFTPC'
        print command + '\t\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while responseValue != '0' or responseConfirm != 'OK':
            time.sleep(.5)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print responseConfirm + '\t\t\t',
        print 'FTPClosed: ' + responseValue
        pass

    def FTPsettype(self):
        """
        :type self: FTPComm.ATCommands

        :return:
        :rtype:
        """
        command = '+AFTPTYPE=1'
        print command[:9] + '\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while responseConfirm != 'OK':
            time.sleep(.5)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print responseConfirm + '\t\t\t',
        print 'AFTPTYPE: ' + responseValue
        pass

    def FTPsetpasv(self):
        """
        :type self: FTPComm.ATCommands

        :return:
        :rtype:
        """
        command = '+AFTPPASV=1'
        print command[:9] + '\t',
        responseValue, responseConfirm = self.sendCommand(command)[1:3]
        while responseConfirm != 'OK':
            time.sleep(.5)
            responseValue, responseConfirm = self.sendCommand(command)[1:3]
        print responseConfirm + '\t\t\t',
        print 'AFTPPASV: ' + responseValue

        pass


def main():
    """
    Main method.
    """
    print '\n\nCmnd\t|\tConfirm\t|\tValue'
    modem = ATCommands()
    modem.initModem()
    time.sleep(1)
    modem.checkSignal()
    time.sleep(1)
    modem.checkSIM()
    time.sleep(1)
    modem.attachNetwork()
    time.sleep(1)
    modem.activateGPRS()
    time.sleep(1)
    modem.setAutoQuality()
    time.sleep(1)
    modem.FTPconnect()
    time.sleep(1)
    modem.FTPsettype()
    time.sleep(1)
    modem.FTPsetpasv()
    time.sleep(1)
    modem.FTPclose()
    time.sleep(1)
    modem.closeConn()


if __name__ == "__main__":
    #noinspection PyArgumentList
    main()
