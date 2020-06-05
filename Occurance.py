from pathlib import Path


class Occurance:
    def __init__(self, num, files):
        self.num = num
        self.files = files

    def __add__(self, other: tuple):
        if isinstance(other, Occurance):
            self.num += other.num
            self.files.extend(other.files)
        else:
            self.num += other[0]
            self.files.append(other[1])
        return self

    def __eq__(self, other):
        return self.num == other.num and len(set(map(Path, self.files)) ^ set(map(Path, other.files))) == 0

    def __repr__(self):
        return f'{self.num} - {self.files}'
