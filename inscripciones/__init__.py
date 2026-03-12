from flask import Blueprint 

inscripciones = Blueprint(
    'inscripciones',
    __name__,
    template_folder = 'templates'

)

from . import routes_inscripcion