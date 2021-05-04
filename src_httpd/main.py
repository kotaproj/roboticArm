import sys
import machine
import socket
import time

from stepper import Stepper
from servo import Servo

# servo
SERVO_NO1_PIN = (16)

# smotor
MOTOR_STEPS = (2048)

SMOTOR_NO1_PIN1 = (25)
SMOTOR_NO1_PIN2 = (26)
SMOTOR_NO1_PIN3 = (27)
SMOTOR_NO1_PIN4 = (13)

SMOTOR_NO2_PIN1 = (17)
SMOTOR_NO2_PIN2 = (5)
SMOTOR_NO2_PIN3 = (18)
SMOTOR_NO2_PIN4 = (19)

SMOTOR_NO3_PIN1 = (15)
SMOTOR_NO3_PIN2 = (21)
SMOTOR_NO3_PIN3 = (22)
SMOTOR_NO3_PIN4 = (23)

# Set your Wifi SSID and password
SSID = "XXXXXXXXXXXX"
PASS = "XXXXXXXXXXXX"

class HttpdProc():
    
    def __init__(self):
        self._servo = {}
        self._servo["no1"] = Servo(SERVO_NO1_PIN)
        self._smotor = {}
        self._smotor["no1"] = Stepper(MOTOR_STEPS, SMOTOR_NO1_PIN1, SMOTOR_NO1_PIN2, SMOTOR_NO1_PIN3, SMOTOR_NO1_PIN4)
        self._smotor["no2"] = Stepper(MOTOR_STEPS, SMOTOR_NO2_PIN1, SMOTOR_NO2_PIN2, SMOTOR_NO2_PIN3, SMOTOR_NO2_PIN4)
        self._smotor["no3"] = Stepper(MOTOR_STEPS, SMOTOR_NO3_PIN1, SMOTOR_NO3_PIN2, SMOTOR_NO3_PIN3, SMOTOR_NO3_PIN4)
        return

    def _do_connect(self):
        import network
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            # wlan.connect('essid', 'password')
            wlan.connect(SSID, PASS)
            while not wlan.isconnected():
                pass
                # time.sleep(1)
                time.sleep(3)
                print(".")
        print('network config:', wlan.ifconfig())
        time.sleep(3)
        print('connect - done!!!')
        return


    def run(self):
        self._do_connect()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)

        while True:
            # If an exception occurs, reboot.
            try:
                conn, addr = s.accept()
                print("Got a connection from %s" % str(addr))
                request = conn.recv(1024* 2)
                request = str(request)
                print(request)

                # shutdown - For farm writing
                if "exit_htttpd" in request:
                    sys.exit()

                if len(request) == 0:
                    print("nodata!!!")
                    conn.close()
                    continue

                # parse
                # ex. GET http://ipadr:80?name=smotor&no=1&val=-2048&end=dummy
                #       => name = "smotor", no = "1", val = "-2048"
                name = request[request.find("name=") + len("name="): request.find("&no=")]
                no = request[request.find("&no=") + len("&no="): request.find("&val=")]
                val = request[request.find("&val=") + len("&val="):request.find("&end=")]

                # http response
                response = "response_dummy"
                conn.send("HTTP/1.1 200 OK")
                conn.send("Content-Type: text/html; encoding=utf8\nContent-Length: ")
                conn.send(str(len(response)))
                conn.send("\nConnection: close\n")
                conn.send("\n")
                conn.send(response)
                conn.close()

                if "servo" == name:
                    self._servo["no" + no].set_duty(int(val))
                if "smotor" == name:
                    self._smotor["no" + no].step(int(val))
            except:
                print('Error -> reboot')
                machine.deepsleep(3*1000)


def main():
    httpd_th = HttpdProc()
    httpd_th.run()
    return

# main()
