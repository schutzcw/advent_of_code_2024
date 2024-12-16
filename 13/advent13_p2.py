import argparse
import pathlib
import pprint
import re

from typing import NamedTuple

class Button(NamedTuple):
	x: int
	y: int

class Prize(NamedTuple):
	x: int
	y: int

class Problem(NamedTuple):
	a: Button
	b: Button
	prize: Prize

class Solution(NamedTuple):
	a_presses: int
	b_presses: int


def read_data(file: pathlib.Path) -> list[int]:
	data = file.read_text()
	data = data.split("\n")
	

	# patterns
	BUTTON_A_PAT = r"Button A: X([-+]?\d+), Y([-+]?\d+)"
	BUTTON_B_PAT = r"Button B: X([-+]?\d+), Y([-+]?\d+)"
	PRIZE_PAT = r"Prize: X=([-+]?\d+), Y=([-+]?\d+)"
	PATTERNS = {
		"a": BUTTON_A_PAT,
		"b": BUTTON_B_PAT,
		"prize": PRIZE_PAT
	}

	cprob = {}
	problems = []
	for line in data:
		for (key,pattern) in PATTERNS.items():
			match = re.match(pattern, line)
			if match:
				if key in ["a", "b"]:	
					cprob[key] = Button(int(match.group(1)), int(match.group(2)))
				else:
					cprob[key] = Prize(int(match.group(1))+10000000000000, 
									   int(match.group(2))+10000000000000)
				break
		if len(cprob) == 3:
			problems.append(Problem(cprob["a"], cprob["b"], cprob["prize"]))
			cprob = dict()

	return problems


def loop_size(prize_distance: int,
			  a_button_distance: int,
			  b_button_distance: int,
			  multiplier: int = 1) -> tuple[int, int] | tuple[None, None]:
	""" Must loop if prize_distance is sufficiently large"""

	# map from moduluo_b number to the number of 
	idx_map: dict[int, int] = dict()
	idx = 0
	while prize_distance > 0:
		distance_mod_b_button = prize_distance % b_button_distance
		if distance_mod_b_button in idx_map:
			break
		idx_map[distance_mod_b_button] = idx
		print(f"\tidx_map[distance_mod_b_button]: idx_map[{distance_mod_b_button}] = {idx}")
		prize_distance -= (a_button_distance * multiplier)
		idx += 1

	# no loops because starting prize_distance isn't sufficiently large
	if prize_distance < 0:
		print("prize distance < 0")
		return None, None
	elif 0 not in idx_map:
		print("modulo never equals 0")
		return None, None
	return idx, idx_map[0]


def solve_problem(problem: Problem) -> (Solution | None):
	""" """

	# it costs 3 tokens to push A and 1 token to push B
	distance_y = problem.prize.y
	distance_x = problem.prize.x

	# 0) Check if b presses work right away...
	if (distance_y % problem.b.y == 0) and (distance_x % problem.b.x == 0):
		if (distance_y / problem.b.y) == (distance_x / problem.b.x):
			return Solution(0, distance_y / problem.b.y)

	# 1) Figure out how often the repeat is on a_x
	ax_loop_size, l1_subtractions_to_zero_mod = loop_size(distance_x, problem.a.x, problem.b.x)
	if ax_loop_size is None:
		return None

	if ax_loop_size is None:
		if (distance_y % problem.b.y == 0) and (distance_x % problem.b.x == 0):
			return int(distance_y / problem.b.y)
		else:
			print("impossible")
			return None

	# 2) Subtract using button_a until prize_distance.x % button_b.x == 0
	button_presses_a = 0
	while (distance_x % problem.b.x) != 0:
		distance_x -= problem.a.x
		distance_y -= problem.a.y
		button_presses_a += 1

	if button_presses_a != l1_subtractions_to_zero_mod:
		raise RuntimeError("invalid")

	# 3) do step (1) for y with a multiplier of ax_loop_size. If we hit 0 twice, then return as not possible
	ay_loop_size, l2_subtractions_to_zero_mod = loop_size(distance_y,
													   	  problem.a.y,
														  problem.b.y,
														  multiplier=ax_loop_size)
	if ay_loop_size is None:
		return None

	pressed_per_round = ax_loop_size
	# 4) do l2_subtractions to get to mod 0 on both x and y
	distance_y_mod_b = (distance_y % problem.b.y)
	while distance_y_mod_b != 0:
		distance_x -= (problem.a.x * pressed_per_round)
		distance_y -= (problem.a.y * pressed_per_round)
		distance_y_mod_b = (distance_y % problem.b.y)
		distance_x_mod_b = (distance_x % problem.b.x)
		button_presses_a += pressed_per_round

	if (button_presses_a - (pressed_per_round * l2_subtractions_to_zero_mod)) != l1_subtractions_to_zero_mod:
		raise RuntimeError("invalid")

	pressed_per_round *= ay_loop_size

	# TODO: given the data, it's possible that the correct solution falls inside these button presses.
	# I'm skipping that for now...

	# 5) press a once more
	distance_x -= (problem.a.x * pressed_per_round)
	distance_y -= (problem.a.y * pressed_per_round)
	button_presses_a += pressed_per_round

	r1_button_b_x_presses_needed = int(distance_x / problem.b.x)
	r1_button_b_y_presses_needed = int(distance_y / problem.b.y)
	r1_button_b_presses_needed_y_minux_x = abs(r1_button_b_y_presses_needed - r1_button_b_x_presses_needed)

	# 6) press a once more for a second time...
	distance_x -= (problem.a.x * pressed_per_round)
	distance_y -= (problem.a.y * pressed_per_round)
	button_presses_a += pressed_per_round

	r2_button_b_x_presses_needed = int(distance_x / problem.b.x)
	r2_button_b_y_presses_needed = int(distance_y / problem.b.y)
	r2_button_b_presses_needed_y_minux_x = abs(r2_button_b_y_presses_needed - r2_button_b_x_presses_needed)

	r1_minus_r2 = r1_button_b_presses_needed_y_minux_x - r2_button_b_presses_needed_y_minux_x

	# if this is non-zero, them it's impossible and we return None
	rounds_needed_mod = r2_button_b_presses_needed_y_minux_x % r1_minus_r2
	if rounds_needed_mod != 0:
		return None

	rounds_needed = int(r2_button_b_presses_needed_y_minux_x / r1_minus_r2)

	# 7) Go N more rounds
	distance_x -= (rounds_needed * pressed_per_round * problem.a.x)
	distance_y -= (rounds_needed * pressed_per_round * problem.a.y)
	button_presses_a += rounds_needed * pressed_per_round
	button_presses_b = distance_x / problem.b.x
	button_presses_b_check = distance_y / problem.b.y

	assert button_presses_b == button_presses_b_check

	return Solution(button_presses_a, button_presses_b)

def part_one(file: pathlib.Path):
	problems = read_data(file)
	print(f"# problems: {len(problems)}")
	total_cost = 0
	for idx, problem in enumerate(problems):
		solution = solve_problem(problem)
		cost = 0
		if solution is not None:
			cost = 3*solution.a_presses + 1*solution.b_presses
			print(f"{idx}: {solution}")
		total_cost += cost
		print("*"*50)
	print(f"TOTAL_COST: {total_cost}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file)