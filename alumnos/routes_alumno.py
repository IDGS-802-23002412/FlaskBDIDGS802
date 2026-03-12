from flask import Flask, render_template, request, redirect, url_for 
from flask import flash 
from flask_wtf.csrf import CSRFProtect 
from config import DevelopmentConfig 
from flask import g 
from flask_migrate import Migrate

from . import alumnos
import forms 
from models import db, Alumnos

from flask import Blueprint
alumnos_bp = Blueprint('alumnos', __name__)

@alumnos_bp.route('/alumnos', methods=['GET','POST'])
def alumnos(): 
    create_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    return render_template("/alumno/alumnos.html", form=create_form, alumno=alumno) 

@alumnos_bp.route("/alumnos/nuevo", methods=['GET', 'POST'])
def registrar():
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
        return redirect(url_for('alumnos.alumnos'))
    return render_template("/alumno/registrar.html", form=create_form)

@alumnos_bp.route("/alumnos/detalles", methods=['GET','POST'])
def detalles():
    create_form = forms.UserForm2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        nombre = alum1.nombre
        apellidos = alum1.apellidos
        email = alum1.email
        telefono = alum1.telefono
    
    return render_template("/alumno/detalles.html", nombre=nombre, apellidos=apellidos, email=email, telefono=telefono)

@alumnos_bp.route("/alumnos/modificar", methods=['GET', 'POST'])
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
        return redirect(url_for('alumnos.alumnos'))

    return render_template("/alumno/modificar.html", form=create_form)

@alumnos_bp.route("/alumnos/eliminar", methods=['GET', 'POST'])
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

        return redirect(url_for('alumnos.alumnos'))

    return render_template("/alumno/eliminar.html", form=create_form)