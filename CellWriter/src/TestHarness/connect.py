import serial
import sys
import time
import logging

logger = logging.getLogger('connectiontest')
# noinspection PyArgumentEqualDefault
hdlr = logging.handlers.RotatingFileHandler(
    '/root/snowcloud/ARM/cm/CellWriter/log/connectiontest.log', mode='a',
    maxBytes=50000,
    backupCount=100)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def FTPsendData(ser, path):
    """
    :type self: ftpcomm.ATCommands

    :return:
    :rtype:
    """
    # print command[:9] + '\t',
    ser.write("AT+AFTPDATA\r")
    time.sleep(1)
    tries = 1
    while tries <= 5:
        response = ser.read(256)
        if response.find('CONNECT') >= 0:
            connection = True
            logger.info("CONNECTION ESTABLISHED. READY TO SEND")
            break
        elif response.find('ERROR') >= 0:
            ser.write("AT+AFTPDATA\r")
            logger.warn("CONNECTION ERROR. RETRYING")
        else:
            logger.warn("UNPARSED RESPONSE")
        time.sleep(1)
        tries += 1
    if connection:
        print "connect"
    else:
        print "abort"


def main(argv):
    ser = argv[1]
    path = argv[2]
    FTPsendData(ser, path)

if __name__ == "__main__":
    # noinspection PyArgumentList
    main(sys.argv[1:])

