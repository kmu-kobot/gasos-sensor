import serial
import time
import requests
import RPi.GPIO as GPIO


class main_cordinator(object):
    def __init__(self, device_num):
        # Init Serial COM
        GPIO.setmode(GPIO.BCM)
        self.xbee = serial.Serial()
        self.xbee.port = "/dev/ttyAMA1"
        self.xbee.baudrate = 9600
        self.xbee.timeout = 1
        self.xbee.writeTimeout = 1

        # Init device_id
        self.device_id = device_num

        # Init requests
        self.url = 'http://127.0.0.1:52275/data'
        self.data = {'device_id': device_num, 'status': -1}
        self.headers = {'Content-Type': 'application/json'}

        # Create session
        self.session = requests.Session()

        if not self.xbee.is_open:
            self.xbee.open()
            print("Port open status: ", xbee.is_open)
            print("Receive & Transfer start")

    @staticmethod
    def receive():
        xbee.flushInput()
        rsByte = xbee.readline().strip()
        print(rsByte)

        return rsByte

    @staticmethod
    def transfer(data):
        if type(data) == type(b''):
            xbee.write(data)
        else:
            data = re.sub('\n', '', data)
            tsData = bytes(data, 'utf-8')
            xbee.write(tsData)

    def update_status(self, status, value):
        self.data = {'device_id': self.device_id, 'status': status, 'value': value}

    def send_data(self, status, value):
        if not status == '' or not value == '':
            self.update_status(status, value)
        try:
            request_id = self.session.post(self.url, json=self.data, headers=self.headers)
            if request_id == 200:
                print("Send success !")
        except requests.exceptions.RequestException as e:
            print(e)

    def device_off(self):
        time.sleep(0.1)
        self.xbee.close()


if __name__ == "__main__":
    dev = main_cordinator(1)
    while True:
        try:
            print("Please type the device to check (LPG / CO / EXIT) :")
            tsString = input()

            if tsString == "LPG":
                dev.transfer(tsString)
                time.sleep(0.1)
                rsByte = dev.receive()

                if rsByte == b'LPGOK':
                    print("LPG status is OK")

                elif rsByte == b'LPGWARN':
                    print("LPG WARNING")

                # Implements
                dev.send_data(rsString, '')

            elif tsString == "CO":
                dev.transfer(tsString)
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
                dev.send_data(rsString, COStat)

            elif tsString == "EXIT":
                break
            else:
                print("Please Input the correct command")
                continue

        except KeyboardInterrupt:
            dev.device_off()
            break