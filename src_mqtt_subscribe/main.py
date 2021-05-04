import sys
import machine
import time
from umqtt.simple2 import MQTTClient

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

# Set the IPAdrress of the MQTT broker
HOST = "192.168.xxx.xxx"
TOPIC = b"topic_dev"

class SubsProc():
    
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
        # self._wiFiAccessPoint(AP_SSID,AP_PASSWORD,IP,'255.255.255.0',IP,'8.8.8.8')
        self._do_connect()

        # Received messages from subscriptions will be delivered to this callback
        def sub_cb(topic, msg, retain, dup):
            print((topic, msg, retain, dup))
            # parse
            msg = str(msg)
            # >>> bmoji =  b'_servo_no1_val_100_'
            # >>> moji = str(bmoji)
            # >>> _, name, no, _, val, _ = moji.split("_")
            
            if "exit" in msg:
                sys.exit()
            
            _, name, no, _, val, _ = msg.split("_")
            print("name:", name)
            print("no:", no)
            print("val:", val)

            if "servo" == name:
                self._servo[no].set_duty(int(val))
            if "smotor" == name:
                self._smotor[no].step(int(val))
            return

        blocking_method=False

        # If an exception occurs, reboot.
        try:
            c = MQTTClient("umqtt_client", HOST)
            c.set_callback(sub_cb)
            c.connect()
            # c.subscribe(b"foo_topic")
            c.subscribe(TOPIC)

            while True:
                if blocking_method:
                    # Blocking wait for message
                    c.wait_msg()
                else:
                    # Non-blocking wait for message
                    c.check_msg()
                    # Then need to sleep to avoid 100% CPU usage (in a real
                    # app other useful actions would be performed instead)
                    time.sleep(1)

            c.disconnect()
        except:
            print('Error -> reboot')
            machine.deepsleep(3*1000)

def main():
    subs_th = SubsProc()
    subs_th.run()
    return

# main()
