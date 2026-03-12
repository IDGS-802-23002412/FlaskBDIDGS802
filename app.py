from flask import Flask, render_template, request, redirect, url_for 
from flask import flash 
from flask_wtf.csrf import CSRFProtect 
from config import DevelopmentConfig 
from flask import g 
from flask_migrate import Migrate
from maestros.routes import maestros_bp
from alumnos.routes_alumno import alumnos_bp
from cursos.routes_curso import cursos_bp
from inscripciones.routes_inscripcion import inscripciones_bp

import forms 
from models import db, Alumnos

app = Flask(__name__) 
app.config.from_object(DevelopmentConfig) 
app.register_blueprint(maestros_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(inscripciones_bp)
db.init_app(app) 
csrf = CSRFProtect()
migrate = Migrate(app,db)


@app.errorhandler(404) 
def page_not_found(e): 
    return render_template("404.html"), 404 

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__': 
    csrf.init_app(app) 
    with app.app_context(): 
        db.create_all() 
    app.run(debug=True)
