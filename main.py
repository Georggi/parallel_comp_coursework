import timeit
from Index import Index
var = 22


if __name__ == '__main__':
    thread_count = int(input("Input thread count: "))
    print('Starting parallel index build...')
    ind = Index('F:/aclImdb', 22, True)
    print(timeit.timeit(lambda: ind.build(thread_count), number=1))
    print('Starting sequential index build...')
    ind2 = Index('F:/aclImdb', 22, True)
    print(timeit.timeit(lambda: ind2.build_sequential(), number=1))

    while (user_input := input('Enter words to search in index: ')) != '':
        for val in user_input.split(' '):
            print(val, ind.find(val))
