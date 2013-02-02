import web
import json

#--------------------------------
# URLS
#--------------------------------
urls = (
    '/favicon.ico', 'catch',
    '/', 'root',
    '/todos/(.*)', 'todos'
)

#-------------------------------
# CONFIG
#-------------------------------
app = web.application(urls, globals())

render = web.template.render('../../html/')

db = web.database(dbn='sqlite', db='../../todos.db')
#-------------------------------
# HELPERS
#-------------------------------
def return_json(d, status='200 OK'):
    """
    prepare your data to return json
    """
    ret = json.dumps(d)
    web.ctx.status = status
    web.header('Content-Type', 'application/json')
    web.header('Content-Length', len(ret))
    return ret

def clean_todo(todo):
    """
    Update the todos completed field to a JSON compatible boolean

    returns the todo
    """
    if todo['completed']:
        todo['completed'] = True
    else:
        todo['completed'] = False
    return todo

#--------------------------------
# HANDLERS 
#--------------------------------
class root:
    
    def GET(self):
        """
        This returns our HTML page
        """
        return render.index()
        
class todos:

    def GET(self, tid=None):
        """
        GET --> Read
        """
        if tid:
            # If there was a todo ID passed in return just that todo
            res = db.select('todos', {'id':tid}, where='id = $id')
            try:
                #Check to make sure we got a response matching that ID
                todo = res[0]
                todo = clean_todo(todo)
                return return_json(todo)

            except IndexError:
                return return_json({})
        else:
            # Return a list of all of the available todos
            res = db.select('todos')
            todos = [t for t in res]

            for todo in todos:
                todo = clean_todo(todo)
            return return_json(todos)


    def POST(self, tid=None):
        """
        POST --> Create
        """
        data = json.loads(web.data())
        # Inserting with web.py returns the id of the row inserted
        tid = db.insert('todos', title=data.get('title'), completed=0)
        
        # Return the current representation of the object so the server is the authority
        res = db.select('todos', {'id':tid}, where='id = $id')
        todo = clean_todo(res[0])
        return return_json(todo, status='201 Created')


    def PUT(self, tid):
        """
        PUT --> Update
        """
        data = json.loads(web.data())
        # Change completed for sqlite
        completed = 0
        if data['completed']:
            completed = 1

        db.update('todos', where='id = $id', vars={'id':data.get('id')}, completed=completed, title=data.get('title'))

        # Return the current representation of the object so the server is the authority
        res = db.select('todos', {'id':data.get('id')}, where='id = $id')
        todo = clean_todo(res[0])

        return return_json(todo)


    def DELETE(self, tid):
        """
        DELETE --> Delete
        """
        db.delete('todos', where='id = $id', vars={'id':tid})
        web.ctx.status = '204 No Content'
        return None
        

class catch:

    def GET(self):
        return None


if __name__ == '__main__':
    app.run()
