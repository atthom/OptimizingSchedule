import datetime
from django import forms
from easy_select2 import Select2Multiple, Select2Mixin, select2_modelform
from django.forms import formset_factory

class SessionForm(forms.Form):
    session_range = forms.CharField(widget=forms.TextInput(
        attrs={ 'class':'form-control datepicker', 'placeholder':'Range'}))

class WorkerForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput({"class": "form-control", 'placeholder': 'Worker\'s name'}))
    # self.unavailable_periodes = unavailable_periodes
    # preferences

class TaskForm(forms.Form):
    task_type = forms.CharField(widget=
        forms.TextInput({"class": "form-control", 'placeholder': 'Task\'s name'}))
    nb_workers = forms.IntegerField(widget=
        forms.NumberInput({"class": "form-control input-sm", 'placeholder': 'Nb of ppl needed'}))
    start = forms.CharField(widget=
        forms.TextInput({"class": "form-control input-sm date_time", 'placeholder': 'Start'}))
    duration = forms.DurationField(widget=
    forms.TextInput({"class": "form-control input-sm time", 'placeholder': 'Duration'}))
    #difficulty = forms.IntegerField(widget=forms.TextInput({"class": "form-control input-md"}))
    each_days = forms.BooleanField(required=False,initial=False)

TaskFormSet = formset_factory(TaskForm)
WorkerFormSet = formset_factory(WorkerForm)
