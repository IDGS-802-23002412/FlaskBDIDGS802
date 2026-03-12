from flask import Flask, render_template, request, redirect, url_for 
from flask import flash 
from flask_wtf.csrf import CSRFProtect 
from config import DevelopmentConfig 
from flask import g 
from flask_migrate import Migrate

from . import cursos
import forms 
from models import db, Cursos, Maestros, Alumnos

from flask import Blueprint
cursos_bp = Blueprint('cursos', __name__)

@cursos_bp.route('/cursos', methods=['GET','POST'])
def cursos():
    create_form = forms.CursosForm(request.form)
    curso = Cursos.query.all()
    maestro = Maestros.query.all()
    
    return render_template("/curso/cursos.html", form=create_form, curso=curso) 

@cursos_bp.route("/cursos/nuevo", methods=['GET', 'POST'])
def nuevo():
    create_form = forms.CursosForm(request.form)

    maestro = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestro]

    if request.method == 'POST':
        curso_existente = db.session.query(Cursos).filter(
            Cursos.nombre == create_form.nombre.data
        ).first()

        if curso_existente:
            flash("El alumno ya está inscrito a este curso")
        else:
            curs = Cursos(
                nombre=create_form.nombre.data,
                descripcion=create_form.descripcion.data,
                maestro_id=create_form.maestro_id.data
            )

            db.session.add(curs)
            db.session.commit()
            return redirect(url_for('cursos.cursos'))

    return render_template("/curso/registrar.html", form=create_form)
@cursos_bp.route("/cursos/detalles", methods=['GET','POST'])
def detalles():
    create_form = forms.CursosForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        curs = db.session.query(Cursos).filter(Cursos.id == id).first()
        nombre = curs.nombre
        descripcion = curs.descripcion
        maestro = f"{curs.maestro.nombre} {curs.maestro.apellidos}"
    
    return render_template("/curso/detalles.html", id= id, nombre=nombre, descripcion=descripcion, maestro=maestro)

@cursos_bp.route("/cursos/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.CursosForm(request.form)
    
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros]

    if request.method == 'GET':
        id = request.args.get('id')
        curs = db.session.query(Cursos).filter(Cursos.id == id).first()

        create_form.id.data = id
        create_form.nombre.data = curs.nombre
        create_form.descripcion.data = curs.descripcion
        create_form.maestro_id.data = curs.maestro_id  

    if request.method == 'POST':
        id = create_form.id.data
        curs = db.session.query(Cursos).filter(Cursos.id == id).first()

        curs.nombre = create_form.nombre.data.strip()
        curs.descripcion = create_form.descripcion.data
        curs.maestro_id = create_form.maestro_id.data
        
        db.session.commit()
        return redirect(url_for('cursos.cursos'))

    return render_template("/curso/modificar.html", form=create_form)

@cursos_bp.route("/cursos/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.CursosForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        curs = db.session.query(Cursos).filter(Cursos.id == id).first()

        create_form.id.data = id
        create_form.nombre.data = curs.nombre
        create_form.descripcion.data = curs.descripcion
        maestro = f"{curs.maestro.nombre} {curs.maestro.apellidos}"

    if request.method == 'POST':
        id = create_form.id.data
        curs = Cursos.query.get(id)

        if curs:
            db.session.delete(curs)
            db.session.commit()

        return redirect(url_for('cursos.cursos'))

    return render_template("/curso/eliminar.html", form=create_form, maestro=maestro)