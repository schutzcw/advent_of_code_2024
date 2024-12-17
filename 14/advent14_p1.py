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

def part_one(file: pathlib.Path):
	robots = read_data(file)
	for robot in robots:
		print(robot)
	
	#WIDTH = 11
	#HEIGHT = 7
	WIDTH = 101
	HEIGHT = 103

	print("*"*50)
	DURATION_SEC = 100
	for idx, robot in enumerate(robots):
		for _ in range(DURATION_SEC):
			robots[idx] = update_robot(robots[idx], WIDTH, HEIGHT)
	
	quadrants = split_into_quadrants(robots, WIDTH, HEIGHT)
	
	safety_factor = 0
	for quadrant_num, robots in quadrants.items():
		#print(f"{quadrant_num}: {len(robots)}")
		if safety_factor == 0:
			safety_factor = len(robots)
		else:
			safety_factor *= len(robots)
	
	print(f"safety factor: {safety_factor}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file)