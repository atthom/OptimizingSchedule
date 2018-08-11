from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import *

def frontpage(request):
    sessionform = SessionForm(request.POST or None, prefix="session")
    taskFormSet = TaskFormSet(request.POST or None, prefix="task")
    workerFormSet = WorkerFormSet(request.POST or None, prefix="worker")
    
    ctx = {"sessionform":sessionform, "taskFormSet":taskFormSet, "workerFormSet": workerFormSet}
    return render(request, 'frontpage.html', context=ctx)