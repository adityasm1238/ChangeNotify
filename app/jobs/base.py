from logging import getLogger
import threading
import os
import json
import os.path


class Job(threading.Thread):
    JOB_NAME = 'jobName'
    def __init__(self,id, name):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.logger = getLogger('chngNotify.job.'+str(id))
        self.context = {}

    def start(self) -> None:
        """Starts bot thread.
        """
        self.logger.debug("Job is starting for {}".format(self.name))
        self.loadContext()
        super().start()
    
    def loadContext(self) -> None:
        contextPath = os.environ['CONTEXT_DIRECTORY']
        print(contextPath)
        if os.path.isfile(contextPath+self.JOB_NAME+'.context'):
            with open(contextPath+self.JOB_NAME+'.context') as f:
                self.context = json.load(f)
    
    def dumpContext(self) -> None:
        contextPath = os.environ['CONTEXT_DIRECTORY']
        with open(contextPath+self.JOB_NAME+'.context', 'w') as f:
            json.dump(self.context, f)

    def run(self):
        raise NotImplementedError()

    def __str__(self):
        return 'Job: {}'.format(self.name)

    def __repr__(self):
        return '<Job : {}>'.format(self.name)