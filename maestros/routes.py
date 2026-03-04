from flask import Flask, render_template, request, redirect, url_for 
from flask import flash 
from flask_wtf.csrf import CSRFProtect 
from config import DevelopmentConfig 
from flask import g 
from flask_migrate import Migrate

from . import maestros
import forms 
from models import db, Maestros

from flask import Blueprint
maestros_bp = Blueprint('maestros', __name__)

@maestros_bp.route('/maestros', methods=['GET','POST'])
def maestros():
    create_form = forms.MaestrosForm(request.form)
    maestro = Maestros.query.all()
    return render_template("/maestro/maestros.html", form=create_form, maestro=maestro) 

@maestros_bp.route("/maestros/nuevo", methods=['GET', 'POST'])
def nuevo():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'POST':
        maes = Maestros(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email = create_form.email.data
        )
        db.session.add(maes)
        db.session.commit()
        return redirect(url_for('maestros.maestros'))
    return render_template("/maestro/registrar.html", form=create_form)

@maestros_bp.route("/maestros/detalles", methods=['GET','POST'])
def detalles():
    create_form = forms.MaestrosForm(request.form)
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        nombre = maes.nombre
        apellidos = maes.apellidos
        especialidad = maes.especialidad
        email = maes.email
    
    return render_template("/maestro/detalles.html", matricula= matricula, nombre=nombre, apellidos=apellidos, especialidad=especialidad, email=email)

@maestros_bp.route("/maestros/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.MaestrosForm(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

        create_form.matricula.data = matricula
        create_form.nombre.data = maes.nombre
        create_form.apellidos.data = maes.apellidos
        create_form.especialidad.data = maes.especialidad
        create_form.email.data = maes.email

    if request.method == 'POST':
        matricula = create_form.matricula.data
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

        maes.nombre = create_form.nombre.data.strip()
        maes.apellidos = create_form.apellidos.data
        maes.especialidad = create_form.especialidad.data
        maes.email = create_form.email.data
        
        db.session.commit()
        return redirect(url_for('maestros.maestros'))

    return render_template("/maestro/modificar.html", form=create_form)

@maestros_bp.route("/maestros/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.MaestrosForm(request.form)

    if request.method == 'GET':
        matricula = request.args.get('matricula')
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

        create_form.matricula.data = matricula
        create_form.nombre.data = maes.nombre
        create_form.apellidos.data = maes.apellidos
        create_form.especialidad.data = maes.especialidad
        create_form.email.data = maes.email

    if request.method == 'POST':
        matricula = create_form.matricula.data
        maes = Maestros.query.get(matricula)

        if maes:
            db.session.delete(maes)
            db.session.commit()

        return redirect(url_for('maestros.maestros'))

    return render_template("/maestro/eliminar.html", form=create_form)