# coding=utf-8
home_dir = '/'
up_dir = '..'


class Directory:
    def __init__(self, parent, name: str):
        self.parent = parent
        self.name = name
        self.child_directories = []
        self.files = []

    def __str__(self):
        s = '\t' * (self.depth - 1)
        s += f"- {self.name} (dir, size = {self.size})\n"
        for child in self.child_directories:
            s += child.__str__()
        for file in self.files:
            s += '\t' * self.depth
            s += f"{file.__str__()}"
        return s

    def change_directory(self, dir_name: str):
        if dir_name == up_dir:
            return self.parent
        elif dir_name == home_dir:
            if self.parent is None:
                return self
            else:
                self.parent.change_directory(home_dir)
        else:
            for child in self.child_directories:
                if child.name == dir_name:
                    return child

    def add_directory(self, dir_name: str):
        self.child_directories.append(Directory(self, dir_name))

    def add_file(self, file_name: str, file_size: int):
        self.files.append(File(self, file_name, file_size))

    @property
    def size(self):
        sum_size = 0
        for child in self.child_directories:
            sum_size += child.size
        for file in self.files:
            sum_size += file.size
        return sum_size

    @property
    def depth(self):
        if self.parent is None:
            return 1
        else:
            return self.parent.depth + 1


class File:
    def __init__(self, parent_dir: Directory, name: str, size: int):
        self.parent_directory = parent_dir
        self.name = name
        self.size = size

    def __str__(self):
        return f"- {self.name} (file, size = {self.size})\n"


def read_file(filename: str):
    f = open(filename)
    contents = f.readlines()
    return contents


def parse_file(lines: list[str]):
    cmd = '$'
    cd = 'cd'

    file_system = Directory(None, '/')
    curr_dir = file_system

    for line in lines:
        if cmd in line:
            if cd in line:
                dir_name = line.split()[-1]
                curr_dir = curr_dir.change_directory(dir_name)
        elif 'dir' in line:
            dir_name = line.split()[-1]
            curr_dir.add_directory(dir_name)
        else:
            file_size = int(line.split()[0])
            file_name = line.split()[-1]
            curr_dir.add_file(file_name, file_size)

    return file_system


def dir_with_max_size(dirs, directory: Directory, max_size: int):
    if directory.size <= max_size:
        dirs.append(directory)
    for child in directory.child_directories:
        dir_with_max_size(dirs, child, max_size)


def dir_with_min_size(dirs, directory: Directory, min_size: int):
    if directory.size >= min_size:
        dirs.append(directory)
    for child in directory.child_directories:
        dir_with_min_size(dirs, child, min_size)


def part_one(file_system: Directory):
    dirs = []
    dir_with_max_size(dirs, file_system, 100000)
    print(sum([x.size for x in dirs]))


def part_two(file_system: Directory):
    total_disk_space = 70000000
    needed_unused = 30000000
    unused = total_disk_space - file_system.size
    needed = needed_unused - unused
    dirs = []
    dir_with_min_size(dirs, file_system, needed)
    print(min([x.size for x in dirs]))


if __name__ == '__main__':
    files = parse_file(read_file('input.txt'))
    part_one(files)
    part_two(files)
