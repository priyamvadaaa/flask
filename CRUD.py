from pyexpat.errors import messages

from flask import Flask , request
from flask_restful import Resource, Api , marshal_with , fields , abort
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db=SQLAlchemy(app)

class Task(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.name

fakeDb = {
    1:{'name':'Doggo'},
    2:{'name':'Cleanest Bug'},
    3:{'name':'Cat'},
}

taskFields = {
    'id': fields.Integer,
    'name': fields.String
}


class Items(Resource):
    @marshal_with(taskFields)
    def get(self):
        tasks =Task.query.all()
        return tasks

    @marshal_with(taskFields)
    def post(self):
       data=request.json
       task = Task(name=data['name'])
       db.session.add(task)
       db.session.commit()

       tasks= Task.query.all()
       # itemID = len(fakeDb.keys()) + 1
       # fakeDb[itemID] = {'name': data['name']}
       return tasks


class Item(Resource):
    @marshal_with(taskFields)
    def get(self,pk):
        task = Task.query.filter_by(id=pk).first()
        if not task:
            abort(404,message=f'Task with id {pk} does not exist')
        return task

    @marshal_with(taskFields)
    def put(self,pk):
       task = Task.query.filter_by(id=pk).first()
       if not task:
           abort(404,message=f'item with id {pk} does not exist')
       data = request.json
       if not data or 'name' not in data:
           abort(404,message='name field missing')
       task.name=data['name']
       db.session.commit()
       return task

    @marshal_with(taskFields)
    def delete(self, pk):
        task = Task.query.filter_by(id=pk).first()
        if not task :
            abort(404,message=f'item with id {pk} does not exist')
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks


api.add_resource(Items,'/')
api.add_resource(Item,'/<int:pk>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


