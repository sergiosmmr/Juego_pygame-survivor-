import pygame as pg
import pygame.sprite 


class Damage_text(pg.sprite.Sprite):
    def __init__(self, x, y, damage, font, color):
        super().__init__()
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.contador = 0

    def update(self, posicion_pantalla):
        # reposicion de texto en pantalla del daño
        self.rect.x += posicion_pantalla[0]            
        self.rect.y += posicion_pantalla[1]     

        self.rect.y -= 2
        self.contador += 1
        if self.contador > 30:
            self.kill()