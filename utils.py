from consts import Consts
import time


def read_rfid(reader):
    util = reader.util()
    rfid_data = []

    while True:
        print("Reading RFID Card, waiting for card...")

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
                        print(f"Reading block no. {block_id}")
                    else:
                        rfid_data.append([])
                        print(f"Error while reading block no. {block_id}")

                util.deauth()

                break

        time.sleep(1)

    return rfid_data


def write_rfid(reader, file_name):
    parsed_data = parse_txt_data_file(file_name)

    util = reader.util()

    while True:
        print("Writing RFID Card, waiting for card...")

        reader.wait_for_tag()

        (error, data) = reader.request()
        if not error:
            print("\nDetected")

            (error, uid) = reader.anticoll()
            if not error:
                print(f"Card read UID: {str(uid[0])} {str(uid[1])} {str(uid[2])} {str(uid[3])}")

                util.set_tag(uid)

                util.auth(reader.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

                for block_id, block_data in enumerate(parsed_data):
                    error = util.do_auth(block_id)
                    id = block_id + 1

                    if not error:
                        if (id == 1 and not Consts.WRITABLE_UID) or id % Consts.TOTAL_BLOCKS_PER_SECTOR == 0:
                            print(f"Passing block no. {block_id}")
                        else:
                            bd = [int(hex(b), base=16) for b in block_data]
                            reader.write(block_id, bd)

                            print(f"Writing block no. {block_id}")
                    else:
                        print(f"Error while reading block no. {block_id}")

                util.deauth()

                break

        time.sleep(1)


def check_diff_rfid(reader):
    block_id = 0
    diffs = []

    print("Processing first card...")
    rfid_data_1 = read_rfid(reader)
    print("Done...")

    time.sleep(1)

    print("Processing second card...")
    rfid_data_2 = read_rfid(reader)
    print("Done...")

    for sector in range(Consts.TOTAL_SECTORS_COUNT):
        for block in range(Consts.TOTAL_BLOCKS_PER_SECTOR):
            f_data = rfid_data_1[block_id]
            s_data = rfid_data_2[block_id]

            f_data.sort()
            s_data.sort()

            if f_data == s_data:
                print(f"Block no. {block_id} match")
            else:
                print(f"Block no. {block_id} diff")
                diffs.append(block_id)

            block_id += 1

    return diffs


def check_diff_rfid_txt(reader, file_name):
    block_id = 0
    diffs = []

    print("Processing card...")
    rfid_data_1 = read_rfid(reader)
    print("Done...")

    print(f"Parsing data txt file {file_name}...")
    rfid_data_2 = parse_txt_data_file(file_name)
    print("Done...")

    for sector in range(Consts.TOTAL_SECTORS_COUNT):
        for block in range(Consts.TOTAL_BLOCKS_PER_SECTOR):
            f_data = rfid_data_1[block_id]
            s_data = rfid_data_2[block_id]

            f_data.sort()
            s_data.sort()

            if f_data == s_data:
                print(f"Block no. {block_id} match")
            else:
                print(f"Block no. {block_id} diff")
                diffs.append(block_id)

            block_id += 1

    return diffs


def parse_txt_data_file(file_name):
    with open(file_name, "r") as file_data:
        data = file_data.readlines()

    parsed_data = []

    for block_id_data in data:
        parsed_data.append([int(b) for b in block_id_data.split()])

    return parsed_data
