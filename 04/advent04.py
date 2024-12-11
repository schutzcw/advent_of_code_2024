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


def part_one(file: pathlib.Path, to_find: str):
	
	grid, n_rows, n_cols = read_and_validate(file)

	def find_string(row: int,
				 	col: int,
					to_find: str,
					row_offsets: list[int],
					col_offsets: list[int],
					prefix: str = "\t") -> int:
		"""
		Arguments:
			row: the row where the last letter was found
			col: the col where the last letter was found
			to_find: The remaining characters to find

		Return the number of times the string was found from the current location
		"""

		# no more characters to find
		if to_find == "":
			return 1

		count = 0
		for row_offset in row_offsets:
			row_to_check = row + row_offset
			if (row_to_check < 0) or (row_to_check >= n_rows):
				continue
			for col_offset in col_offsets:
				col_to_check = col + col_offset
				if (col_to_check < 0) or (col_to_check >= n_cols):
					continue
				if grid[row_to_check][col_to_check] == to_find[0]:
					#print(f"{prefix}{to_find[0]} found at ({row_to_check},{col_to_check})")
					count += find_string(row_to_check,
						  				 col_to_check,
										 to_find[1:],
										 row_offsets=[row_offset],
										 col_offsets=[col_offset],
										 prefix = prefix + "\t")
	
		return count

	OFFSETS = [-1,0,1]
	find_count = 0
	for row in range(n_rows):
		for col in range(n_cols):
			if grid[row][col] == to_find[0]:
				#print(f"Start: ({row}, {col})")
				find_count += find_string(row, col, to_find[1:], row_offsets=OFFSETS, col_offsets=OFFSETS, prefix="\t")
	print(f"Part 1 Count: {find_count}")


def part_two(file: pathlib.Path):
	
	grid, n_rows, n_cols = read_and_validate(file)

	count = 0
	for row in range(1, n_rows-1):
		for col in range(1, n_cols-1):
			if grid[row][col] == "A":
				positive_diag = set([grid[row+1][col-1], grid[row-1][col+1]])
				negative_diag = set([grid[row+1][col+1], grid[row-1][col-1]])
				if positive_diag == negative_diag == set(["M", "S"]):
					count += 1
	print(f"Part 2 Count: {count}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file, to_find="XMAS")
	part_two(file)