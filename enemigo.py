import pygame as pg
import constantes_varaibles as cons
import math

class Enemigo(pg.sprite.Sprite):
    """
    Representa un enemigo en el juego.
    """
    def __init__(self, x, y, animaciones, energia, velocidad):
        pg.sprite.Sprite.__init__(self) # Inicializa la clase Sprite
        
        self.velocidad = velocidad
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0 # Es más seguro empezar en 0 que en 1
        self.update_time = pg.time.get_ticks()
        self.image = self.animaciones[self.frame_index]
        
        # Crear rectángulos
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        
        # Variables de animación (copiadas de tu Personaje)
        self.cooldown_animacion = 100

        # Variables de IA y ataque
        self.ultimo_ataque = 0
        self.cooldown_ataque = 1000 # El 'golpe_cooldown' del jugador

    def update(self): 
        """
        Actualiza el estado (vida y animación) del enemigo cada frame.
        """
        # Comprobar si el enemigo ha muerto
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False
            
        # Lógica de animación (idéntica a la de Personaje)
        self.image = self.animaciones[self.frame_index]
        if pg.time.get_ticks() - self.update_time >= self.cooldown_animacion:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def movimiento_enemigo(self, delta_x, delta_y, osbtaculos_tile):
        """
        Maneja el movimiento y colisiones BÁSICAS del enemigo.
        (Es una copia de 'Personaje.movimiento' pero sin cámara ni 'exit_tile')
        """
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

    def ia(self, jugador, obstaculos_tiles, posicion_pantalla, exit_tile):
        """
        La lógica de "Inteligencia Artificial" (IA) del enemigo.
        (Este es tu método 'enemigos()' movido aquí).
        """
        clipped_line = ()
        ene_dx = 0
        ene_dy = 0

        # 1. Reposicion de enemigos con el movimiento de pantalla
        self.forma.x += posicion_pantalla[0] 
        self.forma.y += posicion_pantalla[1]  

        # 2. Persecución (Línea de visión y distancia)
        linea_de_vision = ((self.forma.centerx, self.forma.centery), (jugador.forma.centerx, jugador.forma.centery))
        for obs in obstaculos_tiles:
            if obs[1].clipline(linea_de_vision):
                clipped_line = obs[1].clipline(linea_de_vision) 

        distancia = math.sqrt(((self.forma.centerx - jugador.forma.centerx)**2) + ((self.forma.centery - jugador.forma.centery)**2))
        
        if not clipped_line and distancia < cons.RANGO_PERSECUCION:
            if self.forma.centerx > jugador.forma.centerx:
                ene_dx = -cons.VELOCIDAD_ENEMIGOS
            if self.forma.centerx < jugador.forma.centerx:
                ene_dx = cons.VELOCIDAD_ENEMIGOS
            if self.forma.centery > jugador.forma.centery:
                ene_dy = -cons.VELOCIDAD_ENEMIGOS
            if self.forma.centery < jugador.forma.centery:
                ene_dy = cons.VELOCIDAD_ENEMIGOS
                
        # 3. Moverse (Llama a su propio método de movimiento)
        self.movimiento_enemigo(ene_dx, ene_dy, obstaculos_tiles)

        # 4. Atacar al jugador (con su propio cooldown de ataque)
        if distancia < cons.RANGO_ATAQUE and jugador.golpe == False:
            if pg.time.get_ticks() - self.ultimo_ataque > self.cooldown_ataque:
                jugador.energia -= 10
                jugador.golpe = True
                jugador.ultimo_golpe = pg.time.get_ticks()
                self.ultimo_ataque = pg.time.get_ticks() # Resetea su propio timer

    def dibujar (self, interfaz):
        """ Dibuja el enemigo en la pantalla. """
        imagen_flip = pg.transform.flip (self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)