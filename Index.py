import os
import string
from multiprocessing import Process, Manager, Queue
from collections import Counter
from Occurance import Occurance


class Index:
    def __init__(self, scope, variant, _all):
        self.files = []
        self.init_files(scope, variant, _all)
        self.db = Manager().dict()
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

        queue = Queue()
        send_queue = Queue()
        processes = [Process(target=self.add_to_index, args=(queue, send_queue, ), name=f'proc{i}') for i in range(cpu_count)]
        updaters = [Process(target=self.process_queue, args=(send_queue,), name=f'upd{i}') for i in range(cpu_count)]
        for updater in updaters:
            updater.start()
        for i in processes:
            i.start()
        for i in self.files:
            queue.put(i)
        for _ in processes:
            queue.put(None)
        for i in processes:
            i.join()
        for _ in updaters:
            send_queue.put(None)
        for updater in updaters:
            updater.join()

    @staticmethod
    def add_to_index(queue, send_queue):
        while (file := queue.get()) is not None:
            try:
                with open(file, encoding="utf8") as f:
                    text = f.read()
                    text.translate(str.maketrans('', '', string.punctuation))
                    words = text.split(' ')
                counter = Counter(words)
                send_queue.put((counter, file))
            except Exception as e:
                print(e, file)

    def process_queue(self, s_queue):
        local_dict = {}
        while item := s_queue.get():
            counter, file = item
            for k, v in counter.items():
                if k in local_dict:
                    local_dict[k] += (v, file)
                else:
                    local_dict[k] = Occurance(v, file)
        self.db.update(local_dict)

    def find(self, value):
        return self.db.get(value, None)

    def build_sequential(self):
        local_dict = {}
        for file in self.files:
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
                        local_dict[k] = Occurance(v, file)
            except Exception as e:
                print(e, file)
        self.db.update(local_dict)
