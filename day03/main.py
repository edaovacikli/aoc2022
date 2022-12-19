# coding=utf-8
def read_file(filename: str) -> list[str]:
    f = open(filename)
    contents = list(map(lambda x: x.strip(), f.readlines()))
    return contents


def parse_rucksack_comps(file_contents: list[str], num_comps: int) -> \
        list[list[list[int]]]:
    rucksacks = []
    for line in file_contents:
        comps = get_compartments(line, num_comps)
        rucksacks.append(comps)
    return rucksacks


def parse_rucksack_groups(file_contents: list[str], num_in_group: int) -> \
        list[list[list[int]]]:
    groups = []
    for idx in range(0, len(file_contents), num_in_group):
        group = []
        for idy in range(0, num_in_group):
            line = file_contents[idx + idy]
            line = convert_to_priority(line)
            group.append(line)
        groups.append(group)
    return groups


def get_compartments(line: str, num_comps: int) -> list[list[int]]:
    comp_len = len(line) // num_comps
    comps = []
    for idx in range(num_comps):
        comp = line[idx * comp_len:(idx + 1) * comp_len]
        comp = convert_to_priority(comp)
        comps.append(comp)
    return comps


def get_char_value(char) -> int:
    old_big_a = ord('A')
    new_big_a = 27
    new_small_a_offset = ord('a') % old_big_a + new_big_a - 1
    return (ord(char) % old_big_a + new_big_a) % new_small_a_offset


def convert_to_priority(comp: str) -> list[int]:
    return list(map(get_char_value, comp))


def find_same_item(rucksacks) -> int:
    for item in rucksacks[0]:
        result = True
        for rucksack in rucksacks[1:]:
            if item not in rucksack:
                result = False
                break
        if result:
            return item


def part_one(file_contents):
    rucksacks = parse_rucksack_comps(file_contents, 2)
    prio_sum = 0
    for idx in range(len(rucksacks)):
        prio_sum += find_same_item(rucksacks[idx])
    print(prio_sum)


def part_two(file_contents):
    rucksacks = parse_rucksack_groups(file_contents, 3)
    badge_sum = 0
    for idx in range(len(rucksacks)):
        badge_sum += find_same_item(rucksacks[idx])
    print(badge_sum)


if __name__ == '__main__':
    file = read_file('input.txt')
    part_one(file)
    part_two(file)
