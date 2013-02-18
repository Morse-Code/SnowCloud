#!/usr/bin/env python

# FTPComm
# 12/15/12
__author__ = 'Christopher Morse'
import shutil
import sys
import time
import os
import logging
import logging.handlers

logger = logging.getLogger('ftpcomm')
# noinspection PyArgumentEqualDefault
hdlr = logging.handlers.RotatingFileHandler(
    '/root/snowcloud/ARM/cm/CellWriter/log/ftpcomm.log', mode='a', maxBytes=50000,
    backupCount=100)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info("************** START **************")


# noinspection PyClassicStyleClass
# class ATCommands:
#     """
#     AT Command set class. Contains methods to intitialize serial connection
#     to ADH8066 modem and issue standard set of commands to establish and
#     verify modem data communication.
#     """
#
#     def __init__(self):
#         """
#         Constructor for ATCommands.
#         """
#         self.newLine = '\r\n'
#
#     def initModem(self,
#                   port='/dev/ttyUSB0',
#                   baudrate=115200,
#                   timeout=1):
#         """
#         Initializes serial connection to modem. Issues 'AT' command to
#         verify 'OK' response. Loops until 'OK'.
#
#         Issues 'ATE0' to turn off echo. Loops until 'OK'.
#
#         :type self: ftpcomm.ATCommands
#         :type port: str
#         :type baudrate: int
#         :type timeout: int
#         """
#         self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
#         self.ser.flush()
#         # print "ATE0\t\t",
#         command = 'E0'
#         responseConfirm = self.sendCommand(command)[2]
#         while responseConfirm != 'OK':
#             time.sleep(.5)
#             responseConfirm = self.sendCommand('E0')[2]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         # print responseConfirm
#         # print "AT\t\t",
#         command = ''
#         responseConfirm = self.sendCommand(command)[2]
#         while responseConfirm != 'OK':
#             time.sleep(.5)
#             responseConfirm = self.sendCommand('')[2]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         # print responseConfirm
#         time.sleep(1)
#         return
#
#     def sendCommand(self, command, getline=True):
#         """
#         Sends formatted AT Command over serial connection. Prefixes passed
#         command string with 'AT+', and appends '\r' after.
#
#         :type self: ftpcomm.ATCommands
#         :type command: str
#         :type getline: bool
#         """
#         self.ser.write('AT' + command + '\r')
#         self.ser.flush()
#         if getline:
#             return self.ReadLine()
#
#     def ReadLine(self, retries=0):
#         """
#         Returns 3-tuple by reading modem output from serial port. Regular
#         expressions used to parse responses into tokens
#
#         responseConfirm is the confirmation at the end of a response from
#         the modem. Will ususlly be 'OK' or 'ERROR'.
#
#         responseValue if present will be the acutal tuple of values returned
#          according to the AT Command issued. ie. signal quality
#
#          responseType is the ususlly the echo of the command issued followed
#         :type self: FTPComm.ATCommands
#           by a ':'.
#         """
#         responseConfirm = ''
#         responseValue = ''
#         responseType = ''
#         # if retries > 10:
#         #     return responseType, responseValue, responseConfirm
#         # data = self.ser.read(1)              # read one, blocking
#         # n = self.ser.inWaiting()
#         # if n:
#         #     print n
#         #     data += self.ser.read(n)
#         # if data:
#         #     print data
#         data = self.ser.read(256)
#         while data == '':
#             time.sleep(1)
#             data = self.ser.read(256)
#             # print data
#         r = re.compile("(\s*((?P<type>\S+):)\s*(?P<value>[\S+\s*]+)"
#                        "*)*\s*[\r\n]*(?P<ok>\w{2,})\r*$")
#         m = r.match(data)
#         if m and m.group('type'):
#             responseType = m.group('type')
#             # print responseType
#         if m and m.group('value'):
#             responseValue = m.group('value').strip()
#             # print responseValue
#         if m and m.group('ok'):
#             responseConfirm = m.group('ok').strip()
#             # print responseConfirm
#         # self.ser.flush()
#         return responseType, responseValue, responseConfirm
#         # else:
#         #     retries += 1
#         #     return self.ReadLine(retries)
#
#     def closeConn(self):
#         """
#         """
#         self.activateGPRS(on=0)
#         self.ser.close()
#
#     def checkSignal(self):
#         """
#         Issues AT+CSQ command to check signal quality. First value of
#         tuple in AT command response has valid range 0-31.
#
#         :type self: ftpcomm.ATCommands
#         :return: 1 if success, other if error
#         :rtype: int
#         """
#         command = '+CSQ'
#         # print command + '\t\t',
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         while responseConfirm != 'OK':
#             time.sleep(1)
#             responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         # print responseConfirm + '\t\t\t',
#         # print 'Signal: ' + responseValue.split(',')[0]
#         return 1
#
#     def checkSIM(self):
#         """Check to make sure the SIM card is ready.
#
#         :type self: ftpcomm.ATCommands
#         :return: 1 if success; otherwise != 1
#         :rtype: int
#         """
#         command = '+CPIN?'
#         # print command + '\t\t',
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         while responseValue != 'READY' or responseConfirm != 'OK':
#             time.sleep(.5)
#             responseValue, responseConfirm = self.sendCommand(command)[1:3]
#             # print responseConfirm + '\t\t\t',
#         # print 'SIM: ' + responseValue
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         return 1
#
#     def attachNetwork(self):
#         """
#         :type self: ftpcomm.ATCommands
#         """
#         command = '+AIPDCONT="Embeddedworks.globalm2m.net"'
#         # print '+AIPDCONT' + '\t',
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         while responseValue.split(',')[0] != '"Embeddedworks.globalm2m.net"' or\
#               responseConfirm != 'OK':
#             time.sleep(.5)
#             responseValue, responseConfirm = self.sendCommand(command)[1:3]
#             # print responseConfirm + '\t\t\t',
#         # print 'APN: ' + responseValue.split(',')[0]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         return 1
#
#     def activateGPRS(self, on=1):
#         """
#         Activate GPRS data connection.
#         :type self: ftpcomm.ATCommands
#         :return:
#         :rtype:
#         """
#         command = '+AIPA=%(on)s' % {'on': on}
#         # print command + '\t\t',
#         responseType, responseValue, responseConfirm = self.sendCommand(
#             command)
#         while responseType.find('ERROR') >= 0:
#             time.sleep(.5)
#             responseType, responseValue, responseConfirm = self.sendCommand(
#                 command)
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         # print responseConfirm + '\t\t\t',
#         # print 'GPRS: ' + responseValue.split(',')[1]
#         return 1
#
#     def setAutoQuality(self):
#         """
#         :type self: ftpcomm.ATCommands
#         """
#         command = '+AIPQREQ=0,0,0,0,0'
#         # print command[:8] + '\t',
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         while responseConfirm != 'OK':
#             time.sleep(.5)
#             responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         # print responseConfirm + '\t\t\t',
#         # print 'AIPQREQ: ' + responseValue
#         return 1
#
#     # noinspection PyTypeChecker
#     def FTPconnect(self,
#                    IP='174.63.100.132',
#                    port=21,
#                    user='christophermorse',
#                    pw='driven24age4you'):
#         """
#         :type self: ftpcomm.ATCommands
#         :type IP: str
#         :type port: int
#         :type user: str
#         :type pw: str
#         """
#         command = '+AFTPO="%(ip)s",%(p)d,"%(u)s","%(pw)s"' % {'ip': IP,
#                                                               'p': port,
#                                                               'u': user,
#                                                               'pw': pw}
#         # print '\n' + command
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         while responseValue != 'Login On':
#             # print command[:6] + '\t\t',
#             # print responseConfirm + '\t\t\t',
#             # print 'AFTPO: ' + responseValue
#             time.sleep(.5)
#             self.activateGPRS(on=0)
#             self.activateGPRS()
#             time.sleep(.5)
#             #            print command
#             responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command[:6],
#                                                             'r': responseConfirm})
#         # print command[:6] + '\t\t',
#         # print responseConfirm + '\t\t\t',
#         # print 'AFTPO: ' + responseValue
#         pass
#
#     def FTPsettype(self):
#         """
#         :type self: ftpcomm.ATCommands
#
#         :return:
#         :rtype:
#         """
#         command = '+AFTPTYPE=1'
#         # print command[:9] + '\t',
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         while responseConfirm != 'OK':
#             time.sleep(.5)
#             responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         # print responseConfirm + '\t\t\t',
#         # print 'AFTPTYPE: ' + responseValue
#         pass
#
#     def FTPsetpasv(self):
#         """
#         :type self: ftpcomm.ATCommands
#
#         :return:
#         :rtype:
#         """
#         command = '+AFTPPASV=1'
#         # print command[:9] + '\t',
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         while responseConfirm != 'OK':
#             time.sleep(.5)
#             responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         # print responseConfirm + '\t\t\t',
#         # print 'AFTPPASV: ' + responseValue
#
#         pass
#
#     def FTPsetFile(self, fileName):
#         """
#         :type self: ftpcomm.ATCommands
#
#         :return:
#         :rtype:
#         """
#         command = '+AFTPSTOR="~/ARM-RecievedData/%(f)s"' % {'f': fileName}
#         # print command[:9] + '\t',
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         time.sleep(1)
#         while responseConfirm != 'OK':
#             time.sleep(.5)
#             responseValue, responseConfirm = self.ReadLine()[1:3]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#
#         pass
#
#     def FTPsendData(self, path):
#         """
#         :type self: ftpcomm.ATCommands
#
#         :return:
#         :rtype:
#         """
#         command = '+AFTPDATA'
#         # print command[:9] + '\t',
#         responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         while responseConfirm != 'CONNECT':
#             time.sleep(.5)
#             responseValue, responseConfirm = self.sendCommand(command)[1:3]
#         logger.info("Command: %(c)s --> Response: %(r)s" % {'c': command,
#                                                             'r': responseConfirm})
#         f = open(path, 'r')
#         for line in f:
#             self.sendLine(line)
#         f.close()
#         pass
#
#     # noinspection PyBroadException
#     def sendLine(self, line, tries=0):
#         if tries > 10:
#             self.ser.flush()
#             return
#         try:
#             self.ser.write(line)
#             self.ser.flush()
#             time.sleep(.1)
#             return
#         except:
#             tries += 1
#             self.ser.flushInput()
#             time.sleep(.2)
#             logger.warning("Exception sending. Flushing input to retry.")
#             self.sendLine(line, tries)
#             # print "no"
#
#     def FTPclose(self):
#         """
#         :return:
#         :rtype:
#         """
#         self.sendLine('+')
#         time.sleep(0.3)
#         self.sendLine('+')
#         time.sleep(0.3)
#         self.sendLine('+')
#         time.sleep(1)
#         logger.info('Termination string "+++" sent.')
#         responseConfirm = self.ReadLine()[2]
#         tries = 1
#         while responseConfirm.find("OK") < 0 and tries < 10:
#             self.sendLine('+')
#             time.sleep(0.3)
#             self.sendLine('+')
#             time.sleep(0.3)
#             self.sendLine('+')
#             time.sleep(1)
#             responseConfirm = self.ReadLine()[2]
#             tries += 1
#         if tries >= 10:
#             self.ser.flushInput()
#             time.sleep(1)
#             self.ser.flushOutput()
#             time.sleep(1)
#         logger.info('Termination string "+++" accepted.')
#         command = '+AFTPC'
#         logger.info("Command: %(c)s" % {'c': command})
#         # print 'FTPClosed: ' + responseValue
#         pass
#
#         # def abortAndRetry(self, retry=True):
#         #     if retry:
#         #
#         #     pass


# noinspection PyUnusedLocal,PyArgumentEqualDefault
def main():
    """
    Main method.
    """
    # infile = ''
    # try:
    #     opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    # except getopt.GetoptError:
    #     print 'ftpcomm.py -i <infile>'
    #     sys.exit(2)
    # for opt, arg in opts:
    #     if opt == '-h':
    #         print 'ftpcomm.py -i <infile>'
    #         sys.exit()
    #     elif opt in ("-i", "--ifile"):
    #         infile = arg
    # print 'Input file is "', infile
    # f = open(fileName, 'w')
    abortedJobPath = "/root/snowcloud/ARM/cm/CellWriter/FailedData/"
    fileName = "%(t)d.txt" % {'t': time.time()}
    path = "/root/snowcloud/ARM/cm/CellWriter/SentData/%(f)s" % {'f': fileName}
    exitStatus = os.popen(
        "/root/snowcloud/ARM/cm/CellWriter/dbReader > "
        "%(p)s" %
        {'p': path})
    ftp = os.popen("/root/snowcloud/ARM/cm/CellWriter/ftpprocess.py -i %(p)s" % {
        'p': path}, 'r', 1)
    tries = 1
    while True:
        status = ftp.readline()
        print status
        if status.find('success') >= 0:
            exitStatus = ftp.close()
            logger.info("Child process successful. Data file sent.")
            break
        elif tries > 2:
            exitStatus = ftp.close()
            shutil.move(path, abortedJobPath)
            print "Exit status of child: ", exitStatus
            print "Failed. Moving failed file to..."
            logger.error("Failed Send. Moving failed file to ./FailedData")
            break
        elif status.find('abort') >= 0:
            exitStatus = ftp.close()
            logger.warning("Process ABORT ----- RETRYING ")
            print "Exit status of child: ", exitStatus
            print "Retrying"
            ftp = os.popen("/root/snowcloud/ARM/cm/CellWriter/ftpprocess.py -i %(p)s" % {
                'p': path}, 'r', 1)
            tries += 1

    # if exitStatus ==
    # print '\n\nCmnd\t|\tConfirm\t|\tValue'
    # modem = ATCommands()
    # modem.initModem()
    # time.sleep(1)
    # modem.checkSignal()
    # time.sleep(1)
    # modem.checkSIM()
    # time.sleep(1)
    # modem.attachNetwork()
    # time.sleep(1)
    # modem.activateGPRS()
    # time.sleep(1)
    # modem.setAutoQuality()
    # time.sleep(1)
    # modem.FTPconnect()
    # time.sleep(1)
    # modem.FTPsettype()
    # time.sleep(1)
    # modem.FTPsetpasv()
    # time.sleep(1)
    # modem.FTPsetFile(fileName)
    # time.sleep(1)
    # modem.FTPsendData(path)
    # time.sleep(1)
    # modem.FTPclose()
    # time.sleep(1)
    # modem.closeConn()
    logger.info("************** END **************")


if __name__ == "__main__":
    # noinspection PyArgumentList
    main()
    sys.exit(0)
