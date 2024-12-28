# Python
import random

''' CREATING ARRAY (bArr2) '''

# Define the array with random values for specific indices
bArr2 = [
    3,
    102,
    20,
    random.randint(0, 255),     # Third value
    random.randint(0, 255),     # Fourth value
    random.randint(0, 255),     # Fifth value
    random.randint(0, 255),     # Sixth value
    random.randint(0, 15),      # Seventh value
    random.randint(0, 15),      # Eighth value
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
    random.randint(0, 255),     # Nineteenth value
    -103
]

# Turn the list into a list of bytes
byte_list = bytearray((value % 256) for value in bArr2)
'''
print(byte_list)
'''

# Convert each byte into its binary representation and print as 0s and 1s
binary_representation = ' '.join(format(byte, '08b') for byte in byte_list)

print(binary_representation)