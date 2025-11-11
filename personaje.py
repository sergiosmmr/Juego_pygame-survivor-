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
    def __init__(self, x, y, animaciones_dict, energia, tipo):
        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        # --- Logica de Animacion a ---
        self.animaciones = animaciones_dict
        # estado inicial
        self.estado = "idle"
        self.accion_actual = self.animaciones[self.estado]# Lista de frames de "idle"
        #imagen de la animacion que se muestra
        self.frame_index = 0
        #se almacena la hora actual desde que se inicio pygame en milisegundos
        self.update_time = pg.time.get_ticks()
        self.cooldown_animacion = 100
        self.image = self.accion_actual[self.frame_index]# imagen inicial

        # crea el rectangulo para el personaje
        self.forma = self.image.get_rect()
        # posiciona el centro del rectángulo en las coordenadas (x, y)
        self.forma.center = (x, y)
        self.tipo = tipo

        #logica de golpe
        self.golpe = False
        self.ultimo_golpe = pg.time.get_ticks()
        self.golpe_cooldown = 500

    def actualizar_coordenadas (self, tupla):
        self.forma.center = (tupla[0], tupla[1])
        

    def movimiento (self, delta_x, delta_y, osbtaculos_tile, exit_tile):
        # --- logica de Estado (idle/run) ---
        if delta_x != 0 or delta_y != 0:
            self.set_accion("run")
        else:
            # Si está quieto, poné el estado "idle"
            self.set_accion("idle")
        # ----------------------------------
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
        
    def set_accion(self, nueva_accion):
        """
        Función helper para cambiar de estado ("idle" a "run")
        de forma segura, reiniciando la animación.
        """
        # si ya estamos en esta accion, no hacer nada
        if self.estado == nueva_accion:
            return
        
        # cambiar a la nueva accioon
        self.estado = nueva_accion
        # obtener la nueva lista de frames
        self.accion_actual = self.animaciones[self.estado]
        self.frame_index = 0 # reiniciar el frame para la nueva animacion
        self.update_time = pg.time.get_ticks() # reeinicia el timer

    def update(self): 
        # ---  logica de vida y cooldown de golpe ---
        #comprobar si el personaje ha muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False
        # timer para poder volver a recibir daño
        if self.tipo == 1:
            if self.golpe == True:
                if pg.time.get_ticks() - self.ultimo_golpe > self.golpe_cooldown:
                    self.golpe = False

        # ---  loogica de animacion  ---
        # revisa el timer
        if pg.time.get_ticks() - self.update_time >= self.cooldown_animacion:
            self.frame_index += 1 # avanza el frame
            self.update_time = pg.time.get_ticks()

        # si se paso del final, vuelve al principio
        if self.frame_index >= len(self.accion_actual):
            self.frame_index = 0

        # asigna la imagen correcta del frame actual
        self.image = self.accion_actual[self.frame_index]

    def dibujar (self, interfaz):
        # voltea la imagen si 'self.flip' es True
        imagen_flip = pg.transform.flip (self.image, self.flip, False)
        # dibuja la imagen (volteada o no)
        interfaz.blit(imagen_flip, self.forma)
        