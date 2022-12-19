# coding=utf-8
def read_file(filename: str) -> list[str]:
    f = open(filename)
    contents = f.readlines()
    contents = list(map(lambda x: x.strip(), contents))
    return contents


def parse_pairs(contents: list[str]) -> list[list[set[int]]]:
    g = []
    for line in contents:
        group1, group2 = line.split(',')
        group1 = get_sections(group1)
        group2 = get_sections(group2)
        g.append([group1, group2])
    return g


def get_sections(section: str):
    section = section.split('-')
    section = list(map(int, section))
    section = set(range(section[0], section[1] + 1))
    return section


def part_one(groups: list[list[set[int]]]):
    result = 0
    for pair in groups:
        if pair[0].issubset(pair[1]) or pair[1].issubset(pair[0]):
            result += 1
    print(result)


def part_two(groups: list[list[set[int]]]):
    result = 0
    for pair in groups:
        if len(pair[0].intersection(pair[1])) != 0:
            result += 1
    print(result)


if __name__ == '__main__':
    file = read_file('input.txt')
    pairs = parse_pairs(file)
    part_one(pairs)
    part_two(pairs)
