import sys


def main():
    filename = sys.argv[2]
    mode = sys.argv[1]
    with open(filename, mode=mode) as file:
        print(file.read())


if __name__ == '__main__':
    main()
