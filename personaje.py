import pygame as pg
import constantes_varaibles as cons
import math


class Personaje():
    """
    representa un personaje dentro del juego.

    atributos
    ----------
    forma : pygame.Rect
        el rectángulo que define la posición y el área de colisión
        del personaje en la pantalla.
    """
    def __init__(self, x, y, animaciones, energia, tipo):
        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        #imagen de la animacion que se muestra
        self.frame_index = 1
        #se almacena la hora actual desde que se inicio pygame en milisegundos
        self.update_time = pg.time.get_ticks()
        self.image = animaciones[self.frame_index]
        # crea el rectángulo para el personaje
        self.forma = self.image.get_rect()
        # posiciona el centro del rectángulo en las coordenadas (x, y)
        self.forma.center = (x, y)
        self.tipo = tipo

    def movimiento (self, delta_x, delta_y, osbtaculos_tile):
        posicion_pantalla = [0, 0]
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
 
        self.forma.x = self.forma.x + delta_x

        for obstacle in osbtaculos_tile:
            if obstacle[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obstacle[1].left
                if delta_x < 0:
                    self.forma.left = obstacle[1].right

        self.forma.y = self.forma.y + delta_y
        
        for obstacle in osbtaculos_tile:
            if obstacle[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obstacle[1].top
                if delta_y < 0:
                    self.forma.top = obstacle[1].bottom

        #logica, solo aplica al jugador y no a los enemisgos
        if self.tipo == 1:
            #actualiza la pantalla segun estado del jugador
            #mover pantalla izquierda o derecha
            if self.forma.right > (cons. ANCHO_VENTANA - cons.LIMITES_PANTALLA):
                posicion_pantalla [0] = (cons.ANCHO_VENTANA - cons.LIMITES_PANTALLA) - self.forma.right
                self.forma.right = cons.ANCHO_VENTANA - cons.LIMITES_PANTALLA

            if self.forma.left < cons.LIMITES_PANTALLA:
                posicion_pantalla [0] = cons.LIMITES_PANTALLA - self.forma.left
                self.forma.left = cons.LIMITES_PANTALLA

            #mover pantalla arriba y bajo
            if self.forma.bottom > (cons. ALTO_VENTANA - cons.LIMITES_PANTALLA):
                posicion_pantalla [1] = (cons.ALTO_VENTANA - cons.LIMITES_PANTALLA) - self.forma.bottom
                self.forma.bottom = cons.ALTO_VENTANA - cons.LIMITES_PANTALLA

            if self.forma.top < cons.LIMITES_PANTALLA:
                posicion_pantalla [1] = cons.LIMITES_PANTALLA - self.forma.top
                self.forma.top = cons.LIMITES_PANTALLA
            return posicion_pantalla

    def enemigos(self, jugador, obstaculos_tiles, posicion_pantalla):
        clipped_line = ()
        ene_dx = 0
        ene_dy = 0

        # reposicion de enemigos con el movimiento de pantalla o camara
        self.forma.x += posicion_pantalla[0]            
        self.forma.y += posicion_pantalla[1]   

        # crear una linea de vision
        linea_de_vision = ((self.forma.centerx, self.forma.centery), (jugador.forma.centerx, jugador.forma.centery))

        # chequear si hay obstaculos en la linea de vision de enemigo
        for obs in obstaculos_tiles:
            if obs[1].clipline(linea_de_vision):
                clipped_line = obs[1].clipline(linea_de_vision) 

        # distancia con el jugador
        distancia =  math.sqrt(((self.forma.centerx - jugador.forma.centerx)**2) + ((self.forma.centery - jugador.forma.centery)**2))
        if not clipped_line and distancia < cons.RANGO:
                
            if self.forma.centerx > jugador.forma.centerx:
                ene_dx = -cons.VELOCIDAD_ENEMIGOS
            if self.forma.centerx < jugador.forma.centerx:
                ene_dx = cons.VELOCIDAD_ENEMIGOS
            if self.forma.centery > jugador.forma.centery:
                ene_dy = -cons.VELOCIDAD_ENEMIGOS
            if self.forma.centery < jugador.forma.centery:
                ene_dy = cons.VELOCIDAD_ENEMIGOS
            

        self.movimiento(ene_dx, ene_dy, obstaculos_tiles)

    def update(self): 
        #comprobar si el personaje ha muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False
           
        cooldown_animacion = 100
        self.image = self.animaciones[self.frame_index]   
        if pg.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def dibujar (self, interfaz):
        imagen_flip = pg.transform.flip (self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        #dibuja el personaje en la superficie especificada
        #pg.draw.rect(interfaz, cons.COLOR_AMARILLO, self.forma, width=1)