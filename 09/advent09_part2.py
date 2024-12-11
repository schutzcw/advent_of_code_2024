import argparse
import pathlib


def read_data(file: pathlib.Path) -> list[int]:
	data = file.read_text()
	data = data.strip()
	data = [int(d) for d in data]
	return data

def part_two(file: pathlib.Path):
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
		for idx, element in enumerate(output):
			fd.write(f"{idx}: {element}\n")

	ridx = len(output) - 1
	#print(f"starting ridx: {ridx}")
	while ridx > 0:
		print(ridx)
		if output[ridx] is None:
			ridx -= 1
			continue
		
		# find a number at the end
		value = output[ridx]
		back_idx_start = ridx
		value_count = 1
		ridx -= 1
		while output[ridx] == value:
			value_count += 1
			back_idx_start = ridx
			ridx -=1
		#print(f"{value} goes from idx {back_idx_start} to {back_idx_start+value_count-1}")
		
		
		# found value and count at the end
		# now find a location from from to point it
		idx = 0
		while idx < len(output):
			if output[idx] is not None:
				idx += 1
				continue

			start_idx = idx
			space_count = 1
			idx += 1
			if idx < len(output):
				while idx < len(output) and output[idx] is None:
					space_count += 1
					idx += 1
				
			if space_count >= value_count and start_idx < back_idx_start:
				#print(f"None goes from idx {start_idx} to {start_idx+value_count-1}")
				#print(output)
				for i in range(value_count):
					output[start_idx+i] = value
					output[back_idx_start+i] = None
				#print(output)
				break

	with open("output2.txt", "wt") as fd:
		for element in output:
			fd.write(f"{element}\n")

	total = 0
	for idx, val in enumerate(output):
		if val is None:
			continue
		total += idx * val

	print(f"PART TWO: {total}")



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_two(file)