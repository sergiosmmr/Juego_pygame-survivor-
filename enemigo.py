import pygame as pg
import constantes_varaibles as cons
import math

class Enemigo(pg.sprite.Sprite):
    """
    Representa un enemigo en el juego.
    """
    def __init__(self, x, y, animaciones_dict, base_energia, base_velocidad, base_dano, tipo_ia, multiplicador, puntaje_base, tile_id):
        pg.sprite.Sprite.__init__(self) # inicializa la clase Sprite
        
        # --- stats  ---
        self.energia = int(base_energia * multiplicador)
        self.vivo = True
        self.velocidad = base_velocidad * multiplicador
        self.dano = int(base_dano * multiplicador)
        self.tipo_ia = tipo_ia
        self.score_value = int(puntaje_base * multiplicador)
        
        # --- animacin ---
        self.flip = False
        self.animaciones = animaciones_dict
        self.estado = "idle" # estado inicial
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.cooldown_animacion = 100
        self.tile_id = tile_id

        # --- logica de carga ---
        if "idle" in self.animaciones:
            self.accion_actual = self.animaciones["idle"]
        elif "run" in self.animaciones:
            self.accion_actual = self.animaciones["run"]
            self.estado = "run" # el estado por defecto ahora es "run"
        else:
            # Si no hay 'idle' NI 'run', usa la PRIMERA animación que encuentre
            # (ej. "walk")
            self.accion_actual = list(self.animaciones.values())[0]
            self.estado = list(self.animaciones.keys())[0]

        self.image = self.accion_actual[self.frame_index]
        # --------------------------------------------------
        
        # --- rectangulos ---
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        
        # --- variables de IA y ataque ---
        self.cooldown_ataque = 1000 
        self.ultimo_ataque = pg.time.get_ticks() - self.cooldown_ataque
        
        
        # --- variables solo para "patrulla" ---
        self.contador_movimiento = 0
        self.direccion_patrulla = 1

    def set_accion(self, nueva_accion):
        """
        Función de ayuda para cambiar de estado (idle a run)
        de forma segura, reiniciando la animación.
        """
        if self.estado == nueva_accion:
            return
        
        # si la nueva accion no existe (sin idle o run), no hacer nada
        if nueva_accion not in self.animaciones:
            return

        self.estado = nueva_accion
        self.accion_actual = self.animaciones[self.estado]
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

    def update(self): 
        """
        Actualiza el estado (vida y animación) del enemigo cada frame.
        """
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False
            
        # --- logica de animacion ---
        # revisa el timer
        if pg.time.get_ticks() - self.update_time >= self.cooldown_animacion:
            self.frame_index += 1 # avanza el frame
            self.update_time = pg.time.get_ticks()
            
            # si se paso del final, vuelve al principio
            if self.frame_index >= len(self.accion_actual):
                self.frame_index = 0
        
        # asigna la imagen correcta del frame actual
        self.image = self.accion_actual[self.frame_index]


    def movimiento_enemigo(self, delta_x, delta_y, osbtaculos_tile):
        """
        Maneja el movimiento y colisiones BÁSICAS del enemigo.
        (Es una copia de 'Personaje.movimiento' pero sin cámara ni 'exit_tile')
        """
        # --- Lógica de Flip (corregida para enemigos) ---
        if delta_x < 0:
            self.flip = False # Mover a la izquierda (sprite original)
        if delta_x > 0:
            self.flip = True # Mover a la derecha (voltear sprite)
        # -----------------------------------------------

        self.forma.x = self.forma.x + delta_x
        # Colisión en X
        for obstacle in osbtaculos_tile:
            # Asegúrate de que 'obstacle' es una lista/tupla (como [imagen, rect])
            if obstacle[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obstacle[1].left
                if delta_x < 0:
                    self.forma.left = obstacle[1].right

        self.forma.y = self.forma.y + delta_y
        # Colisión en Y
        for obstacle in osbtaculos_tile:
            if obstacle[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obstacle[1].top
                if delta_y < 0:
                    self.forma.top = obstacle[1].bottom

    def ia(self, jugador, obstaculos_tiles, posicion_pantalla):
        ene_dx = 0
        ene_dy = 0

        # 1. Reposicion de enemigos con el movimiento de pantalla
        self.forma.x += posicion_pantalla[0]
        self.forma.y += posicion_pantalla[1] 

        # --- mover el calculo de distancia ---
        # (Ahora se calcula SIEMPRE, para todas las IAs)
        distancia = math.sqrt(((self.forma.centerx - jugador.forma.centerx)**2) + ((self.forma.centery - jugador.forma.centery)**2))

        # 2. Lógica de Movimiento (según el tipo de IA)
        if self.tipo_ia == "persecucion":
            clipped_line = ()
            linea_de_vision = ((self.forma.centerx, self.forma.centery), (jugador.forma.centerx, jugador.forma.centery))
            for obs in obstaculos_tiles:
                if obs[1].clipline(linea_de_vision):
                    clipped_line = obs[1].clipline(linea_de_vision) 

            if not clipped_line and distancia < cons.RANGO_PERSECUCION:
                # Calcula la dirección del movimiento
                if self.forma.centerx > jugador.forma.centerx:
                    ene_dx = -self.velocidad
                if self.forma.centerx < jugador.forma.centerx:
                    ene_dx = self.velocidad
                if self.forma.centery > jugador.forma.centery:
                    ene_dy = -self.velocidad
                if self.forma.centery < jugador.forma.centery:
                    ene_dy = self.velocidad                
                    
                self.set_accion("run") 
            else:
                self.set_accion("idle")
        
        elif self.tipo_ia == "patrulla":
            self.set_accion("run") # <-- CAMBIO: Pone estado "run"
            
            ene_dx = self.velocidad * self.direccion_patrulla
            self.contador_movimiento += 1
            
            if self.contador_movimiento > 100:
                self.direccion_patrulla *= -1 
                self.contador_movimiento = 0
                
        # 3. Aplicar Movimiento
        self.movimiento_enemigo(ene_dx, ene_dy, obstaculos_tiles)

        # --- CORRECCIÓN 2: Volver a la lógica de ataque por distancia ---
        if distancia < cons.RANGO_ATAQUE and jugador.golpe == False:
            if pg.time.get_ticks() - self.ultimo_ataque > self.cooldown_ataque:
                jugador.energia -= self.dano 
                jugador.golpe = True
                jugador.ultimo_TAQUE = pg.time.get_ticks()
                self.ultimo_ataque = pg.time.get_ticks()

    def dibujar (self, interfaz):
        """ Dibuja el enemigo en la pantalla. """
        imagen_flip = pg.transform.flip (self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.forma)