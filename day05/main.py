# coding=utf-8
class Stack:
    def __init__(self):
        self.stack = []


class CrateStack(Stack):
    def __init__(self):
        super().__init__()

    def move_crate(self, move_to_stack: Stack, num_crates: int = -1):
        if num_crates == -1:
            move_to_stack.stack.append(self.stack.pop())
        else:
            temp_stack = []
            for _ in range(num_crates):
                temp_stack.append(self.stack.pop())
            for _ in range(num_crates):
                move_to_stack.stack.append(temp_stack.pop())


class Instruction:
    def __init__(self, amount: int, stack_from: int, stack_to: int):
        self.amount = amount
        self.stack_from = stack_from
        self.stack_to = stack_to

    def run(self, stacks: list[CrateStack], second_part: bool = False) -> \
            list[CrateStack]:
        if not second_part:
            for idx in range(self.amount):
                stacks[self.stack_from].move_crate(stacks[self.stack_to])
        else:
            stacks[self.stack_from].move_crate(stacks[self.stack_to],
                                               self.amount)
        return stacks


def read_file(filename: str) -> list[str]:
    f = open(filename)
    contents = f.readlines()
    return contents


def parse_file(file: list[str]):
    parting_idx = -1
    for idx, line in enumerate(file):
        if 'move' in line:
            parting_idx = idx
            break
    stacks = file[:parting_idx - 1]
    instructions = file[parting_idx:]
    return stacks, instructions


def parse_stacks(stack_block: list[str]):
    stack_line = stack_block[-1]
    stack_names = stack_line.strip().split('   ')
    stack_indices = []
    for stack_name in stack_names:
        idx = stack_line.index(stack_name)
        stack_indices.append(idx)

    stacks = [CrateStack() for _ in range(len(stack_indices))]

    for idx in range(len(stack_block) - 2, -1, -1):
        for idy, stack_idx in enumerate(stack_indices):
            crate = stack_block[idx][stack_idx]
            if crate.isalpha():
                stacks[idy].stack.append(crate)

    return stacks


def parse_instructions(instruction_block: list[str]) -> list[Instruction]:
    instructions = []

    for line in instruction_block:
        if 'move' in line:
            move_cmd = -1
            from_cmd = -1
            to_cmd = -1
            line = line.split()
            for idx, word in enumerate(line):
                if word == 'move':
                    move_cmd = int(line[idx + 1])
                elif word == 'from':
                    from_cmd = int(line[idx + 1]) - 1
                elif word == 'to':
                    to_cmd = int(line[idx + 1]) - 1
            instructions.append(Instruction(move_cmd, from_cmd, to_cmd))
    return instructions


def part_one(stacks: list[CrateStack], instructions: list[Instruction]):
    for inst in instructions:
        stacks = inst.run(stacks)
    print_stacks(stacks)
    print('Result: ' + ''.join([stacks[x].stack[-1] for x in range(len(
        stacks))]))


def part_two(stacks: list[CrateStack], instructions: list[Instruction]):
    for inst in instructions:
        stacks = inst.run(stacks, True)
    print_stacks(stacks)
    print('Result: ' + ''.join([stacks[x].stack[-1] for x in range(len(
        stacks))]))


def print_stacks(stacks):
    max_stack = max([len(stacks[x].stack) for x in range(len(stacks))])
    s = ''
    for idx in range(max_stack - 1, -1, -1):
        for stack in stacks:
            if len(stack.stack) > idx:
                s += '[' + stack.stack[idx] + ']' + '\t'
            else:
                s += '\t'
        s += '\n'
    for idx in range(len(stacks)):
        s += ' ' + str(idx + 1) + ' ' + '\t'
    print(s)


if __name__ == '__main__':
    ff = read_file('input.txt')
    ss, ii = parse_file(ff)
    stack_list = parse_stacks(ss)
    instruction_list = parse_instructions(ii)
    part_one(stack_list, instruction_list)
    stack_list = parse_stacks(ss)
    part_two(stack_list, instruction_list)
