import datetime
from django import forms
from easy_select2 import Select2Multiple, Select2Mixin, select2_modelform
from django.forms import formset_factory


class WorkerForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput({"class": "form-control"}))
    # self.unavailable_periodes = unavailable_periodes
    # preferences

class TaskForm(forms.Form):
    task_type = forms.CharField(widget=forms.TextInput({"class": "form-control"}))
    nb_workers = forms.IntegerField(widget=forms.TextInput({"class": "form-control input-sm"}))
    start = forms.DateField(widget=forms.TextInput({"class": "form-control input-sm"}))
    duration = forms.IntegerField(widget=forms.TextInput({"class": "form-control input-sm"}))
    #difficulty = forms.IntegerField(widget=forms.TextInput({"class": "form-control input-md"}))
    each_days = forms.BooleanField(widget=forms.TextInput({"class": "form-control input-sm"}))

class SessionForm(forms.Form):
    start = forms.DateField(widget=forms.TextInput({"class": "form-control input-sm"}))
    end = forms.DateField(widget=forms.TextInput({"class": "form-control input-sm"}))


TaskFormSet = formset_factory(TaskForm)
WorkerFormSet = formset_factory(WorkerForm)
