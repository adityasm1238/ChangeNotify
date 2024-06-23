import time


class JobRunner:
    def __init__(self) -> None:
        self._curID = 0
        self.jobs = {}
        self.timestamps = {}
        self.context = {}
        self.intervals = {}
    
    def run(self):
        while True:
            for key in self.jobs.keys():
                if key in self.timestamps:
                    if time.time() - self.timestamps[key] > self.intervals[key]:
                        self.runJob(key)
                else:
                    self.runJob(key)
            time.sleep(5)



    def submit(self, job, interval):
        self.jobs[self._curID] = job
        self.intervals[self._curID] = interval
        self._curID += 1
    
    def runJob(self, id):
        self.timestamps[id] = time.time()
        jb = self.jobs[id]
        jb(id).start()


