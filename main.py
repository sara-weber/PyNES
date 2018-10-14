import argparse
from cpu import *
from instructions import *


def main():
    # Create parser to take specific command line input
    parser = argparse.ArgumentParser(description='NES Emulator')
    parser.add_argument('rom_path',                 # Creates a class variable with name 'rom_path'
                        metavar='R',                # A name for the argument in usage messages
                        type=str,                   # Type of argument being passed
                        help='path to nes rom')     # Helper string that is displayed next to the positional argument

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

    # Create CPI
    cpu = CPU(ram, ppu)
    cpu.start_up()
    cpu.run_rom(rom)


if __name__ == "__main__":
    main()
