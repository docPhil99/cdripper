import sys
import os
import threading
import queue
import subprocess

tail_queue = queue.Queue(maxsize=100)

def tail(file):
    p = subprocess.Popen(["tail", "-n", "100", "-f", file], stdout=subprocess.PIPE)
    while 1:
        line = p.stdout.readline().decode('UTF-8')
        if line.startswith(('Tagging track', 'Encoding track','Grabbing track','Grabbing entire CD')):
            tail_queue.put(line)
        if not line:
            break

def main():
    threading.Thread(target=tail, args=(sys.argv[1],)).start()

    while 1:
        line = tail_queue.get()
        # do something here
        print (line)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

