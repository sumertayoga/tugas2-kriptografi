import hashlib
import numpy as np


def binToHexa(n):
    # convert binary to int
    num = int(n, 2)

    # convert int to hexadecimal
    hex_num = format(num, 'x')
    paddingLength = 32 - len(hex_num)
    for i in range(paddingLength):
        hex_num = "0" + hex_num
    return(hex_num)


def cyclicShift(binaryString):
    # Melakukan pergeseran 1 bit ke kiri secara siklik
    temp = binaryString[4:]
    return temp + binaryString[:4]


def xorBinary(binary1, binary2):
    # Melakukan xor dua binarystring
    # dan outputkan binarystring hasilnya
    # dengan padding agar panjang bit tetap 128
    temp = bin(int(binary1, 2) ^ int(binary2, 2))[2:]
    paddingLength = 128 - len(temp)
    for i in range(paddingLength):
        temp = "0" + temp
    return temp


class SBox():
    def __init__(self, key):
        key = hashlib.md5(key.encode('utf-8'))
        res = bin(int(key.hexdigest(), 16)).zfill(8)[2:]

        chunkArr = [res]
        for i in range(15):
            chunkArr.append(xorBinary(chunkArr[i], cyclicShift(chunkArr[i])))

        for i in range(16):
            chunkArr[i] = binToHexa(chunkArr[i])

        tempArr = []
        for i in range(16):
            for j in range(16):
                tempArr.append(int(chunkArr[i][j*2:j*2+2], 16))

        index = np.unique(tempArr, return_index=True)[1]
        unique = []
        for i in np.sort(index):
            unique.append(tempArr[i])

        for i in range(256):
            if i not in unique:
                unique.append(i)

        mat = []
        for i in range(16):
            mat.append(unique[i*16:i*16+16])

        self.sbox_table = mat

        invMat = [[0 for _ in range(16)] for _ in range(16)]
        hex = ["0", "1", "2", "3", "4",
               "5", "6", "7", "8", "9",
               "a", "b", "c", "d", "e",
               "f"]
        temp = np.array(mat)

        for i in range(16):
            for j in range(16):
                val = int(hex[i] + hex[j], 16)
                index = np.where(temp == val)
                invMat[i][j] = int(hex[index[0][0]] + hex[index[1][0]], 16)

        self.inv_table = invMat

    def substitute(self, input, isInverse):
        row = (input & 0x0f)
        col = input >> 4
        if(isInverse):
            return self.inv_table[row][col]
        else:
            return self.sbox_table[row][col]

    def subBytes(self, bytess, isInverse):
        ciphertext = b''
        for byte in bytess:
            ciphertext += self.substitute(byte, isInverse).to_bytes(1, 'big')
        return ciphertext


if __name__ == "__main__":
    sbox = SBox("sabtu")
    plaintext = b'\x0F\x0b\xa2\x13'
    # substitusi dengan sbox biasa
    ciphertext = sbox.subBytes(plaintext, isInverse=False)
    print("plaintext = ", plaintext)
    print("ciphertext = ", ciphertext)
