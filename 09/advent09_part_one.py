import argparse
import pathlib


def read_data(file: pathlib.Path) -> list[int]:
	data = file.read_text()
	data = data.strip()
	data = [int(d) for d in data]
	return data

def part_one(file: pathlib.Path):
	data = read_data(file)
	output = []
	file_id = 0
	element = 0
	for idx, element in enumerate(data):
		if idx % 2 == 0:
			value = file_id
			file_id += 1
		else:
			value = None
		for i in range(element):
			output.append(value)

	with open("output1.txt", "wt") as fd:
		for element in output:
			fd.write(f"{element}\n")

	idx = 0
	import pdb; pdb.set_trace()
	while idx < len(output):
		ridx = len(output) - 1
		if output[idx] is not None:
			idx += 1
			continue
		
		while output[ridx] is None:
			ridx -= 1
		
		if ridx > idx:
			#import pdb; pdb.set_trace()
			output[idx] = output[ridx]
			output[ridx] = None
			
		idx += 1
		
		print(idx)

# guess: 6382875730645
#        6382875730645
	with open("output2.txt", "wt") as fd:
		for element in output:
			fd.write(f"{element}\n")

	total = 0
	for idx, val in enumerate(output):
		if val is None:
			continue
		total += idx * val

	print(f"PART ONE: {total}")



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file)