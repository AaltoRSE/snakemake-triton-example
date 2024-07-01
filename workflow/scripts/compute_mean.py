import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as fin:
    random_numbers = [float(number) for number in fin.read().split()]

mean = sum(random_numbers) / len(random_numbers)

with open(output_file, 'w') as fout:
    fout.write(str(mean) + '\n')
