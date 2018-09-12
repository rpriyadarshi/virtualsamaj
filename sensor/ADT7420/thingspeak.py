from time import sleep
import urllib.request
from ADT7420 import *

myAPI = "3A8LZ0TLMX7W34EL"


def main():
    ts = ADT7420(1, 0x49, .240, '/home/pi/temp_mon.csv', False)
    print('Starting thingspeak.com push...')
    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    while True:
        try:
            ts.read_once()
            f = urllib.request.urlopen(baseURL + "&field1=%s" % ts.temp)
            print(f.read())
            f.close()
            sleep(15)  # uploads ADT7420 sensor values every 15 seconds

        except:
            print('Shutting down thingspeak.com push.')
            break


# call main
if __name__ == '__main__':
    main()
