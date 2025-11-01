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


##### FUENTES ######
font = pg.font.Font("assets/font/Ryga.ttf", cons.TAMANIO_FUENTE_ENEMIGOS)
font_score = pg.font.Font("assets/font/Ryga.ttf", cons.TAMANIO_FUENTE_SCORE)

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

def dibujar_texto_pantalla(texto, fuente, color, x, y):
    img = fuente.render (texto, True, color)
    ventana.blit(img, (x, y))

def vida_jugador():
    corazon_mitad_dibujado = False
    for i in range(5):
        if jugador.energia >= ((i+1)*20):
            ventana.blit(corazon_lleno, (5+i*50, 5))
        elif jugador.energia % 20 >= 0 and not corazon_mitad_dibujado:
            ventana.blit(corazon_medio, (5+i*50, 5))
            corazon_mitad_dibujado = True
        else: 
            ventana.blit(corazon_vacio, (5+i*50, 5))

world_data = []

for fila in range(cons.FILAS):
    filas = [7] * cons.COLUMNAS
    world_data.append(filas)

#cargar el archivo con nivel
with open("niveles/nivel_prueba_1.csv", newline="") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for y, fila in enumerate(reader):
        for x, tile in enumerate(fila):
            world_data [y] [x] = int(tile)


world = md.Mundo()
world.procesar_data(world_data, lista_tile)

def dibujar_grid():
    for x in range(50):
        pg.draw.line(ventana, cons.COLOR_BLANCO, (x*cons.TAMANIO_TILES, 0), (x*cons.TAMANIO_TILES, cons.ALTO_VENTANA))
        pg.draw.line(ventana, cons.COLOR_BLANCO, (0, x*cons.TAMANIO_TILES), (cons.ANCHO_VENTANA, x*cons.TAMANIO_TILES))


#crear un jugador de la clase personaje en posicion x , y
jugador = per.Personaje (550, 450, animaciones, 80, 1)

#crear un enemigo de la clase personaje
alien = per.Personaje(400, 300, animacion_enemigos[0], 100, 2)
dragon = per.Personaje(200, 400, animacion_enemigos[1], 100, 2)
rana = per.Personaje(900, 600, animacion_enemigos[2], 100, 2)
rana2 = per.Personaje(500, 300, animacion_enemigos[2], 100, 2)
dragon2 = per.Personaje(800, 400, animacion_enemigos[1], 100, 2)

#crear una lista de enemigos
lista_enemigos = []
lista_enemigos.append(alien)
lista_enemigos.append(dragon)
lista_enemigos.append(rana)
lista_enemigos.append(rana2)
lista_enemigos.append(dragon2)

#crear un arma de la clase weapon centrada en jugador
arma = wp.weapon(imagen_arma, imagen_bala)

#crear un grupo de sprites
grupo_damage_text = pg.sprite.Group()
grupo_balas = pg.sprite.Group()
grupo_items = pg.sprite.Group()

moneda = ts.Item(380, 60, 0, monedas_imagen)
posion = ts.Item(650, 155, 1, [posion_roja])

grupo_items.add(moneda)
grupo_items.add(posion)

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


    ventana.fill(cons.COLOR_DE_FONDO)

    dibujar_grid()

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
    posicion_pantalla = jugador.movimiento(delta_x, delta_y)

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
        damage, post_damage = bala.update(lista_enemigos)    
        if damage:
            damage_text = tx.Damage_text(post_damage.centerx, post_damage.centery, str(damage), font, cons.COLOR_ROJO)
            grupo_damage_text.add(damage_text)

    # actualizar el daño
    grupo_damage_text.update()

    #actualizar items
    grupo_items.update(posicion_pantalla, jugador)

    #dibujar mundo
    world.draw(ventana)
    

    #dibujar al jugador
    jugador.dibujar(ventana)

    #dibujar al enemigo
    for ene in lista_enemigos:
        ene.enemigos(posicion_pantalla)
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

    #dibujar items
    grupo_items.draw(ventana)

    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                mover_arriba = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                mover_abajo = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                mover_derecha = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                mover_izquierda = True

        #cuando la tecla se suelta
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                mover_arriba = False
            if event.key == pg.K_s:
                mover_abajo = False
            if event.key == pg.K_d:
                mover_derecha = False
            if event.key == pg.K_a:
                mover_izquierda = False

        
        


    pg.display.update()

pg.quit()


