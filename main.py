import argparse
import RPi.GPIO as GPIO
from pirc522 import RFID
import os
from consts import Consts
import utils


def main(opt):
    mode = opt.mode[0]

    reader = RFID()

    try:
        if mode == "ch":
            print("Checking RFID cards...")

            diffs = utils.check_diff_rfid(reader)

            print(f"Diffs at blocks no. {diffs}")

        elif mode == "r":
            rfid_data = utils.read_rfid(reader)
            block_id = 0

            for sector in range(Consts.TOTAL_SECTORS_COUNT):
                for block in range(Consts.TOTAL_BLOCKS_PER_SECTOR):
                    print(f"S{sector}B{block} {rfid_data[block_id]}")

                    block_id += 1

        elif mode == "d":
            print("Dumping RFID Card data to txt file...")
            file_name = input("filename > ")

            rfid_data = utils.read_rfid(reader)

            with open(file_name, "w") as dump_file:
                for block_data in rfid_data:
                    seq = ""

                    for data in block_data:
                        seq += " ".join(str(data)) + " "

                    dump_file.write(seq)
                    dump_file.write("\n")

        elif mode == "w":
            print("Writing RFID Card data from txt file...")
            file_name = input("filename > ")

            if os.path.exists(file_name):
                utils.write_rfid(reader, file_name)
            else:
                print(f"File {file_name} doesnt exist...")

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
    parser.add_argument('--mode', nargs='+', type=str, default='r', help='RFID mode (r = read, w = write, ch = check, d = dump to txt)')
    opt = parser.parse_args()

    return opt


if __name__ == '__main__':
    main(get_args())
