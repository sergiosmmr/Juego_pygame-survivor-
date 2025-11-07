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
        self.golpe = False
        self.ultimo_golpe = pg.time.get_ticks()
        self.golpe_cooldown = 1000 
        self.cooldown_animacion = 100

    def actualizar_coordenadas (self, tupla):
        self.forma.center = (tupla[0], tupla[1])
        

    def movimiento (self, delta_x, delta_y, osbtaculos_tile, exit_tile):
        posicion_pantalla = [0, 0]
        nivel_completo = False
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
            if exit_tile[1].colliderect(self.forma):   
                nivel_completo = True

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
            return posicion_pantalla, nivel_completo

    def update(self): 
        #comprobar si el personaje ha muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False
        # timer para poder volver a recibir daño
        if self.tipo == 1:
            if self.golpe == True:
                if pg.time.get_ticks() - self.ultimo_golpe > self.golpe_cooldown:
                    self.golpe = False
                    
        self.image = self.animaciones[self.frame_index]   
        if pg.time.get_ticks() - self.update_time >= self.cooldown_animacion:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def dibujar (self, interfaz):
        imagen_flip = pg.transform.flip (self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)
        