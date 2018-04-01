import datetime

class Worker:
    def __init__(self, name, type_list, unavailable_periodes=[], preferences=None):
        self.name = name
        self.task_list = []
        self.charge = 0
        self.unavailable_periodes = unavailable_periodes

        if preferences:
            self.preferences = preferences
        else:
            avg = len(type_list) // 2
            self.preferences = dict()
            for type_task in type_list:
                self.preferences[type_task] = avg

    def addTask(self, task):
        self.charge += task.difficulties
        self.task_list.append(task.addworker())

    def canAccept(self, try_task):
        for periode in self.unavailable_periodes:
            if periode[0] <= try_task.start < periode[1] or periode[0] < try_task.end < periode[1]:
                return False

        for task in self.task_list:
            if task.start <= try_task.start < task.end or task.start < try_task.end < task.end:
                return False
        return True

    def __repr__(self):
        return str(self.task_list)

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

class Solver:
    def __init__(self, task_list, nb_types, worker_list):
        self.workers = dict()
        self.task_list = task_list
        self.nb_types = nb_types
        for worker in worker_list:
            self.workers[worker.name] = worker

    def solve(self):
        for task in self.task_list:
            workers_sorted = sorted(self.workers.values(), key = lambda item: item.preferences[task.task_type], reverse=True)
            workers_sorted = sorted(workers_sorted, key = lambda item: item.charge)
            for worker in workers_sorted:
                if not task.is_full() and worker.canAccept(task):
                    worker.addTask(task)
        reste = [task for task in self.task_list if task.nb_workers != task.current_nb_workers]
        return self.workers, reste
