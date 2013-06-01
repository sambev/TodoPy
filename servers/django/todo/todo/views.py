from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.core import serializers
from models import Todos

def main(request):
    return render_to_response('index.html')

def todo(request):
    todos = Todos.objects.all()
    data = serializers.serialize('json', todos, fields=('completed', 'id', 'title'))
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
