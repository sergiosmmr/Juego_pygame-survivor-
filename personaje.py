import pygame as pg
import constantes_varaibles as cons


class Personaje():
    """
    representa un personaje dentro del juego.

    atributos
    ----------
    forma : pygame.Rect
        el rectángulo que define la posición y el área de colisión
        del personaje en la pantalla.
    """
    def __init__(self, x, y, animaciones):
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

    def movimiento (self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y

    def update(self): 
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