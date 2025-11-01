import pygame as pg
import constantes_varaibles as cons


class Mundo():
    def __init__(self):
        self.maps_tile = []

    def procesar_data (self, data, lista_tile):
        self.level_lenght = len(data)
        for y, row in enumerate (data):
            for x, tile in enumerate(row):
                #print(f"Intentando acceder al índice: {tile} | Tamaño de la lista: {len(lista_tile)}")
                image = lista_tile[tile]
                image_rect = image.get_rect()
                image_x = x * cons.TAMANIO_TILES
                image_y = y * cons.TAMANIO_TILES
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]
                self.maps_tile.append(tile_data)

    def update(self, posicion_pantalla):
        for tile in self.maps_tile:
            tile [2] += posicion_pantalla[0]
            tile [3] += posicion_pantalla[1]
            tile [1].center = (tile[2], tile[3])
 
    def draw(self, surface):
        for tile in self.maps_tile:
            surface.blit(tile[0], tile[1])
