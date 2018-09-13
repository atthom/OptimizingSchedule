from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import *
from .launcher import launch 

def frontpage2(request):
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

        launch(session_range, worker_names, all_tasks)
    else:
        print(sessionform.errors)
        print(taskFormSet.errors)
        print(workerFormSet.errors)
    ctx = {"sessionform":sessionform, "taskFormSet":taskFormSet, "workerFormSet": workerFormSet}
    return render(request, 'frontpage2.html', context=ctx)