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