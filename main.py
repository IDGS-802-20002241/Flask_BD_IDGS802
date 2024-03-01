from flask import Flask, request, render_template,Response,redirect,url_for
from flask_wtf.csrf import CSRFProtect
import forms 
from flask import flash
from flask import g
from config import DevelopmentConfig 
from models import db
from models import Alumnos
app=Flask(__name__)


app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()


'''     
Decoradores o rutas
'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404



@app.route("/index",methods=["GET","POST"])
def index():
    
    alumn_form=forms.UserForm2(request.form)
    if request.method == 'POST' and alumn_form.validate():
        alumn=Alumnos(nombre=alumn_form.nombre.data,
                      email=alumn_form.email.data,
                      apaterno=alumn_form.apaterno.data
                      )
        
        #insert into values()
        db.session.add(alumn)
        db.session.commit()
      
        
        return redirect("ABC_Completo")

    return render_template("index.html",form=alumn_form)

@app.route("/alumnos",methods=["GET","POST"])
def alumnos():
    
    alumn_form=forms.UserForm(request.form)
    if request.method == 'POST' and alumn_form.validate():
        nom=alumn_form.nombre.data    
        email=alumn_form.email.data    
        apaterno=alumn_form.apaterno.data   
        mensaje='Bienvenido: {}'.format(nom)
        flash(mensaje)
        print("nombre: {}".format(nom)) 
        print("email: {}".format(email)) 
        print("Apellido paterno: {}".format(apaterno)) 
    return render_template("alumnos.html", form =alumn_form )
 
@app.route("/ABC_Completo",methods=["GET","POST"])
def ABC_Completo():   
    alumn_form=forms.UserForm2(request.form)
    alumnos=Alumnos.query.all()
    
    return render_template("ABC_Completo.html",alumno=alumnos)

@app.route("/eliminar",methods=["GET","POST"])
def eliminar():   
    alumn_form=forms.UserForm2(request.form)
    if request.method =='GET':
        id=request.args.get('id')
        alumn1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alumn_form.id.data=id
        alumn_form.nombre.data=alumn1.nombre 
        alumn_form.apaterno.data=alumn1.apaterno 
        alumn_form.email.data=alumn1.email
    if request.method == 'POST':
        id= alumn_form.id.data
        alumn=Alumnos.query.get(id)
        db.session.delete(alumn) 
        db.session.commit() 
    
        return redirect(url_for("ABC_Completo"))
    return render_template('eliminar.html',form=alumn_form)


@app.route("/modificar",methods=["GET","POST"])
def modificar():   
    alumn_form=forms.UserForm2(request.form)
    if request.method =='GET':
        id=request.args.get('id')
        alumn1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alumn_form.id.data=id
        alumn_form.nombre.data=alumn1.nombre 
        alumn_form.apaterno.data=alumn1.apaterno 
        alumn_form.email.data=alumn1.email
    if request.method == 'POST':
        id= alumn_form.id.data
        alumn=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alumn.nombre=alumn_form.nombre.data
        alumn.apaterno=alumn_form.apaterno.data
        alumn.email=alumn_form.email.data

        
        db.session.add(alumn) 
        db.session.commit() 
    
        return redirect(url_for("ABC_Completo"))
    return render_template('modificar.html',form=alumn_form)

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()

