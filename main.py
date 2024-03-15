from flask import Flask, request, render_template,Response,redirect,url_for
from flask_wtf.csrf import CSRFProtect
import forms 
from flask import flash
from flask import g
from config import DevelopmentConfig 
from models import db
from models import Profesores
from models import Pizzeria2
import creacionArch
from sqlalchemy import create_engine, Column, String, Integer, text, and_, or_,func
from sqlalchemy.orm import declarative_base
from datetime import datetime
from datetime import datetime, timedelta   
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
    
    prof_form=forms.UserForm2(request.form)
    if request.method == 'POST' and prof_form.validate():
        profe=Profesores(nombre=prof_form.nombre.data,
                      email=prof_form.email.data,
                      apaterno=prof_form.apaterno.data,
                      amaterno=prof_form.apaterno.data,
                      edad=int(prof_form.edad.data)
                      )
        
        #insert into values()
        db.session.add(profe)
        db.session.commit()
      
        
         
    return render_template("index.html",form=prof_form)

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
    prof_form=forms.UserForm2(request.form)
    profesores=Profesores.query.all()
    
    return render_template("ABC_Completo.html",profesor=profesores)





data=forms.UserForm3()  
@app.route("/pizzeria", methods=[ "POST","GET"])
def pizzeria():   
    respuesta = []
    prof_form = forms.UserForm3(request.form)
    
    manejador = creacionArch.ManejadorArchivo('lista.txt')  
    manejador2 = creacionArch.ManejadorArchivo('lista2.txt')  
    ventasDia = Pizzeria2.query.filter(Pizzeria2.fecha_orden.like( f"%{str(datetime.now().date())}%")).all()
    total=0
    global data 
    respuesta = manejador.mostrar_contenido()  
    if request.method == 'POST' and prof_form.validate():
        costo = 10
        subtotal = 0
        
        
        data = prof_form
        
        if int(prof_form.tamano.data)== 40:
            subtotal+= int(prof_form.tamano.data)
            palabra1 = "Chica" + " : "
        elif int(prof_form.tamano.data)== 80:
            subtotal+= int(prof_form.tamano.data)
            palabra1 = "Mediana" + " : "
        else:
            subtotal+= int(prof_form.tamano.data)
            palabra1 = "Grande" + " : "
        # Verifica y agrega Jamon si está seleccionado
        if prof_form.ing1.data == 1:
            palabra1 += "Jamon - "
            subtotal += costo
        

        # Verifica y agrega Piña si está seleccionado
        if prof_form.ing2.data== 1:
            palabra1 += " Piña - "
            subtotal += costo
        

        # Verifica y agrega Champiñones si está seleccionado
        if prof_form.ing3.data== 1:
            palabra1 += "Champiñones - "
            subtotal += costo
      
      
        palabra1 += " : " +str(prof_form.num_pizzas.data) + " : " + str(subtotal*prof_form.num_pizzas.data)
        palabra2 =str(prof_form.nombre.data)+":"+ str(prof_form.direccion.data)+":"+str(prof_form.telefono.data)+":"+str(prof_form.fecha.data)
        try:
            manejador.insertar(palabra1)
            manejador2.insertar(palabra2)
            print(f'Palabras insertadas: {palabra1}')
        except Exception as e:
            print(f"Error durante la inserción: {e}")

        respuesta = manejador.mostrar_contenido()     
    if request.form.get("_method") == "PUT": 
       
        respuesta = manejador.mostrar_contenido()
        respuesta2=manejador2.mostrar_contenido()
        ingredientes =""
        nombre=""
        direccion=""
        telefono=""
        fecha=""
        for n in respuesta2:
            dato = n.split(":")
            nombre = dato[0]
            direccion = dato[1]
            telefono = dato[2]
            fecha = dato[3]
        
        for r in respuesta:
            # Procesar cada línea de la respuesta
            palabras = r.split(' : ')
            tamano = palabras[0]  # Tamaño de la pizza
                       
            ingredientes+= str(palabras[1].replace("-"," "))  if len(palabras) > 1 else "" # Lista de ingredientes
            num_pizzas = palabras[2] if len(palabras) > 2 else ""  # Número de pizzas
            subtotal = palabras[3] if len(palabras) > 3 else 0  # Subtotal

            # Crear una instancia del modelo Pizzeria2 y agregar a la base de datos
            orden = Pizzeria2(
                nombre=nombre,
                direccion=direccion,
                tamano=tamano,
                telefono=telefono,
                ingredietes=ingredientes,
                num_pizzas=num_pizzas,
                total=subtotal,
                fecha_orden=fecha
            )
            db.session.add(orden)
        db.session.commit() 
        manejador2.eliminar_todo()
        manejador.eliminar_todo()
        return redirect(url_for("pizzeria"))
    if request.form.get("_method") == "DELETE":
         indice =int(request.form.get("indice"))
         manejador = creacionArch.ManejadorArchivo('lista.txt')
         manejador.eliminar(indice)
         return render_template("pizzeria.html", form=data, request=respuesta if respuesta else [],ventas=ventasDia,total=total )


    if request.form.get("_method") == "Busqueda":
        print("IF "+str(request.form.get('fecha')))
        ventasDia = obtener_ventas(str(request.form.get('fecha')).lower())
        
        for pizza in ventasDia:
                total += float(pizza.total)
    for pizza in ventasDia:
                total += float(pizza.total)          
              
        
       
    return render_template("pizzeria.html", form=prof_form, request=respuesta if respuesta else [],ventas=ventasDia,total=total )



def obtener_ventas(fecha_busqueda):
    if fecha_busqueda:
        
        dias=['','domingo','lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado']
        dias2 = ['', 'domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado']
        meses=['','enero','febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio','agosto','septiembre', 'octubre','noviembre','diciembre']
        dia_semana=0
        dia_semana2=0
        mes=0
        año_actual = 2024
        años = list(range(año_actual - 1, año_actual + 1))

        if fecha_busqueda.lower() in dias:
            dia_semana = dias.index(fecha_busqueda.lower())
            print("Día de la semana: " + str(dia_semana))
            
        if fecha_busqueda.lower() in meses:
            mes = meses.index(fecha_busqueda.lower())
            print("Mes: " + str(mes))
        if fecha_busqueda.lower() in dias2:
            dia_semana2 = dias2.index(fecha_busqueda.lower())
            print("Mes: " + str(dia_semana2))
        
        # Consulta para días de la semana
        if dia_semana:
            ventasDia = Pizzeria2.query.filter((func.DAYOFWEEK(Pizzeria2.fecha_orden) == dia_semana)).all()
            print("Consulta por día de la semana: " + str(ventasDia))
            return ventasDia
        
        # Consulta para meses
        elif mes:
            ventasMes = Pizzeria2.query.filter((func.MONTH(Pizzeria2.fecha_orden) == mes)).all()
            print("Consulta por mes: " + str(ventasMes))
            return ventasMes
        elif dia_semana2:
            ventasDia = Pizzeria2.query.filter(func.DAYOFWEEK(Pizzeria2.fecha_orden) == dia_semana2,
                                                func.YEAR(Pizzeria2.fecha_orden).in_(años)).all()
            return ventasDia
        elif fecha_busqueda.lower() == "todo":
            todo = Pizzeria2.query.filter().all()
            return todo
        else:
            ventasMes = Pizzeria2.query.filter(
                
                (Pizzeria2.nombre.like(f"%{fecha_busqueda}%")) |
                (Pizzeria2.telefono.like(f"%{fecha_busqueda}%")) |
                (Pizzeria2.tamano.like(f"%{fecha_busqueda}%")) |
                (Pizzeria2.ingredietes.like(f"%{fecha_busqueda}%")) |
                (Pizzeria2.num_pizzas.like(f"%{fecha_busqueda}%")) |
                (Pizzeria2.total.like(f"%{fecha_busqueda}%")) |
                (Pizzeria2.fecha_orden.like(f"%{fecha_busqueda}%"))|
                (Pizzeria2.direccion.like(f"%{fecha_busqueda}%"))
            )
            print("Consulta por mes: " + str(ventasMes))
            return ventasMes
    else:
        
        ventasMes = Pizzeria2.query.filter(Pizzeria2.fecha_orden.like( f"%{str(datetime.now().date())}%")).all()
        print("FECHA DE HOY: " + str(datetime.now().date()))
        
        return ventasMes




        
if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()

