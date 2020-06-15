from flask import Flask, render_template,request,redirect,url_for,jsonify,abort
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:admin@localhost:5432/project'
app.debug = True
# creating the app

db = SQLAlchemy(app)
# defining the db object

# creating model for our APP
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean,nullable=False,default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#using migration
migrate = Migrate(app,db)
#Creates all tables.
# db.create_all()

@app.route('/todos/create',methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        #get the data 
        todo = Todo(description=description)
        #create the object
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())


if __name__ == "__main__":
    app.run()
