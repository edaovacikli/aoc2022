# coding=utf-8
# starting items: worry level
# operation: how worry level changes
# relief: divide by three, rounded down
# test: how monkey uses worry level to decide
# monkeys take turn, on turn throws all items = round
# fifo

class Monkey:
    def __init__(self, monkey_idx: int):
        self.idx = monkey_idx
        self.items = []
        self.monkey_false = -1
        self.monkey_true = -1
        self.operands = []
        self.operators = []
        self.test_operand = -1
        self.num_inspections = 0

    def __str__(self):
        s = f'Monkey {self.idx}:\n'
        s += f'\tStarting items: {self.items}\n'
        s += f'\tOperation: new = '
        for idx in range(len(self.operators)):
            s += f'{self.operands[idx]} '
            s += f'{self.operators[idx]} '
        s += f'{self.operands[-1]}\n'
        s += f'\tTest: divisible by {self.test_operand}\n'
        s += f'\t\tIf true: throw to monkey {self.monkey_true}\n'
        s += f'\t\tIf false: throw to monkey {self.monkey_false}\n'
        return s

    def operation(self, old_value, s):
        if len(self.operands) != (len(self.operators) + 1):
            raise
        else:
            x = self.__parse_operand(0, old_value)
            for idx in range(len(self.operators)):
                y = self.__parse_operand(idx + 1, old_value)
                x, s = self.__parse_operator_result(idx, x, y, s)
            return x, s

    def __parse_operator_result(self, idx, x, y, s):
        s += f'\t\tWorry level is '
        if self.operators[idx] == '+':
            s += f'increased '
            result = x + y
        elif self.operators[idx] == '-':
            s += f'decreased '
            result = x - y
        elif self.operators[idx] == '*':
            s += f'multiplied '
            result = x * y
        elif self.operators[idx] == '/':
            s += f'divided '
            result = x / y
        elif self.operators[idx] == '//':
            s += f'divided (rounded) '
            result = x // y
        elif self.operators[idx] == '%':
            s += f'modulo operated '
            result = x % y
        elif self.operators[idx] == '**':
            s += f'raised to the power '
            result = x ** y
        else:
            raise
        s += f'by {y} to {result}.\n'
        return result, s

    def __parse_operand(self, idx, old_value):
        if self.operands[idx] == 'old':
            x = old_value
        else:
            x = self.operands[idx]
        return x

    @staticmethod
    def relieve(old_value, custom_relief: int = -1):
        if custom_relief == -1:
            return old_value // 3
        else:
            return old_value % custom_relief

    def test(self, value, print_string):
        print_string += f'\t\tCurrent worry level is '
        if (value % self.test_operand) == 0:
            idx = self.monkey_true
        else:
            print_string += f'not '
            idx = self.monkey_false
        print_string += f'divisible by {self.test_operand}.\n'
        return idx, print_string

    @staticmethod
    def throw(monkeys, monkey_idx, item):
        monkeys[monkey_idx].items.append(item)

    def take_turn(self, monkeys, verbose: bool, custom_relief: int = -1):
        if verbose:
            print(f'Monkey {self.idx}:')
        while len(self.items) != 0:
            self.num_inspections += 1
            worry_level = self.items.pop(0)
            s = f'\tMonkey inspects an item with a worry level of {worry_level}.\n'
            worry_level, s = self.operation(worry_level, s)
            s += f'\t\tMonkey gets bored with item. '
            worry_level = Monkey.relieve(worry_level, custom_relief)
            s += f'Worry level is divided by 3 to {worry_level}.'
            s += f'\n'
            monkey_idx, s = self.test(worry_level, s)
            s += f'\t\tItem with worry level {worry_level} is thrown to monkey {monkey_idx}.'
            Monkey.throw(monkeys, monkey_idx, worry_level)
            if verbose:
                print(s)

    def print(self):
        print(f'Monkey {self.idx}: ' + ', '.join(map(str, self.items)))


class MonkeyParser(object):
    @staticmethod
    def parse_monkey(monkey_id: int, block: list[str]) -> Monkey:
        line_items = 'Starting items: '
        line_operation = 'Operation: '
        line_test = 'Test: '
        line_throw = 'throw to monkey'

        result = Monkey(monkey_id)

        for line in block:
            if line_items in line:
                MonkeyParser.__parse_items(result, line)
            elif line_operation in line:
                MonkeyParser.__parse_operation(result, line)
            elif line_test in line:
                MonkeyParser.__parse_test(result, line)
            elif line_throw in line:
                MonkeyParser.__parse_monkey_throw(result, line)

        return result

    @staticmethod
    def __parse_items(monkey: Monkey, line: str):
        items = []
        line = list(map(lambda x: x.strip(','), line.split()))
        for word in line:
            if word.isnumeric():
                items.append(int(word))
        monkey.items = items.copy()

    @staticmethod
    def __parse_operation(monkey: Monkey, line: str):
        line = line.split('=')[-1]
        line = line.split()
        operands = []
        operators = []
        for word in line:
            if word in ['+', '-', '*', '/', '**', '//', '%']:
                operators.append(word)
            else:
                if word.isnumeric():
                    operands.append(int(word))
                else:
                    operands.append(word)
        monkey.operators = operators.copy()
        monkey.operands = operands.copy()

    @staticmethod
    def __parse_test(monkey: Monkey, line: str):
        line = line.split()
        for word in line:
            if word.isnumeric():
                monkey.test_operand = int(word)

    @staticmethod
    def __parse_monkey_throw(monkey: Monkey, line: str):
        line = line.split()
        for word in line:
            if word.isnumeric():
                if 'true:' in line:
                    monkey.monkey_true = int(word)
                elif 'false:' in line:
                    monkey.monkey_false = int(word)


def parse_file(file_contents: list[str]):
    monkey_id = 0
    monkey_blocks = []
    for idx in range(len(file_contents)):
        if f'Monkey {monkey_id}:' in file_contents[idx]:
            for idy in range(idx + 1, len(file_contents)):
                if (f'Monkey {monkey_id + 1}:' in file_contents[idy]) or (idy == len(file_contents) - 1):
                    block = file_contents[idx + 1:idy + 1]
                    monkey_blocks.append(block)
                    monkey_id += 1
                    break
    return monkey_blocks


def read_file(filename: str) -> list[str]:
    f = open(filename)
    contents = list(map(str.strip, f.readlines()))
    return contents


def parse_monkeys(monkey_file):
    monkeys = []
    blocks = parse_file(monkey_file)
    for i in range(len(blocks)):
        monkeys.append(MonkeyParser.parse_monkey(i, blocks[i]))
    return monkeys


def calc_monkey_business(monkeys):
    inspections = [m.num_inspections for m in monkeys]
    monkey_business = max(inspections)
    inspections.remove(monkey_business)
    monkey_business *= max(inspections)
    return monkey_business


def part_one(monkeys):
    num_rounds = 20
    for i in range(num_rounds):
        for m in monkeys:
            m.take_turn(monkeys, False)
    monkey_business = calc_monkey_business(monkeys)
    print(monkey_business)


def part_two(monkeys):
    num_rounds = 10000
    relief = 1
    for m in monkeys:
        relief *= m.test_operand

    for i in range(num_rounds):
        for m in monkeys:
            m.take_turn(monkeys, False, relief)
        s = f'== After round {i + 1} ==\n'
        for m in monkeys:
            s += f'Monkey {m.idx} inspected items {m.num_inspections} times.\n'
        print(s)
    monkey_business = calc_monkey_business(monkeys)
    print(monkey_business)


if __name__ == '__main__':
    file = read_file('input.txt')

    # monkey_list = parse_monkeys(file)
    # part_one(monkey_list)

    monkey_list = parse_monkeys(file)
    part_two(monkey_list)
