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
    
    Busca carpetas de personajes y DENTRO
    busca carpetas de acción ("idle", "run").
    
    Devuelve una lista de DICCIONARIOS 
    """
    lista_principal_de_personajes = []
    
    # 1. Lee las carpetas de personajes 
    try:
        tipo_personajes = nombre_carpetas(directorio_principal) 
        tipo_personajes.sort()
    except FileNotFoundError:
        print(f"Error: No se encontró el directorio de personajes: {directorio_principal}")
        return []

    for tipo in tipo_personajes:
        # Crea la ruta al personaje 
        ruta_personaje = os.path.join(directorio_principal, tipo)
        
        if not os.path.isdir(ruta_personaje):
            continue

        # Diccionario para las animaciones de ESTE personaje
        animaciones_del_personaje = {}
        
        # 2. Lee las carpetas de acción ("idle", "run")
        try:
            tipo_acciones = nombre_carpetas(ruta_personaje)
        except FileNotFoundError:
            continue # Salta este personaje si su carpeta está vacía

        for accion in tipo_acciones:
            lista_temporal_frames = []
            # Crea la ruta a la acción
            ruta_accion = os.path.join(ruta_personaje, accion)
            
            if not os.path.isdir(ruta_accion):
                continue
            
            # 3. Lee los frames 
            try:
                nombres_de_archivos = nombre_carpetas(ruta_accion)
                nombres_de_archivos.sort() # Ordena los frames
            except FileNotFoundError:
                continue

            for nombre_archivo in nombres_de_archivos:
                ruta_completa = os.path.join(ruta_accion, nombre_archivo)
                imagen = cargar_imagen(ruta_completa, escala)
                lista_temporal_frames.append(imagen)
            
            # Guarda la lista de frames en el diccionario
            # ej. animaciones_del_personaje["idle"] = [<img1>, <img2>]
            if lista_temporal_frames: # Solo si se cargaron imágenes
                animaciones_del_personaje[accion] = lista_temporal_frames
        
        # 4. === EL ARREGLO PARA EL PERSONAJE SI NO TIENE IDLE ===
        # Si el personaje (dragon) no tiene "idle" PERO sí tiene "run"...
        if "idle" not in animaciones_del_personaje and "run" in animaciones_del_personaje:
            # ...crea una animación "idle" usando el primer frame de "run"
            print(f"Aviso: El personaje '{tipo}' no tiene anim. 'idle'. Usando el primer frame de 'run'.")
            animaciones_del_personaje["idle"] = [ animaciones_del_personaje["run"][0] ]
        
        # 5. Añade el diccionario de este personaje a la lista principal
        if animaciones_del_personaje: # Solo si cargó algo
            lista_principal_de_personajes.append(animaciones_del_personaje)
            
    return lista_principal_de_personajes

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