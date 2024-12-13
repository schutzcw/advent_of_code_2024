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


from typing import NamedTuple
class Line(NamedTuple):
	row: (tuple[int, int] | int)
	col: (tuple[int, int] | int)


def calc_area_and_num_lines(letter: str, region: set[tuple[int,int]], grid: list[list[int]])-> tuple[int, int]:
	AREA = len(region)

	OFFSET_MAP = {"left": (0, -1), 
				  "right": (0, 1),
				  "top": (-1, 0),
				  "bottom": (1, 0)}

	ROWS = len(grid)
	COLS = len(grid[0])

	# compute the set of boundary lines
	unchecked_lines: set[Line] = set()
	for loc in region:
		line_bottom = Line(row=loc[0]+1, col=(loc[1], loc[1]+1))
		line_top = Line(row=loc[0], col=(loc[1], loc[1]+1))
		line_left = Line(row=(loc[0], loc[0]+1), col=loc[1])
		line_right = Line(row=(loc[0], loc[0]+1), col=loc[1]+1)
		for (key,offset) in OFFSET_MAP.items():
			check_row = loc[0] + offset[0]
			
			if check_row < 0:
				print(f"Adding line_top: {line_top}")
				unchecked_lines.add(line_top)
				continue
			if check_row >= ROWS:
				print(f"Adding line_bottom: {line_bottom}")
				unchecked_lines.add(line_bottom)
				continue
			
			check_col = loc[1] + offset[1]
			if check_col < 0:
				print(f"Adding line_left: {line_left}")
				unchecked_lines.add(line_left)
				continue
			if check_col >= COLS:
				print(f"Adding line_right: {line_right}")
				unchecked_lines.add(line_right)
				continue

			check_letter = grid[check_row][check_col]
			if check_letter != letter:
				if key == "left":
					print(f"Adding line_left: {line_left}")
					unchecked_lines.add(line_left)
				elif key == "right":
					print(f"Adding line_right: {line_right}")
					unchecked_lines.add(line_right)
				elif key == "top":
					print(f"Adding line_top: {line_top}")
					unchecked_lines.add(line_top)
				elif key == "bottom":
					print(f"Adding line_bottom: {line_bottom}")
					unchecked_lines.add(line_bottom)
				else:
					raise RuntimeError("error")
 
	# make a duplicate to check for crosses
	unchecked_lines_start = unchecked_lines.copy()

	total_lines = 0
	# loop through boundary segments to determine the number of lines
	while len(unchecked_lines) > 0:
		# grab the next unchecked line and see if it's horizontal or vertical
		start_line: Line = next(iter(unchecked_lines))
		print(f"\tSTART LINE: {start_line}")
		# have a set of segments that are in-line with the starting segment, interate
		# through neighbors to see if they are in-line. Once segments_to_check is
		# empty, we've removed all segments that we've checked from unchecked_lines
		# and we have exactly 1 line
		segments_to_check = set([start_line])

		while len(segments_to_check) > 0:
			current_line: Line = next(iter(segments_to_check))
			segments_to_check.remove(current_line)
			line_type = "horizontal" if type(current_line.row) == int else "vertical"
			if line_type == "horizontal":
				# check on left
				check_line_left = Line(row=current_line.row,
									   col=(current_line.col[0]-1, current_line.col[0]))
				if check_line_left in unchecked_lines:
					# check left up and left down for cross
					check_line_left_up = Line(row=(current_line.row -1, current_line.row),
											  col=current_line.col[0])
					check_line_left_down = Line(row=(current_line.row, current_line.row+1),
												col=current_line.col[0])
					if not((check_line_left_up in unchecked_lines_start) and (check_line_left_down in unchecked_lines_start)):
						segments_to_check.add(check_line_left)
					
				# check on right
				check_line_right = Line(row=current_line.row,
										col=(current_line.col[1], current_line.col[1] + 1))
				if check_line_right in unchecked_lines:
					# check right up and right down for cross
					check_line_right_up = Line(row=(current_line.row -1, current_line.row),
											  col=current_line.col[1])
					check_line_right_down = Line(row=(current_line.row, current_line.row+1),
												col=current_line.col[1])
					if not((check_line_right_up in unchecked_lines_start) and (check_line_right_down in unchecked_lines_start)):
						segments_to_check.add(check_line_right)

			elif line_type == "vertical":
				# check on top
				check_line_top = Line(row=(current_line.row[0]-1, current_line.row[0]),
						  			  col=current_line.col)
				if check_line_top in unchecked_lines:
					# check top_left and top_right for cross
					check_line_top_left = Line(row=current_line.row[0],
											   col=(current_line.col-1, current_line.col))
					check_line_top_right = Line(row=current_line.row[0],
											   col=(current_line.col, current_line.col+1))
					if not((check_line_top_left in unchecked_lines_start) and (check_line_top_right in unchecked_lines_start)):
						segments_to_check.add(check_line_top)

				# check on bottom
				check_line_bottom = Line(row=(current_line.row[1], current_line.row[1]+1),
						  			     col=current_line.col)
				if check_line_bottom in unchecked_lines:
					# check bottom-left and bottom-right for cross
					check_line_top_left = Line(row=current_line.row[1],
											   col=(current_line.col-1, current_line.col))
					check_line_top_right = Line(row=current_line.row[1],
											   col=(current_line.col, current_line.col+1))
					if not((check_line_top_left in unchecked_lines_start) and (check_line_top_right in unchecked_lines_start)):
						segments_to_check.add(check_line_bottom)

			else:
				raise RuntimeError(f"valid line type: {line_type}")
			
			# remove current_line
			print(f"Removed:{current_line}")
			unchecked_lines.remove(current_line)
		total_lines += 1
	return (AREA, total_lines)


def part_two(file: pathlib.Path):
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
		print(f"LETTER: {letter}")
		for region in region_map[letter]:
			area, total_lines = calc_area_and_num_lines(letter, region, grid)
			cost += area * total_lines
			print(f"{letter}: {region}")
			print(f"\tArea: {area}, Lines: {total_lines}")
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

	part_two(file)