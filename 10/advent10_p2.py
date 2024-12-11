import argparse
import pathlib
from typing import NamedTuple


class Point(NamedTuple):
	row: int
	col: int

def read_data(file: pathlib.Path) -> list[int]:
	data = file.read_text()
	data = data.split("\n")
	for i in range(len(data)):
		data[i] = [int(element) if element != "." else 10 for element in data[i]]
	return data


def rate_trailhead(trailhead: Point, data: list[list[int]]) -> int:

	print(f"Rating trailhead: {trailhead}")

	if data[trailhead.row][trailhead.col] != 0:
		raise RuntimeError("invalid")

	paths = []
	def explore(row: int, col: int, data, current_path: list[Point] = None):
		if current_path is None:
			current_path = []
		current_path.append(Point(row, col))

		value = data[row][col]
		if value == 9:
			paths.append(current_path)
			print("resetting")
			current_path = []
			return
		for offset in [(0,1), (1,0), (0,-1), (-1,0)]:
			new_row = row + offset[0]
			if new_row < 0 or new_row >= len(data):
				continue

			new_col = col + offset[1]
			if new_col < 0 or new_col >= len(data[0]):
				continue
			if data[new_row][new_col] == value + 1:
				explore(new_row, new_col, data, current_path.copy())

	explore(trailhead.row, trailhead.col, data)
	print(f"Rating: {len(paths)}")
	for rating_idx, rating in enumerate(paths):
		print("New path")
		for idx, point in enumerate(rating):
			print(f"\t{idx}: {point} -> {data[point.row][point.col]}")

	return len(paths)

def part_two(file: pathlib.Path):
	data = read_data(file)

	ROWS = len(data)
	COLS = len(data[0])

	trailheads = []
	for row in range(ROWS):
		for col in range(COLS):
			if data[row][col] == 0:
				trailheads.append(Point(row, col))
	
	total_score = 0
	for trailhead in trailheads:
		total_score += rate_trailhead(trailhead, data)
		print("*"*100)
	print(f"PART TWO: {total_score}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_two(file)