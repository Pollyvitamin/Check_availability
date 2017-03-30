import os
import multiprocessing
import subprocess


devices = ['192.168.100.1', '192.168.100.155', '8.8.8.8', '4.4.4.4']

DNULL = open(os.devnull, 'w')
def ping(host,mp_queue):
    response = subprocess.call(["ping", "-c", "2", "-w", '2', host], stdout=DNULL)
    if response == 0:
        print(host, 'is up!')
        result = True
    else:
        print(host, 'is down!')
        result = False
    mp_queue.put((result,host))

def worker(devices):
    mp_queue = multiprocessing.Queue()
    processes = []
    for device in devices:
        p = multiprocessing.Process(target=ping, args=(device, mp_queue))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    results = {True:[], False:[]}
    for p in processes:
        key, value =  mp_queue.get()
        results[key] += [value]
    return results[True], results[False]

success, failed = worker(devices)
