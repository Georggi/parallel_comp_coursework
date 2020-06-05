import os
import string
from multiprocessing import Pool
from collections import Counter
from Occurance import Occurance
from more_itertools import distribute, flatten


def merge_into_dict(initital, *dicts):
    for k, v in flatten(i.items() for i in dicts):
        if k in initital:
            initital[k] += v
        else:
            initital[k] = v


class Index:
    def __init__(self, scope, variant, _all):
        self.files = []
        self.init_files(scope, variant, _all)
        self.db = {}
        self._all = _all

    def init_files(self, scope, variant, all_):
        for folder in os.listdir(scope):
            for folder2 in os.listdir(os.path.join(scope, folder)):
                if os.path.isdir(file_folder := os.path.join(scope, folder, folder2)):
                    files = os.listdir(file_folder)
                    if all_:
                        self.files.extend(os.path.join(file_folder, file) for file in files)
                    else:
                        self.files.extend(os.path.join(file_folder, file)
                                          for file in sorted(files, key=lambda x: int(x.split('_')[0]))[
                                                      len(files) // 50 * (variant - 1):len(files) // 50 * variant])

    def build(self, cpu_count):
        with Pool(processes=cpu_count) as pool:
            data = pool.starmap(self.add_to_local_index, ([chunk] for chunk in distribute(cpu_count, self.files)))
        merge_into_dict(self.db, *data)

    @staticmethod
    def add_to_local_index(files):
        local_dict = {}
        for file in files:
            try:
                with open(file, encoding="utf8") as f:
                    text = f.read()
                text.translate(str.maketrans('', '', string.punctuation))
                words = text.split(' ')
                counter = Counter(words)
                for k, v in counter.items():
                    if k in local_dict:
                        local_dict[k] += (v, file)
                    else:
                        local_dict[k] = Occurance(v, [file])
            except Exception as e:
                print(e, file)
        return local_dict

    def find(self, value):
        return self.db.get(value, None)

    def build_sequential(self):
        for file in self.files:
            try:
                with open(file, encoding="utf8") as f:
                    text = f.read()
                text.translate(str.maketrans('', '', string.punctuation))
                words = text.split(' ')
                counter = Counter(words)
                for k, v in counter.items():
                    if k in self.db:
                        self.db[k] += (v, file)
                    else:
                        self.db[k] = Occurance(v, file)
            except Exception as e:
                print(e, file)
