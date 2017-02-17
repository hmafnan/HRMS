import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from .forms import CandidateForm
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from .models import Candidate


def index(request):
    if request.user.is_authenticated():
        return render(request, 'interview/index.html')
    else:
        return HttpResponseRedirect('/login/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/index/")
    else:
        form = UserCreationForm()
    return render(request, "interview/register.html", {
        'form': form,
    })


@csrf_exempt
def build_profile(request):
    response = {'success': False, 'form': ''}
    template = loader.get_template('interview/candidate.html')
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            response['success'] = True
    else:
        form = CandidateForm()
    response['form'] = template.render({'form': form}, request)
    return HttpResponse(json.dumps(response))

@csrf_exempt
def candidates_list(request):
    response = {}
    candidates = Candidate.objects.all()

    response['data'] = serializers.serialize('json', candidates)
    return HttpResponse(json.dumps(response))


def schedule_interview(request):
    response = {}
    return HttpResponse(json.dumps(response))