import argparse
import pathlib

def log(msg, debug):
	if not debug:
		return
	print(msg)

def read_and_validate(file: pathlib.Path) -> tuple[dict[int,set[int]], list[str]]:
	"""Return:
		- rules_map
		- updates list
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


def get_lowest_index(rules_map, before_page, update_idx_map, debug=False) -> (int | None):
	"""
	Given the rules_map, the page_num, and the update_idx_map, 
	return the index of the lowest page_num in rules_map for page_num rule.
	"""

	after_page_idxs = []
	rule = rules_map[before_page]
	for after_page in rule:
		if after_page in update_idx_map:
			#log(f"After Page {after_page} update index is {update_idx_map[after_page]}", debug)
			after_page_idxs.append(update_idx_map[after_page])
	return min(after_page_idxs) if len(after_page_idxs) > 0 else None


def verify_update(rules_map, update, incorrect_only = False, debug = False) -> int:
	"""
	If incorrect_only=False, return only naturally valid updates. If incorrect_only=True,
	fix incorrect updates and return their updated, correct middle entry

	return middle value if valid update, else 0
	"""
	log(f"\nStarting Update: {update}", debug)

	correct_made = False
	update_idx_map = create_index_map(update)
	for before_page_idx in range(len(update)):
		before_page = update[before_page_idx]
		if before_page not in rules_map:
			continue

		# get lowest index in update_idx_map that exists in rules
		lowest_after_idx = get_lowest_index(rules_map, before_page, update_idx_map, debug=debug)
		if lowest_after_idx is None:
			continue
		
		if update_idx_map[before_page] < lowest_after_idx:
			continue
		else:
			log(f"Rule broken: {before_page} [{rules_map[before_page]}]", debug=debug)

		# if correct only, return 0
		if not incorrect_only:
			return 0
		# else, we want to fix the entry and return the middle
		else:
			correct_made = True
			if before_page_idx != update_idx_map[before_page]:
				raise RuntimeError("page idx error")
			tmp = update[before_page_idx]
			update[before_page_idx] = update[lowest_after_idx]
			update[lowest_after_idx] = tmp
			update_idx_map = create_index_map(update)
			log(f"After swap: {update}", debug=debug)

	# if we're in incorrect_only mode and no correction was made, return 0
	if incorrect_only and (not correct_made):
		return 0

	log(f"Valid update: {update}", debug)
	# if we've reached here, the update list is valid, just determine middle value
	n_vals = len(update)
	if n_vals % 2 == 0:
		raise RuntimeError(f"No middle value in update. Length is even.")

	return update[n_vals // 2]

def run(file: pathlib.Path, incorrect_only: bool = False, debug = False):
	rules_map, updates_list = read_and_validate(file)
	middle_val_sum = 0
	for update in updates_list:
		middle_val = verify_update(rules_map, update, incorrect_only=incorrect_only, debug=debug)
		middle_val_sum += middle_val
	
	print(f"Answer: {middle_val_sum}")


def part_one(file, debug=False):
	print("PART ONE")
	run(file, incorrect_only=False, debug=debug)

def part_two(file, debug=False):
	print("PART TWO")
	run(file, incorrect_only=True, debug=debug)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("data_file", help="path to data file")
	parser.add_argument("--debug", action="store_true", help="enable debugging")
	args = parser.parse_args()

	file = pathlib.Path(args.data_file)
	if not file.is_file():
		raise RuntimeError(f"Path does not exist: {file.absolute()}")

	#part_one(file, debug=args.debug)
	#print("")
	part_two(file, debug=args.debug)
