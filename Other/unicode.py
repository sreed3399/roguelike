import numpy as np

#prints all the characters in the tcod tileset

chars = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 91, 92, 93, 94, 95, 96, 123, 124, 125, 126, 9617, 9618, 9619, 9474, 9472, 9532, 9508, 9524, 9500, 9516, 9492, 9484, 9488, 9496, 9624, 9629, 9600, 9622, 9626, 9616, 9623, 8593, 8595, 8592, 8594, 9650, 9660, 9668, 9658, 8597, 8596, 9744, 9745, 9675, 9673, 9553, 9552, 9580, 9571, 9577, 9568, 9574, 9562, 9556, 9559, 9565, 0, 0, 0, 0, 0, 0, 0, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 0, 0, 0, 0, 0, 0, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 0, 0, 0, 0, 0, 0]

uni_chars = np.empty((8,32))
a = 0

print(len(chars))
text = ""

#for char in chars:
for x in range(9):
    for y in range(33):
        if a < len(chars):
            #print(x,y)
            #print(chr(chars[a]))
            #text += (chr(chars[a]))
            text = text + (chr(chars[a])) 
            a += 1            
            

print(text)
#print(uni_chars)