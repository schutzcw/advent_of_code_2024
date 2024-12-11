import argparse
import pathlib


def read_and_validate(file: pathlib.Path) -> tuple[list[str], int, int]:
	"""Returns: grid, n_rows, n_cols"""
	output = []

	data = file.read_text()
	lines = data.strip().split("\n")
	for line in lines:
		parsed = []
		tokens = line.split(":")
		parsed.append(int(tokens[0]))
		tokens = tokens[1].strip().split(" ")
		for token in tokens:
			parsed.append(int(token))
		output.append(parsed)
	
	return output

def possible_equation(result: int, inputs: list[int]) -> bool:
	
	if len(inputs) == 0:
		return False

	if len(inputs) == 1:
		return True if inputs[0] == result else False

	multiply = inputs[0] * inputs[1]
	add = inputs[0] + inputs[1]

	return possible_equation(result, [multiply] + inputs[2:]) or possible_equation(result, [add] + inputs[2:])
	       

def part_one(file):
	data = read_and_validate(file)

	calibration_total = 0
	for line in data:
		possible = possible_equation(line[0], line[1:])
		print(f"{possible}: {line}")
		if possible:
			calibration_total += line[0]
	print(f"PART ONE: {calibration_total}")



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file)