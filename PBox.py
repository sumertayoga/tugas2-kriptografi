class PBox():
    def __init__(self, pbox_table):
        self.pbox_table = pbox_table
    
    def permute(self, input, isInverse):
        array =[]
        for i in range(len(input)):
            if (isInverse):
                idx =self.pbox_table[i]
                array.append(input[idx])
            else:
                idx = self.pbox_table.index(i)
                array.append(input[idx])
        return array

    
    def permute_all(self, input, isInverse):
        array =[]
        for i in range(0, len(input), 16):
            if (i+16<=len(input)):
                array.extend(self.permute(input[i:(min((i+16), len(input)))], isInverse))
            else:
                array.extend(input[i:(min((i+16), len(input)))])
        return array
    
if __name__ == '__main__':
    p16 = PBox([7,2,0,15,12,10,14,8,6,11,1,9,13,4,5,3])
    p = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,0x76,0x76,0x76,0x76]
    print(p)
    ciphertext = p16.permute_all(p,True)
    decrypt = p16.permute_all(ciphertext,False)
    print(ciphertext)
    print(decrypt)