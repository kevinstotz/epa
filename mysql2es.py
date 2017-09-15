#!/usr/bin/python
#!/usr/bin/env python
from multiprocessing import Lock, Process, Queue, current_process

def worker(work_queue, done_queue):
    try:
        for i in iter(work_queue.get, 'STOP'):
           print(i)
    except Exception, e:
        done_queue.put("%s failed on %s with: %s" % (current_process().name, url, e.message))
    return True


def main():
    workers = 2
    work_queue = Queue()
    done_queue = Queue()
    processes = []

    for i in range(150000):
        work_queue.put(i)

    for w in xrange(workers):
        p = Process(target=worker, args=(work_queue, done_queue))
        p.start()
        processes.append(p)
        work_queue.put('STOP')

    for p in processes:
        p.join()

    done_queue.put('STOP')

    for status in iter(done_queue.get, 'STOP'):
        print status


if __name__ == '__main__':
    main()
