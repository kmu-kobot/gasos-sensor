import serial
import time
import requests
import RPi.GPIO as GPIO
import re
from firebase import *
from GTTS import tts

class main_cordinator(object):
    def __init__(self, device_num):
        # Init Serial COM
        GPIO.setmode(GPIO.BCM)
        self.xbee = serial.Serial()
        self.xbee.port = "/dev/ttyAMA1"
        self.xbee.baudrate = 9600
        self.xbee.timeout = 1
        self.xbee.writeTimeout = 1
        self.Manager_name = "대창너무조아"
        self.Protected_name = "최지희"
        self.address = "101호"

        # Init device_id
        self.device_id = device_num

        if not self.xbee.is_open:
            self.xbee.open()
            print("Port open status: ", self.xbee.is_open)
            print("Receive & Transfer start")


    def receive(self):
        self.xbee.flushInput()
        rsByte = self.xbee.readline().strip()
        print(rsByte)

        return rsByte

    def transfer(self, data):
        if type(data) == type(b''):
            self.xbee.write(data)
        else:
            data = re.sub('\n', '', data)
            tsData = bytes(data, 'utf-8')
            self.xbee.write(tsData)

    def update_status(self, status, value):
        self.data = {'device_id': self.device_id, 'status': status, 'value': value}

    def send_data(self, fcmCO, fcmLPG):
        if fcmCO > 85:
            print("FCM CO")
            sendMessage(self.Manager_name, "{0} CO가 위험수치입니다.".format(self.Protected_name))
            tts("{0}호 {1}씨 댁에서 CO 누출이 감지되었습니다.".format(self.address, self.Protected_name))
        if fcmLPG.find('warn') != -1:
            print("FCM LPG") 
            sendMessage(self.Manager_name, "{0} 가스가 누출되었습니다.".format(self.Protected_name))
            tts("{0}호 {1}씨 댁에서 LPG 누출이 감지되었습니다.".format(self.address, self.Protected_name))



    def device_off(self):
        time.sleep(0.1)
        self.xbee.close()


if __name__ == "__main__":
    dev = main_cordinator(1)
    doc_ref = db.collection(u'Manager_%s'%dev.Manager_name).document(u'Protected_%s'%dev.Protected_name)

    alter = 0
    while True:
        try:
            #print("Please type the device to check (LPG / CO / EXIT) :")
            if alter == 0:
                tsString = "LPG"
                alter = 1
            elif alter == 1:
                tsString = "CO"
                alter = 2
            elif alter == 2:
                dev.send_data(COStat, LPGrsString)
                uploadState(doc_ref, COStat, LPGrsString)
                alter = 0

            if tsString == "LPG":
                dev.transfer(tsString)
                time.sleep(0.1)
                rsByte = dev.receive()

                if rsByte == b'LPGOK':
                    print("LPG status is OK")
                    LPGrsString = "LPGOK"

                elif rsByte == b'LPGWARN':
                    print("LPG WARNING")
                    LPGrsString = "LPGWARN"

                # Implements
                #dev.send_data(rsString, '')
                print("Send OK")
                


            elif tsString == "CO":
                dev.transfer(tsString)
                time.sleep(0.2)
                rsByte = dev.receive()
                rsString = rsByte.decode('utf-8')

                if rsString == "WARNING":
                    COStat_Byte = dev.receive()
                    time.sleep(0.01)
                    COStat = int(COStat_Byte.decode('utf-8'))
                    print("COstat = {0}\n".format(COStat))
                else:
                    COStat = int(rsString)
                    print("COstat = {0}\n".format(COStat))

                # Implements
                #dev.send_data(rsString, COStat)
                print("Send OK")

            elif tsString == "EXIT":
                break
            else:
                print("Please Input the correct command")
                continue

        except KeyboardInterrupt:
            dev.device_off()
            break