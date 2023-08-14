#create a bar chart of the distribution of classes in each download patches of Obj365 dataset
import matplotlib.pyplot as plt
from collections import Counter

# Read the input file
input_filename = 'classes.txt'
output_image_filename = 'bar_plot.png'

# Dictionary to store number counts
number_counts = Counter()

# Read the input file and count numbers
with open(input_filename, 'r') as file:
    for line in file:
        number = int(line.strip())
        number_counts[number] += 1

# Create list of numbers and counts for the pie chart
numbers = list(number_counts.keys())
counts = list(number_counts.values())

#create the pie chart
plt.figure(figsize=(50,50))
plt.bar(numbers, counts, color='blue')
plt.xlabel('Classes')
plt.ylabel('Count')
plt.title('Classes Distribution Bar Graph')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show

plt.savefig(output_image_filename)

print(f"Bar plot image saved as {output_image_filename}")
