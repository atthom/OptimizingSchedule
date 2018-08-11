
class Task:
    def __init__(self, number, task_type, start, end, nb_workers, difficulties=1):
        self.start = start
        self.end = end
        self.nb_workers = nb_workers
        self.current_nb_workers = 0
        self.name = task_type + "_" + number
        self.task_type = task_type
        self.difficulties = difficulties

    def addworker(self):
        self.current_nb_workers += 1
        return self

    def is_full(self):
        return self.nb_workers == self.current_nb_workers

    def __repr__(self):
        return self.name