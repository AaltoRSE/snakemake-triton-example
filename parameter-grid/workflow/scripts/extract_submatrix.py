import sys

print("here")

input_file = sys.argv[1]
output_file = sys.argv[2]
width = sys.argv[3]
height = sys.argv[4]

print("Arguments: ", input_file, output_file, width, height)

# Read original 5x5 matrix
data = []
with open(input_file, "r") as fin:
    for line in fin:
        data.append(line.strip().split())

# Extract width x height submatrix starting from left-top corner
submatrix = []
for i in range(int(height)):
    submatrix.append(data[i][:int(width)])

# Save submatrix
with open(output_file, "w") as fout:
    fout.write("\n".join([" ".join(row) for row in submatrix]) + "\n")
