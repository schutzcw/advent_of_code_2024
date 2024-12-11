import argparse
import pathlib
import time

def read_data(file: pathlib.Path) -> list[int]:
	data = file.read_text()
	data = data.strip().split(" ")
	data = [int(token) for token in data]
	return data


def blink(value_map: dict[int,int]) -> dict[int,int]:
	new_value_map = {}

	for (value, val_count) in value_map.items():
		#print(f"\t{value}: {val_count}")
		if value == 0:
			if 1 in new_value_map:
				new_value_map[1] += val_count
			else:
				new_value_map[1] = val_count
		elif len(str(value)) % 2 == 0:
			digits_str = str(value)
			half_count = int(len(digits_str) / 2)
			left_num = int(digits_str[0:half_count])
			right_num = int(digits_str[half_count:])

			if left_num in new_value_map:
				new_value_map[left_num] += val_count
			else:
				new_value_map[left_num] = val_count
			
			if right_num in new_value_map:
				new_value_map[right_num] += val_count
			else:
				new_value_map[right_num] = val_count
		else:
			new_value = value * 2024
			
			if new_value in new_value_map:
				new_value_map[new_value] += val_count
			else:
				new_value_map[new_value] = val_count

	return new_value_map

def part_two(file: pathlib.Path, blinks: int):
	data = read_data(file)
	# map from number to count of that number
	value_map = {}
	for value in data:
		if value in value_map:
			value_map[value] += 1
		else:
			value_map[value] = 1

	#print(f"starting map: {value_map}")
	for i in range(blinks):
		t0 = time.time()
		value_map = blink(value_map)
		runtime = time.time() - t0


	num_stones = 0
	for (k,v) in value_map.items():
		num_stones += v
	print(f"new_map: {sorted(value_map.items())}")
	print(f"# stones: {num_stones}")
	#print(f"blink #{i+1} took {runtime} seconds and resulting in {num_stones} stones")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	parser.add_argument("--blinks", default=1, type=int, help="number of blinks")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_two(file, args.blinks)