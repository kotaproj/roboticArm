import time
import paho.mqtt.client as mqtt

HOST = '192.168.XXX.XXX'
PORT = 1883
TOPIC = 'topic_dev'

def publish_moji(topic, msg):
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(HOST, port=PORT, keepalive=60)
    client.publish(topic, msg)
    client.disconnect()
    return


def run_smmotor(no=1, val=0):
    str_cmd = "_smotor_no" + str(no) + "_val_" + str(val) + "_"
    publish_moji(TOPIC, str_cmd)
    return


def run_servo(val=70):
    str_cmd = "_servo_no" + str(1) + "_val_" + str(val) + "_"
    publish_moji(TOPIC, str_cmd)
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
