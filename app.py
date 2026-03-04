from flask import Flask, render_template, request, redirect, url_for 
from flask import flash 
from flask_wtf.csrf import CSRFProtect 
from config import DevelopmentConfig 
from flask import g 
from flask_migrate import Migrate
from maestros.routes import maestros_bp

import forms 
from models import db, Alumnos

app = Flask(__name__) 
app.config.from_object(DevelopmentConfig) 
app.register_blueprint(maestros_bp)
db.init_app(app) 
csrf = CSRFProtect()
migrate = Migrate(app,db)


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
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            telefono = create_form.telefono.data
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
        apellidos = alum1.apellidos
        email = alum1.email
        telefono = alum1.telefono
    
    return render_template("detalles.html", nombre=nombre, apellidos=apellidos, email=email, telefono=telefono)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm2(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        create_form.id.data = id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

    if request.method == 'POST':
        id = create_form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()  

        alum1.nombre = create_form.nombre.data.strip()
        alum1.apellidos = create_form.apellidos.data
        alum1.email = create_form.email.data
        alum1.telefono = create_form.telefono.data
        
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm2(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        create_form.id.data = id
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

    if request.method == 'POST':
        id = create_form.id.data
        alum1 = Alumnos.query.get(id)

        if alum1:
            db.session.delete(alum1)
            db.session.commit()

        return redirect(url_for('index'))

    return render_template("eliminar.html", form=create_form)

if __name__ == '__main__': 
    csrf.init_app(app) 
    with app.app_context(): 
        db.create_all() 
    app.run(debug=True)
