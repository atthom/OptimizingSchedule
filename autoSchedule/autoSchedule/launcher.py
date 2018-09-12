from datetime import datetime, timedelta

from .core.Solver import Solver
from .core.Task import Task
from .core.Worker import Worker


def launch(session_range, worker_names, str_tasks):
    print("launch")
    all_types = [t[0] for t in str_tasks]
    workers = [Worker(name, all_types) for name in worker_names]
    
    begin, end = session_range.split(" - ")
    begin = datetime.strptime(begin, '%d/%m/%Y')
    end = datetime.strptime(end, '%d/%m/%Y')
    delta_days = (end - begin).days
    all_tasks = []
    
    for t in str_tasks:
        one_day = timedelta(days=1)
        for i in range(delta_days):
            start = datetime.strptime(t[2], '%d/%m/%Y %H:%M') + one_day * i
            end = start + t[3]
            task = Task(i, t[0], start, end, t[1], difficulty=t[4])
            all_tasks.append(task)
            if t[-1] == False:
                break
    solver = Solver(all_tasks, len(all_types), workers)
    true_workers, rest = solver.solve()

    print("task taken:")
    for w in list(true_workers.values()):
        print(w)
    
    print("task not taken:")
    for w in rest:
        print(w)

