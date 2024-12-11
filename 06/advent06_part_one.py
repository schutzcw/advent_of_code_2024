import argparse
import pathlib

from enum import Enum
from typing import NamedTuple

Grid = list[list[str]]

class Direction(Enum):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4

class Position(NamedTuple):
	row: int
	col: int
	direction: Direction

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

def move_up(position: Position, grid: Grid) -> (Position | None):
	for row in range(position.row, -1, -1):
		if grid[row][position.col] == "#":
			return Position(row+1, position.col, Direction.RIGHT)
		else:
			grid[row][position.col] = "X"
	return None # no blocking "#" means we're off the board

def move_right(position: Position, grid: Grid) -> (Position | None):
	for col in range(position.col, len(grid[0]), 1):
		if grid[position.row][col] == "#":
			return Position(position.row, col-1, Direction.DOWN)
		else:
			grid[position.row][col] = "X"
	return None # no blocking "#" means we're off the board

def move_down(position: Position, grid: Grid) -> (Position | None):
	for row in range(position.row, len(grid), 1):
		if grid[row][position.col] == "#":
			return Position(row-1, position.col, Direction.LEFT)
		else:
			grid[row][position.col] = "X"
	return None # no blocking "#" means we're off the board

def move_left(position: Position, grid: Grid) -> (Position | None):
	for col in range(position.col, -1, -1):
		if grid[position.row][col] == "#":
			return Position(position.row, col+1, Direction.UP)
		else:
			grid[position.row][col] = "X"
	return None # no blocking "#" means we're off the board


def create_grid(file: pathlib.Path) -> Grid:
	data = file.read_text()
	data = data.split("\n")
	
	grid = []
	for line in data:
		line_chars = [char for char in line]
		grid.append(line_chars)
	return grid

def part_one(file: pathlib.Path):
	grid = create_grid(file)

	position = find_start_pos(grid)
	while position is not None:
		if position.direction == Direction.UP:
			position = move_up(position, grid)
		elif position.direction == Direction.RIGHT:
			position = move_right(position, grid)
		elif position.direction == Direction.DOWN:
			position = move_down(position, grid)
		elif position.direction == Direction.LEFT:
			position = move_left(position, grid)
		else:
			raise RuntimeError("Invalid state")

	x_count = 0
	for grid_line in grid:
		for val in grid_line:
			if val == "X":
				x_count += 1
	print(f"PART ONE: X count: {x_count}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file)