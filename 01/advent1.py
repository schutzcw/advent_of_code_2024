import argparse
import pathlib
import re


def similarity_score(vals1, vals2) -> int:
	vals2_map = dict()
	for val in vals2:
		if val not in vals2_map:
			vals2_map[val] = 1
		else:
			vals2_map[val] += 1
	
	sscore = 0
	for val in vals1:
		multiplier = 0 if val not in vals2_map else vals2_map[val]
		sscore += val * multiplier
	
	return sscore


def main(file: pathlib.Path):
	data = file.read_text()
	data = data.split("\n")
	vals1 = [None] * len(data)
	vals2 = [None] * len(data)

	for idx, entry in enumerate(data):
		clean = re.sub(r"\s+", " ", entry).strip()
		tokens = clean.split(" ")

		if len(tokens) != 2:
			raise RuntimeError(f"Invalid entry: {entry}")
		
		vals1[idx] = int(tokens[0])
		vals2[idx] = int(tokens[1])
	
	vals1 = sorted(vals1)
	vals2 = sorted(vals2)

	distances = [abs(v1 - v2) for (v1,v2) in zip(vals1, vals2)]
	total_distance = sum(distances)
	print(f"Total distance: {total_distance}")
	sscore = similarity_score(vals1, vals2)
	print(f"Similarity Score: {sscore}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	main(file)