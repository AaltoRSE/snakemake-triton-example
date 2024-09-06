import sys

input_files = sys.argv[1:-1]
output_file = sys.argv[-1]

means = []
for input_file in input_files:
    with open(input_file, 'r') as fin:
        mean = float(fin.readline().strip())
        means.append(mean)
        
variance = sum([(mean - sum(means) / len(means))**2 for mean in means]) / len(means)

with open(output_file, 'w') as fout:
    fout.write(str(variance) + '\n')
