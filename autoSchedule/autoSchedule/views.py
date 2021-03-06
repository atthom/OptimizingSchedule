from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import *
from .launcher import launch 

def frontpage(request):
    sessionform = SessionForm(request.POST or None, prefix="session")
    taskFormSet = TaskFormSet(request.POST or None, prefix="task")
    workerFormSet = WorkerFormSet(request.POST or None, prefix="worker")

    if sessionform.is_valid() and taskFormSet.is_valid() and workerFormSet.is_valid():
        session_range = sessionform.cleaned_data["session_range"]
        worker_names = [w.cleaned_data["name"] for w in workerFormSet]

        all_tasks = []
        for task in taskFormSet:
            task_type = task.cleaned_data["task_type"]
            nb_workers = task.cleaned_data["nb_workers"]
            start = task.cleaned_data["start"]
            duration = task.cleaned_data["duration"]
            difficulty = task.cleaned_data["difficulty"]
            each_days = task.cleaned_data["each_days"]
            all_tasks.append((task_type, nb_workers, start, duration, difficulty, each_days))

        true_workers, rest = launch(session_range, worker_names, all_tasks)
        print("task taken:")
        for w in true_workers.values():
            print(w)
        
        print("task not taken:")
        for w in rest:
            print(w)
        
        print("all task:")
        for t in all_tasks:
            pass
            print(t)
        true_workers = list(true_workers.values())
        all_tasks = []
        [all_tasks.extend(worker.task_list) for worker in true_workers]
        ctx = {"true_workers": true_workers, "rest":rest, "all_tasks":all_tasks}
        return render(request, 'resultpage.html', context=ctx)
    else:
        print(sessionform.errors)
        print(taskFormSet.errors)
        print(workerFormSet.errors)
    ctx = {"sessionform":sessionform, "taskFormSet":taskFormSet, "workerFormSet": workerFormSet}
    return render(request, 'frontpage.html', context=ctx)