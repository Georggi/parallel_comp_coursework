class Occurance:
    def __init__(self, num, file):
        self.num = num
        self.files = [file]

    def __add__(self, other: tuple):
        if isinstance(other, Occurance):
            self.num += other.num
            self.files.extend(other.files)
        else:
            self.num += other[0]
            self.files.append(other[1])
        return self

    def __repr__(self):
        return f'{self.num} - {self.files}'
