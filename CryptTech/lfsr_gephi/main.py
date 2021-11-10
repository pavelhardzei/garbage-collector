from gephi import Gephi


def print_file():
    # gephi_generator = Gephi(0x40001F, 0x10000061, 0x40000020, 0x4DB270, 0x1F951D70, 0x6500C12C)
    gephi_generator = Gephi(0x400026, 0x1000007C, 0x40000023, 0x4AFE85, 0x1EF46F79, 0x4E2BF982)
    with open("output.bin", "wb") as file:
        for _ in range(1250000):
            file.write(gephi_generator.generate_gephi_sequence(8).to_bytes(1, "big"))


def main():
    print_file()


if __name__ == "__main__":
    main()