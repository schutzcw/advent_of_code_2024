import argparse
import pathlib

from enum import Enum
from typing import NamedTuple

Grid = list[list[str]]

GRID_ROWS = 0
GRID_COLS = 0

class Direction(Enum):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4

class Position(NamedTuple):
	row: int
	col: int
	direction: Direction

def print_grid(grid: Grid):
	for grid_line in grid:
		print(grid_line)

def find_start_pos(grid: Grid) :
	for row_idx, row_data in enumerate(grid):
		for col_idx, col_data in enumerate(row_data):
			if col_data == "^":
				return Position(row_idx, col_idx, Direction.UP)
			elif col_data == ">":
				return Position(row_idx, col_idx, Direction.RIGHT)
			elif col_data == "v":
				return Position(row_idx, col_idx, Direction.DOWN)
			elif col_data == "<":
				return Position(row_idx, col_idx, Direction.LEFT)

	raise RuntimeError("could not find starting position")

def move_up(position: Position, grid: Grid) -> tuple[(Position | None),
													 (Position | None)]:
	"""keep moving up from the current postion until you hit an obstacle or go off the grid"""
	if position.row == 0:
		# starting position given is on edge
		return None, None

	for row in range(position.row-1, -1, -1):
		if grid[row][position.col] in set(["#", "O"]):
			new_position = Position(row+1, position.col, Direction.RIGHT)
			obstacle_hit = Position(row, position.col, Direction.UP)
			grid[row+1][position.col] = "+"
			break
		else:
			grid[row][position.col] = "X"
			# no blocking '#' or "O" means we're off the board
			new_position = None
			obstacle_hit = None
	return new_position, obstacle_hit

def move_right(position: Position, grid: Grid) -> tuple[(Position | None),
														(Position | None)]:
	
	if position.col == GRID_COLS - 1:
		# starting position given is on edge
		return None, None

	for col in range(position.col+1, GRID_COLS, 1):
		if grid[position.row][col] in set(["#", "O"]):
			new_position = Position(position.row, col-1, Direction.DOWN)
			obstacle_hit = Position(position.row, col, Direction.RIGHT)
			grid[position.row][col-1] = "+"
			break
		else:
			# no blocking '#' or "O" means we're off the board
			grid[position.row][col] = "X"
			new_position = None
			obstacle_hit = None
	return new_position, obstacle_hit

def move_down(position: Position, grid: Grid) -> tuple[(Position | None),
													   (Position | None)]:
	if position.row == GRID_ROWS - 1:
		# starting position given is valid
		return None, None

	for row in range(position.row+1, GRID_ROWS, 1):
		if grid[row][position.col] in set(["#", "O"]):
			new_position = Position(row-1, position.col, Direction.LEFT)
			obstacle_hit = Position(row, position.col, Direction.DOWN)
			grid[row-1][position.col] = "+"
			break
		else:
			# no blocking '#' or "O" means we're off the board
			grid[row][position.col] = "X"
			new_position = None
			obstacle_hit = None
	return new_position, obstacle_hit

def move_left(position: Position, grid: Grid) -> tuple[(Position | None),
													   (Position | None)]:
	
	if position.col == 0:
		# starting position given is on edge
		return None, None

	for col in range(position.col - 1, -1, -1):
		
		if grid[position.row][col] in set(["#", "O"]):
			new_position = Position(position.row, col+1, Direction.UP)
			obstacle_hit = Position(position.row, col, Direction.LEFT)
			grid[position.row][col+1] = "+"
			break
		else:
			# no blocking '#' or "O" means we're off the board
			grid[position.row][col] = "X"
			new_position = None
			obstacle_hit = None
	return new_position, obstacle_hit


def create_grid(file: pathlib.Path) -> Grid:
	data = file.read_text()
	data = data.split("\n")
	
	grid = []
	for line in data:
		line_chars = [char for char in line]
		grid.append(line_chars)
	return grid

def move_one_left(position: Position,
				  grid: Grid,
				attempts: (list[Direction] | None) = None ) -> (Position | None):
	
	if attempts is None:
		attempts = []

	# we've already tried to move left from this position on the same move_one()
	# call. We're bounded by obstables on all sides
	if Direction.LEFT in attempts:
		return None

	# next move would be off the grid
	if position.col == 0:
		return None
	if grid[position.row][position.col - 1] in ["#", "O"]:
		position = Position(position.row, position.col, Direction.UP)
		return move_one_up(position, grid)
	return Position(position.row, position.col-1, Direction.LEFT)

def move_one_down(position: Position,
				  grid: Grid,
				attempts: (list[Direction] | None) = None ) -> (Position | None):
	
	if attempts is None:
		attempts = []

	# we've already tried to move down from this position on the same move_one()
	# call. We're bounded by obstables on all sides
	if Direction.DOWN in attempts:
		return None

	# next move would be off the grid
	if position.row == GRID_ROWS - 1:
		return None
	if grid[position.row + 1][position.col] in ["#", "O"]:
		position = Position(position.row, position.col, Direction.LEFT)
		return move_one_left(position, grid)
	return Position(position.row + 1, position.col, Direction.DOWN)

def move_one_right(position: Position,
				   grid: Grid,
				attempts: (list[Direction] | None) = None ) -> (Position | None):
	
	if attempts is None:
		attempts = []

	# we've already tried to move right from this position on the same move_one()
	# call. We're bounded by obstables on all sides
	if Direction.RIGHT in attempts:
		return None

	# next move would be off the grid
	if position.col == GRID_COLS - 1:
		return None
	if grid[position.row][position.col + 1] in ["#", "O"]:
		position = Position(position.row, position.col, Direction.DOWN)
		return move_one_down(position, grid)
	return Position(position.row, position.col + 1, Direction.RIGHT)

def move_one_up(position: Position,
				grid: Grid,
				attempts: (list[Direction] | None) = None ) -> (Position | None):
	
	if attempts is None:
		attempts = []

	# we've already tried to move up from this position on the same move_one()
	# call. We're bounded by obstables on all sides
	if Direction.UP in attempts:
		return None

	# next move would be off the grid
	if position.row == 0:
		return None
	if grid[position.row - 1][position.col] in ["#", "O"]:
		position = Position(position.row, position.col, Direction.RIGHT)
		return move_one_right(position, grid)
	return Position(position.row - 1, position.col, Direction.UP)

def move_one(position: Position, grid: Grid) -> (Position | None):

	# NOTE: This will infinite loop if you're surrounded by objects on all sides...
	if position.direction == Direction.UP:
		return move_one_up(position, grid)
	elif position.direction == Direction.RIGHT:
		return move_one_right(position, grid)
	elif position.direction == Direction.DOWN:
		return move_one_down(position, grid)
	elif position.direction == Direction.LEFT:
		return move_one_left(position, grid)
	else:
		raise RuntimeError("Invalid")

def original_obstacle_in_front(position: Position, grid: Grid) -> bool:
	if position.direction == Direction.UP:
		if position.row == 0:
			return False
		elif grid[position.row-1][position.col] == "#":
			return True
		else:
			return False
	elif position.direction == Direction.RIGHT:
		if position.col == GRID_COLS - 1:
			return False
		elif grid[position.row][position.col + 1] == "#":
			return True
		else:
			return False
	elif position.direction == Direction.DOWN:
		if position.row == GRID_ROWS - 1:
			return False
		elif grid[position.row+1][position.col] == "#":
			return True
		else:
			return False
	elif position.direction == Direction.LEFT:
		if position.col == 0:
			return False
		elif grid[position.row][position.col - 1] == "#":
			return True
		else:
			return False
	else:
		raise RuntimeError("invalid")

def rotate_position(position: Position) -> Position:
	if position.direction == Direction.UP:
		return Position(position.row, position.col, Direction.RIGHT)
	elif position.direction == Direction.RIGHT:
		return Position(position.row, position.col, Direction.DOWN)
	elif position.direction == Direction.DOWN:
		return Position(position.row, position.col, Direction.LEFT)
	elif position.direction == Direction.LEFT:
		return Position(position.row, position.col, Direction.UP)
	else:
		raise RuntimeError("invalid")

def add_artificial_obstacle_in_front(position: Position, 
									 grid: Grid) -> (tuple[int,int] | None):
	"""returns (row,col) of artificial obstacle. if obstacle would  be off the grid, return None"""
	if position.direction == Direction.UP:
		if position.row == 0:
			return None
		else:
			grid[position.row-1][position.col] = "O"
			return position.row-1, position.col
	elif position.direction == Direction.RIGHT:
		if position.col == (GRID_COLS - 1):
			return None
		else:
			grid[position.row][position.col + 1] = "O"
			return position.row, position.col + 1
	elif position.direction == Direction.DOWN:
		if position.row == (GRID_ROWS - 1):
			return None
		else:
			grid[position.row+1][position.col] = "O"
			return position.row+1, position.col
	elif position.direction == Direction.LEFT:
		if position.col == 0:
			return None
		else:
			grid[position.row][position.col - 1] = "O"
			return position.row, position.col - 1


def save_grid_file(grid: Grid, debug_count: int):
	file_path = f"loop_detected_{debug_count}.txt"
	with open(file_path, 'w') as file:
		for row in grid:
			file.write(''.join(row) + '\n')


def restore_grid(original: Grid, grid: Grid):
	for row_idx, row in enumerate(original):
		for col_idx, _ in enumerate(row):
			grid[row_idx][col_idx] = original[row_idx][col_idx]


def add_starting_position_visualization_to_grid(position: Position, grid: Grid) -> None:
	char = ""
	if position.direction == Direction.UP:
		char = "^"
	elif position.direction == Direction.RIGHT:
		char = ">"
	elif position.direction == Direction.DOWN:
		char = "v"
	elif position.direction == Direction.LEFT:
		char = "<"
	else:
		raise RuntimeError("Invalid")
	grid[position.row][position.col] = char


def grid_loop_detected(position: Position, grid: Grid, debug_count: (int | None)) -> bool:
	"""return True if loop detected. Otherwise False"""
	import copy
	original = copy.deepcopy(grid)
	starting_position = position

	obstacles_hit = []
	while position is not None:
		#print(position)
		if position.direction == Direction.UP:
			position, obstacle = move_up(position, grid)
		elif position.direction == Direction.RIGHT:
			position, obstacle = move_right(position, grid)
		elif position.direction == Direction.DOWN:
			position, obstacle = move_down(position, grid)
		elif position.direction == Direction.LEFT:
			position, obstacle = move_left(position, grid)
		else:
			raise RuntimeError("Invalid state")
		#print(f"new_position: {position}. obstacle_hit: {obstacle}")
		# no obstacle hit (we'll break look on next check)
		if obstacle is None:
			continue
		
		# we've already hit the same obstacle from the same direction previously,
		# so loop detected
		#print(f"obstacle: {obstacle}. obstacles_hit: {obstacles_hit}")
		if obstacle in obstacles_hit:
			add_starting_position_visualization_to_grid(position, grid)
			if debug_count is not None:
				save_grid_file(grid, debug_count)
			restore_grid(original, grid)
			return True
		else:
			obstacles_hit.append(obstacle)
	restore_grid(original, grid)
	return False

def write_tuples_to_file(tuples_set, file_path):
    # Sort the set of tuples
    sorted_tuples = sorted(tuples_set)
    
    # Open the file in write mode
    with open(file_path, 'w') as f:
        # Write each tuple to the file on a new line
        for t in sorted_tuples:
            f.write(f"{t[0]}, {t[1]}\n")  # Format tuple as "int, int"

def count_initial_obstacles(grid: Grid) -> int:
	count = 0
	for row in grid:
		for val in row:
			if val == "#":
				count += 1
	return count

def part_two_take_one(file: pathlib.Path):
	# first approach was an epic fail (believe I'm getting caught in "islands")
	grid = create_grid(file)
	global GRID_ROWS
	global GRID_COLS
	GRID_ROWS = len(grid)
	GRID_COLS = len(grid[0])

	print(f"Grid size: {GRID_ROWS} x {GRID_COLS}")
	starting_position = find_start_pos(grid)
	print(f"Starting position: {starting_position}")

	moves = 0
	artificial_causes_loop_set = set()

	artificial_locations_attempted = set()
	position = starting_position
	while position is not None:
		# check if '#' already in front of current position. If it is,
		# we don't add a 'O' obstacle on top of it. Instead, we want to
		# rotate positions
		#print(f"Moves: {moves}")
		if original_obstacle_in_front(position, grid):
			position = rotate_position(position)
			continue

		artificial_location = add_artificial_obstacle_in_front(position, grid)

		if artificial_location is None:
			# artificial locaiton is off the board, meaning next position is off 
			# the board, so break
			break
		else:
			artificial_locations_attempted.add(artificial_location)

		# check infinite
		if grid_loop_detected(position, grid, len(artificial_causes_loop_set)):
			if artificial_location not in artificial_causes_loop_set:
				artificial_causes_loop_set.add(artificial_location)
		
		grid[artificial_location[0]][artificial_location[1]] = "."
		position = move_one(position, grid)
		moves += 1

	if (starting_position.row, starting_position.col) in artificial_causes_loop_set:
		print(f"Starting position in set. Removing")
		artificial_causes_loop_set.remove((starting_position.row, starting_position.col))
	
	# debugging: write all artificial locations attempts to a file in sorted order
	write_tuples_to_file(artificial_locations_attempted, "locations_attempted.txt")
	initial_obstacle_count = count_initial_obstacles(grid)
	print(f"Artificial locations attempted: {len(artificial_locations_attempted)}")
	print(f"Count initial obstacles: {initial_obstacle_count}")

	total_locations = GRID_ROWS * GRID_COLS
	locations_not_checked = total_locations - len(artificial_locations_attempted) - initial_obstacle_count
	print(f"Locations NOT checked: {locations_not_checked}")
	print(f"PART TWO: len(set):{len(artificial_causes_loop_set)}")
	if True:
		print(artificial_causes_loop_set)

def part_two(file: pathlib.Path):
	grid = create_grid(file)
	global GRID_ROWS
	global GRID_COLS
	GRID_ROWS = len(grid)
	GRID_COLS = len(grid[0])

	starting_position = find_start_pos(grid)
	print(f"Starting position: {starting_position}")

	possible_obstacle_locations = set()
	for row_idx, row in enumerate(grid):
		for col_idx, val in enumerate(row):
			if val not in ["#", "^"]:
				possible_obstacle_locations.add((row_idx, col_idx))

	import copy
	original_grid = copy.deepcopy(grid)
	count = 0
	for obs_loc in possible_obstacle_locations:
		grid[obs_loc[0]][obs_loc[1]] = "O"

		if grid_loop_detected(starting_position, grid, None):
			count += 1	
		restore_grid(original_grid, grid)
	print(count)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_two(file)