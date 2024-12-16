#Button A: X+26, Y+66
#Button B: X+67, Y+21
#Prize: X=10000000012748, Y=10000000012176

from typing import NamedTuple

class Button(NamedTuple):
	x: int
	y: int

class Prize(NamedTuple):
	x: int
	y: int

if __name__ == "__main__":



	#a_button = Button(26, 66)
	#b_button = Button(67, 21)

	#prize = Prize(10000000012748, 10000000012176)

	#if False:
	#	x_distance = prize.x
	#	for i in range(100):
	#		print(f"{i}: off by: {x_distance % b_button.x}")
	#		x_distance -= a_button.x
	#else:
	#	y_distance = prize.y
	#	for i in range(100):
	#		print(f"{i}: off by: {y_distance % b_button.y}")
	#		y_distance -= a_button.y
	

	# 1) figure out how often the repeat is on x
	#	 map[int] -> idx
	#	 iterate until we hit a duplicate key and do the subtraction
	# 2) perform the number of subtractions specified in (1)
	# 3) Do step (1) for y. If we hit 0 twice, then return as not possible

	# 4 + (4 * 67) =  272  a buttons presses

	ax = 26
	ay = 66

	bx = 67
	by = 21

	dx = 10000000012748
	dy = 10000000012176

	for i in range(4+ (3*67)):
		dx -= ax
		dy -= ay

	print(f"mod_bx: {dx % bx}")
	print(f"mod_by: {dy % by}")


"""
(Pdb) c
> /home/cory.schutz@str.us/Projects/home/advent_of_code_2024/13/advent13_p2.py(85)loop_size()
-> return idx, idx_map[0]
(Pdb) idx, idx_map[0]
(7, 4)
(Pdb) idx_map
{6: 0, 15: 1, 3: 2, 12: 3, 0: 4, 9: 5, 18: 6}
"""