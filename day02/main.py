# coding=utf-8
class Shape:
    def __init__(self):
        self.value = 0

    def win_decision(self, opponent_move) -> int:
        pass

    def win(self):
        pass

    def lose(self):
        pass

    def draw(self):
        pass


class Game:
    win = 6
    lose = 0
    draw = 3

    @staticmethod
    def play_round(your_move: Shape, opponent_move: Shape) -> int:
        return your_move.value + your_move.win_decision(opponent_move)

    def play(self, your_moves: list[Shape], opponent_moves: list[Shape]) -> \
            int:
        score = 0
        for idx in range(len(your_moves)):
            score += self.play_round(your_moves[idx], opponent_moves[idx])
        return score


class Rock(Shape):
    def __init__(self):
        super().__init__()
        self.value = 1

    def win_decision(self, opponent: Shape) -> int:
        if isinstance(opponent, Rock):
            return Game.draw
        elif isinstance(opponent, Paper):
            return Game.lose
        elif isinstance(opponent, Scissors):
            return Game.win
        else:
            raise ValueError

    def win(self) -> Shape:
        return Scissors()

    def lose(self) -> Shape:
        return Paper()

    def draw(self) -> Shape:
        return Rock()


class Paper(Shape):
    def __init__(self):
        super().__init__()
        self.value = 2

    def win_decision(self, opponent: Shape) -> int:
        if isinstance(opponent, Rock):
            return Game.win
        elif isinstance(opponent, Paper):
            return Game.draw
        elif isinstance(opponent, Scissors):
            return Game.lose
        else:
            raise ValueError

    def win(self) -> Shape:
        return Rock()

    def lose(self) -> Shape:
        return Scissors()

    def draw(self) -> Shape:
        return Paper()


class Scissors(Shape):
    def __init__(self):
        super().__init__()
        self.value = 3

    def win_decision(self, opponent: Shape) -> int:
        if isinstance(opponent, Rock):
            return Game.lose
        elif isinstance(opponent, Paper):
            return Game.win
        elif isinstance(opponent, Scissors):
            return Game.draw
        else:
            raise ValueError

    def win(self) -> Shape:
        return Paper()

    def lose(self) -> Shape:
        return Rock()

    def draw(self) -> Shape:
        return Scissors()


def get_opponent_move(move: str) -> Shape:
    if move == 'A':
        return Rock()
    elif move == 'B':
        return Paper()
    elif move == 'C':
        return Scissors()
    else:
        raise ValueError


def get_your_move_part1(move: str) -> Shape:
    if move == 'X':
        return Rock()
    elif move == 'Y':
        return Paper()
    elif move == 'Z':
        return Scissors()
    else:
        raise ValueError


def get_your_move_part2(opponent_move: Shape, move: str) -> Shape:
    if move == 'X':
        return opponent_move.win()
    elif move == 'Y':
        return opponent_move.draw()
    elif move == 'Z':
        return opponent_move.lose()
    else:
        raise ValueError


def read_file(filename: str) -> list[str]:
    f = open(filename)
    contents = f.readlines()
    return contents


def parse_file(file_contents: list[str], move_chooser,
               is_part_two: bool = False):
    your_move = []
    opponent_move = []
    for line in file_contents:
        moves = (line.strip()).split()
        opponent_move.append(get_opponent_move(moves[0]))
        if is_part_two:
            your_move.append(move_chooser(opponent_move[-1], moves[1]))
        else:
            your_move.append(move_chooser(moves[1]))

    return your_move, opponent_move


def part_one(file_contents: list[str]):
    your_move, opponent_move = parse_file(file_contents, get_your_move_part1)
    game = Game()
    print(f'Part 1: {game.play(your_move, opponent_move)}')


def part_two(file_contents: list[str]):
    your_move, opponent_move = parse_file(file_contents, get_your_move_part2,
                                          True)
    game = Game()
    print(f'Part 2: {game.play(your_move, opponent_move)}')


if __name__ == '__main__':
    file = read_file('input.txt')
    part_one(file)
    part_two(file)
