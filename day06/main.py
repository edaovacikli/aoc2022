# coding=utf-8
def read_file(filename: str) -> str:
    f = open(filename)
    return f.readline()


def is_all_different(buffer: str):
    for idx in range(len(buffer)):
        for idy in range(idx + 1, len(buffer)):
            if buffer[idx] == buffer[idy]:
                return False
    return True


def puzzle(file: str, num_diff_char):
    for idx in range(len(file)):
        buffer = file[idx:idx + num_diff_char]
        if is_all_different(buffer):
            print(idx + num_diff_char)
            return


if __name__ == '__main__':
    message = read_file('input.txt')
    puzzle(message, 4)
    puzzle(message, 14)
