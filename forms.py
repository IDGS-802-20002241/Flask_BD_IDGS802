from wtforms import Form,validators
from wtforms import StringField, TextAreaField,SelectField,RadioField,IntegerField, BooleanField,FieldList
from wtforms import EmailField, DateField


""" class UserForm(Form):
    nombre=StringField("nombre")
    email=EmailField("correo")
    apaterno=StringField("apaterno")
    materias=SelectField(choices=[('Español','esp'),('Matematicas','mat'), ('Ingles','ING') ])
    radios=RadioField('Curso',choices=[('1','1'),('2','2'),('3','3')]) """
    
class UserForm(Form):
    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=10, message='Ingrese un nombre válido')
    ])
    email = EmailField("correo", [
        validators.Email(message='Ingrese un correo válido')
    ])
    apaterno = StringField("apaterno")
    edad = IntegerField("edad", [
        validators.NumberRange(min=1, max=20, message='Ingrese un valor válido, debe estar entre 1 y 20')
    ]) 
    
    
    """ materias=SelectField(choices=[('Español','esp'),('Matematicas','mat'), ('Ingles','ING') ])
    radios=RadioField('Curso',choices=[('1','1'),('2','2'),('3','3')]) """
    
class UserForm2(Form):
    id=IntegerField('id')
    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=10, message='Ingrese un nombre válido')
    ])
    email = EmailField("correo", [
        validators.Email(message='Ingrese un correo válido')
    ])
    apaterno = StringField("apaterno")
    amaterno = StringField("amaterno")
    edad = StringField("edad",[
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=1, max=30, message='Ingrese un nombre válido')
        ])
    
class UserForm3(Form):
    id=IntegerField('Id')
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=10, message='Ingrese un nombre válido')
    ])
    direccion = StringField("Direccion", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=10, message='Ingrese una dirección válida')
    ])
    tamano = RadioField('Tamaño Pizza ',choices=[('40','Chica'),('80','Mediana'),('120','Grande')])
    ing1 = BooleanField('Jamon', default=False)
    ing2 = BooleanField('Piña', default=False)
    ing3 = BooleanField('Champiñones', default=False)

    """  
    ingredientes = FieldList(BooleanField("Ingredientes"), min_entries=3, max_entries=3, default=[False, False, False]) """
    telefono = StringField("Telefono",[
        validators.DataRequired(message="El telefono es requerido"),
        validators.Length(min=1, max=30, message='Ingrese un telefono válido')
        ])
    num_pizzas = IntegerField("Número de Pizzas", [
        validators.NumberRange(min=1, max=20, message='Ingrese un valor válido, debe estar entre 1 y 20')
    ]) 
    fecha = DateField("Fecha",format='%Y-%m-%d',validators=[validators.DataRequired(message="El campo es requerido")])