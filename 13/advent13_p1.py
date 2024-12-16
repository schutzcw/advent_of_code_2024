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
					cprob[key] = Prize(int(match.group(1)), int(match.group(2)))
				break
		if len(cprob) == 3:
			problems.append(Problem(cprob["a"], cprob["b"], cprob["prize"]))
			cprob = dict()

	return problems


def solve_problem(problem: Problem) -> (Solution | None):
	""" """
	# it costs 3 tokens to push A and 1 token to push B
	distance_y = problem.prize.y
	distance_x = problem.prize.x

	a_presses = 0
	b_presses = 0
	while (distance_y >= 0) and (distance_x >= 0):
		print(f"\tdistance_x: {distance_x}, distance_y: {distance_y}")

		# if we're at the prize, return
		if (distance_y == 0) and (distance_x == 0):
			return Solution(a_presses, b_presses)

		# first, check if all B pushes would work
		if (distance_y % problem.b.y == 0) and (distance_x % problem.b.x == 0):
			presses_y = int(distance_y / problem.b.y)
			presses_x = int(distance_x / problem.b.x)
			import pdb; pdb.set_trace()
			if presses_y == presses_x:
				return Solution(a_presses, presses_y)
		
		# only option left is a A push
		distance_y -= problem.a.y
		distance_x -= problem.a.x
		a_presses += 1
	
	#print(f"\tfinal - distance_x: {distance_x}, distance_y: {distance_y}")
	return None


def part_one(file: pathlib.Path):
	problems = read_data(file)
	print(f"# problems: {len(problems)}")
	total_cost = 0
	for idx, problem in enumerate(problems):
		solution = solve_problem(problem)
		cost = 0
		if solution is not None:
			cost = 3*solution.a_presses + 1*solution.b_presses
		total_cost += cost
		#print("*"*50)
	print(f"TOTAL_COST: {total_cost}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_one(file)