# S = a, E = z
# up, down, left, right
# destination at most one higher
# destination can be much lower
import matrix as m


def read_file(filename: str) -> list[str]:
    f = open(filename)
    contents = list(map(str.strip, f.readlines()))
    return contents


def parse_file(file_contents: list[str]):
    map_dim = [len(file_contents[0]), len(file_contents)]
    heightmap = m.create_matrix(map_dim, 0)

    source_node = [None, None]
    destination_node = [None, None]

    for idy, line in enumerate(file_contents):
        for idx, char in enumerate(line):
            if char == 'S':
                value = ord('a') - ord('a')
                source_node = [idx, idy]
            elif char == 'E':
                value = ord('z') - ord('a')
                destination_node = [idx, idy]
            else:
                value = ord(char) - ord('a')
            m.set_matrix_value(heightmap, [idx, idy], value)

    return heightmap, source_node, destination_node


def parse_file_reverse(file_contents: list[str]):
    map_dim = [len(file_contents[0]), len(file_contents)]
    heightmap = m.create_matrix(map_dim, 0)

    source_node = [None, None]
    destination_node = [None, None]

    for idy, line in enumerate(file_contents):
        for idx, char in enumerate(line):
            if char == 'S':
                value = ord('z') - ord('a')
                destination_node = [idx, idy]
            elif char == 'E':
                value = ord('a') - ord('a')
                source_node = [idx, idy]
            else:
                value = ord('z') - ord(char)
            m.set_matrix_value(heightmap, [idx, idy], value)

    return heightmap, source_node, destination_node


def calc_paths(heightmap: list[list[object]], source_node: list[int], destination_node=None):
    map_dim = m.get_matrix_dim(heightmap)
    unvisited = m.create_matrix(map_dim, None)
    visited = m.create_matrix(map_dim, None)

    m.set_matrix_value(unvisited, source_node, 0)
    curr_node = source_node
    while 1:
        for idy in range(-1, 2):
            for idx in range(-1, 2):
                if abs(idx) != abs(idy):
                    neighbor_node = [curr_node[0] + idx, curr_node[1] + idy]
                    consider_neighbor(heightmap, unvisited, visited, curr_node, neighbor_node)

        set_visited(unvisited, visited, curr_node)
        curr_node = get_min_node(unvisited)
        if ((destination_node is not None) and (
                m.get_matrix_value(visited, destination_node) is not None)) or not m.is_any(unvisited):
            break
    return visited


def get_min_node(unvisited):
    map_dim = m.get_matrix_dim(unvisited)
    min_val = None
    min_node = []
    for idy in range(map_dim[1]):
        for idx in range(map_dim[0]):
            value = m.get_matrix_value(unvisited, [idx, idy])
            if value is not None:
                if (min_val is None) or (value < min_val):
                    min_val = value
                    min_node = [idx, idy]
    return min_node


def consider_neighbor(heightmap: list[list[object]], unvisited: list[list[object]], visited: list[list[object]],
                      source_node: list[int], neighbor_node: list[int]):
    if can_visit(heightmap, source_node, neighbor_node):
        if m.get_matrix_value(visited, neighbor_node) is None:
            value = m.get_matrix_value(unvisited, source_node) + 1
            neighbor_distance = m.get_matrix_value(unvisited, neighbor_node)
            if (neighbor_distance is None) or (value < neighbor_distance):
                m.set_matrix_value(unvisited, neighbor_node, value)


def can_visit(heightmap: list[list[object]], source_node: list[int], neighbor_node: list[int]) -> bool:
    is_neighbor_accessible = False

    if m.is_matrix_index_valid(heightmap, neighbor_node):
        source_height = m.get_matrix_value(heightmap, source_node)
        neighbor_height = m.get_matrix_value(heightmap, neighbor_node)
        is_neighbor_accessible = (source_height == neighbor_height - 1) or (source_height >= neighbor_height)

    return is_neighbor_accessible


def set_visited(unvisited: list[list[object]], visited: list[list[object]], node: list[int]):
    m.set_matrix_value(visited, node, m.get_matrix_value(unvisited, node))
    m.set_matrix_value(unvisited, node, None)


def part_one(heightmap, source_node, destination_node):
    visited = calc_paths(heightmap, source_node, destination_node)
    path = m.get_matrix_value(visited, destination_node)
    print(path)


def part_two(heightmap, source_node):
    visited = calc_paths(heightmap, source_node)
    node_val = ord('z') - ord('a')
    map_dim = m.get_matrix_dim(visited)
    min_path = None
    for idy in range(map_dim[1]):
        for idx in range(map_dim[0]):
            node = [idx, idy]
            if m.get_matrix_value(heightmap, node) == node_val:
                path = m.get_matrix_value(visited, node)
                if (min_path is None) or (path is not None and (path < min_path)):
                    min_path = path
    print(min_path)


if __name__ == '__main__':
    file_ = read_file('input.txt')
    h_map, s_node, d_node = parse_file(file_)
    part_one(h_map, s_node, d_node)
    h_map, s_node, d_node = parse_file_reverse(file_)
    part_two(h_map, s_node)
