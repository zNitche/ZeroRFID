import argparse
import RPi.GPIO as GPIO
from pirc522 import RFID
import time
from consts import Consts


def read_rfid(reader):
    util = reader.util()
    rfid_data = []

    while True:
        reader.wait_for_tag()

        (error, data) = reader.request()
        if not error:
            print("\nDetected")

            (error, uid) = reader.anticoll()
            if not error:
                print(f"Card read UID: {str(uid[0])} {str(uid[1])} {str(uid[2])} {str(uid[3])}")

                util.set_tag(uid)

                # Key B for read only
                util.auth(reader.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

                blocks_count = Consts.TOTAL_SECTORS_COUNT * Consts.TOTAL_BLOCKS_PER_SECTOR

                for block_id in range(blocks_count):
                    error = util.do_auth(block_id)

                    if not error:
                        (error, data) = reader.read(block_id)

                        rfid_data.append(data)
                    else:
                        rfid_data.append([])

                util.deauth()

                break

        time.sleep(1)

    return rfid_data


def write_rfid(reader, text):
    reader.write(text)


def main(opt):
    mode = opt.mode[0]

    reader = RFID()

    try:
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

            rfid_data = read_rfid(reader)
            block_id = 0

            for sector in range(Consts.TOTAL_SECTORS_COUNT):
                for block in range(Consts.TOTAL_BLOCKS_PER_SECTOR):
                    print(f"S{sector}B{block} {rfid_data[block_id]}")

                    block_id += 1

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

    except Exception as e:
        print(e)

    finally:
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
