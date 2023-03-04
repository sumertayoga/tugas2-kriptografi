class PBox():
    def __init__(self, pbox_table):
        self.pbox_table = pbox_table
    
    def permute(self, input):
        array =[]
        for i in range(len(input)):
            array.append(input[self.pbox_table[i]])
        return array

    def inverse_permute(self, input):
        array =[]
        for i in range(len(input)):
            idx = self.pbox_table.index(i)
            array.append(input[idx])
        return array