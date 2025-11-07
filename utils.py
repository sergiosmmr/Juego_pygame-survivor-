import pygame as pg
import os
import csv
import constantes_varaibles as cons 

# --- COMIENZA EL BLOQUE DE FUNCIONES ---

def escalar_img(image, scale):
    """ Escala una imagen manteniendo la proporción. """
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pg.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_imagen

def contar_elementos(directorio):
    """ Cuenta los archivos en un directorio. """
    return len (os.listdir(directorio)) 

def nombre_carpetas(directorio):
    """ Devuelve una lista de nombres de archivos/carpetas en un directorio. """
    return os.listdir(directorio)

def cargar_imagen(path, escala=None):
    """ Carga una imagen, la convierte (alpha) y la escala. """
    img = pg.image.load(path).convert_alpha()
    if escala is not None:
        img = escalar_img(img, escala)
    return img

def cargar_set_animaciones(directorio_principal, escala):
    """
    Carga, ordena y escala múltiples sets de animaciones desde las 
    subcarpetas de un directorio principal.
    """
    lista_principal = []
    tipo_personajes = nombre_carpetas(directorio_principal) 

    for tipo in tipo_personajes:
        lista_temporal = []
        ruta_temporal = os.path.join(directorio_principal, tipo)
        
        if not os.path.isdir(ruta_temporal):
            continue

        nombres_de_archivos = nombre_carpetas(ruta_temporal)
        nombres_de_archivos.sort() # Ordena los frames

        for nombre_archivo in nombres_de_archivos:
            ruta_completa = os.path.join(ruta_temporal, nombre_archivo)
            imagen = cargar_imagen(ruta_completa, escala)
            lista_temporal.append(imagen)
        
        lista_principal.append(lista_temporal)
        
    return lista_principal

def leer_csv_nivel(nivel):
    """ Lee un archivo CSV de nivel y devuelve una matriz (lista de listas). """
    data = [[7] * cons.COLUMNAS for _ in range(cons.FILAS)]
    ruta_csv = f"niveles/nivel_{nivel}.csv"
    
    try:
        with open(ruta_csv, newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for x, fila in enumerate(reader):
                for y, columna in enumerate(fila):
                    data[x][y] = int(columna)
    except FileNotFoundError:
        print(f"¡ERROR! No se encontró el archivo: {ruta_csv}")
    
    return data