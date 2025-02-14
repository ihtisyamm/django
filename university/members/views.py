from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from members.models import Member

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def members(request):
    members = Member.objects.all().values()
    template = loader.get_template('members.html')
    context = {
        'members': members
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    member = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'member': member
    }
    return HttpResponse(template.render(context, request))
