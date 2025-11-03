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
    nueva_imagen = pg.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

# funcion para contar elementos
def contar_elementos (directorio):
    return len (os.listdir(directorio)) 

#funcion listar elementos
def nombre_carpetas(directorio):
    return os.listdir(directorio)



pg.init()

ventana = pg.display.set_mode((cons.ANCHO_VENTANA, cons.ALTO_VENTANA))
pg. display.set_caption(cons.NOMBRE_JUEGO)

### variables ####
posicion_pantalla = [0, 0]
nivel = 1

##### FUENTES ######
font = pg.font.Font("assets/font/Ryga.ttf", cons.TAMANIO_FUENTE_ENEMIGOS)
font_score = pg.font.Font("assets/font/Ryga.ttf", cons.TAMANIO_FUENTE_SCORE)
font_game_over = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 110)
font_reinicio = pg.font.Font("assets/font/Colorfiction - Gothic - Regular.otf", 30)

game_over_text = font_game_over.render("GAME OVER", True, cons.COLOR_BLANCO)
texto_boton_reinicio = font_reinicio.render("Reiniciar", True, cons.COLOR_NEGRO)

##############importar imagenes#############

# energia
corazon_vacio = pg.image.load("assets/images/items/corazon_vacio_1.png")
corazon_vacio = escalar_img(corazon_vacio, cons.ESCALA_CORAZONES)
corazon_medio = pg.image.load("assets/images/items/corazon_mitad_1.png")
corazon_medio = escalar_img(corazon_medio, cons.ESCALA_CORAZONES)
corazon_lleno = pg.image.load("assets/images/items/corazon_lleno_1.png")
corazon_lleno = escalar_img(corazon_lleno, cons.ESCALA_CORAZONES)

#personaje
animaciones = []
for i in range(7):
    img = pg.image.load(f"assets/images/characters/players/necro_mov_{i+1}.png")
    img = escalar_img(img, cons.ESCALA_PERSONAJE)
    animaciones.append(img)

directorio_enemigos = ("assets/images/characters/enemigos") 
tipo_enemigos = nombre_carpetas(directorio_enemigos)

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
        imagen_enemigo = pg.image.load(ruta_completa)
        imagen_enemigo = escalar_img(imagen_enemigo, cons.ESCALA_ENEMIGOS)
        lista_temporal.append(imagen_enemigo)
    
    animacion_enemigos.append(lista_temporal)

#armas
imagen_arma = pg.image.load(f"assets/images/weapons/vacio.png")
imagen_arma = escalar_img(imagen_arma, cons.ESCALA_ARMA)

#balas
imagen_bala = pg.image.load(f"assets/images/weapons/bullets/fuego_1.png")
imagen_bala = escalar_img(imagen_bala, cons.ESCALA_BALA)

#cargar imagenes del mundo
lista_tile = []
for x in range(cons.TIPOS_TILES):
    tile_image = pg.image.load(f"assets/images/tiles/tile_{x+1}.png")
    tile_image = pg.transform.scale(tile_image, (cons.TAMANIO_TILES, cons.TAMANIO_TILES))
    lista_tile.append(tile_image)

#cargar imagen de los items
posion_roja = pg.image.load("assets/images/items/posion/posion.png")
posion_roja = escalar_img(posion_roja, cons.ESCALA_POSION_ROJA)

monedas_imagen = []
ruta_imagen = "assets/images/items/moneda"
numero_monedas_imagen = contar_elementos(ruta_imagen)
for i in range (numero_monedas_imagen):
    img = pg.image.load(f"assets/images/items/moneda/moneda_frame_{i+1}.png")
    img = escalar_img(img, cons.ESCALA_MONEDA)
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
    for fila in range (cons.FILAS):
        filas = [2] * cons.COLUMNAS
        data.append(filas)
    return data

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

def dibujar_grid():
    for x in range(50):
        pg.draw.line(ventana, cons.COLOR_BLANCO, (x*cons.TAMANIO_TILES, 0), (x*cons.TAMANIO_TILES, cons.ALTO_VENTANA))
        pg.draw.line(ventana, cons.COLOR_BLANCO, (0, x*cons.TAMANIO_TILES), (cons.ANCHO_VENTANA, x*cons.TAMANIO_TILES))


#crear un jugador de la clase personaje en posicion x , y
jugador = per.Personaje (80, 80, animaciones, 80, 1)

#crear una lista de enemigos
lista_enemigos = []
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)

#crear un arma de la clase weapon centrada en jugador
arma = wp.weapon(imagen_arma, imagen_bala)

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


while run:

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

    for ene in lista_enemigos:
        if ene.energia <= 0:
            lista_enemigos.remove(ene)
        else:
            ene.enemigos(jugador, world.obstaculos_tiles, posicion_pantalla, world.exit_tile)
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
            world_data = resetear_mundo()
            
            #cargar el archivo con nivel
            with open(f"niveles/nivel_{nivel}.csv", newline="") as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for x, fila in enumerate(reader):
                    for y, columna in enumerate(fila):
                        world_data [x] [y] = int(columna)
            world = md.Mundo()
            world.procesar_data(world_data, lista_tile, item_imagenes, animacion_enemigos) 
            jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])
            #crear una lista de enemigos######################### tratar de hacer una funcion, mejorar##############
            lista_enemigos = []
            for ene in world.lista_enemigo:
                lista_enemigos.append(ene)
            #añadir items de la data de world ######################### tratar de hacer una funcion, mejorar##############
            for item in world.lista_item:
                grupo_items.add(item)

    if not jugador.vivo:
        ventana.fill(cons.ROJO_OSCURO)
        text_rect = game_over_text.get_rect(center = (cons.ANCHO_VENTANA/2, cons.ALTO_VENTANA/2))

        ventana.blit(game_over_text, text_rect)
        # boton de reinicio
        boton_reinicio = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 150, 200, 50)
        pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_reinicio)
        ventana.blit(texto_boton_reinicio, (boton_reinicio.x + 50, boton_reinicio.y + 10))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
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

        #cuando la tecla se suelta
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                mover_arriba = False
            elif event.key == pg.K_s:
                mover_abajo = False
            elif event.key == pg.K_d:
                mover_derecha = False
            elif event.key == pg.K_a:
                mover_izquierda = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if boton_reinicio.collidepoint(event.pos) and not jugador.vivo:
                #################################### optimizar con funcion ####################################
                jugador.vivo = True
                jugador.energia = 100
                jugador.score = 0
                nivel = 1
                world_data = resetear_mundo()
                    #cargar el archivo con nivel
                with open(f"niveles/nivel_{nivel}.csv", newline="") as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    for x, fila in enumerate(reader):
                        for y, columna in enumerate(fila):
                                world_data [x] [y] = int(columna)
                world = md.Mundo()
                world.procesar_data(world_data, lista_tile, item_imagenes, animacion_enemigos) 
                jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])

                  #añadir items de la data de world ################# tratar de hacer una funcion, mejorar##############
                for item in world.lista_item:
                    grupo_items.add(item)
                #crear una lista de enemigos################### tratar de hacer una funcion, mejorar##############
                lista_enemigos = []
                for ene in world.lista_enemigo:
                    lista_enemigos.append(ene)
                



        
        


    pg.display.update()

pg.quit()


