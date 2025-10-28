import pygame as pg
import constantes_varaibles as cons
import personaje as per

pg.init()

ventana = pg.display.set_mode((cons.ANCHO_VENTANA, cons.ALTO_VENTANA))
pg. display.set_caption(cons.NOMBRE_JUEGO)

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pg.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen
animaciones = []
for i in range(7):
    img = pg.image.load(f"assets/images/characters/players/necro_mov_{i+1}.png")
    img = escalar_img(img, cons.ESCALA_PERSONAJE)
    animaciones.append(img)

#posicion del jugador
jugador = per.Personaje (550, 450, animaciones)



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
    jugador.movimiento(delta_x, delta_y)

    jugador.update()
    
    
    jugador.dibujar(ventana)

    
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


