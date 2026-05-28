import serial
import time

serial = serial.Serial('/dev/ttyACM0', 115200,timeout=1)
time.sleep(2)

try:
    while True:

        print("Sending:1")
        serial.write(b'1')

        time.sleep(2)

        print("Sending:0")
        serial.write(b'0')

        time.sleep(2)

except KeyboardInterrupt:
    print("stop")
    ser.close()



