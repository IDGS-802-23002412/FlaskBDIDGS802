from flask import Flask, render_template, request, redirect, url_for 
from flask import flash 
from flask_wtf.csrf import CSRFProtect 
from config import DevelopmentConfig 
from flask import g 
from flask_migrate import Migrate

import forms 
from models import db, Cursos, Maestros, Alumnos, Inscripciones

from flask import Blueprint
inscripciones_bp = Blueprint('inscripciones', __name__)

@inscripciones_bp.route('/inscripciones', methods=['GET','POST'])
def inscripciones():
    create_form = forms.InscripcionesForm(request.form)
    inscripcion = Inscripciones.query.all()
    alumno = Alumnos.query.all()
    curso = Cursos.query.all()
    
    return render_template("/inscripcion/inscripciones.html", form=create_form, inscripcion=inscripcion) 

@inscripciones_bp.route("/inscripciones/nuevo", methods=['GET', 'POST'])
def nuevo():
    create_form = forms.InscripcionesForm(request.form)

    alumno = Alumnos.query.all()
    curso = Cursos.query.all()

    create_form.alumno_id.choices = [(a.id, a.nombre) for a in alumno]
    create_form.curso_id.choices = [(c.id, c.nombre) for c in curso]

    if request.method == 'POST':
        insc = Inscripciones(
            alumno_id=create_form.alumno_id.data,
            curso_id=create_form.curso_id.data
        )

        curso = Cursos.query.get(create_form.curso_id.data)
        alumno = Alumnos.query.get(create_form.alumno_id.data)
        curso.alumnos.append(alumno)
        db.session.commit()
        return redirect(url_for('inscripciones.inscripciones'))
    return render_template("/inscripcion/registrar.html", form=create_form)

@inscripciones_bp.route("/inscripciones/detalles", methods=['GET', 'POST'])
def detalles():

    if request.method == 'GET':
        id = request.args.get('id')
        insc = Inscripciones.query.get(id)
        alumno = f"{insc.alumno.nombre} {insc.alumno.apellidos}"
        curso = f"{insc.curso.nombre}"
        maestro = f"{insc.curso.maestro.nombre} {insc.curso.maestro.apellidos}"
        fecha = insc.fecha_inscripcion

    return render_template("/inscripcion/detalles.html", alumno=alumno, curso=curso, maestro=maestro, fecha=fecha)

@inscripciones_bp.route("/inscripciones/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.InscripcionesForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        insc = db.session.query(Inscripciones).filter(Inscripciones.id == id).first()

        create_form.id.data = id
        curso = f"{insc.curso.nombre}"
        alumno = f"{insc.alumno.nombre} {insc.alumno.apellidos}"

    if request.method == 'POST':
        id = create_form.id.data
        insc = Inscripciones.query.get(id)

        if insc:
            db.session.delete(insc)
            db.session.commit()

        return redirect(url_for('inscripciones.inscripciones'))

    return render_template("/inscripcion/eliminar.html", form=create_form, curso=curso, alumno=alumno)