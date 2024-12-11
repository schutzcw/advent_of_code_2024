import argparse
import pathlib


def read_and_validate(file: pathlib.Path) -> tuple[list[str], int, int]:
	"""Returns: grid, n_rows, n_cols"""
	data = file.read_text()
	grid = data.strip().split("\n")
	n_rows = len(grid)
	n_cols = len(grid[0])

	# ensure valid grid dimensions
	for idx, row in enumerate(grid):
		if len(row) != n_rows:
			raise RuntimeError(f"Invalid row length for row {idx} (0-based)")

	return grid, n_rows, n_cols


def part_one(file: pathlib.Path):
	pass


def part_two(file: pathlib.Path):
	pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	#part_one(file)
	#part_two(file)