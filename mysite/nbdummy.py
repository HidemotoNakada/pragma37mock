
from enum import Enum
import datetime
import uuid

class NotebookStatus(Enum):
    INIT = 0
    RUNNING = 1
    SHUTTINGDOWN = 2
    DONE = 3

class Notebook(object):
    def __init__(self, id, cr, dr, mod):
        self.id = id
        self.cr = cr    
        self.dr = dr
        self.mod = mod
        self.time = datetime.datetime.now()
        self.url = None
        self.status = NotebookStatus.INIT

    def getStatusDict(self):
        if self.status == NotebookStatus.INIT and datetime.datetime.now() - self.time > datetime.timedelta(0, 10, 0):
            self.status = NotebookStatus.RUNNING 
        
        return {"id": self.id.__str__(), 
                "time": self.time.__str__(), 
                "url": self.url, 
                "cr": self.cr,
                "status": self.status.name}


class NotebookManager(object):
    def __init__(self):
        self.notebooks = []

    def launch(self, cr, dr, mod):
        id = uuid.uuid4()
        self.notebooks.append(Notebook(id, cr, dr, mod))

    def shutdown(self, id):
        for nb in self.notebooks:
            if nb.id.__str__() == id:
                nb.status = NotebookStatus.DONE

    def getStatusDictList(self):
        return [nb.getStatusDict() for nb in self.notebooks]

