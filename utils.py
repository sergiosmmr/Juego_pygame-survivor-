import pygame as pg
import os
import csv
import constantes_varaibles as cons 


def dibujar_texto_pantalla(ventana, texto, fuente, color, x, y):
    """
    Dibuja texto en la pantalla (ventana).
    """
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))

def vida_jugador(ventana, jugador, assets_corazon):
    """
    Dibuja la vida del jugador en la ventana, usando las imágenes del dict assets_corazon.
    """
    corazon_mitad_dibujado = False
    
    # extraemos las imagenes del diccionario
    corazon_lleno = assets_corazon["lleno"]
    corazon_medio = assets_corazon["medio"]
    corazon_vacio = assets_corazon["vacio"]
    
    for i in range(5):
        if jugador.energia >= ((i + 1) * 20):
            ventana.blit(corazon_lleno, (5 + i * 50, 5))
        elif jugador.energia % 20 > 0 and not corazon_mitad_dibujado:
            ventana.blit(corazon_medio, (5 + i * 50, 5))
            corazon_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio, (5 + i * 50, 5))

def aplicar_volumen(sonido_disparo, vol_musica, vol_sonido):
    """
    Aplica el volumen seleccionado a la música y a todos los sonidos.
    """
    # aplica a la musica 
    pg.mixer.music.set_volume(vol_musica)
    # aplica al sonido del disparo
    sonido_disparo.set_volume(vol_sonido)
    
    print(f"Volumen aplicado: Música={vol_musica}, Sonidos={vol_sonido}")

def cargar_scores(scores_file_path):
    """
    Carga los puntajes desde el archivo CSV.
    """
    scores_list = []
    # primero, revisa si el archivo existe
    if not os.path.isfile(scores_file_path):
        return []  # devuelve una lista vacia si no hay archivo

    try:
        with open(scores_file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # salta el encabezado ("nombre", "score")
            for row in reader:
                if row:  # asegura que la fila no este vacia
                    scores_list.append((row[0], int(row[1])))
    except Exception as e:
        print(f"Error al leer {scores_file_path}: {e}")
        return []

    # ordena la lista
    scores_list.sort(key=lambda item: item[1], reverse=True)
    
    # devuelve solo los 5 mejores puntajes
    return scores_list[:5]

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
    
    # lee las carpetas de personajes 
    try:
        tipo_personajes = nombre_carpetas(directorio_principal) 
        tipo_personajes.sort()
    except FileNotFoundError:
        print(f"Error: No se encontró el directorio de personajes: {directorio_principal}")
        return []

    for tipo in tipo_personajes:
        # crea la ruta al personaje 
        ruta_personaje = os.path.join(directorio_principal, tipo)
        
        if not os.path.isdir(ruta_personaje):
            continue

        # diccionario para las animaciones de ESTE personaje
        animaciones_del_personaje = {}
        
        # lee las carpetas de accion ("idle", "run")
        try:
            tipo_acciones = nombre_carpetas(ruta_personaje)
        except FileNotFoundError:
            continue # salta este personaje si su carpeta esta vacia

        for accion in tipo_acciones:
            lista_temporal_frames = []
            # crea la ruta a la accion
            ruta_accion = os.path.join(ruta_personaje, accion)
            
            if not os.path.isdir(ruta_accion):
                continue
            
            #  lee los frames 
            try:
                nombres_de_archivos = nombre_carpetas(ruta_accion)
                nombres_de_archivos.sort() # ordena los frames
            except FileNotFoundError:
                continue

            for nombre_archivo in nombres_de_archivos:
                ruta_completa = os.path.join(ruta_accion, nombre_archivo)
                imagen = cargar_imagen(ruta_completa, escala)
                lista_temporal_frames.append(imagen)
            
            # Guarda la lista de frames en el diccionario
            if lista_temporal_frames: # solo si se cargaron imagenes
                animaciones_del_personaje[accion] = lista_temporal_frames
        
        # si el personaje no tiene "idle" PERO si tiene "run"
        if "idle" not in animaciones_del_personaje and "run" in animaciones_del_personaje:
            # crea una animacion "idle" usando el primer frame de "run"
            print(f"Aviso: El personaje '{tipo}' no tiene anim. 'idle'. Usando el primer frame de 'run'.")
            animaciones_del_personaje["idle"] = [ animaciones_del_personaje["run"][0] ]
        
        # añade el diccionario de este personaje a la lista principal
        if animaciones_del_personaje: # solo si cargo algo
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

