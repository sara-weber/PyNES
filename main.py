import argparse
from cpu import *
from instructions import *
from nes_test import NesTestLog


def main():
    # Create parser to take specific command line input
    parser = argparse.ArgumentParser(description='NES Emulator')
    parser.add_argument('rom_path',                 # Creates a class variable with name 'rom_path'
                        metavar='R',                # A name for the argument in usage messages
                        type=str,                   # Type of argument being passed
                        help='path to nes rom')     # Helper string that is displayed next to the positional argument
    parser.add_argument('--test')

    args = parser.parse_args()

    # TODO: validate rom path is correct
    print(args.rom_path)

    # Open ROM from input arg
    with open(args.rom_path, 'rb') as file:
        rom_bytes = file.read()

    rom = ROM(rom_bytes)

    # Create RAM
    ram = RAM()

    # Create PPU
    ppu = PPU()

    # Create APU
    apu = APU()

    # Create CPU
    cpu = CPU(ram, ppu, apu)
    cpu.start_up()
    cpu.load_rom(rom)

    # Check if running the test rom
    if args.test:
        # load in the nes_test.log
        with open('nes_test.log', 'r') as nes_test_file:
            nes_test_log = NesTestLog(nes_test_file.readlines())
        while True:
            cpu.identify()
            nes_test_log.compare(cpu)
            cpu.execute()
    else:
        while True:
            cpu.identify()
            cpu.execute()



if __name__ == "__main__":
    main()
