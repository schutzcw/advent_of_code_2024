import argparse
import pathlib


def read_data(file: pathlib.Path) -> list[int]:
	data = file.read_text()
	data = data.strip().split(" ")
	data = [int(token) for token in data]
	return data


def blink(data: list[int]) -> list[int]:
	i = 0
	while i != len(data):
		#print(f"{i}: Before: {data}")
		# Rule 1: if the stone is engraved with the number 0, it is
		# replaced by a stone engraved with the number 1
		if data[i] == 0:
			data[i] = 1
		elif len(str(data[i])) % 2 == 0:
			digits_str = str(data[i])
			half_count = int(len(digits_str) / 2)
			#print(f"half_count of {data[i]}: {half_count}")
			left_num = int(digits_str[0:half_count])
			right_num = int(digits_str[half_count:])
			#print(f"left_num: {left_num}")
			#print(f"right_num: {right_num}")
			data[i] = left_num
			data.append(None)
			for j in range(len(data)-1, i+1, -1):
				data[j] = data[j-1]
				#print(f"replace data[{j}] == {data[j]} with data[{j-1}] == {data[j-1]}")
			i += 1
			data[i] = right_num
		else:
			data[i] *= 2024
		#print(f"{i}:  After: {data}")
		#print("*" * 25)
		i += 1
	return data

def part_one(file: pathlib.Path, blinks: int):
	import time
	data = read_data(file)
	for i in range(blinks):
		t0 = time.time()
		data = blink(data)
		runtime = time.time() - t0
		output_map = {}
		for i in data:
			if i in output_map:
				output_map[i] += 1
			else:
				output_map[i] = 1
	print(f"new_map: {sorted(output_map.items())}")
		#print(f"blink #{i+1} took {runtime} seconds, resulting in {len(data)} stones")
	#print(data)
	#print(f"len(stones): {len(data)}")

	

"""
-If the stone is engraved with the number 0, it is replaced by a stone
engraved with the number 1.
-If the stone is engraved with a number that has an even number of digits, it is
replaced by two stones. The left half of the digits are engraved on the new left
stone, and the right half of the digits are engraved on the new right stone.
(The new numbers don't keep extra leading zeroes: 1000 would become stones 10
and 0.) 
-If none of the other rules apply, the stone is replaced by a new stone;
the old stone's number multiplied by 2024 is engraved on the new stone.

- Order is preserved
"""


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	parser.add_argument("--blinks", default=1, type=int, help="number of blinks")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file, args.blinks)