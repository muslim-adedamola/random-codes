# inserts the extracted classes from extract2 into another text file with the corresponding number of occurences
from collections import Counter

# Read the input file
input_filename = 'classes.txt'
output_filename = 'result1.txt'

# Dictionary to store number counts
number_counts = Counter()

# Read the input file and count numbers
with open(input_filename, 'r') as file:
    for line in file:
        number = int(line.strip())
        number_counts[number] += 1

# Write results to the output file
with open(output_filename, 'w') as file:
    for number, count in number_counts.items():
        file.write(f"{number} {count}\n")

print("Output written to", output_filename)
