# Generate byte sequences of length 2
import itertools

length = 2  # Length of the byte sequence
sequences = []

# Generate all possible byte sequences of the given length
for combination in itertools.product(range(256), repeat=length):
    sequences.append(bytearray(combination))

# Write the sequences in a TXT file in binary
for i, seq in enumerate(sequences):
    binary_sequence = ' '.join(format(byte, '08b') for byte in seq)
    with open("byte_sequence.txt", 'a') as file:
        file.write(f"{binary_sequence}\n")
