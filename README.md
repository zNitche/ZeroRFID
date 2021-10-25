### ZeroRFID

---

#### CLI tool for working with Classic 1K MIFARE tags using Raspberry Pi and RC522 RFID reader.

---
##### RPi Wiring
from `https://github.com/ondryaso/pi-rc522`

| Board pin name | Board pin | Physical RPi pin | RPi pin name |
|----------------|-----------|------------------|--------------|
| SDA            | 1         | 24               | GPIO8, CE0   |
| SCK            | 2         | 23               | GPIO11, SCKL |
| MOSI           | 3         | 19               | GPIO10, MOSI |
| MISO           | 4         | 21               | GPIO9, MISO  |
| IRQ            | 5         | 18               | GPIO24       |
| GND            | 6         | 6, 9, 20, 25     | Ground       |
| RST            | 7         | 22               | GPIO25       |
| 3.3V           | 8         | 1,17             | 3V3          |


##### Some useful MIFARE info
also from `https://github.com/ondryaso/pi-rc522`

Classic 1K MIFARE tag has **16 sectors**, each contains **4 blocks**. Each block has 16 bytes. All this stuff is indexed - you must count from zero.
The library uses "**block addresses**", which are positions of blocks - so block address 5 is second block of second sector, 
thus it's block 1 of sector 1 (indexes). Block addresses 0, 1, 2, 3 are from the first sector - sector 0. Block addresses 4, 5, 6, 7 are
from the second sector - sector 1, and so on. You should **not write** to first block - S0B0, because it contains manufacturer data. Each sector has it's **sector trailer**,
which is located at it's last block - block 3. This block contains keys and access bits for corresponding sector. For more info, look at page 10 of the datasheet.

##### Tool Setup
1. clone this repo.
2. install dependencies `pip3 install -r requirements.txt`.
3. run `python3 main.py --help` to see all available modes.
4. run `python3 main.py --mode <mode>` to run tool in `<mode> `mode.

##### Modes
1. `r` - reads and displays card data.
2. `w` - writes data from txt file to card.
3. `ch` - checks if two cards have the same content.
4. `d` - dumps card data to txt file.
5. `chf` - checks if card data and txt file have the same content

##### Config
- `TOTAL_SECTORS_COUNT` - Card sectors count.
- `TOTAL_BLOCKS_PER_SECTOR` - Blocks per sector.
- `TOTAL_BYTES_PER_BLOCK` - Bytes per block.
- `WRITABLE_UID` - If card allows writing to first block (block no. 0)
- `WRITE_SECTOR_TRAILER` - If write sector trailers (last block of every sector)
