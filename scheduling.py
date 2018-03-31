import datetime

class Worker:
    def __init__(self, name, type_list, preferences=None):
        self.name = name
        self.task_list = []
        if preferences:
            self.preferences = preferences
        else:
            avg = len(type_list) // 2
            self.preferences = dict()
            for type_task in type_list:
                self.preferences[type_task] = avg

    def addTask(self, task):
        self.task_list.append(task.addworker())

    def canAccept(self, try_task):
        for task in self.task_list:
            if task.start <= try_task.start < task.end or task.start < try_task.end < task.end:
                return False
        return True

    def __repr__(self):
        return str(self.task_list)

class Task:
    def __init__(self, name, task_type, start, end, nb_workers):
        self.start = start
        self.end = end
        self.nb_workers = nb_workers
        self.current_nb_workers = 0
        self.name = name
        self.task_type = task_type

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
            workers_sorted = sorted(self.workers.values(), key = lambda key: key.preferences[task.task_type])
            for worker in workers_sorted:
                if not task.is_full() and worker.canAccept(task):
                    worker.addTask(task)
        reste = [task for task in self.task_list if task.nb_workers != task.current_nb_workers]
        return str(self.workers) + "_" + str(reste)
now = datetime.datetime.now()

tasks = []
names = ["Toto", "Tata", "Titi"]
types = ["Vaisselle", "Menage"]

preference1 = {"Vaisselle":0, "Menage": 2}
workers = [Worker(name, types) for name in names]
workers[1].preferences = preference1

offset = datetime.timedelta(days=1)

for i in range(7):
    current_start = now + offset
    current_end = current_start + datetime.timedelta(days=1)
    offset += datetime.timedelta(days=1)
    name = "Task_" + str(i)
    if i % 2 == 0:
        tasks.append(Task(name, types[0], current_start, current_end, 1))
    else:        
        tasks.append(Task(name, types[1], current_start, current_end, 2))

solver = Solver(tasks, len(types), workers)
print(solver.solve())



