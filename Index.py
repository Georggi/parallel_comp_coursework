import os
from multiprocessing import Manager, Pool


class Index:
    def __init__(self, scope, variant):
        self.files = []
        self.init_files(scope, variant)

    def init_files(self, scope, variant):
        for folder in os.listdir(scope):
            for folder2 in os.listdir(os.path.join(scope, folder)):
                if os.path.isdir(file_folder := os.path.join(scope, folder, folder2)):
                    files = os.listdir(file_folder)
                    self.files.extend(os.path.join(file_folder, file)
                                      for file in sorted(files, key=lambda x: int(x.split('_')[0]))[
                                                  len(files) // 50 * (variant - 1):len(files) // 50 * variant])

    def build(self, cpu_count):
        with Pool(cpu_count) as pool:
            pool.map(self.add_to_index, self.files)
