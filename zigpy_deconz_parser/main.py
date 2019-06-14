import getopt
import os.path
import sys

import zigpy_deconz_parser.parser as parser


def main():
    argv = sys.argv[1:]
    infile = None
    try:
        opts, args = getopt.getopt(argv, "hi:", ["in-file=",])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, args in opts:
        if opt == '-h':
            help()
            sys.exit(0)
        elif opt in ('-i', '--in-file'):
            infile = args

    if infile in (None, '-'):
        proccess(sys.stdin)
    else:
        with open(infile, mode='r') as file:
            proccess(file)


if __name__ == '__main__':
    main()


def proccess(file):
    for line in file:
        print(line.strip())
        parser.parse(line)


def help():
    name = os.path.basename(sys.argv[0])
    print(name + " -i <input file name>")
