from flask import Flask, render_template,redirect
from flask_sqlalchemy import SQLAlchemy    #database 
from datetime import datetime               #for date_created
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =  SQLAlchemy(app)
app.app_context().push()

class ToDo(db.Model):
    sno =db.Column(db.Integer,primary_key = True)
    title=db.Column(db.String(200),nullable = False)
    content=db.Column(db.String(500),nullable = False)
    date_created= db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:     #whenever i print the obj(of class ToDo),what should i see?
        return f"{self.sno} - {self.title}"

@app.route('/',methods =['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        content =request.form['content']
        todo = ToDo(title=title , content=content)
        db.session.add(todo)
        db.session.commit()
    allTodo = ToDo.query.all()
    return render_template('index.html',allTodo = allTodo)   
   #allTodo (we're using jinja2 here)
   # return 'Hello, World!'

@app.route('/show')
def productions():
    allTodo = ToDo.query.all()
    #print(allTodo)
    return 'This is production page'

@app.route('/update/<int:sno>',methods =['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        content =request.form['content']
        todo = ToDo.query.filter_by(sno=sno).first() 
        ToDo.query.filter_by(sno=sno).first() 
        todo.title= title
        todo.content = content
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = ToDo.query.filter_by(sno=sno).first() 
    return render_template('update.html',todo = todo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()   #.first() bcoz i wanna dlt the 1st record i choose
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

#@app.route('/productions')
#def productions():
#    return 'This is production page'

if __name__ =="__main__":
    app.run(debug=True,port=8000)