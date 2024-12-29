# Python
import random

''' CREATING ARRAY (bArr2) '''

# Define arrays elements
controlByte1 = random.randint(0, 255)
controlByte2 = random.randint(0, 255)
controlAccelerator = random.randint(0, 255)
controlTurn = random.randint(0, 255)
i9 = random.randint(0, 15)
i10 = random.randint(0, 15)
XORControl = i9 ^ (((controlByte1 ^ controlByte2) ^ controlAccelerator) ^ controlTurn) ^ (i10 & 255)

# Define the array with random values for specific indices
bArr2 = [
    3,
    102,
    20,
    controlByte1,
    controlByte2,
    controlAccelerator,
    controlTurn,
    i9,
    i10,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    XORControl,
    -103
]

# Turn the list into a list of bytes
byte_list = bytearray([(value % 256) for value in bArr2])
#print(byte_list)


# Convert each byte into its binary representation and print as 0s and 1s
binary_representation = ' '.join(format(byte, '08b') for byte in byte_list)

print(binary_representation)