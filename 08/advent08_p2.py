import argparse
import pathlib

from typing import NamedTuple

class Point(NamedTuple):
	row: int
	col: int

def read_data(file: pathlib.Path) -> dict[str, list[Point]]:
	output = dict()

	data = file.read_text()
	grid = data.split("\n")
	grid_rows = len(grid)
	grid_cols = len(grid[0])
	for row_idx, row in enumerate(grid):
		for col_idx, val in enumerate(row):
			if val != ".":
				if val not in output:
					output[val] = []
				output[val].append(Point(row_idx, col_idx))
	return output, grid_rows, grid_cols

def part_two(file):
	import itertools

	frequency_map, grid_rows, grid_cols = read_data(file)
	
	anti_nodes = set()

	for (frquency, locations) in frequency_map.items():
		print(frquency)
		combinations = list(itertools.combinations(locations, 2))
	
		for comb in combinations:
			print(comb)
			p1 = comb[0]
			p2 = comb[1]

			# postive down, positive right
			rise = p2.row - p1.row
			run_ = p2.col - p1.col

			point = p1
			if rise == 0:
				# horizontal
				while (point.col >= 0):
					point = Point(point.row, point.col - abs(run_))
				
				point = Point(point.row, point.col + abs(run_))
				while (point.col < grid_cols):
					anti_nodes.add(point)
					point = Point(point.row, point.col + abs(run_))
						
			elif run_ == 0:
				# vertical
				while (point.row >= 0):
					point = Point(point.row - abs(rise), point.col)
				
				point = Point(point.row + abs(rise), point.col)
				while (point.row < grid_rows):
					print(f"adding: {point}")
					anti_nodes.add(point)
					point = Point(point.row + abs(rise), point.col)
					
			elif float(rise) / float(run_) > 0:
				# top-left to bottom-right
				while (point.row >= 0) and (point.col >= 0):
					point = Point(point.row - abs(rise), point.col - abs(run_))
				
				point = Point(point.row + abs(rise), point.col + abs(run_))
				while (point.row < grid_rows) and (point.col < grid_cols):
					print(f"adding: {point}")
					anti_nodes.add(point)
					point = Point(point.row + abs(rise), point.col + abs(run_))
			elif float(rise) / float(run_) < 0:
				# bottom-left to top-right
				while (point.row >= 0) and (point.col < grid_cols):
					point = Point(point.row - abs(rise), point.col + abs(run_))
				
				point = Point(point.row + abs(rise), point.col - abs(run_))
				while (point.row < grid_rows) and (point.col >= 0):
					print(f"adding: {point}")
					anti_nodes.add(point)
					point = Point(point.row + abs(rise), point.col - abs(run_))
			else:
				raise RuntimeError("invlaid")

	print(f"PART TWO: {len(anti_nodes)}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_two(file)