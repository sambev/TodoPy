from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from models import Todos
import json

def pretty_todo(todo):
    """
    Make the todo completed value a bool since that is what backbone is expecting
    """
    if todo.completed:
        todo.completed = True
    else:
        todo.completed = False


def ugly_completed(arg):
    """
    Turn true and false back to 1 or 0
    """
    if arg:
        return 1
    return 0


def main(request):
    """
    Return the main page
    """
    return render_to_response('index.html')

@csrf_exempt
def todos(request):
    """
    GET: return all the Todos
    POST: create a new todo
    """
    if request.method == 'GET':
        todos = Todos.objects.all()
        ret_data = []
        for todo in todos:
            pretty_todo(todo)
            ret_data.append({
                'id': todo.id,
                'title': todo.title,
                'completed': todo.completed
            })

        return HttpResponse(json.dumps(ret_data), mimetype='application/json')
    
    elif request.method == 'POST':
        # create a new todo
        data = json.loads(request.body)
        new_todo = Todos()
        new_todo.title = data['title']
        new_todo.completed = ugly_completed(data['completed'])
        print new_todo
        new_todo.save()

        return HttpResponse('Hi')
