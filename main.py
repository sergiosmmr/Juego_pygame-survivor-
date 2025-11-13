import pygame as pg
import constantes_varaibles as cons
import personaje as per
import weapon as wp
import os
import texto as tx
import items as ts
import mundo as md
import csv
import enemigo as ene
import utils
import pantalla  

pg.init()
pg.mixer.init()

ventana = pg.display.set_mode((cons.ANCHO_VENTANA, cons.ALTO_VENTANA))
pg.display.set_caption(cons.NOMBRE_JUEGO)
icono = pg.image.load(cons.RUTA_ICONO)
pg.display.set_icon(icono)

############### variables ###############
posicion_pantalla = [0, 0]
nivel = 1
multiplicador_dificultad = 1.0

############### musica ###############
pg.mixer.music.set_volume(cons.MUSICA_VOLUMEN_NORMAL)  # volumen medio

# cargar el sonido del disparo ---
sonido_disparo = pg.mixer.Sound(cons.SONIDO_DISPARO)
sonido_disparo.set_volume(cons.SONIDO_DISPARO_NORMAL)  # ajusto el volumen

#######################  FUNCIONES (las que se quedan en Main)   #######################

# funciones de nivel / mundo
def cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos, multiplicador):
    # crea world + lista_enemigos sin tocar grupos (grupo_items se maneja afuera)
    world_data_local = utils.leer_csv_nivel(nivel)
    world_local = md.Mundo()
    # pasa el multiplicador a la siguiente funcion
    world_local.procesar_data(world_data_local, lista_tile, item_imagenes, animacion_enemigos, multiplicador)

    lista_enemigos_local = []
    for ene in world_local.lista_enemigo:
        lista_enemigos_local.append(ene)

    return world_local, lista_enemigos_local

def iniciar_juego(nivel_a_cargar):
    """
    prepara todas las variables y carga los assets para iniciar el juego.
    """
    global mostrar_inicio, mostrar_menu, mostrar_ranking, mostrar_selec_dificultad, evitar_click_fantasma
    global world, lista_enemigos, jugador  # hacemos globales las variables del juego
    
    # configura la musica y los estados
    pg.mixer.music.load(cons.MUSICA_JUEGO)
    pg.mixer.music.play(-1)
    mostrar_inicio = False
    mostrar_menu = False
    mostrar_ranking = False
    evitar_click_fantasma = True  # activa el anti-click
    
    # resetea al jugador
    jugador.energia = 100
    jugador.vivo = True
    jugador.score = 0
    
    # limpia los grupos de sprites
    grupo_damage_text.empty()
    grupo_balas.empty()
    grupo_items.empty()
    
    # carga el mundo (pasando el multiplicador)
    world, lista_enemigos = cargar_world_y_enemigos(nivel_a_cargar, lista_tile, item_imagenes, animacion_enemigos, multiplicador_dificultad)
    
    # crea el nuevo jugador seleccionado y lo coloca
    anim_dict_seleccionado = sets_anim_jugadores[personaje_seleccionado_idx]
    jugador = per.Personaje(80, 80, anim_dict_seleccionado, 100, 1)  # reinicia energia a 100
    jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel_a_cargar)])
    for item in world.lista_item:
        grupo_items.add(item)

def reiniciar_juego_completo():
    """ resetea todas las variables globales al estado de inicio. """
    global nivel, input_activo, nombre_jugador, puntaje_guardado, t_fin_juego
    global mensaje_fin_juego, font_fin_juego
    
    # resetea estado del jugador
    jugador.vivo = True
    jugador.energia = 100
    jugador.score = 0
    nivel = 1
    
    # resetea variables de input
    input_activo = False
    nombre_jugador = ""
    puntaje_guardado = False
    t_fin_juego = 0
    mensaje_fin_juego = "GAME OVER"
    font_fin_juego = font_game_over
    
    # limpia grupos
    grupo_damage_text.empty()
    grupo_balas.empty()
    grupo_items.empty()


##########################         FUENTES         ###########################

# --- carga de objetos de fuente ---
font_titulo = pg.font.Font(cons.FUENTE_GOTHIC, 100)
font_game_over = pg.font.Font(cons.FUENTE_GOTHIC, 110)
font_titulo_secundario = pg.font.Font(cons.FUENTE_TEXTO, 100)
font_inicio = pg.font.Font(cons.FUENTE_TEXTO, 30)
font_reinicio = pg.font.Font(cons.FUENTE_TEXTO, 30)
font_input = pg.font.Font(cons.FUENTE_TEXTO, 28)
font_volumen = pg.font.Font(cons.FUENTE_TEXTO, 20)
font_score = pg.font.Font(cons.FUENTE_TEXTO, cons.TAMANIO_FUENTE_SCORE)
font = pg.font.Font(cons.FUENTE_TEXTO, cons.TAMANIO_FUENTE_ENEMIGOS)

# --- renderizado de textos estaticos ---
game_over_text = font_game_over.render("GAME OVER", True, cons.COLOR_BLANCO)
texto_boton_reinicio = font_reinicio.render("Reiniciar", True, cons.COLOR_NEGRO)
texto_boton_salir_final = font_reinicio.render("Salir", True, cons.COLOR_BLANCO)
texto_boton_volver_menu = font_reinicio.render("Menu Principal", True, cons.COLOR_NEGRO)
label_nombre = font_input.render("Ingresá tus iniciales (3) y presiona ENTER:", True, cons.COLOR_BLANCO)
texto_ganaste = font_titulo.render("¡GANASTE!", True, cons.COLOR_BLANCO)
rect_ganaste = texto_ganaste.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2))

# textos de botones de inicio
boton_jugar = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, cons.ALTO_VENTANA / 2 + 15, 200, 50)
boton_menu = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, cons.ALTO_VENTANA / 2 + 75, 200, 50)
boton_salir = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, cons.ALTO_VENTANA / 2 + 135, 200, 50)
texto_boton_jugar = font_inicio.render("JUGAR", True, cons.COLOR_NEGRO)
texto_boton_menu = font_inicio.render("MENU", True, cons.COLOR_NEGRO)
texto_boton_salir = font_inicio.render("SALIR", True, cons.COLOR_BLANCO)

# textos de menu
texto_titulo_menu = font_titulo_secundario.render("M E N U", True, cons.COLOR_BLANCO)
rect_titulo_menu = texto_titulo_menu.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA / 2 - 150))
y_base_menu = cons.ALTO_VENTANA / 2 - 60
espacio_menu = 60
boton_dificultad = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, y_base_menu, 200, 50)
boton_ranking = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, y_base_menu + espacio_menu, 200, 50)
boton_volumen = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, y_base_menu + (espacio_menu * 2), 200, 50)
boton_controles = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, y_base_menu + (espacio_menu * 3), 200, 50)
boton_volver = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, y_base_menu + (espacio_menu * 4), 200, 50)
texto_boton_dificultad = font_inicio.render("DIFICULTAD", True, cons.COLOR_NEGRO)
texto_boton_ranking = font_inicio.render("RANKING", True, cons.COLOR_NEGRO)
texto_boton_volumen = font_inicio.render("VOLUMEN", True, cons.COLOR_NEGRO)
texto_boton_controles = font_inicio.render("CONTROLES", True, cons.COLOR_NEGRO)
texto_boton_volver = font_inicio.render("VOLVER", True, cons.COLOR_NEGRO)

# textos de sub-menus (volumen y dificultad)
ancho_boton_vol = 60
espacio_boton_vol = 10
x_inicio_dif = cons.ANCHO_VENTANA / 2 + 110
y_boton_dif = boton_dificultad.y
boton_dif_facil = pg.Rect(x_inicio_dif, y_boton_dif, ancho_boton_vol, 50)
boton_dif_norm = pg.Rect(x_inicio_dif + ancho_boton_vol + espacio_boton_vol, y_boton_dif, ancho_boton_vol, 50)
boton_dif_fuerte = pg.Rect(x_inicio_dif + (ancho_boton_vol + espacio_boton_vol) * 2, y_boton_dif, ancho_boton_vol, 50)
x_inicio_vol = cons.ANCHO_VENTANA / 2 + 110
y_boton_vol = boton_volumen.y
boton_vol_bajo = pg.Rect(x_inicio_vol, y_boton_vol, ancho_boton_vol, 50)
boton_vol_norm = pg.Rect(x_inicio_vol + ancho_boton_vol + espacio_boton_vol, y_boton_vol, ancho_boton_vol, 50)
boton_vol_fuerte = pg.Rect(x_inicio_vol + (ancho_boton_vol + espacio_boton_vol) * 2, y_boton_vol, ancho_boton_vol, 50)
texto_vol_bajo = font_volumen.render("M I N", True, cons.COLOR_NEGRO)
texto_vol_norm = font_volumen.render("N O R", True, cons.COLOR_NEGRO)
texto_vol_fuerte = font_volumen.render("M A X", True, cons.COLOR_NEGRO)
texto_dif_facil = font_volumen.render("Facil", True, cons.COLOR_NEGRO)
texto_dif_norm = font_volumen.render("Normal", True, cons.COLOR_NEGRO)
texto_dif_fuerte = font_volumen.render("Dificil", True, cons.COLOR_NEGRO)

# textos de ranking
texto_titulo_ranking = font_titulo.render("RANKING", True, cons.COLOR_BLANCO)
rect_titulo_ranking = texto_titulo_ranking.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA / 2 - 250))

# textos de controles
texto_titulo_controles = font_titulo_secundario.render("C O N T R O L E S", True, cons.COLOR_BLANCO)
rect_titulo_controles = texto_titulo_controles.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA / 2 - 200))
texto_controles_1 = font_reinicio.render("W, A, S, D = Moverse", True, cons.COLOR_BLANCO)
texto_controles_2 = font_reinicio.render("Click Izquierdo = Disparar", True, cons.COLOR_BLANCO)
texto_controles_3 = font_reinicio.render("E = Abrir Puertas", True, cons.COLOR_BLANCO)

# textos de historia 
texto_titulo_briefing = font_titulo_secundario.render("S O B R E V I V E", True, cons.COLOR_BLANCO)
rect_titulo_briefing = texto_titulo_briefing.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA / 2 - 250))
texto_historia_1 = font_reinicio.render("Hordas de monstruos han invadido.", True, cons.COLOR_BLANCO)
texto_historia_2 = font_reinicio.render("¡Elimínalos a todos y encuentra la salida!", True, cons.COLOR_AMARILLO)
texto_cofre = font_reinicio.render("¡Busca el cofre para escapar!", True, cons.COLOR_AMARILLO)
boton_comenzar = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, cons.ALTO_VENTANA / 2 + 250, 200, 50)
texto_boton_comenzar = font_inicio.render("COMENZAR", True, cons.COLOR_NEGRO)

# --- variables de la pantalla de selección de personaje ---
texto_titulo_personaje = font_titulo_secundario.render("ELIGE TU HEROE", True, cons.COLOR_BLANCO)
rect_titulo_personaje = texto_titulo_personaje.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA / 2 - 250))
boton_selec_p1 = pg.Rect(cons.ANCHO_VENTANA / 2 - 200, cons.ALTO_VENTANA / 2 - 100, 100, 150)
boton_selec_p2 = pg.Rect(cons.ANCHO_VENTANA / 2 - 50, cons.ALTO_VENTANA / 2 - 100, 100, 150)
boton_selec_p3 = pg.Rect(cons.ANCHO_VENTANA / 2 + 100, cons.ALTO_VENTANA / 2 - 100, 100, 150)
texto_boton_siguiente = font_inicio.render("SIGUIENTE", True, cons.COLOR_NEGRO)

# --- variables de estado (fin de juego) ---
mensaje_fin_juego = "GAME OVER"
font_fin_juego = font_game_over
input_activo = False
nombre_jugador = ""
puntaje_guardado = False
t_fin_juego = 0
input_rect = pg.Rect(cons.ANCHO_VENTANA // 2 - 80, cons.ALTO_VENTANA // 2, 160, 40)
color_inactivo = (cons.COLOR_NEGRO)
color_activo = (cons.COLOR_BLANCO)

############### importar imagenes ###############

imagen_fondo_inicio = pg.image.load("assets/images/fondos_de_pantalla/fondo_inicio.webp").convert()
imagen_fondo_inicio = pg.transform.scale(imagen_fondo_inicio, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))
imagen_fondo_menu = pg.image.load("assets/images/fondos_de_pantalla/imagen_fondo_menu.jpg").convert()
imagen_fondo_menu = pg.transform.scale(imagen_fondo_menu, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))
imagen_fondo_victoria = pg.image.load("assets/images/fondos_de_pantalla/imagen_fondo_victoria.png").convert()
imagen_fondo_victoria = pg.transform.scale(imagen_fondo_victoria, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))
imagen_fondo_derrota = pg.image.load("assets/images/fondos_de_pantalla/imagen_fondo_derrota.png").convert()
imagen_fondo_derrota = pg.transform.scale(imagen_fondo_derrota, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))

# energia
corazon_vacio = utils.cargar_imagen("assets/images/items/corazon_vacio_1.png", cons.ESCALA_CORAZONES)
corazon_medio = utils.cargar_imagen("assets/images/items/corazon_mitad_1.png", cons.ESCALA_CORAZONES)
corazon_lleno = utils.cargar_imagen("assets/images/items/corazon_lleno_1.png", cons.ESCALA_CORAZONES)

# --- cargar animaciones de jugadores ---
directorio_jugadores = "assets/images/characters/players"
sets_anim_jugadores = utils.cargar_set_animaciones(directorio_jugadores, cons.ESCALA_PERSONAJE)
for anim_dict in sets_anim_jugadores:
    anim_dict["frame_index"] = 0
    anim_dict["update_time"] = pg.time.get_ticks()
    anim_dict["cooldown"] = 150

# --- cargar animaciones de enemigos ---
directorio_enemigos = "assets/images/characters/enemigos"
animacion_enemigos = utils.cargar_set_animaciones(directorio_enemigos, cons.ESCALA_ENEMIGOS)

# armas y balas
imagen_arma = utils.cargar_imagen("assets/images/weapons/vacio.png", cons.ESCALA_ARMA)
imagen_bala = utils.cargar_imagen("assets/images/weapons/bullets/fuego_1.png", cons.ESCALA_BALA)

# cargar imagenes del mundo
lista_tile = []
for x in range(cons.TIPOS_TILES):
    tile_image = pg.image.load(f"assets/images/tiles/tile_{x+1}.png").convert_alpha()
    tile_image = pg.transform.scale(tile_image, (int(cons.TAMANIO_TILES), int(cons.TAMANIO_TILES)))
    lista_tile.append(tile_image)

# cargar imagen de los items
posion_roja = utils.cargar_imagen("assets/images/items/posion/posion.png", cons.ESCALA_POSION_ROJA)
monedas_imagen = []
ruta_imagen = "assets/images/items/moneda"
numero_monedas_imagen = utils.contar_elementos(ruta_imagen)
for i in range(numero_monedas_imagen):
    img = utils.cargar_imagen(f"assets/images/items/moneda/moneda_frame_{i+1}.png", cons.ESCALA_MONEDA)
    monedas_imagen.append(img)
item_imagenes = [monedas_imagen, [posion_roja]]

#################### CREACIÓN DE DICCIONARIO DE ASSETS  ############################
# Agrupamos todos los assets imagenes, fuentes y rects de botones en un solo diccionario 
assets = {
    # fuentes
    "font_titulo": font_titulo,
    "font_game_over": font_game_over,
    "font_titulo_secundario": font_titulo_secundario,
    "font_inicio": font_inicio,
    "font_reinicio": font_reinicio,
    "font_input": font_input,
    "font_volumen": font_volumen,
    "font_score": font_score,
    "font": font,
    
    # textos fin de Juego
    "game_over_text": game_over_text,
    "texto_boton_reinicio": texto_boton_reinicio,
    "texto_boton_salir_final": texto_boton_salir_final,
    "texto_boton_volver_menu": texto_boton_volver_menu,
    "label_nombre": label_nombre,
    
    # textos victoria
    "texto_ganaste": texto_ganaste,
    "rect_ganaste": rect_ganaste,
    
    # textos/botones Inicio
    "boton_jugar": boton_jugar,
    "boton_menu": boton_menu,
    "boton_salir": boton_salir,
    "texto_boton_jugar": texto_boton_jugar,
    "texto_boton_menu": texto_boton_menu,
    "texto_boton_salir": texto_boton_salir,
    
    # textos/botones Menu
    "texto_titulo_menu": texto_titulo_menu,
    "rect_titulo_menu": rect_titulo_menu,
    "boton_dificultad": boton_dificultad,
    "boton_ranking": boton_ranking,
    "boton_volumen": boton_volumen,
    "boton_controles": boton_controles,
    "boton_volver": boton_volver,
    "texto_boton_dificultad": texto_boton_dificultad,
    "texto_boton_ranking": texto_boton_ranking,
    "texto_boton_volumen": texto_boton_volumen,
    "texto_boton_controles": texto_boton_controles,
    "texto_boton_volver": texto_boton_volver,
    
    # textos/botones Sub-menus
    "boton_dif_facil": boton_dif_facil,
    "boton_dif_norm": boton_dif_norm,
    "boton_dif_fuerte": boton_dif_fuerte,
    "boton_vol_bajo": boton_vol_bajo,
    "boton_vol_norm": boton_vol_norm,
    "boton_vol_fuerte": boton_vol_fuerte,
    "texto_vol_bajo": texto_vol_bajo,
    "texto_vol_norm": texto_vol_norm,
    "texto_vol_fuerte": texto_vol_fuerte,
    "texto_dif_facil": texto_dif_facil,
    "texto_dif_norm": texto_dif_norm,
    "texto_dif_fuerte": texto_dif_fuerte,
    
    # textos/botones Ranking
    "texto_titulo_ranking": texto_titulo_ranking,
    "rect_titulo_ranking": rect_titulo_ranking,
    
    # textos/botones controles
    "texto_titulo_controles": texto_titulo_controles,
    "rect_titulo_controles": rect_titulo_controles,
    "texto_controles_1": texto_controles_1,
    "texto_controles_2": texto_controles_2,
    "texto_controles_3": texto_controles_3,
    
    # textos/botones Historia 
    "texto_titulo_briefing": texto_titulo_briefing,
    "rect_titulo_briefing": rect_titulo_briefing,
    "texto_historia_1": texto_historia_1,
    "texto_historia_2": texto_historia_2,
    "texto_cofre": texto_cofre,
    "boton_comenzar": boton_comenzar,
    "texto_boton_comenzar": texto_boton_comenzar,
    
    # textos/botones Selec. Personaje
    "texto_titulo_personaje": texto_titulo_personaje,
    "rect_titulo_personaje": rect_titulo_personaje,
    "boton_selec_p1": boton_selec_p1,
    "boton_selec_p2": boton_selec_p2,
    "boton_selec_p3": boton_selec_p3,
    "texto_boton_siguiente": texto_boton_siguiente,
    
    # variables Fin de Juego
    "input_rect": input_rect,
    "color_inactivo": color_inactivo,
    "color_activo": color_activo,
    
    # Imagenes de Fondo
    "imagen_fondo_inicio": imagen_fondo_inicio,
    "imagen_fondo_menu": imagen_fondo_menu,
    "imagen_fondo_victoria": imagen_fondo_victoria,
    "imagen_fondo_derrota": imagen_fondo_derrota,
    
    # Animaciones
    "sets_anim_jugadores": sets_anim_jugadores,
    
    # Separamos los corazones para pasarlos a 'vida_jugador' más facil
    "assets_corazon": {
        "vacio": corazon_vacio,
        "medio": corazon_medio,
        "lleno": corazon_lleno
    }
}



##################  CONFIGURACIÓN DEL MUNDO INICIAL  ##################

world_data = []
for fila in range(cons.FILAS):
    filas = [7] * cons.COLUMNAS
    world_data.append(filas)

# cargar el archivo con nivel
with open("niveles/nivel_1.csv", newline="") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data [x] [y] = int(columna)
world = md.Mundo()
world.procesar_data(world_data, lista_tile, item_imagenes, animacion_enemigos, multiplicador_dificultad)

# crear una lista de enemigos
lista_enemigos = []
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)

# crear un arma de la clase weapon centrada en jugador
arma = wp.weapon(imagen_arma, imagen_bala, sonido_disparo)

# crear un grupo de sprites
grupo_damage_text = pg.sprite.Group()
grupo_balas = pg.sprite.Group()
grupo_items = pg.sprite.Group()

# añadir items de la data de world
for item in world.lista_item:
    grupo_items.add(item)


# crear un jugador de la clase personaje en posicion x , y
jugador = per.Personaje(80, 80, sets_anim_jugadores[1], 80, 1)  # inicia con heroina por defecto

  
#################  VARIABLES DE ESTADO DEL JUEGO  #########################

mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

reloj = pg.time.Clock()
run = True
mostrar_inicio = True
mostrar_menu = False
mostrar_opciones_volumen = False
mostrar_ranking = False
mostrar_opciones_dificultad = False
mostrar_selec_dificultad = False
mostrar_controles = False
mostrar_historia = False  
mostrar_selec_personaje = False
evitar_click_fantasma = False
personaje_seleccionado_idx = 1  # heroina por defecto

# estado de victoria
mostrar_ganaste = False
t_inicio_ganaste = 0



############## BUCLE PRINCIPAL DEL JUEGO  ###############
while run:
    ############ DICCIONARIO DE ESTADO  ##############

    # agrupamos todas las variables de estado que cambian para pasarlas a las funciones de pantalla
    estado_juego = {
        "mostrar_opciones_volumen": mostrar_opciones_volumen,
        "mostrar_opciones_dificultad": mostrar_opciones_dificultad,
        "personaje_seleccionado_idx": personaje_seleccionado_idx,
        "input_activo": input_activo,
        "nombre_jugador": nombre_jugador,
        "puntaje_guardado": puntaje_guardado,
        "mensaje_fin_juego": mensaje_fin_juego,
        "font_fin_juego": font_fin_juego
    }
    
    # --- SECCION DE DIBUJADO (Pantallas)

    if mostrar_inicio:
        pantalla.pantalla_inicio(ventana, assets)
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(cons.MUSICA_PRINCIPAL)
            pg.mixer.music.play(-1)

    elif mostrar_menu:
        pantalla.pantalla_menu(ventana, assets, estado_juego)

    elif mostrar_ranking:
        pantalla.pantalla_ranking(ventana, assets)

    elif mostrar_controles:
        pantalla.pantalla_controles(ventana, assets)

    elif mostrar_historia: 
        pantalla.pantalla_historia(ventana, assets)

    elif mostrar_selec_personaje:
        pantalla.pantalla_selec_personaje(ventana, assets, estado_juego)

    # --- JUEGO PRINCIPAL  ---
    else:
        # que valla a 60 fps
        reloj.tick(cons.FPS)
        ventana.fill(cons.COLOR_SUELO)

        if jugador.vivo:
            # calcular movimiento del jugador
            delta_x = 0
            delta_y = 0
            if mover_derecha: delta_x = cons.VELOCIDAD_PERSONAJE
            if mover_izquierda: delta_x = -cons.VELOCIDAD_PERSONAJE
            if mover_abajo: delta_y = cons.VELOCIDAD_PERSONAJE
            if mover_arriba: delta_y = -cons.VELOCIDAD_PERSONAJE

            # mover al jugador
            posicion_pantalla, nivel_completo = jugador.movimiento(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)
            world.update(posicion_pantalla)
            jugador.update()

            # actualiza estado de enemigo
            for ene_data in lista_enemigos:
                ene_obj = ene_data[0]
                ene_obj.update()
            
            # actualiza el esatdo del arma
            bala = None
            if evitar_click_fantasma:
                if not pg.mouse.get_pressed()[0]:
                    evitar_click_fantasma = False
            else:
                bala = arma.update(jugador)
            if bala:
                grupo_balas.add(bala)

            # "desempaquetamos"
            lista_de_objetos_enemigos = [ene_data[0] for ene_data in lista_enemigos]

            for bala in grupo_balas:
                damage, post_damage = bala.update(lista_de_objetos_enemigos, world.obstaculos_tiles)
                if damage:
                    damage_text = tx.Damage_text(post_damage.centerx, post_damage.centery, "-" + str(damage), font, cons.COLOR_ROJO)
                    grupo_damage_text.add(damage_text)

            # actualizar grupos
            grupo_damage_text.update(posicion_pantalla)
            grupo_items.update(posicion_pantalla, jugador)

            # dibujar mundo
            world.draw(ventana)
            jugador.dibujar(ventana)

            # dibujar al enemigo
            for ene_data in lista_enemigos.copy():
                ene = ene_data[0]
                if ene.energia <= 0:
                    jugador.score += ene.score_value
                    lista_enemigos.remove(ene_data)
                    continue
                ene.ia(jugador, world.obstaculos_tiles, posicion_pantalla,)
                ene.dibujar(ventana)

            # dibujar arma y balas
            arma.dibujar(ventana)
            grupo_balas.draw(ventana) 

            # dibujar corazones
            utils.vida_jugador(ventana, jugador, assets["assets_corazon"]) 

            # dibujar textos
            grupo_damage_text.draw(ventana)
            utils.dibujar_texto_pantalla(ventana, f"SCORE : {jugador.score}", font_score, cons.COLOR_AMARILLO, cons.POSICION_TEXTO_SCORE_X, cons.POSICION_TEXTO_SCORE_Y) 
            utils.dibujar_texto_pantalla(ventana, f"N I V E L: " + str(nivel), font, cons.COLOR_BLANCO, cons.ANCHO_VENTANA / 2, 5) 

            # dibujar items
            grupo_items.draw(ventana)

            # chuequear si el nivel esta completo
            if nivel_completo:
                if nivel < cons.NIVEL_MAXIMO:
                    nivel += 1
                    world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos, multiplicador_dificultad)
                    jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])
                    grupo_items.empty()
                    for item in world.lista_item:
                        grupo_items.add(item)
                else:
                    # ganar
                    mensaje_fin_juego = "¡GANASTE!"
                    font_fin_juego = font_titulo
                    jugador.vivo = False
                    #t_fin_juego = pg.time.get_ticks()
                    pg.event.clear()

        # --- LOGICA DE FIN DE JUEGO (si no esta vivo) ---
        else:
            if t_fin_juego == 0:
                t_fin_juego = pg.time.get_ticks()
                pg.event.clear()
                if pg.mixer.music.get_busy():
                    pg.mixer.music.stop()
                if mensaje_fin_juego == "GAME OVER":
                    pg.mixer.music.load(cons.MUSICA_GAME_OVER)
                    pg.mixer.music.play(-1) # -1 para que suene en bucle
                elif mensaje_fin_juego == "¡GANASTE!":
                    pg.mixer.music.load(cons.MUSICA_GANASTE)
                    pg.mixer.music.play(-1)

            if not input_activo and (pg.time.get_ticks() - t_fin_juego > 1000):
                input_activo = True

            # llamar a la funcion de DIBUJO de fin de juego
            pantalla.pantalla_fin_juego(ventana, assets, estado_juego)

    # --- BUCLE DE EVENTOS logica
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        # --- eventos de Menus (si NO estamos en el juego) ---
        if mostrar_inicio:
            if event.type == pg.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                    mostrar_selec_personaje = True
                elif boton_menu.collidepoint(event.pos):
                    pg.mixer.music.load(cons.MUSICA_MENU)
                    pg.mixer.music.play(-1)
                    mostrar_inicio = False
                    mostrar_menu = True
                elif boton_salir.collidepoint(event.pos):
                    run = False
        
        elif mostrar_menu:
            if event.type == pg.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(event.pos):
                    pg.mixer.music.load(cons.MUSICA_PRINCIPAL)
                    pg.mixer.music.play(-1)
                    mostrar_menu = False
                    mostrar_inicio = True
                    mostrar_opciones_volumen = False
                    mostrar_opciones_dificultad = False
                    mostrar_controles = False

                elif boton_volumen.collidepoint(event.pos):
                    mostrar_opciones_volumen = not mostrar_opciones_volumen
                    mostrar_opciones_dificultad = False

                elif boton_ranking.collidepoint(event.pos):
                    mostrar_menu = False
                    mostrar_ranking = True
                    mostrar_opciones_volumen = False
                    mostrar_opciones_dificultad = False

                elif boton_dificultad.collidepoint(event.pos):
                    mostrar_opciones_dificultad = not mostrar_opciones_dificultad
                    mostrar_opciones_volumen = False

                elif boton_controles.collidepoint(event.pos):
                    mostrar_menu = False
                    mostrar_controles = True
                    mostrar_opciones_volumen = False
                    mostrar_opciones_dificultad = False

                elif mostrar_opciones_volumen:
                    if boton_vol_bajo.collidepoint(event.pos):
                        utils.aplicar_volumen(sonido_disparo, cons.MUSICA_VOLUMEN_BAJO, cons.SONIDO_DISPARO_BAJO) 
                        mostrar_opciones_volumen = False
                    elif boton_vol_norm.collidepoint(event.pos):
                        utils.aplicar_volumen(sonido_disparo, cons.MUSICA_VOLUMEN_NORMAL, cons.SONIDO_DISPARO_NORMAL) 
                        mostrar_opciones_volumen = False
                    elif boton_vol_fuerte.collidepoint(event.pos):
                        utils.aplicar_volumen(sonido_disparo, cons.MUSICA_VOLUMEN_FUERTE, cons.SONIDO_DISPARO_FUERTE) 
                        mostrar_opciones_volumen = False

                elif mostrar_opciones_dificultad:
                    if boton_dif_facil.collidepoint(event.pos):
                        multiplicador_dificultad = 0.7
                        mostrar_opciones_dificultad = False
                    elif boton_dif_norm.collidepoint(event.pos):
                        multiplicador_dificultad = 1.0
                        mostrar_opciones_dificultad = False
                    elif boton_dif_fuerte.collidepoint(event.pos):
                        multiplicador_dificultad = 1.5
                        mostrar_opciones_dificultad = False

        elif mostrar_ranking:
            if event.type == pg.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(event.pos):
                    mostrar_ranking = False
                    mostrar_menu = True

        elif mostrar_controles:
            if event.type == pg.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(event.pos):
                    mostrar_controles = False
                    mostrar_menu = True
        
        elif mostrar_historia: 
            if event.type == pg.MOUSEBUTTONDOWN:
                if boton_comenzar.collidepoint(event.pos):
                    mostrar_historia = False 
                    iniciar_juego(nivel)

        elif mostrar_selec_personaje:
            if event.type == pg.MOUSEBUTTONDOWN:
                if boton_comenzar.collidepoint(event.pos):
                    mostrar_selec_personaje = False
                    mostrar_historia = True 
                elif boton_selec_p1.collidepoint(event.pos):
                    personaje_seleccionado_idx = 0
                elif boton_selec_p2.collidepoint(event.pos):
                    personaje_seleccionado_idx = 1
                elif boton_selec_p3.collidepoint(event.pos):
                    personaje_seleccionado_idx = 2

        # --- eventos del JUEGO (si el jugador esta vivo) ---
        elif jugador.vivo:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w: mover_arriba = True
                elif event.key == pg.K_s: mover_abajo = True
                elif event.key == pg.K_d: mover_derecha = True
                elif event.key == pg.K_a: mover_izquierda = True
                elif event.key == pg.K_e:
                    if world.cambiar_puerta(jugador, lista_tile):
                        print("puerta cambiada")
            if event.type == pg.KEYUP:
                if event.key == pg.K_w: mover_arriba = False
                elif event.key == pg.K_s: mover_abajo = False
                elif event.key == pg.K_d: mover_derecha = False
                elif event.key == pg.K_a: mover_izquierda = False
        
        # --- eventos de FIN DE JUEGO (si el jugador NO esta vivo) ---
        else:
            # eventos de teclado (input)
            if event.type == pg.KEYDOWN:
                if input_activo:
                    if event.key == pg.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    elif event.key == pg.K_RETURN:
                        if len(nombre_jugador.strip()) == 3 and not puntaje_guardado:
                            try:
                                file_existe = os.path.isfile(cons.SCORES_FILE)
                                with open(cons.SCORES_FILE, "a", newline="", encoding="utf-8") as f:
                                    writer = csv.writer(f)
                                    if not file_existe:
                                        writer.writerow(["nombre", "score"])
                                    writer.writerow([nombre_jugador.strip().upper(), jugador.score])
                                puntaje_guardado = True
                            except Exception as e:
                                print("[ERROR guardando score]", e)
                    elif event.unicode.isalpha() and len(nombre_jugador) < 3 and not puntaje_guardado:
                        nombre_jugador += event.unicode.upper()
            
            # eventos de Clic (botones)
            if event.type == pg.MOUSEBUTTONDOWN:
                if puntaje_guardado:
                    boton_reinicio = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, cons.ALTO_VENTANA / 2 + 100, 200, 50)
                    boton_volver_menu = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, cons.ALTO_VENTANA / 2 + 160, 200, 50)
                    boton_salir_final = pg.Rect(cons.ANCHO_VENTANA / 2 - 100, cons.ALTO_VENTANA / 2 + 220, 200, 50)

                    if boton_reinicio.collidepoint(event.pos):
                        reiniciar_juego_completo()
                        iniciar_juego(nivel)
                    elif boton_volver_menu.collidepoint(event.pos):
                        reiniciar_juego_completo()
                        mostrar_inicio = True
                        pg.mixer.music.load(cons.MUSICA_PRINCIPAL)
                        pg.mixer.music.play(-1)
                    elif boton_salir_final.collidepoint(event.pos):
                        run = False
                else:
                    # logica de clic en el input
                    if input_rect.collidepoint(event.pos):
                        if pg.time.get_ticks() - t_fin_juego > 1000:
                            input_activo = True
                    else:
                        input_activo = False

    pg.display.update()

pg.quit()