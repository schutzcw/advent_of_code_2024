import argparse
import pathlib
import re


def is_safe(tokens: list[int]) -> int:
	"""return 1 if safe, else 1"""

	all_positive = True
	all_negative = True
	for idx in range(1,len(tokens)):
		diff = tokens[idx] - tokens[idx-1]
		all_positive = all_positive and (diff > 0)
		all_negative = all_negative and (diff < 0)
		if not (1 <= abs(diff) <= 3):
			return 0

	if not (all_positive or all_negative):
		return 0
	return 1


def is_safe_dampener(tokens: list[int]) -> int:
	"""return 1 if safe, else 1"""

	for exclude_idx in range(len(tokens)):
		vals = [v for (idx,v) in enumerate(tokens) if idx != exclude_idx]
		if is_safe(vals) == 1:
			return 1
	return 0


def main(file: pathlib.Path):
	data = file.read_text()
	data = data.split("\n")

	safe_count = 0
	# goal: count number of safe.
	for line_idx, entry in enumerate(data):
		clean = re.sub(r"\s+", " ", entry).strip()
		tokens = clean.split(" ")
		tokens = [int(token) for token in tokens]

		if len(tokens) < 2:
			# not sure if one value sequences are safe or not... There
			# aren't any in the data though
			print("Skipping single number line")
			continue

		safe = is_safe(tokens)

		if safe == 0:
			safe = is_safe_dampener(tokens)
		
		safe_count += safe

	print(f"safe count: {safe_count}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	main(file)