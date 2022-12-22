# coding=utf-8
class Knot:
    def __init__(self, name):
        self.name = name
        self._position = [0, 0]
        self.tail = None
        self.grid = [[0]]
        self.grid[0][0] = 1

    def __str__(self):
        rope = self
        grid = [['.'] * len(self.grid[0]) for _ in range(len(self.grid))]

        while rope is not None:
            grid[rope.position[1]][rope.position[0]] = rope.name
            rope = rope.tail
        s = '\t'
        for idx in range(len(grid[0])):
            s += str(idx + 1)
        s += '\n\n'
        for idy in range(len(grid) - 1, -1, -1):
            s += str(idy + 1) + '\t'
            for point in grid[idy]:
                s += point
            s += '\n'

        return s

    def move(self, direction: int, steps: int):
        for _ in range(abs(steps)):
            x = self.position[0]
            y = self.position[1]
            value = steps // abs(steps)
            if direction == 0:
                self.position = [x + value, y]
            else:
                self.position = [x, y + value]
            self.pull_tail()

    def pull_tail(self):
        if self.tail is not None:
            while (abs(self.diff[0]) > 1) or (abs(self.diff[1]) > 1):
                x = self.tail.position[0]
                y = self.tail.position[1]
                if self.diff[0] != 0:
                    x += self.diff[0] // abs(self.diff[0])
                if self.diff[1] != 0:
                    y += self.diff[1] // abs(self.diff[1])
                self.tail.position = [x, y]

            self.tail.pull_tail()

    def print_grid(self):
        s = ''
        for idy in range(len(self.grid) - 1, -1, -1):
            for point in self.grid[idy]:
                s += str(point) + ' '
            s += '\n'
        print(s)

    @property
    def diff(self):
        if self.tail is not None:
            x = self.position[0] - self.tail.position[0]
            y = self.position[1] - self.tail.position[1]
            return [x, y]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        while self._position[0] < 0:
            self.insert_column(0)
        while self._position[0] >= len(self.grid[0]):
            self.insert_column(len(self.grid[0]))
        while self._position[1] < 0:
            self.insert_row(0)
        while self._position[1] >= len(self.grid):
            self.insert_row(len(self.grid))
        self.grid[self._position[1]][self._position[0]] += 1

    def insert_row(self, index):
        self.grid.insert(index, [0] * len(self.grid[0]))
        if index == 0:
            self._position[1] += 1
        if self.tail is not None:
            self.tail.insert_row(index)

    def insert_column(self, index):
        for row in self.grid:
            row.insert(index, 0)
        if index == 0:
            self._position[0] += 1
        if self.tail is not None:
            self.tail.insert_column(index)


def read_file(filename: str):
    f = open(filename)
    contents = f.readlines()
    contents = list(map(str.strip, contents))
    return contents


def create_rope(num_knots: int):
    head = Knot('H')
    curr_knot = head
    for idx in range(1, num_knots):
        if idx == (num_knots - 1):
            knot_name = 'T'
        else:
            knot_name = str(idx)
        curr_knot.tail = Knot(knot_name)
        curr_knot = curr_knot.tail
    return head


def parse_motions(motion_list: list[str]):
    motions = []
    for motion in motion_list:
        direction, num_steps = motion.split()
        num_steps = int(num_steps)
        if (direction == 'U') or (direction == 'D'):
            d = 1
        else:
            d = 0
        if (direction == 'L') or (direction == 'D'):
            num_steps -= 2 * int(num_steps)
        motions.append([d, num_steps])
    return motions


def get_num_visited(rope: Knot):
    num_visited = 0
    for idx in rope.grid:
        for idy in idx:
            if idy > 0:
                num_visited += 1
    return num_visited


def puzzle(motions, num_knots):
    rope = create_rope(num_knots)
    for m in motions:
        rope.move(m[0], m[1])
        # print(rope)
    while rope.tail is not None:
        rope = rope.tail
    print(get_num_visited(rope))


if __name__ == '__main__':
    list_motions = parse_motions(read_file('input.txt'))
    puzzle(list_motions, 2)
    puzzle(list_motions, 10)
