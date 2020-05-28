from Index import Index
from multiprocessing import Lock
var = 22
thread_count = 1


if __name__ == '__main__':
    ind = Index('../aclImdb', 22)
    ind.build(3)
