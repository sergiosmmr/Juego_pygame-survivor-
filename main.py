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

# === MÚSICA ===
pg.mixer.music.set_volume(cons.MUSICA_VOLUMEN_NORMAL)  # volumen medio

# Cargar el sonido del disparo ---
sonido_disparo = pg.mixer.Sound(cons.SONIDO_DISPARO)  
sonido_disparo.set_volume(cons.SONIDO_DISPARO_NORMAL)  # Ajusto el volumen 

##### FUENTES ######
font = pg.font.Font("assets/font/Ryga.ttf", cons.TAMANIO_FUENTE_ENEMIGOS)
font_score = pg.font.Font("assets/font/Ryga.ttf", cons.TAMANIO_FUENTE_SCORE)

font_game_over = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 110)
font_reinicio = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 30)

font_inicio = pg.font.Font("assets/font/Halloweenpixels.ttf", 30)
font_titulo = pg.font.Font("assets/font/Halloweenpixels.ttf", 100)

game_over_text = font_game_over.render("GAME OVER", True, cons.COLOR_BLANCO)
texto_boton_reinicio = font_reinicio.render("Reiniciar", True, cons.COLOR_NEGRO)

texto_boton_salir_final = font_reinicio.render("Salir", True, cons.COLOR_BLANCO)

#  Variables para ingreso de nombre 
font_input = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 28)
label_nombre = font_input.render("Ingresá tus iniciales (3) y presiona ENTER:", True, cons.COLOR_BLANCO)

input_rect = pg.Rect(cons.ANCHO_VENTANA//2 - 80, cons.ALTO_VENTANA//2 + 100, 160, 40)
color_inactivo = (cons.COLOR_NEGRO)
color_activo = (cons.COLOR_BLANCO)

SCORES_FILE = "scores.csv"   # Archivo donde se guardará

# AÑADIDO: Variables de estado para el input 
mensaje_fin_juego = "GAME OVER" # Cambiará a "¡GANASTE!" si ganas
font_fin_juego = font_game_over # Para usar la fuente grande o la de título
input_activo = False
nombre_jugador = ""
puntaje_guardado = False
t_fin_juego = 0 # Temporizador para el delay

# pantalla de victoria 
texto_ganaste = font_titulo.render("¡GANASTE!", True, cons.COLOR_BLANCO)
rect_ganaste = texto_ganaste.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2))


# botones de inicio
boton_jugar = pg.Rect(cons.ANCHO_VENTANA/2 -100, cons.ALTO_VENTANA/2 +15, 200, 50)
boton_menu = pg.Rect(cons.ANCHO_VENTANA/2 -100, cons.ALTO_VENTANA/2 +75, 200, 50)
boton_salir = pg.Rect(cons.ANCHO_VENTANA/2 -100, cons.ALTO_VENTANA/2 +135, 200, 50)
texto_boton_jugar = font_inicio.render("JUGAR", True, cons.COLOR_NEGRO)# cambiar fuente, no se lee bien
texto_boton_menu = font_inicio.render("MENU", True, cons.COLOR_NEGRO)# cambiar fuente, no se lee bien
texto_boton_salir = font_inicio.render("SALIR", True, cons.COLOR_BLANCO)# cambiar fuente, no se lee bien

# pantalla de inicio
def pantalla_inicio():

    ventana.blit(imagen_fondo_inicio, (0, 0))

    # Creo el texto y obtengo su ancho
    texto_titulo_str = "S U R V I V O R"
    texto_surface = font_titulo.render(texto_titulo_str, True, cons.ROJO_OSCURO)
    ancho_texto = texto_surface.get_width()

    #  centrada
    x_centrada = (cons.ANCHO_VENTANA // 2) - (ancho_texto // 2)
    
    # Dibujamos el texto en la x centrada
    ventana.blit(texto_surface, (x_centrada, cons.ALTO_VENTANA/2 - 200))
    pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_jugar)
    pg.draw.rect(ventana, cons.COLOR_ROJO, boton_salir)
    pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_menu)
    ventana.blit(texto_boton_jugar, (boton_jugar.x + 50, boton_jugar.y + 10))
    ventana.blit(texto_boton_salir, (boton_salir.x + 50, boton_salir.y + 10))
    ventana.blit(texto_boton_menu, (boton_menu.x + 50, boton_menu.y + 10))
    pg.display.update()

##############importar imagenes#############

# Cargar y escalar imagen de fondo al tamaño de la ventana

imagen_fondo_inicio = pg.image.load("assets/images/fondos_de_pantalla/fondo_inicio.webp").convert()
imagen_fondo_inicio = pg.transform.scale(imagen_fondo_inicio, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))

imagen_fondo_victoria = pg.image.load("assets/images/fondos_de_pantalla/imagen_fondo_victoria.png").convert()
imagen_fondo_victoria = pg.transform.scale(imagen_fondo_victoria, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))

imagen_fondo_derrota = pg.image.load("assets/images/fondos_de_pantalla/imagen_fondo_derrota.png").convert()
imagen_fondo_derrota = pg.transform.scale(imagen_fondo_derrota, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))

# energia
corazon_vacio = cargar_imagen("assets/images/items/corazon_vacio_1.png", cons.ESCALA_CORAZONES)
corazon_medio = cargar_imagen("assets/images/items/corazon_mitad_1.png", cons.ESCALA_CORAZONES)
corazon_lleno = cargar_imagen("assets/images/items/corazon_lleno_1.png", cons.ESCALA_CORAZONES)

#personaje
animaciones = []
for i in range(7):
    img = cargar_imagen(f"assets/images/characters/players/necro_mov_{i+1}.png", cons.ESCALA_PERSONAJE)
    animaciones.append(img)

directorio_enemigos = ("assets/images/characters/enemigos") 
tipo_enemigos = nombre_carpetas(directorio_enemigos)

# realizamos la animacion del enemigo
animacion_enemigos = []
for eni in tipo_enemigos:
    lista_temporal = []
    ruta_temporal = f"assets/images/characters/enemigos/{eni}" 
    
    # 1. Obtenemos la lista de nombres de archivo REALES
    nombres_de_archivos = nombre_carpetas(ruta_temporal)
    
    # 2. Los ordenamos para que la animación (0, 1, 2, 3...) sea correcta
    nombres_de_archivos.sort()

    # 3. Iteramos sobre los nombres reales, no sobre un rango
    for nombre_archivo in nombres_de_archivos:
        # Construimos la ruta completa al archivo
        ruta_completa = f"{ruta_temporal}/{nombre_archivo}"
        
        # Cargamos la imagen usando esa ruta
        imagen_enemigo = cargar_imagen(ruta_completa, cons.ESCALA_ENEMIGOS)
        lista_temporal.append(imagen_enemigo)
    
    animacion_enemigos.append(lista_temporal)

#armas
imagen_arma = cargar_imagen("assets/images/weapons/vacio.png", cons.ESCALA_ARMA)

#balas
imagen_bala = cargar_imagen("assets/images/weapons/bullets/fuego_1.png", cons.ESCALA_BALA)

#cargar imagenes del mundo
lista_tile = []
for x in range(cons.TIPOS_TILES):
    tile_image = pg.image.load(f"assets/images/tiles/tile_{x+1}.png").convert_alpha()
    tile_image = pg.transform.scale(tile_image, (int(cons.TAMANIO_TILES), int(cons.TAMANIO_TILES)))
    lista_tile.append(tile_image)

#cargar imagen de los items
posion_roja = cargar_imagen("assets/images/items/posion/posion.png", cons.ESCALA_POSION_ROJA)


monedas_imagen = []
ruta_imagen = "assets/images/items/moneda"
numero_monedas_imagen = contar_elementos(ruta_imagen)
for i in range(numero_monedas_imagen):
    img = cargar_imagen(f"assets/images/items/moneda/moneda_frame_{i+1}.png", cons.ESCALA_MONEDA)
    monedas_imagen.append(img)

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

def resetear_mundo():
    grupo_damage_text.empty()
    grupo_balas.empty()
    grupo_items.empty()
    # crear una lista de tile vacias
    data = []
    for filas in range (cons.FILAS):
        filas = [2] * cons.COLUMNAS
        data.append(filas)
    return data

# funciones de nivel / mundo  
def leer_csv_nivel(nivel):
    # lee el CSV del nivel y devuelve la matriz world_data
    data = [[7] * cons.COLUMNAS for _ in range(cons.FILAS)]
    with open(f"niveles/nivel_{nivel}.csv", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for x, fila in enumerate(reader):
            for y, columna in enumerate(fila):
                data[x][y] = int(columna)
    return data

def cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos):
    # crea world + lista_enemigos sin tocar grupos (grupo_items se maneja afuera)
    world_data_local = leer_csv_nivel(nivel)
    world_local = md.Mundo()
    world_local.procesar_data(world_data_local, lista_tile, item_imagenes, animacion_enemigos)

    lista_enemigos_local = []
    for ene in world_local.lista_enemigo:
        lista_enemigos_local.append(ene)

    return world_local, lista_enemigos_local


world_data = []

for fila in range(cons.FILAS):
    filas = [7] * cons.COLUMNAS
    world_data.append(filas)

#cargar el archivo con nivel
with open("niveles/nivel_1.csv", newline="") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data [x] [y] = int(columna)
world = md.Mundo()
world.procesar_data(world_data, lista_tile, item_imagenes, animacion_enemigos) 

# def dibujar_grid():
#     for x in range(50):
#         pg.draw.line(ventana, cons.COLOR_BLANCO, (x*cons.TAMANIO_TILES, 0), (x*cons.TAMANIO_TILES, cons.ALTO_VENTANA))
#         pg.draw.line(ventana, cons.COLOR_BLANCO, (0, x*cons.TAMANIO_TILES), (cons.ANCHO_VENTANA, x*cons.TAMANIO_TILES))


#crear un jugador de la clase personaje en posicion x , y
jugador = per.Personaje (80, 80, animaciones, 80, 1)

#crear una lista de enemigos
lista_enemigos = []
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)

#crear un arma de la clase weapon centrada en jugador
arma = wp.weapon(imagen_arma, imagen_bala, sonido_disparo)

#crear un grupo de sprites
grupo_damage_text = pg.sprite.Group()
grupo_balas = pg.sprite.Group()
grupo_items = pg.sprite.Group()

#añadir items de la data de world
for item in world.lista_item:
    grupo_items.add(item)



#variables de movimiento del jugador

mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

#conrolar el frame rate
reloj = pg.time.Clock()
prueba = True
run = True
mostrar_inicio = True
evitar_click_fantasma = False

# estado de victoria
mostrar_ganaste = False
t_inicio_ganaste = 0

while run:
        # pantalla de victoria (3 segundos y volver al menú) 
    if mostrar_ganaste:
        ventana.fill(cons.COLOR_SUELO)
        ventana.blit(texto_ganaste, rect_ganaste)
        pg.display.update()

        # tras 3s, reset y volver al inicio
        if pg.time.get_ticks() - t_inicio_ganaste >= 3000:
            # resetear estado básico
            jugador.vivo = True
            jugador.energia = 100
            jugador.score = 0
            nivel = 1

            # limpiar grupos
            grupo_damage_text.empty()
            grupo_balas.empty()
            grupo_items.empty()

            # recargar nivel 1
            world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos)
            jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])
            for item in world.lista_item:
                grupo_items.add(item)

            # volver a pantalla de inicio
            mostrar_ganaste = False
            mostrar_inicio = True

        continue  # saltar el resto del frame mientras está la pantalla de victoria

    if mostrar_inicio:
        pantalla_inicio()
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(cons.MUSICA_MENU)
            pg.mixer.music.play(-1)  # -1 = loop infinito

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    pg.mixer.music.load(cons.MUSICA_JUEGO)
                    pg.mixer.music.play(-1)

                    mostrar_inicio = False
                    evitar_click_fantasma = True
                    ############################# arreglar que el clicks se borre y no dispare al iniciar el juego#######
                if boton_salir.collidepoint(event.pos):
                    run = False

    else:
            
        #que valla a 60 fps
        reloj.tick(cons.FPS)


        ventana.fill(cons.COLOR_SUELO)

        if jugador.vivo:



            #calcular movimiento del jugador
            delta_x = 0
            delta_y = 0

            if mover_derecha == True:
                delta_x = cons.VELOCIDAD_PERSONAJE
            if mover_izquierda == True:
                delta_x = -cons.VELOCIDAD_PERSONAJE
            if mover_abajo == True:
                delta_y = cons.VELOCIDAD_PERSONAJE
            if mover_arriba == True:
                delta_y = -cons.VELOCIDAD_PERSONAJE

                #mover al jugador
            posicion_pantalla, nivel_completo = jugador.movimiento(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)

            # actualiza el mapa
            world.update(posicion_pantalla)

            #actualiza estado de jugador
            jugador.update()

            #actualiza estado de enemigo
            for ene in lista_enemigos:
                ene.update()
        
            
            #actualiza el esatdo del arma
            bala = None
            
            # Revisamos la bandera (tu "retardo")
            if evitar_click_fantasma:
                # Si está activa, la consumimos y no hacemos nada.
                # El click se ignora este frame.
                if not pg.mouse.get_pressed()[0]:
                    evitar_click_fantasma = False
            else:
                # Si la bandera está inactiva, actualizamos el arma normalmente.
                bala = arma.update(jugador)

            if bala:
                grupo_balas.add(bala)
            for bala in grupo_balas:
                damage, post_damage = bala.update(lista_enemigos, world.obstaculos_tiles)    
                if damage:
                    damage_text = tx.Damage_text(post_damage.centerx, post_damage.centery, "-" + str(damage), font, cons.COLOR_ROJO)
                    grupo_damage_text.add(damage_text)



            # actualizar el daño
            grupo_damage_text.update(posicion_pantalla)

            #actualizar items
            grupo_items.update(posicion_pantalla, jugador)

            #dibujar mundo
            world.draw(ventana)
        
            #dibujar al jugador
            jugador.dibujar(ventana)
        
            #dibujar al enemigo

            for ene in lista_enemigos.copy():  # iterar sobre copia para poder eliminar
                if ene.energia <= 0:
                    lista_enemigos.remove(ene)
                    continue  #  no seguir procesando/dibujando este enemigo eliminado

                # update IA / colisiones / etc
                ene.enemigos(jugador, world.obstaculos_tiles, posicion_pantalla, world.exit_tile)
                # dibujar sprite
                ene.dibujar(ventana)

            #dibujar el arma
            arma.dibujar(ventana)

            #dibujar balas
            for bala in grupo_balas:
                bala.dibujar(ventana)

            #dibujar corazones
            vida_jugador()

            #dibujar textos
            grupo_damage_text.draw(ventana)
            dibujar_texto_pantalla(f"SCORE : {jugador.score}", font_score, cons.COLOR_AMARILLO, cons.POSICION_TEXTO_SCORE_X, cons.POSICION_TEXTO_SCORE_Y)

            # nivel
            dibujar_texto_pantalla(f"N I V E L: " + str(nivel), font, cons.COLOR_BLANCO, cons.ANCHO_VENTANA / 2, 5)

            #dibujar items
            grupo_items.draw(ventana)

            # chuequear si el nivel esta completo
            if nivel_completo:
                if nivel < cons.NIVEL_MAXIMO:
                    nivel += 1
                    # cargar mundo y enemigos con función
                    world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos)
                    # reposicionar jugador según config
                    jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])
                    # refrescar items del mundo (como ya hacías)
                    for item in world.lista_item:
                        grupo_items.add(item)
                else:
                    # detener música del juego al ganar
                    if pg.mixer.music.get_busy():
                        pg.mixer.music.stop()

                    # Preparamos la pantalla de ingreso ---
                    mensaje_fin_juego = "¡GANASTE!"
                    font_fin_juego = font_titulo # Usamos la fuente de título
                    
                    jugador.vivo = False # Usamos la misma pantalla de "muerto"
                    t_fin_juego = pg.time.get_ticks() # Inicia el timer
                    pg.event.clear() # Limpia teclas 

        # LÓGICA DE FIN DE JUEGO (SI NO ESTÁ VIVO)
        else:
            # --- LÓGICA DE FIN DE JUEGO (GAME OVER O VICTORIA) ---
            
            # 1. Iniciar temporizador 
            if t_fin_juego == 0:
                t_fin_juego = pg.time.get_ticks()
                pg.event.clear() # Limpia teclas 
                if pg.mixer.music.get_busy(): # Parar música
                    pg.mixer.music.stop()

            # 2. Dibujar fondo y título (GAME OVER o ¡GANASTE!)
            if mensaje_fin_juego == "¡GANASTE!":
                ventana.blit(imagen_fondo_victoria, (0, 0))
            else: # Será "GAME OVER"
                ventana.blit(imagen_fondo_derrota, (0, 0))
            texto_renderizado = font_fin_juego.render(mensaje_fin_juego, True, cons.COLOR_BLANCO)
            text_rect = texto_renderizado.get_rect(center = (cons.ANCHO_VENTANA/2, cons.ALTO_VENTANA/2 - 100))
            ventana.blit(texto_renderizado, text_rect)

            # 3. Activar el input SÓLO después de 1 segundo de delay
            if not input_activo and (pg.time.get_ticks() - t_fin_juego > 1000): # 1000ms = 1 seg
                input_activo = True

            # 4. Dibujar el input de nombre
            # Label
            x_label = input_rect.centerx - (label_nombre.get_width() // 2)
            ventana.blit(label_nombre, (x_label, input_rect.y - 30))
            
            # Campo de texto (color cambia si está activo o no)
            if input_activo:
                color_caja = color_activo
            else:
                color_caja = color_inactivo
            pg.draw.rect(ventana, color_caja, input_rect, width=2)
            texto_input = font_input.render(nombre_jugador, True, cons.COLOR_BLANCO)
            ventana.blit(texto_input, (input_rect.x + 10, input_rect.y + 7))

            # 5. Feedback de guardado Y MOSTRAR BOTONES
            if puntaje_guardado:
                msg_ok = font_input.render("¡Puntaje guardado!", True, cons.COLOR_BLANCO)
                x_texto_guardado = input_rect.centerx - (msg_ok.get_width() // 2)
                ventana.blit(msg_ok, (x_texto_guardado, input_rect.y + 45))

                # 6. Botón de reinicio 
                boton_reinicio = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 200, 200, 50)
                pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_reinicio)
                ventana.blit(texto_boton_reinicio, (boton_reinicio.x + 50, boton_reinicio.y + 10))

                # Botón de Salir (Final)
                boton_salir_final = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 260, 200, 50)
                pg.draw.rect(ventana, cons.COLOR_ROJO, boton_salir_final) # Rojo, como en el inicio
                ventana.blit(texto_boton_salir_final, (boton_salir_final.x + 50, boton_salir_final.y + 10))
            
        #  BUCLE DE EVENTOS  ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # --- LÓGICA DE TECLADO (KEYDOWN) ---
            if event.type == pg.KEYDOWN:

                if jugador.vivo:
                    if event.key == pg.K_w:
                        mover_arriba = True
                    elif event.key == pg.K_s:
                        mover_abajo = True
                    elif event.key == pg.K_d:
                        mover_derecha = True
                    elif event.key == pg.K_a:
                        mover_izquierda = True
                    elif event.key == pg.K_e:
                        if world.cambiar_puerta(jugador, lista_tile):
                            print("puerta cambiada")
                else:
                # --- Eventos de INPUT (solo si está muerto/ganó y el input está activo) ---
                    if input_activo:
                        if event.key == pg.K_BACKSPACE:
                            nombre_jugador = nombre_jugador[:-1]
                    
                        elif event.key == pg.K_RETURN:
                            # Guardar puntaje si tiene 3 letras y no se guardó
                            if len(nombre_jugador.strip()) == 3 and not puntaje_guardado:
                                try:
                                    file_existe = os.path.isfile(SCORES_FILE)
                                    with open(SCORES_FILE, "a", newline="", encoding="utf-8") as f:
                                        writer = csv.writer(f)
                                        if not file_existe:
                                            writer.writerow(["nombre", "score"]) # Encabezado
                                        writer.writerow([nombre_jugador.strip().upper(), jugador.score])
                                    puntaje_guardado = True
                                except Exception as e:
                                    print("[ERROR guardando score]", e)

                        # Añadir letra (solo si es alfa, < 3 letras y no guardó)
                        elif event.unicode.isalpha() and len(nombre_jugador) < 3 and not puntaje_guardado:
                            nombre_jugador += event.unicode.upper()

            # LÓGICA DE TECLA LEVANTADA (KEYUP) 
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    mover_arriba = False
                elif event.key == pg.K_s:
                    mover_abajo = False
                elif event.key == pg.K_d:
                    mover_derecha = False
                elif event.key == pg.K_a:
                    mover_izquierda = False

            # LÓGICA DE CLICKS (MOUSEBUTTONDOWN) 
            if event.type == pg.MOUSEBUTTONDOWN:
                if not jugador.vivo:
                    if puntaje_guardado:
                        # 1. Click en el botón REINICIAR
                        if boton_reinicio.collidepoint(event.pos):
                            # resetear estado del jugador
                            jugador.vivo = True
                            jugador.energia = 100
                            jugador.score = 0
                            nivel = 1
                        

                            # --- AÑADIDO: Resetear variables de input ---
                            input_activo = False
                            nombre_jugador = ""
                            puntaje_guardado = False
                            t_fin_juego = 0
                            mensaje_fin_juego = "GAME OVER" # Resetea el título
                            font_fin_juego = font_game_over # Resetea la fuente
                            
                            # Limpiar grupos
                            grupo_damage_text.empty()
                            grupo_balas.empty()
                            grupo_items.empty()

                            # recargar mundo y enemigos
                            world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos)
                            # reposicionar jugador
                            jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])
                            # agregar items
                            for item in world.lista_item:
                                grupo_items.add(item)
                            
                            # Reiniciar música
                            pg.mixer.music.load(cons.MUSICA_JUEGO)
                            pg.mixer.music.play(-1)
                        # 1b. Click en el botón SALIR (Final)
                        elif boton_salir_final.collidepoint(event.pos):
                            run = False
                    else:

                        # 2. Click en la CAJA de input
                        if input_rect.collidepoint(event.pos):
                            if pg.time.get_ticks() - t_fin_juego > 1000: # Solo activa si pasó el delay
                                input_activo = True
                        
                        # 3. Click FUERA de la caja
                        else:
                            input_activo = False


        pg.display.update()

pg.quit()


