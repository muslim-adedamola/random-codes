import re

# List of patches to search for
patches = [
    "patch0", "patch1", "patch2", "patch8", "patch10", "patch12",
    "patch21", "patch23", "patch26", "patch27", "patch28", "patch29",
    "patch35", "patch41", "patch43", "patch45", "patch46"
]

# Input file path
input_file = "364.txt"

# Output file path to save the extracted lines
output_file = "0_total.txt"

# Create a regular expression pattern to match the exact patches
pattern = re.compile(r'\b(?:' + '|'.join(re.escape(patch) for patch in patches) + r')\b')

# Function to extract lines containing specified patches
def extract_patches(file_path):
    extracted_lines = []
    with open(file_path, "r") as file:
        for line in file:
            if pattern.search(line):
                extracted_lines.append(line.strip())
    return extracted_lines

# Extract patches from the input file
extracted_lines = extract_patches(input_file)

# If there are missing patches, display a message
missing_patches = set(patches) - set(patch for line in extracted_lines for patch in patches if patch in line)
if missing_patches:
    print("Warning: The following patches were not found in the text file:", ", ".join(missing_patches))

# Write extracted lines to the output file
with open(output_file, "w") as output:
    for line in extracted_lines:
        output.write(line + "\n")

print("Extraction completed. Extracted lines saved to", output_file)
