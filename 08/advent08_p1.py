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

def part_one(file):
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

			rise = p2.row - p1.row
			run = p2.col - p1.col

			# add slope to p1 to start
			anti_node_1 = Point(p1.row + rise, p1.col + run)
			if anti_node_1 == p2:
				anti_node_1 = Point(p1.row - rise, p1.col - run)
				anti_node_2 = Point(p1.row + 2 * rise, p1.col + 2 * run)
			else:
				anti_node_2 = Point(p1.row - 2 * rise, p1.col - 2 * run)
			
			anodes = [anti_node_1, anti_node_2]
			for anode in anodes:
				if (0 <= anode.row < grid_rows) and (0 <= anode.col < grid_cols):
					print(f"\tAnti-node: {anode}")
					anti_nodes.add(anode)

	print(f"PART ONE: {len(anti_nodes)}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file)