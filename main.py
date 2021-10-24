import argparse
import RPi.GPIO as GPIO
from pirc522 import RFID
import time


def read_rfid(reader):
    util = reader.util()

    while True:
        # Wait for tag
        reader.wait_for_tag()

        # Request tag
        (error, data) = reader.request()
        if not error:
            print("\nDetected")

            (error, uid) = reader.anticoll()
            if not error:
                # Print UID
                print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))

                util.set_tag(uid)
                util.auth(reader.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

                util.dump()
                util.deauth()

                break

        time.sleep(1)


def write_rfid(reader, text):
    reader.write(text)


def main(opt):
    mode = opt.mode[0]

    GPIO.cleanup()

    reader = RFID()

    if mode == "c":
        # print("Copying RFID card, waiting for first card...")
        #
        # id, text = read_rfid(reader)
        #
        # print("Card read, waiting for second card...")
        #
        # write_rfid(reader, text)
        #
        print("Done...")

    elif mode == "r":
        print("Reading RFID Card, waiting for card...")

        read_rfid(reader)

    elif mode == "w":
        # text = input("Content > ")
        #
        # print("Waiting for RFID tag...")
        #
        # write_rfid(reader, text)
        #
        # print("Done...")
        pass

    else:
        print("Unsupported mode...")

    print("Cleaning up GPIO...")

    GPIO.cleanup()

    print("Done...")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', nargs='+', type=str, default='r', help='RFID mode (r = read, w = write, c = copy)')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    main(get_args())
