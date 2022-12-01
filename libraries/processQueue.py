import os
import threading
import queue
from libraries import generateNetwork

class workQueue:

    def __init__(self):
        self.queue = queue.Queue()

    def worker(self):
        while True:
            runId = self.queue.get()
            print(f'Working on {runId}')
            generateNetwork.generate(f"uploadedData/{runId}.biom", runId)
            print(f'Finished {runId}')
            self.queue.task_done()
    def start(self):
        # Turn-on the worker thread.
        threading.Thread(target=self.worker, daemon=True).start()

    def finishTasks(self):
        # Block until all tasks are done.
        self.queue.join()
        print('All work completed')

    def addTask(self,runId):
        self.queue.put(runId)

