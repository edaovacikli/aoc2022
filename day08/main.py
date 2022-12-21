# coding=utf-8
def read_map(filename: str):
    f = open(filename)
    return list(map(list, list(map(str.strip, f.readlines()))))


def transpose_forest(forest):
    return list(map(list, list(zip(*forest))))

def is_tree_visible(forest, tree_m, tree_n):
    down, score_down = is_visible_in_direction(forest, tree_m, tree_n, False)
    up, score_up = is_visible_in_direction(forest, tree_m, tree_n, True)
    forest = transpose_forest(forest)
    left, score_left = is_visible_in_direction(forest, tree_n, tree_m, False)
    right, score_right = is_visible_in_direction(forest, tree_n, tree_m, True)
    return (up or down or left or right), \
           (score_down * score_up * score_left * score_right)


def is_visible_in_direction(forest, tree_m, tree_n, up: bool):
    if up:
        ran = range(tree_m - 1, -1, -1)
    else:
        ran = range(tree_m + 1, len(forest))

    result = True
    score = 0
    tree = forest[tree_m][tree_n]

    for idm in ran:
        score += 1
        if forest[idm][tree_n] >= tree:
            result = False
            break
        else:
            result = True
    return result, score


def puzzle(forest):
    sum_visible = 0
    max_score = 0
    for idm, tree_line in enumerate(forest):
        for idn, tree in enumerate(tree_line):
            is_visible, score = is_tree_visible(forest, idm, idn)
            if is_visible:
                sum_visible += 1
            if score > max_score:
                max_score = score
    print(sum_visible)
    print(max_score)


if __name__ == '__main__':
    forest_map = read_map('input.txt')
    puzzle(forest_map)
