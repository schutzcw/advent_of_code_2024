import argparse
import pathlib

def log(msg, debug):
	if not debug:
		return
	print(msg)

def read_and_validate(file: pathlib.Path) -> tuple[dict[int,set[int]], list[int]]:
	"""Return:
		- rules_map: map from first page in order to a set of pages that must come after, if they exist
		- updates list: the list of updates
	"""
	data = file.read_text()
	data_sections = data.split("\n\n")
	if len(data_sections) != 2:
		raise RuntimeError(f"invalid input data. Expected 2 sections. Received {len(data_sections)}")

	rule_section = data_sections[0]
	updates_section = data_sections[1]

	# map from first page in order to a set of pages that must come after, if they exist
	rules_map = dict()
	for line in rule_section.split("\n"):
		tokens = line.split("|")
		if len(tokens) != 2:
			raise RuntimeError(f"Parsing error on line: {line}")
		before_int = int(tokens[0])
		after_int = int(tokens[1])

		if before_int not in rules_map:
			rules_map[before_int] = set([after_int])
		else:
			rules_map[before_int].add(after_int)

	updates = updates_section.split("\n")
	updates_verified = []
	# verify and transform to ints. probably should've just left as strings...
	for update in updates:
		tokens = update.split(",")
		ints = [int(token) for token in tokens]
		updates_verified.append(ints)

	return rules_map, updates_verified


def create_index_map(update: list[int]) -> dict[int, int]:
	"""map from page number to index in update list"""
	# print warning if page numbe occurrs twice, as that's an assumption I make...
	index_map = dict()
	for idx, val in enumerate(update):
		if val in index_map:
			print(f"WARNING. Found {val} multiple times.")
		else:
			index_map[val] = idx
	return index_map


def get_lowest_index(rules_map: dict[int, list[int]],
					 page: int,
					 update_idx_map: dict[int, int]) -> (int | None):
	"""
	Given the rules_map, the page_num, and the update_idx_map

	return the index of the lowest page_num in rules_map for page_num rule.
	"""

	rule = rules_map[page]
	rule_page_indices = []
	for other_page in rule:
		if other_page in update_idx_map:
			rule_page_indices.append(update_idx_map[other_page])
	return min(rule_page_indices) if len(rule_page_indices) > 0 else None


def update_is_valid(rules_map: dict[int, list[int]],
				    update_sequence: list[int]) -> bool:
	"""
	Return True if valid, else False
	"""

	#print(f"Update sequence: {update_sequence}")
	# map from page number to index in update_sequence list
	update_idx_map = create_index_map(update_sequence)
	#print(f"Update Index Map: {update_idx_map}")
	for idx, page in enumerate(update_sequence):
		#print(f"\tPage: {page}")
		if page not in rules_map:
			continue

		# get lowest index in update_idx_map that exists in rules
		lowest_rule_page_idx: (int | None) = get_lowest_index(rules_map, page, update_idx_map)

		# a rule exists, but the second number is not in the update sequence
		if lowest_rule_page_idx is None:
			continue
		
		if idx < lowest_rule_page_idx:
			# condition satisfied
			continue
		else:
			rule_page = update_sequence[lowest_rule_page_idx]
			print(f"Rule broken: {page}|{rule_page} broken. {page} at index {idx} while {rule_page} at index {lowest_rule_page_idx}")
			return False
	return True


def fix_update(update_sequence: list[int],
			   rules_map: dict[int, list[int]],
			   bad_update_idx: int = 0) -> list[int]:
	"""return the fixed update"""
	# map from page number to index in update_sequence list
	update_idx_map = create_index_map(update_sequence)

	idx_of_current_page = -1
	while idx_of_current_page < (len(update_sequence) - 1):
		idx_of_current_page += 1
		page = update_sequence[idx_of_current_page]
		if page not in rules_map:
			continue
		rules = rules_map[page]
		for after_page in rules:
			if after_page not in update_idx_map:
				continue
			idx_of_after_page = update_idx_map[after_page] 
			if idx_of_after_page < idx_of_current_page:
				# swap update_sequence[idx_of_after_page] and update_sequence[idx]
				tmp = update_sequence[idx_of_after_page]
				update_sequence[idx_of_after_page] = update_sequence[idx_of_current_page]
				update_sequence[idx_of_current_page] = tmp
				# re-calculate idx map
				update_idx_map = create_index_map(update_sequence)
				# decrement idx so we can check the same idx again
				idx_of_current_page = 0
				break
	return update_sequence


def part_two(file: pathlib.Path):
	# map from a page number to the 
	rules_map: dict[int,set[int]]
	updates_list: list[int]

	rules_map, updates_list = read_and_validate(file)

	bad_updates = []
	for update in updates_list:
		if not update_is_valid(rules_map, update):
			bad_updates.append(update)

	middle_sum = 0
	print("*"*100)
	for bad_update_idx, update in enumerate(bad_updates):
		print(f"Before Fix: {update}")
		fixed_update = fix_update(update, rules_map, bad_update_idx)
		print(f"After Fix: {update}")
		update_is_valid(rules_map, fixed_update)
		middle_val = update[len(update) // 2]
		print(f"Middle Value: {middle_val}")
		middle_sum += middle_val
		print("*"*100)

	#still_bad = 0
	#for update in fixed_updates:
	#	if not update_is_valid(rules_map, update):
	#		still_bad += 1
	#print(f"Total Bad: {len(bad_updates)}")
	#print(f"STILL BAD: {still_bad}")
	print(f"PART TWO: {middle_sum}")
# guess: 6365 is too high

	


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	part_two(file)
