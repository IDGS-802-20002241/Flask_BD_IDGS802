from io import open

class ManejadorArchivo:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def insertar(self, palabra1):
        with open(self.nombre_archivo, 'a') as archivo_texto:
            archivo_texto.write(f'{palabra1}\n')

    def mostrar_contenido(self):
        resultados = []
        with open(self.nombre_archivo, 'r') as archivo_texto:
            for linea in archivo_texto.readlines():
                    resultados.append(linea.rstrip())
        
        if resultados:
            return resultados
        else:
            return ''

    def eliminar(self, indice):
        try:
            with open(self.nombre_archivo, 'r') as archivo_texto:
                lineas = archivo_texto.readlines()

            with open(self.nombre_archivo, 'w') as archivo_texto:
                for i, linea in enumerate(lineas, 1):  # Comienza la enumeración desde 1
                    if i != indice:
                        archivo_texto.write(linea)

            return f'Renglón en el índice {indice} eliminado exitosamente.'
        except Exception as e:
            print(f'Error al eliminar el renglón: {e}')
            return f'Error al eliminar el renglón: {e}'


       
                 


    
    def eliminar_todo(self):
        try:
            with open(self.nombre_archivo, 'w') as archivo_texto:
                archivo_texto.write('')
               
            return 'Todo el contenido del archivo ha sido eliminado exitosamente.'
        except Exception as e:
            return f'Error al eliminar todo el contenido: {e}'