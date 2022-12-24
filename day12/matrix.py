def create_matrix(matrix_dim: list[int], initial_value) -> list[list[object]]:
    matrix = [[initial_value] * matrix_dim[0] for _ in range(matrix_dim[1])]
    return matrix


def get_matrix_dim(matrix: list[list[object]]) -> list[int]:
    matrix_dim = [len(matrix[0]), len(matrix)]
    return matrix_dim


def is_matrix_index_valid(matrix: list[list[object]], node: list[int]) -> bool:
    matrix_dim = get_matrix_dim(matrix)
    return (node[0] in range(matrix_dim[0])) and (node[1] in range(matrix_dim[1]))


def is_any(matrix: list[list[object]]) -> bool:
    matrix_dim = get_matrix_dim(matrix)
    for idy in range(matrix_dim[1]):
        for idx in range(matrix_dim[0]):
            if get_matrix_value(matrix, [idx, idy]) is not None:
                return True
    return False


def is_all(matrix: list[list[object]]) -> bool:
    matrix_dim = get_matrix_dim(matrix)
    for idy in range(matrix_dim[1]):
        for idx in range(matrix_dim[0]):
            if get_matrix_value(matrix, [idx, idy]) is None:
                return False
    return True


def set_matrix_value(matrix: list[list[object]], node: list[int], value):
    if is_matrix_index_valid(matrix, node):
        matrix[node[1]][node[0]] = value
    else:
        raise


def get_matrix_value(matrix: list[list[object]], node: list[int]):
    if is_matrix_index_valid(matrix, node):
        return matrix[node[1]][node[0]]
    else:
        raise


def print_matrix(matrix: list[list[object]]):
    s = ''
    for idy in range(len(matrix)):
        for idx in range(len(matrix[0])):
            if matrix[idy][idx] is None:
                s += '--'
            else:
                s += str(matrix[idy][idx]).zfill(2)
            s += ' '
        s += '\n'
    s += '\n'
    print(s)
