import pygame as pg
import constantes_varaibles as cons
import personaje as per
import weapon as wp
import os
import texto as tx
import items as ts
import mundo as md
import csv

#######  FUNCIONES  ########

#  escalar imagen
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    # uso de scale con casteo a int para evitar errores de tipo
    nueva_imagen = pg.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_imagen

# funcion para contar elementos
def contar_elementos (directorio):
    return len (os.listdir(directorio)) 

#funcion listar elementos
def nombre_carpetas(directorio):
    return os.listdir(directorio)

# NUEVO: carga con convert_alpha() y escala opcional
def cargar_imagen(path, escala=None):
    img = pg.image.load(path).convert_alpha()
    if escala is not None:
        img = escalar_img(img, escala)
    return img

pg.init()
pg.mixer.init()

ventana = pg.display.set_mode((cons.ANCHO_VENTANA, cons.ALTO_VENTANA))
pg. display.set_caption(cons.NOMBRE_JUEGO)

### variables ####
posicion_pantalla = [0, 0]
nivel = 1
game_state = "MENU" # NUEVO: Controlador de estado del juego

# === MÚSICA ===
MUSICA_MENU = "assets/sonidos/menu2.mp3"
MUSICA_JUEGO = "assets/sonidos/juego.mp3"
pg.mixer.music.set_volume(0.5)  # volumen medio

# sonidos
sonido_disparo = pg.mixer.Sound("assets/sonidos/disparo.wav")  
sonido_disparo.set_volume(0.35)  # volumen entre 0.0 y 1.0

##### FUENTES ######
font = pg.font.Font("assets/font/Ryga.ttf", cons.TAMANIO_FUENTE_ENEMIGOS)
font_score = pg.font.Font("assets/font/Ryga.ttf", cons.TAMANIO_FUENTE_SCORE)
font_game_over = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 110)
font_reinicio = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 30)
font_inicio = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 30)
font_titulo = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 80)

game_over_text = font_game_over.render("GAME OVER", True, cons.COLOR_BLANCO)
texto_boton_reinicio = font_reinicio.render("Reiniciar", True, cons.COLOR_NEGRO)

# ingreso del nombre al finalizar
font_input = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 28)
label_nombre = font_input.render("Ingresá tu nombre:", True, cons.COLOR_BLANCO)
input_rect = pg.Rect(cons.ANCHO_VENTANA//2 - 160, cons.ALTO_VENTANA//2 + 100, 320, 40)
color_inactivo = (200, 200, 200)
color_activo = (255, 255, 255)
SCORES_FILE = "scores.csv"

# estado input
input_activo = False
nombre_jugador = ""
puntaje_guardado = False

# pantalla de victoria 
texto_ganaste = font_titulo.render("¡GANASTE!", True, cons.COLOR_BLANCO)
rect_ganaste = texto_ganaste.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2))

# botones de inicio
boton_jugar = pg.Rect(cons.ANCHO_VENTANA/2 -100, cons.ALTO_VENTANA/2 -50, 200, 50)
boton_salir = pg.Rect(cons.ANCHO_VENTANA/2 -100, cons.ALTO_VENTANA/2 +50, 200, 50)
texto_boton_jugar = font_inicio.render("JUGAR", True, cons.COLOR_NEGRO)
texto_boton_salir = font_inicio.render("SALIR", True, cons.COLOR_BLANCO)

# pantalla de inicio
def pantalla_inicio():
    ventana.fill(cons.COLOR_SUELO)
    dibujar_texto_pantalla ("Mi primer juego SURVIVOR", font_titulo, cons.COLOR_BLANCO, cons.ANCHO_VENTANA/2 -400, cons.ALTO_VENTANA/2 -200)
    pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_jugar)
    pg.draw.rect(ventana, cons.COLOR_ROJO, boton_salir)
    ventana.blit(texto_boton_jugar, (boton_jugar.x + 50, boton_jugar.y + 10))
    ventana.blit(texto_boton_salir, (boton_salir.x + 50, boton_salir.y + 10))

##############importar imagenes#############
corazon_vacio = cargar_imagen("assets/images/items/corazon_vacio_1.png", cons.ESCALA_CORAZONES)
corazon_medio = cargar_imagen("assets/images/items/corazon_mitad_1.png", cons.ESCALA_CORAZONES)
corazon_lleno = cargar_imagen("assets/images/items/corazon_lleno_1.png", cons.ESCALA_CORAZONES)
animaciones = [cargar_imagen(f"assets/images/characters/players/necro_mov_{i+1}.png", cons.ESCALA_PERSONAJE) for i in range(7)]
directorio_enemigos = "assets/images/characters/enemigos"
tipo_enemigos = nombre_carpetas(directorio_enemigos)
animacion_enemigos = []
for eni in tipo_enemigos:
    lista_temporal = []
    ruta_temporal = f"assets/images/characters/enemigos/{eni}"
    nombres_de_archivos = sorted(nombre_carpetas(ruta_temporal))
    for nombre_archivo in nombres_de_archivos:
        ruta_completa = f"{ruta_temporal}/{nombre_archivo}"
        imagen_enemigo = cargar_imagen(ruta_completa, cons.ESCALA_ENEMIGOS)
        lista_temporal.append(imagen_enemigo)
    animacion_enemigos.append(lista_temporal)
imagen_arma = cargar_imagen("assets/images/weapons/vacio.png", cons.ESCALA_ARMA)
imagen_bala = cargar_imagen("assets/images/weapons/bullets/fuego_1.png", cons.ESCALA_BALA)
lista_tile = []
for x in range(cons.TIPOS_TILES):
    tile_image = pg.image.load(f"assets/images/tiles/tile_{x+1}.png").convert_alpha()
    tile_image = pg.transform.scale(tile_image, (cons.TAMANIO_TILES, cons.TAMANIO_TILES))
    lista_tile.append(tile_image)
posion_roja = cargar_imagen("assets/images/items/posion/posion.png", cons.ESCALA_POSION_ROJA)
monedas_imagen = [cargar_imagen(f"assets/images/items/moneda/moneda_frame_{i+1}.png", cons.ESCALA_MONEDA) for i in range(contar_elementos("assets/images/items/moneda"))]
item_imagenes = [monedas_imagen, [posion_roja]]

def dibujar_texto_pantalla(texto, fuente, color, x, y):
    img = fuente.render (texto, True, color)
    ventana.blit(img, (x, y))

def vida_jugador():
    corazon_mitad_dibujado = False
    for i in range(5):
        if jugador.energia >= ((i+1)*20):
            ventana.blit(corazon_lleno, (5+i*50, 5))
        elif jugador.energia % 20 > 0 and not corazon_mitad_dibujado:
            ventana.blit(corazon_medio, (5+i*50, 5))
            corazon_mitad_dibujado = True
        else: 
            ventana.blit(corazon_vacio, (5+i*50, 5))

def leer_csv_nivel(nivel_a_cargar):
    data = []
    with open(f"niveles/nivel_{nivel_a_cargar}.csv", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for fila in reader:
            data.append([int(col) for col in fila])
    return data

def cargar_world_y_enemigos(nivel_a_cargar, tiles, items_img, enemigos_anim):
    world_data_local = leer_csv_nivel(nivel_a_cargar)
    world_local = md.Mundo()
    world_local.procesar_data(world_data_local, tiles, items_img, enemigos_anim)
    return world_local, list(world_local.lista_enemigo)

# --- Carga Inicial del Nivel 1 ---
world_data = leer_csv_nivel(nivel)
world = md.Mundo()
world.procesar_data(world_data, lista_tile, item_imagenes, animacion_enemigos)
jugador = per.Personaje (80, 80, animaciones, 100, 1) # Energía a 100
lista_enemigos = list(world.lista_enemigo)
arma = wp.weapon(imagen_arma, imagen_bala, sonido_disparo)
grupo_damage_text = pg.sprite.Group()
grupo_balas = pg.sprite.Group()
grupo_items = pg.sprite.Group()
for item in world.lista_item:
    grupo_items.add(item)

#variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

#controlar el frame rate
reloj = pg.time.Clock()
run = True
pg.mixer.music.load(MUSICA_MENU)
pg.mixer.music.play(-1)

# NUEVO: Control de tiempo para delays
tiempo_estado_cambiado = 0 # Guardará cuándo se gana o pierde
DELAY_INPUT = 500 # 500 ms de retraso

# ================================================================= #
# =================== BUCLE PRINCIPAL DEL JUEGO =================== #
# ================================================================= #

while run:
    reloj.tick(cons.FPS)

    # -------------------------------------------------
    # 1. GESTIÓN DE EVENTOS (UNIFICADO)
    # -------------------------------------------------
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        # --- EVENTOS DEL MENÚ ---
        if game_state == "MENU":
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if boton_jugar.collidepoint(event.pos):
                    game_state = "JUGANDO"
                    pg.mixer.music.load(MUSICA_JUEGO)
                    pg.mixer.music.play(-1)
                elif boton_salir.collidepoint(event.pos):
                    run = False
        
        # --- EVENTOS DEL JUEGO ---
        elif game_state == "JUGANDO":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w: mover_arriba = True
                if event.key == pg.K_s: mover_abajo = True
                if event.key == pg.K_a: mover_izquierda = True
                if event.key == pg.K_d: mover_derecha = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_w: mover_arriba = False
                if event.key == pg.K_s: mover_abajo = False
                if event.key == pg.K_a: mover_izquierda = False
                if event.key == pg.K_d: mover_derecha = False

        # --- EVENTOS DE GAME OVER ---
        elif game_state == "GAME_OVER":
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Click en botón de reinicio
                if boton_reinicio.collidepoint(event.pos):
                    # --- Reiniciar todo el juego ---
                    nivel = 1
                    world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos)
                    jugador.reset(80, 80, 100)
                    grupo_damage_text.empty()
                    grupo_balas.empty()
                    grupo_items.empty()
                    for item in world.lista_item:
                        grupo_items.add(item)
                    nombre_jugador = ""
                    puntaje_guardado = False
                    input_activo = False
                    game_state = "MENU"
                    pg.mixer.music.load(MUSICA_MENU)
                    pg.mixer.music.play(-1)
                
                # Activar o desactivar el campo de texto
                if input_rect.collidepoint(event.pos):
                    input_activo = True
                else:
                    input_activo = False

            # Input del teclado para el nombre
            if event.type == pg.KEYDOWN and input_activo:
                # AÑADIDO: Solo procesar teclas si ha pasado el delay
                if pg.time.get_ticks() - tiempo_estado_cambiado > DELAY_INPUT:
                    if event.key == pg.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    elif event.key == pg.K_RETURN:
                        if len(nombre_jugador.strip()) == 3 and not puntaje_guardado:
                            try:
                                file_existe = os.path.isfile(SCORES_FILE)
                                with open(SCORES_FILE, "a", newline="", encoding="utf-8") as f:
                                    writer = csv.writer(f)
                                    if not file_existe:
                                        writer.writerow(["nombre", "score"])
                                    writer.writerow([nombre_jugador.strip().upper(), jugador.score])
                                puntaje_guardado = True
                            except Exception as e:
                                print(f"[ERROR score] {e}")
                    elif event.unicode.isalpha() and len(nombre_jugador) < 3:
                        nombre_jugador += event.unicode.upper()

    # -------------------------------------------------
    # 2. ACTUALIZACIÓN DE ESTADOS
    # -------------------------------------------------
    if game_state == "JUGANDO":
        # Movimiento del jugador
        delta_x = cons.VELOCIDAD_PERSONAJE * (mover_derecha - mover_izquierda)
        delta_y = cons.VELOCIDAD_PERSONAJE * (mover_abajo - mover_arriba)
        posicion_pantalla, nivel_completo = jugador.movimiento(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)

        # Actualizar mundo, jugador, enemigos y grupos
        world.update(posicion_pantalla)
        jugador.update()
        for ene in lista_enemigos:
            ene.enemigos(jugador, world.obstaculos_tiles, posicion_pantalla, world.exit_tile)
            ene.update()
        
        # Arma y balas
        bala = arma.update(jugador)
        if bala:
            grupo_balas.add(bala)
        
        for bala in grupo_balas:
            damage, post_damage = bala.update(lista_enemigos, world.obstaculos_tiles)
            if damage:
                damage_text = tx.Damage_text(post_damage.centerx, post_damage.centery, f"-{damage}", font, cons.COLOR_ROJO)
                grupo_damage_text.add(damage_text)
        
        grupo_damage_text.update(posicion_pantalla)
        grupo_items.update(posicion_pantalla, jugador)

        # Eliminar enemigos muertos
        lista_enemigos[:] = [ene for ene in lista_enemigos if ene.energia > 0]

        # Comprobar si el jugador ha muerto
        if not jugador.vivo:
            game_state = "GAME_OVER"
            tiempo_estado_cambiado = pg.time.get_ticks() # Guardar tiempo para el delay
            input_activo = True # Activar input por defecto
            # Detener movimiento residual
            mover_arriba = mover_abajo = mover_izquierda = mover_derecha = False

        # Comprobar si se ha completado el nivel
        if nivel_completo:
            if nivel < cons.NIVEL_MAXIMO:
                nivel += 1
                world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos)
                jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])
                for item in world.lista_item:
                    grupo_items.add(item)
            else: # Ganó el juego
                game_state = "VICTORIA"
                tiempo_estado_cambiado = pg.time.get_ticks()
                pg.mixer.music.stop()

    # -------------------------------------------------
    # 3. DIBUJADO EN PANTALLA
    # -------------------------------------------------
    ventana.fill(cons.COLOR_SUELO)

    if game_state == "MENU":
        pantalla_inicio()

    elif game_state == "JUGANDO":
        world.draw(ventana)
        jugador.dibujar(ventana)
        for ene in lista_enemigos:
            ene.dibujar(ventana)
        arma.dibujar(ventana)
        grupo_balas.draw(ventana)
        vida_jugador()
        grupo_damage_text.draw(ventana)
        dibujar_texto_pantalla(f"SCORE : {jugador.score}", font_score, cons.COLOR_AMARILLO, cons.POSICION_TEXTO_SCORE_X, cons.POSICION_TEXTO_SCORE_Y)
        dibujar_texto_pantalla(f"N I V E L: {nivel}", font, cons.COLOR_BLANCO, cons.ANCHO_VENTANA / 2, 5)
        grupo_items.draw(ventana)

    elif game_state == "GAME_OVER":
        ventana.fill(cons.ROJO_OSCURO)
        text_rect = game_over_text.get_rect(center=(cons.ANCHO_VENTANA/2, cons.ALTO_VENTANA/2))
        ventana.blit(game_over_text, text_rect)
        
        # Botón de reinicio
        boton_reinicio = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 150, 200, 50)
        pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_reinicio)
        ventana.blit(texto_boton_reinicio, (boton_reinicio.x + 50, boton_reinicio.y + 10))
        
        # Campo de texto para el nombre
        ventana.blit(label_nombre, (input_rect.x, input_rect.y - 30))
        pg.draw.rect(ventana, color_activo if input_activo else color_inactivo, input_rect, width=2)
        texto_input = font_input.render(nombre_jugador, True, cons.COLOR_BLANCO)
        ventana.blit(texto_input, (input_rect.x + 10, input_rect.y + 7))

        if puntaje_guardado:
            msg_ok = font_reinicio.render("¡Puntaje guardado!", True, cons.COLOR_BLANCO)
            ventana.blit(msg_ok, (input_rect.x, input_rect.y + 50))

    elif game_state == "VICTORIA":
        ventana.blit(texto_ganaste, rect_ganaste)
        if pg.time.get_ticks() - tiempo_estado_cambiado > 3000: # Después de 3 segundos
            # --- Reiniciar todo para volver al menú ---
            nivel = 1
            world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos)
            jugador.reset(80, 80, 100)
            grupo_damage_text.empty()
            grupo_balas.empty()
            grupo_items.empty()
            for item in world.lista_item:
                grupo_items.add(item)
            game_state = "MENU"
            pg.mixer.music.load(MUSICA_MENU)
            pg.mixer.music.play(-1)

    # Actualizar la pantalla al final de cada ciclo
    pg.display.update()

pg.quit()