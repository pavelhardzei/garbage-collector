from bitstring import BitArray
from resources import EXPANSION, SBOX, PERMUTATION_TABLE
import textwrap


def extension(encrypting_message, extension_table):
    extended_message = BitArray()
    for index in extension_table:
        extended_message.bin += encrypting_message.bin[index]
    return extended_message


def xor(encryption_message, key):
    return encryption_message ^ key


def split_in_6bits(encryption_message):
    list_of_6bits = textwrap.wrap(encryption_message.bin, 6)
    return [BitArray('0b' + x) for x in list_of_6bits]


def get_first_and_last_bit(bits6):
    return BitArray('0b' + bits6.bin[0] + bits6.bin[-1])


def get_middle_four_bit(bits6):
    return BitArray('0b' + bits6.bin[1:5])


def sbox_lookup(sbox_number, first_last: BitArray, middle4: BitArray):
    first_last.prepend(BitArray('0b000000'))
    middle4.prepend(BitArray('0b0000'))

    d_first_last = int.from_bytes(first_last.bytes, 'big')
    d_middle = int.from_bytes(middle4.bytes, "big")

    sbox_value = SBOX[sbox_number][d_first_last][d_middle]
    return BitArray(uint=sbox_value, length=4)


def permutation(encryption_message, permutation_table):
    cipher_text = BitArray()
    for index in permutation_table:
        cipher_text.bin += encryption_message.bin[index]
    return cipher_text


def round_function(encrypting_message, key):
    result = BitArray()
    encrypting_message = extension(encrypting_message, EXPANSION)
    encrypting_message = xor(encrypting_message, key)
    bits6list = split_in_6bits(encrypting_message)
    for index, bits6 in enumerate(bits6list):
        first_last = get_first_and_last_bit(bits6)
        middle4 = get_middle_four_bit(bits6)
        result.append(sbox_lookup(index, first_last, middle4))
    return permutation(result, PERMUTATION_TABLE)


def encrypt(encrypting_block, key):
    left_part = BitArray(encrypting_block[:32])
    right_part = BitArray(encrypting_block[32:64])

    for i in range(3):
        temp = right_part
        right_part = xor(left_part, round_function(right_part, key))
        left_part = temp

    left_part.append(right_part)
    return left_part


def main():
    # with open("encrypting.bin", "wb") as file:
    #     # file.write(b'keykeyhell') the same
    #     file.write(b'\x6b\x65\x79\x6b\x65\x79\x68\x65\x6c\x6c\x62\x61\x6c\x6c')

    with open("encrypting.bin", "rb") as file:
        content = BitArray(file.readline())
        if len(content) < 112:
            print("Invalid input")
            return
        key = content[:48]
        encryption_message = content[48:112]

    encrypted = encrypt(encryption_message, key)
    print("Encrypting message: {}".format(encryption_message.bytes))
    print("After encrypting: {}".format(encrypted))

    # with open("decrypting.bin", "wb") as file:
    #     file.write(key.bytes)
    #     file.write(encrypted.bytes)

    with open("decrypting.bin", "rb") as file:
        content = BitArray(file.readline())
        if len(content) < 112:
            print("Invalid input")
            return
        key = content[:48]
        encrypted = content[48:112]

    decrypting_block = encrypted[32:64] + encrypted[:32]
    decrypting_block = encrypt(BitArray(decrypting_block), key)
    decrypting_block = decrypting_block[32:64] + decrypting_block[:32]
    print("Decrypting: {}".format(decrypting_block.bytes))


if __name__ == "__main__":
    main()