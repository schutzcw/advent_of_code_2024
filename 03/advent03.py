import argparse
import pathlib
import re
import sys

def get_number(data: str, start_idx: int) -> (int | None):
	"""return None if no number or number more than 3 digits"""

	idx = start_idx
	digits = 0
	while (idx < len(data)) and (data[idx].isdigit()):
		idx += 1
		digits += 1

	#import pdb; pdb.set_trace()
	if 0 < digits <= 3:
		return int(data[start_idx:(start_idx+digits)])
	
	return None

def main(file: pathlib.Path):
	data = file.read_text()

	mult_total = 0
	start_idx = 0
	matches = 0
	do = True
	while start_idx < len(data):
		next_do = data.find("do()", start_idx)
		next_do = sys.maxsize if next_do == -1 else next_do

		next_dont = data.find("don't()", start_idx)
		next_dont = sys.maxsize if next_dont == -1 else next_dont

		next_mul = data.find("mul(", start_idx)
		if next_mul == -1:
			# no more matches found. Return.
			break
	
		if (next_do < next_mul) and (next_do < next_dont):
			print("DO")
			do = True
		elif (next_dont < next_mul) and (next_dont < next_do):
			print("DONT")
			do = False

		start_idx = next_mul
		
		start_idx += len("mul(")
	

		num1 = get_number(data, start_idx)
		if num1 is None:
			#print(f"num1 no valid number: {data[start_idx:(start_idx+4)]}")
			continue

		start_idx += len(str(num1))
		if data[start_idx] != ",":
			#print(f"data[start_idx] = {data[start_idx]} != ,")
			continue
		start_idx += 1

		num2 = get_number(data, start_idx)

		if num2 is None:
			#print(f"num2 no valid number: {data[start_idx:(start_idx+4)]}")
			continue

		start_idx += len(str(num2))

		if data[start_idx] != ")":
			#print(f"Lacking closing bracket: {data[start_idx]}")
			continue
		start_idx += 1

		matches += 1
		print(f"{matches}: MUL({num1},{num2})")
		if do:
			mult_total += (num1 * num2)
	
	print(f"mult total: {mult_total}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	main(file)