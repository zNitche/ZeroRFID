import argparse
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def read_rfid(reader):
    id, text = reader.read()

    return id, text


def write_rfid(reader, text):
    reader.write(text)


def main(opt):
    mode = opt.mode[0]
    reader = SimpleMFRC522()

    if mode == "c":
        print("Copying RFID card, waiting for first card...")

        id, text = read_rfid(reader)

        print("Card read, waiting for second card...")

        write_rfid(reader, text)

        print("Done...")

    elif mode == "r":
        print("Reading RFID Card, waiting for card...")

        id, text = read_rfid(reader)

        print(f"ID: {id}")
        print(f"Content: {text}")

    elif mode == "w":
        text = input("Content > ")

        print("Waiting for RFID tag...")

        write_rfid(reader, text)

        print("Done...")

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
