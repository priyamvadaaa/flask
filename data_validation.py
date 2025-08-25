from flask import Flask , request, jsonify
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError

app=Flask(__name__)
api=Api(app)


app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///todo.db'
db= SQLAlchemy(app)


#DataBase model

class Task(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.name


#Marshmallow Schema

class TaskSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)


task_schema=TaskSchema()
tasks_schema=TaskSchema(many=True)



#Resources

class Items(Resource):
    def get(self):
        '''Getting all tasks'''
        tasks=Task.query_all()
        return tasks_schema.dump(tasks),200

    def post(self):
        '''creating new task with validation'''

        try:
            data=task_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 404

        task=Task(name=data['name'])
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task),201

class Item (Resource):
    def get(self):
        '''get a single task'''
        task=Task.query.filter_by(id=pk).first()
        if not task:
            abort()
