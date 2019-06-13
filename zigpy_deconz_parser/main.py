import binascii

import zigpy_deconz_parser.parser as parser

IF_NAME = '/home/ha/.homeassistant/home-assistant.log'

if __name__ == '__main__':
    with open(IF_NAME, mode='r') as infile:
        for line in infile:
            print(line.strip())
            parser.parse(line)
