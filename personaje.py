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
    def __init__(self, x, y):
        # crea el rectángulo para el personaje
        self.forma = pg.Rect(0, 0, cons.ALTO_PERSONAJE, cons.ANCHO_PERSONAJE)
        # posiciona el centro del rectángulo en las coordenadas (x, y)
        self.forma.center = (x, y)

    def movimiento (self, delta_x, delta_y):
        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y

    def dibujar (self, interfaz):
        #dibuja el personaje en la superficie especificada
        pg.draw.rect(interfaz, cons.COLOR_AMARILLO, self.forma)