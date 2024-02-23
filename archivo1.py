from io import open

def insertar():
    
    archivo_texto=open('anombres.txt', 'r')
    #print(archivo_texto.readlines())
    #archivo_texto.write('\n datos en archivo') 
    #archivo_texto.close()

    for lineas in archivo_texto.readlines():
        print(lineas.rstrip())
        
    archivo_texto.close()