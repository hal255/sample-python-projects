import numpy as np
import timeit
import sys

def sample_numpy_list(n=100_000_000):
  new_arr = np.arange(n)
  print(sys.getsizeof(new_arr))
  other_arr = []
  print(sys.getsizeof(other_arr))
  new_list = {}
  print(sys.getsizeof(new_list))

  new_sum = np.sum(new_arr)
  return new_sum

def test():
  print('time to run numpy list: ', timeit.timeit(sample_numpy_list, number=1))

if __name__ == '__main__':
  test()
