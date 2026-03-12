from wtforms import Form
from wtforms import StringField, IntegerField, PasswordField, RadioField
from wtforms import EmailField, SelectField, SelectMultipleField
from wtforms import validators

class UserForm(Form):
    matricula = IntegerField('Matricula',[
            validators.DataRequired(message='El campo es requerido'),
            validators.NumberRange(min=100, max=1000, message='Ingrese un valor válido')
    ])
    nombre = StringField('Nombre',[
            validators.DataRequired(message='El campo es requerido'),
            validators.Length(min=3, max=10, message='Ingrese nombre válido')
    ])

    apaterno = StringField('Apellido Paterno',[
            validators.DataRequired(message='El campo es requerido')
    ])

    amaterno = StringField('Apellido Materno',[
            validators.DataRequired(message='El campo es requerido')
    ])

    correo = EmailField('Correo',[
            validators.Email(message='Ingrese un correo válido')
    ])

class CinepolisForm(Form): 
        nombre = StringField('nombre', [
                validators.DataRequired(message='El campo es requerido'),
                validators.Length(min=3, max=10, message='Ingrese nombre válido')
        ])
        cantidadCompradores = IntegerField('cantidadCompradores',[
                validators.DataRequired(message='El campo es requerido'),
                validators.NumberRange(min=1, max=1000, message='Ingrese un valor válido')
        ])
        opcion = RadioField('Tarjeta Cineco',
                choices=[('Si', 'Si'), ('No', 'No')],
                validators=[validators.DataRequired(message='Seleccione una opción')
        ])
        cantidadBoletas = IntegerField('cantidadBoletas',[
                validators.DataRequired(message='El campo es requerido'),
                validators.NumberRange(min=1, max=1000, message='Ingrese un valor válido')
        ])

class UserForm2(Form):
        id = IntegerField('id')
        nombre = StringField('Nombre',[
                validators.DataRequired(message='El campo es requerido'),
                validators.Length(min=3, max=10, message='Ingrese nombre válido')
        ])
        
        apellidos = StringField('Apellidos',[
                validators.DataRequired(message='El campo es requerido')
        ])
        
        email = EmailField('correo',[
                validators.Email(message='Ingrese un correo válido')
        ])
                
        telefono = IntegerField('telefono', [
                validators.NumberRange(min=1, max=10, message='Ingrese un telefono valido')
        ])

class MaestrosForm(Form):
        matricula = IntegerField('matricula')
        nombre = StringField('Nombre',[
                validators.DataRequired(message='El campo es requerido'),
                validators.Length(min=3, max=10, message='Ingrese nombre válido')
        ])
        
        apellidos = StringField('Apellidos',[
                validators.DataRequired(message='El campo es requerido')
        ])
        
        especialidad = StringField('Especialidad', [
                validators.DataRequired(message='El campo es requerido')
        ])
        
        email = EmailField('Email',[
                validators.Email(message='Ingrese un correo válido')
        ])

class CursosForm(Form):

    id = IntegerField('id')

    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido')
    ])

    descripcion = StringField('Descripción',[
        validators.Length(min=3, max=500)
    ])

    maestro_id = SelectField('Maestro', coerce=int, 
        validators = [validators.DataRequired(message='El campo es requerido')]
    )

    alumnos = SelectMultipleField('Alumnos',[
        validators.DataRequired(message='El campo es requerido')
    ])

class InscripcionesForm(Form):

    id = IntegerField('id')

    alumno_id = SelectField('Alumno', coerce=int, 
        validators = [validators.DataRequired(message='El campo es requerido')]
    )

    curso_id = SelectField('Curso', coerce=int, 
        validators = [validators.DataRequired(message='El campo es requerido')]
    )




