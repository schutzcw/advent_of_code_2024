import argparse
import pathlib
import pprint

Location = tuple[int,int]


def read_data(file: pathlib.Path) -> list[int]:
	data = file.read_text()
	data = data.split("\n")
	grid = []
	for row in data:
		grid.append([char for char in row])
	return grid


def calc_area_and_perimeter(letter: str, region: set[tuple[int,int]], grid: list[list[int]])-> tuple[int, int]:
	AREA = len(region)
	OFFSETS = [(-1, 0), (0, 1), (0, -1), (1, 0)]
	ROWS = len(grid)
	COLS = len(grid[0])

	perimeter = 0
	for loc in region:
		for offset in OFFSETS:
			check_row = loc[0] + offset[0]
			if (check_row < 0) or (check_row >= ROWS):
				perimeter += 1
				continue
			check_col = loc[1] + offset[1]
			if (check_col < 0) or (check_col >= COLS):
				perimeter += 1
				continue
			check_loc_letter = grid[check_row][check_col]
			if check_loc_letter != letter:
				perimeter +=1
	return (AREA, perimeter)


def part_one(file: pathlib.Path):
	grid = read_data(file)

	ROWS = len(grid)
	COLS = len(grid[0])

	unassigned = set()
	for row in range(ROWS):
		for col in range(COLS):
			unassigned.add((row,col))

	OFFSETS = [(-1, 0), (0, 1), (0, -1), (1, 0)]
	def check_add_region(letter: str, loc_set: set, loc: tuple[int,int]):

		loc_letter = grid[loc[0]][loc[1]]
		if loc_letter != letter:
			return

		print(f"Removing: {loc}")
		unassigned.remove(loc)
		loc_set.add(loc)

		for offset in OFFSETS:
			check_row = loc[0] + offset[0]
			if (check_row < 0) or (check_row >= ROWS):
				continue
			check_col = loc[1] + offset[1]
			if (check_col < 0) or (check_col >= COLS):
				continue
			check_loc = (check_row, check_col)
			if check_loc in unassigned:
				check_add_region(letter, loc_set, check_loc)

	region_map = dict()
	while len(unassigned) > 0:
		LOC = next(iter(unassigned))
		LETTER = grid[LOC[0]][LOC[1]]
		region = set()
		check_add_region(LETTER, region, LOC)
		if LETTER not in region_map:
			region_map[LETTER] = [region]
		else:
			region_map[LETTER].append(region)

	cost = 0
	for letter in region_map:
		for region in region_map[letter]:
			area, perimeter = calc_area_and_perimeter(letter, region, grid)
			cost += area * perimeter
			print(f"{letter}: {region}")
			print(f"\tArea: {area}, Perimeter: {perimeter}")
			print("*"*50)

	print(f"COST: {cost}")
	# Need to know region of fence around each region, which is a function of the region's area and perimeter


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file)