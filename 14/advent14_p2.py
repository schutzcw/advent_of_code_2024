import argparse
import pathlib
import pprint
import re

from typing import NamedTuple

class Position(NamedTuple):
	y: int  # distance from rigth wall (as viewed from above)
	x: int  # distance from left wall

class Velocity(NamedTuple):
	y: int  # tiles per second. Position down
	x: int	# tiles per second. Positive Right

class Robot():
	pos: Position
	vel: Velocity

	def __init__(self, pos, vel):
		self.pos = pos
		self.vel = vel

	def __repr__(self):
		return f"Robot(pos={self.pos}, vel={self.vel})"


def read_data(file: pathlib.Path) -> list[int]:
	data = file.read_text()
	data = data.split("\n")

	output = []
	for line in data:
		matches = re.findall(r"-?\d+", line)
		if len(matches) != 4:
			raise RuntimeError("invalid")
		output.append(Robot(Position(int(matches[1]), int(matches[0])),
					        Velocity(int(matches[3]), int(matches[2]))))
	return output



def update_robot(robot: Robot, board_width: int, board_height: int) -> Robot:
	"""Update the position of the robot"""
	new_x = (robot.pos.x + robot.vel.x) % board_width
	new_y = (robot.pos.y + robot.vel.y) % board_height
	return Robot(pos=Position(new_y, new_x),
			     vel=robot.vel)

def split_into_quadrants(robots: list[Robot], width: int, height: int) -> dict[int, list[Robot]]:
	""" """
	row_divider = height // 2
	col_divider = width // 2

	# 0 is 9-12 on clock,
	# 1 is 0-3, 
	# 2 is 3-6, 
	# 3 is 6-9
	map = {0: [],
		   1: [],
		   2: [],
		   3: []}
	for robot in robots:
		if robot.pos.x < col_divider and robot.pos.y < row_divider:
			map[0].append(robot)
		elif robot.pos.x > col_divider and robot.pos.y < row_divider:
			map[1].append(robot)
		elif robot.pos.x > col_divider and robot.pos.y > row_divider:
			map[2].append(robot)
		elif robot.pos.x < col_divider and robot.pos.y > row_divider:
			map[3].append(robot)
		else:
			print(f"skipping robot {robot}")
	return map

import numpy as np

def part_two(file: pathlib.Path):
	robots = read_data(file)
	
	#WIDTH = 11
	#HEIGHT = 7
	WIDTH = 101
	HEIGHT = 103

	round = 0
	
	grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
	variances = []
	while round < 10_000:
		# 6875 is incorrect: too low
		# 6876 is correct
		print(round)
		x_variance = np.var([r.pos.x for r in robots])
		y_variance = np.var([r.pos.y for r in robots])
		variances.append((x_variance, y_variance))

		# populate grid
		for idx, robot in enumerate(robots):
			robots[idx] = update_robot(robots[idx], WIDTH, HEIGHT)
			robot = robots[idx]
			grid[robot.pos.y][robot.pos.x] = "*"
		
		# Print the grid
		for row in grid:
			print(''.join(row))

		
		if round+1 in [6876, 17279, 27682, 38085, 48488, 58891, 69294, 79697, 90100, 1829, 12232, 22635, 33038, 43441, 53844, 64247, 74650, 85053, 95456, 1108, 11511, 21914, 32317, 42720, 53123, 63526, 73929, 84332, 94735, 387, 10790, 21193, 31596, 41999, 52402, 62805, 73208, 83611, 94014, 2756, 13159, 23562, 33965, 44368, 54771, 65174, 75577, 85980, 96383, 4198]:
			input(f"Current Round {round}. Press any key to continue...")
		round += 1

		# clear grid
		for row_idx, row in enumerate(grid):
			for col_idx, _ in enumerate(row):
				grid[row_idx][col_idx] = " "

	variance_sums = [v[0] + v[1] for v in variances]
	indices_of_lowest = [index for index, value in sorted(enumerate(variance_sums), key=lambda x: x[1])[:50]]
	print(indices_of_lowest)	
	# [6876, 8009, 6979, 5125, 6361, 4404, 7597, 4713, 8112, 8524, 5640]

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_two(file)