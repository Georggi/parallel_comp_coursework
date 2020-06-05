import unittest
import timeit
import pandas as pd

from Index import Index
from multiprocessing import cpu_count

from Occurance import Occurance


class MyTestCase(unittest.TestCase):
    """
    Unit test for automatic testing of speed and validity for reverse index building
    """

    def test_speed(self):
        """
        Function for testing speed of index building and generating speed perfomance result
        """
        df = pd.DataFrame(columns=['Process count', 'Speed (s)'])
        for proc_count in range(min(max(cpu_count(), 1), 12)):
            ind = Index('F:/aclImdb', 22, True)
            speed = timeit.timeit(lambda: ind.build(proc_count+1), number=1)
            df = df.append({'Process count': int(proc_count), 'Speed (s)': speed}, ignore_index=True)
            print(f'{proc_count=} : {speed} seconds')
            self.assertGreater(45, speed)
        ind = Index('F:/aclImdb', 22, True)
        speed = timeit.timeit(lambda: ind.build_sequential(), number=1)
        df = df.append({'Process count': 'Sequential(optimized)', 'Speed (s)': speed}, ignore_index=True)

        for proc_count in range(min(max(cpu_count(), 1), 12)):
            ind = Index('F:/aclImdb', 22, False)
            speed = timeit.timeit(lambda: ind.build(proc_count+1), number=1)
            df = df.append({'Process count': f'Variant only: {proc_count}', 'Speed (s)': speed}, ignore_index=True)
            print(f'{proc_count=} : {speed} seconds')
            self.assertGreater(45, speed)
        ind = Index('F:/aclImdb', 22, False)
        speed = timeit.timeit(lambda: ind.build_sequential(), number=1)
        df = df.append({'Process count': 'Variant only: Sequential(optimized)', 'Speed (s)': speed}, ignore_index=True)

        df.to_csv('test_results.csv', index=False)

    def test_validity(self):
        """
        Function for testing validity of data
        """
        path = 'F:/aclImdb'
        ind = Index(path, 22, True)
        ind.build(12)
        test_occ = Occurance(15, [f'{path}\\test\\neg\\2682_1.txt', f'{path}\\test\\pos\\576_8.txt',
                                  f'{path}\\test\\pos\\7485_7.txt', f'{path}\\train\\neg\\1624_1.txt',
                                  f'{path}\\train\\neg\\1627_1.txt', f'{path}\\train\\neg\\5930_3.txt',
                                  f'{path}\\train\\neg\\5933_2.txt', f'{path}\\train\\neg\\5934_2.txt',
                                  f'{path}\\train\\neg\\9569_4.txt', f'{path}\\train\\unsup\\21375_0.txt',
                                  f'{path}\\train\\unsup\\4353_0.txt', f'{path}\\train\\unsup\\4358_0.txt'])
        self.assertEqual(test_occ, ind.find('Jarvis'))
        self.assertEqual(None, ind.find('SAO'))


if __name__ == '__main__':
    unittest.main()
