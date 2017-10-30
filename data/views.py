from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from data.models import Group01


class RecForm(forms.Form):
    records_name = forms.CharField()
    records_file = forms.FileField()


class ResForm(forms.Form):
    results_file = forms.FileField()


def index(request):
    context = {
        'rec_form': RecForm(),
        'res_form': ResForm(),
    }
    groups = Group01.objects.all()
    if groups.count() > 0:
        context['groups'] = groups

    print(context)
    return HttpResponse(render(request, 'data/index.html', context))


# todo: add group detail view (record list)

# todo: add upload-results-file-function in group detail view
