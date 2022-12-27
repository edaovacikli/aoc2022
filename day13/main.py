def read_file(filename: str) -> list[str]:
    f = open(filename)
    contents = list(map(str.strip, f.readlines()))
    return contents


def parse_file(file_contents: list[str]) -> list:
    parsed_list = []
    word = ''
    for line in file_contents:
        temp_list = parsed_list
        depth = -1
        for char in line:
            if char == '[':
                depth += 1
                temp_list.append([])
                temp_list = temp_list[-1]
            elif char == ']':
                word = append_word(temp_list, word)
                depth -= 1
                temp_list = parsed_list[-1]
                for d in range(depth):
                    temp_list = temp_list[-1]
            elif char == ',':
                word = append_word(temp_list, word)
            else:
                word += char
    return parsed_list


def append_word(temp_list, word) -> str:
    if word != '':
        word = int(word)
        temp_list.append(word)
        word = ''
    return word


def compare_pairs(left_list: list, right_list: list, depth: int, verbose: bool) -> bool:
    if verbose:
        print('\t' * depth + f'- Compare {left_list} vs {right_list}')
    result = None

    for idx in range(len(left_list)):
        if idx >= len(right_list):
            if result is None:
                if verbose:
                    print('\t' * (depth + 1) + '- Right side ran out of items, so inputs are not in the right order')
                result = False
            return result

        # one or both of them are lists
        if isinstance(left_list[idx], list) or isinstance(right_list[idx], list):
            convert_int_to_list(idx, left_list)
            convert_int_to_list(idx, right_list)
            result = compare_pairs(left_list[idx], right_list[idx], depth + 1, verbose)
        else:  # if they are integers
            result = compare_int(left_list[idx], right_list[idx], depth + 1, verbose)

        if result is not None:
            return result

    if result is None:
        if len(left_list) < len(right_list):
            if verbose:
                print('\t' * (depth + 1) + '- Left side ran out of items, so inputs are in the right order')
            result = True
    return result


def compare_int(left_int: int, right_int: int, depth: int, verbose: bool):
    if verbose:
        print('\t' * depth + f'- Compare {left_int} vs {right_int}')
    if left_int < right_int:
        if verbose:
            print('\t' * (depth + 1) + '- Left side is smaller, so inputs are in the right order')
        return True
    elif left_int > right_int:
        if verbose:
            print('\t' * (depth + 1) + ' - Right side is smaller, so inputs are not in the right order')
        return False
    else:
        return None


def convert_int_to_list(int_index: int, list_to_convert: list):
    if not isinstance(list_to_convert[int_index], list):
        value = list_to_convert.pop(int_index)
        list_to_convert.insert(int_index, [value])


def part_one(packet_list: list):
    sum_pairs = 0
    for idx in range(0, len(packet_list), 2):
        pair_index = idx // 2 + 1
        print(f'== Pair {pair_index} ==')
        pair_result = compare_pairs(packet_list[idx], packet_list[idx + 1], 0, True)
        print()
        if pair_result:
            sum_pairs += pair_index
    print(sum_pairs)


def part_two(packet_list: list):
    key1 = [[2]]
    key2 = [[6]]
    packet_list.append(key1)
    packet_list.append(key2)

    bubble_sort(packet_list)

    key_index1 = packet_list.index(key1) + 1
    key_index2 = packet_list.index(key2) + 1

    print(key_index1 * key_index2)


def bubble_sort(packet_list: list):
    for idy in range(len(packet_list)):
        for idx in range(len(packet_list) - idy - 1):
            if not compare_pairs(packet_list[idx], packet_list[idx + 1], 0, False):
                temp = packet_list.pop(idx)
                packet_list.insert(idx + 1, temp)


if __name__ == '__main__':
    part_one(parse_file(read_file('input.txt')))
    part_two(parse_file(read_file('input.txt')))
