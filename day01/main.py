# coding=utf-8

class Elf():
    def __init__(self):
        self.inventory = []

    def __str__(self):
        s = '\nElf inventory: '
        for idx, cal in enumerate(self.inventory):
            if idx != 0:
                s += ' + '
            s += str(cal)
        s += ' = ' + str(self.total_inventory)
        return s

    def __repr__(self):
        return self.__str__()

    @property
    def total_inventory(self):
        return sum(self.inventory)


def read_file(filename: str) -> list[str]:
    f = open(filename)
    contents = f.readlines()
    return contents


def parse_file_contents(contents: list[str]) -> list[Elf]:
    elves = [Elf()]
    for line in contents:
        if line != '\n':
            calorie = line.strip()
            elves[-1].inventory.append(int(calorie))
        else:
            elves.append(Elf())
    return elves


def puzzle_main():
    file = read_file('input.txt')
    elves = parse_file_contents(file)
    return elves


def part_one():
    elves = puzzle_main()
    max_cal = max(elf.total_inventory for elf in elves)
    print(f'The elf with most calories carries {max_cal} calories.')


def part_two():
    num_elves = 3
    elves = puzzle_main()
    elves.sort(key=lambda elf: elf.total_inventory, reverse=True)
    sum_cal = sum(elf.total_inventory for elf in elves[:num_elves])
    print(f'The top {num_elves} carry {sum_cal} calories.')


if __name__ == '__main__':
    part_one()
    part_two()
