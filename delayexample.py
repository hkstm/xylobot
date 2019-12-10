import multiprocessing
import time

def sleep(seconds):
    time.sleep(seconds)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=sleep, args=[3])
    p1.start()
    print(f'test 1')
    p1.join()
    print('test 2')