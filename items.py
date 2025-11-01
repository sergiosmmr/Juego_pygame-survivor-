import pygame as pg
import pygame.sprite
import constantes_varaibles as cons

class Item(pg.sprite.Sprite):
    def __init__(self, x, y, item_type, animacion_list):
        super().__init__()
        self.item_type = item_type
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()
        self.image = self.animacion_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self, posicion_pantalla, personaje):
        # reposicionar los items segun la pantalla o camara
        self.rect.x += posicion_pantalla[0]
        self.rect.y += posicion_pantalla[1]
        #comprobar colision entre el personaje y los items
        if self.rect.colliderect(personaje.forma):
            #si son monedas
            if self.item_type == 0:
                personaje.score += 100
            #si son posiciones
            elif self.item_type == 1:
                personaje.energia += 50
                if personaje.energia > 100:
                     personaje.energia = 100
            self.kill()
            
        cooldown_animacion = cons.COOLDOWN_MONEDA
        self.image = self.animacion_list[self.frame_index]

        if pg.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        if self.frame_index >= len(self.animacion_list):
            self.frame_index = 0
        