import pygame as pg
import constantes_varaibles as cons
import math
import random



class weapon():
    def __init__(self, image, imagen_bala,sonido_disparo):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pg.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.disparada = False
        self.sonido_disparo = sonido_disparo
        self.ultimo_disparo = pg.time.get_ticks()

    def update(self, personaje):
        disparo_cooldown = cons.COOLDOWN_BALAS
        bala = None
        self.forma.center = personaje.forma.center
        if not personaje.flip:
            self.forma.x += 0 #personaje.forma.width/10 (en caso de querer correr el arma)
            self.forma.y += -3 #-personaje.forma.width/10 (en caso de querer correr el arma en eje y)
            self.rotar_arma(False)
        else:
            self.forma.x -= 0 #personaje.forma.width/10 (en caso de querer correr el arma)
            self.forma.y -= 0 #-personaje.forma.width/10 (en caso de querer correr el arma en eje y)
            self.rotar_arma(True)

        #mover arma con el mouse
        mouse_pos = pg.mouse.get_pos()
        diferencia_x = mouse_pos[0] - self.forma.centerx
        diferencia_y = - (mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(diferencia_y, diferencia_x))

        #detectar los clicks del mouse
        if pg.mouse.get_pressed()[0] and not self.disparada and (pg.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown):
            bala = Bullets(self.imagen_bala,self.forma.centerx, self.forma.centery, self.angulo)
            self.sonido_disparo.play()
            self.disparada = True
            self.ultimo_disparo = pg.time.get_ticks()
        #resetear los clicks del mouse
        if not pg.mouse.get_pressed()[0]:
            self.disparada = False

        return bala 


    def rotar_arma(self, rotar):
        if rotar:
            imagen_flip = pg.transform.flip(self.imagen_original, True, False)
            self.imagen = pg.transform.rotate(imagen_flip, self.angulo)
            
        else:
            imagen_flip = pg.transform.flip(self.imagen_original, False, False)
            self.imagen = pg.transform.rotate(imagen_flip, self.angulo)


    def dibujar(self, interfaz):
        self.imagen = pg.transform.rotate(self.imagen, self.angulo)
        interfaz.blit(self.imagen, self.forma)
        #pg.draw.rect(interfaz, cons.COLOR_ARMA, self.forma, width=1)

    
class Bullets (pg.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pg.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pg.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

       #calcular velocidad de balas 
        self.delta_x = math.cos(math.radians(self.angulo))*cons.VELOCIDAD_BALAS
        self.delta_y = - math.sin(math.radians(self.angulo))*cons.VELOCIDAD_BALAS    

    def update(self, lista_enemigos, obstaculos_tiles):

        danio = 0
        pos_danio = None
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        #ver si las balas salieron de pantalla para optimizar y borrar
        if self.rect.right < 0 or self.rect.left > cons.ANCHO_VENTANA or self.rect.bottom < 0 or self.rect.top > cons.ALTO_VENTANA:
            self.kill()

        #verificar si hay colicion con enemigos
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                danio = 15 + random.randint(-7, 7)
                pos_danio = enemigo.forma
                enemigo.energia -= danio
                self.kill()
                break
        #verificar si hay colicion con enemigos
        for obs in obstaculos_tiles:
            if obs[1].colliderect(self.rect):
                self.kill()
                break    
    
        return danio, pos_danio

    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery))
