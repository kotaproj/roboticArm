import time
import requests
from collections import OrderedDict

# Set the IP address of ESP32
ESP32_URL = "http://XXX.XXX.XXX.XXX:80"

def run_servo(val=70):
    """GET method
    - ex. http://ipadr:80?name=servo&no=1&val=70&end=dummy
    Args:
        val ([int]): [55-80]
    """
    payload = OrderedDict()
    payload['name'] = 'servo'
    payload['no'] = str(1)
    payload['val'] = str(val)
    payload['end'] = "dummy"
    r = requests.get(ESP32_URL, params=payload)
    print(r)
    return


def run_smmotor(no=1, val=0):
    """GET method
    - ex. http://ipadr:80?name=smotor&no=1&val=-2048&end=dummy
    Args:
        no ([int]): [1-3]
        val ([int]): [-2048 - +2048]
    """
    payload = OrderedDict()
    payload['name'] = 'smotor'
    payload['no'] = str(no)
    payload['val'] = str(val)
    payload['end'] = "dummy"
    r = requests.get(ESP32_URL, params=payload)
    print(r)
    return


def main():
    run_smmotor(1, -512)
    time.sleep(0.5)
    run_smmotor(1, 512)
    time.sleep(0.5)
    run_smmotor(2, 512)
    time.sleep(0.5)
    run_smmotor(2, -512)
    time.sleep(0.5)
    run_smmotor(3, 512)
    time.sleep(0.5)
    run_smmotor(3, -512)
    time.sleep(0.5)
    run_servo(80)
    time.sleep(0.5)
    run_servo(55)
    time.sleep(0.5)


if __name__ == "__main__":
    main()
