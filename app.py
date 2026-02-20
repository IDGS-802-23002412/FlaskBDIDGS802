from flask import Flask, render_template, request, redirect, url_for 
from flask import flash 
from flask_wtf.csrf import CSRFProtect 
from config import DevelopmentConfig 
from flask import g 

import forms 
from models import db, Alumnos

app = Flask(__name__) 
app.config.from_object(DevelopmentConfig) 
db.init_app(app) 
csrf = CSRFProtect() 

@app.errorhandler(404) 
def page_not_found(e): 
    return render_template("404.html"), 404 
    
@app.route("/", methods=['GET','POST']) 
@app.route("/index") 
def index(): 
    create_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumno=alumno) 

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm2(request.form)
    if request.method == 'POST':
        alumn = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            email=create_form.email.data
        )
        db.session.add(alumn)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("alumnos.html", form=create_form)

@app.route("/detalles", methods=['GET','POST'])
def detalles():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        nombre = alum1.nombre
        apaterno = alum1.apaterno
        email = alum1.email
    
    return render_template("detalles.html", nombre=nombre, apaterno=apaterno, email=email)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm2(request.form)
    id = request.args.get('id') or request.form.get('id')
    alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

    if request.method == 'GET':
        create_form.nombre.data = alum1.nombre
        create_form.apaterno.data = alum1.apaterno
        create_form.email.data = alum1.email

    if request.method == 'POST':
        alum1.nombre = create_form.nombre.data.strip()
        alum1.apaterno = create_form.apaterno.data
        alum1.email = create_form.email.data
        
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("modificar.html", form=create_form, id=id)

if __name__ == '__main__': 
    csrf.init_app(app) 
    with app.app_context(): 
        db.create_all() 
    app.run(debug=True)
