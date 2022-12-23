# coding=utf-8
class CPU:
    def __init__(self):
        self.register = [1]

    def addx(self, value):
        self.noop()
        self.register.append(self.register[-1] + value)

    def noop(self):
        self.register.append(self.register[-1])

    def parse_instructions(self, file_contents):
        for line in file_contents:
            if line == 'noop':
                self.noop()
            elif 'addx' in line:
                value = int(line.split()[-1])
                self.addx(value)

    @property
    def signal_strength(self):
        strength = self.register.copy()
        for idx in range(len(strength)):
            strength[idx] *= (idx + 1)
        return strength


class CRT:
    def __init__(self, width, height, sprite_length):
        self.width = width
        self.height = height
        self.sprite_length = sprite_length
        self.screen = [[' '] * width for _ in range(height)]

    def __str__(self):
        s = ''
        for idy in range(self.height):
            for idx in range(self.width):
                s += self.screen[idy][idx]
            s += '\n'
        return s

    def draw_screen(self, cpu):
        for idx, x in enumerate(cpu.register):
            sprite = x - self.sprite_length // 2
            if (idx % self.width) in range(sprite,
                                           sprite + self.sprite_length):
                self.screen[idx // self.width][idx % self.width] = '#'


def read_file(filename):
    f = open(filename)
    return list(map(str.strip, f.readlines()))


def part_one():
    sum_signal = 0
    for idx in range(19, 240, 40):
        sum_signal += cpu.signal_strength[idx]
    print(sum_signal)


def part_two():
    crt = CRT(40, 6, 3)
    crt.draw_screen(cpu)
    print(crt)


if __name__ == '__main__':
    cpu = CPU()
    instructions = read_file('input.txt')
    cpu.parse_instructions(instructions)
    part_one()
    part_two()
