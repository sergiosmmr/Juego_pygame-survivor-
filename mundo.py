import pygame as pg
import constantes_varaibles as cons
import items as itm
import personaje as per

obstaculos = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55,]
puertas_cerradas = [36, 37, 66, 67]
class Mundo():
    def __init__(self):
        self.maps_tile = []
        self.obstaculos_tiles = []
        self.exit_tile = None
        self.lista_item = []
        self.lista_enemigo = []
        self.puertas_cerradas_tiles = []

    def procesar_data (self, data, lista_tile, item_imagenes, animacion_enemigos):
        self.level_lenght = len(data)
        for y, row in enumerate (data):
            for x, tile in enumerate(row):
                #print(f"Intentando acceder al índice: {tile} | Tamaño de la lista: {len(lista_tile)}")
                image = lista_tile[tile]
                image_rect = image.get_rect()
                image_x = x * cons.TAMANIO_TILES
                image_y = y * cons.TAMANIO_TILES
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y, tile]

                #agregarr los tiles de obstaculos
                if tile in obstaculos:
                    self.obstaculos_tiles.append(tile_data)
                #tiles de puertas
                if tile in puertas_cerradas:
                    self.obstaculos_tiles.append(tile_data)

                #tile de salida
                elif tile == 84:
                    self.exit_tile = tile_data
                    #crear moneda
                elif tile == 86:
                    moneda = itm.Item(image_x, image_y, 0, item_imagenes[0])
                    self.lista_item.append(moneda)
                    tile_data [0] = lista_tile [22]
                    # crear posiones
                elif tile == 89:
                    posion = itm.Item(image_x, image_y, 1, item_imagenes[1])
                    self.lista_item.append(posion)
                    tile_data [0] = lista_tile [22]
                    #crear sapo
                elif tile == 90:
                    sapo = per.Personaje(image_x, image_y, animacion_enemigos [0], 80, 2)
                    self.lista_enemigo.append(sapo)
                    tile_data [0] = lista_tile [22]
                    #crear mosca
                elif tile == 91:
                    mosca = per.Personaje(image_x, image_y, animacion_enemigos [1], 110, 2)
                    self.lista_enemigo.append(mosca)
                    tile_data [0] = lista_tile [22]
                    # crear dragon
                elif tile == 92:
                    dragon = per.Personaje(image_x, image_y, animacion_enemigos [2], 150, 2)
                    self.lista_enemigo.append(dragon)
                    tile_data [0] = lista_tile [22]

                self.maps_tile.append(tile_data)
        # al final de procesar_data ########################### BORRAR DESPUES DEL DEBUGUEO ##############
        t84 = sum(1 for _,_,_,_,tt in self.maps_tile if tt == 84)
        print(f"[DEBUG mundo] tiles 84 en mapa: {t84}  | exit_tile seteado: {self.exit_tile is not None}")


    def cambiar_puerta (self, jugador, lista_tile):
        buffer = 50
        proximidad_rect = pg.Rect(jugador.forma.x - buffer, jugador.forma.y - buffer, jugador.forma.width + 2 * buffer, jugador.forma.height + 2 * buffer)
        for tile_data in self.maps_tile:
            image, rect, x, y, tile_type = tile_data
            if proximidad_rect.colliderect(rect):
                if tile_type in puertas_cerradas:
                    if tile_type == 36 or tile_type == 66:
                        new_tile_type = 57
                    elif tile_type == 37 or tile_type == 67:
                        new_tile_type = 58

                    tile_data[-1] = new_tile_type
                    tile_data[0] = lista_tile[new_tile_type]

                    #eliminar el tile de las lista de colisiones
                    if tile_data in self.obstaculos_tiles:
                        self.obstaculos_tiles.remove(tile_data)

                    return True
        return False        

    def update(self, posicion_pantalla):
        for tile in self.maps_tile:
            tile [2] += posicion_pantalla[0]
            tile [3] += posicion_pantalla[1]
            tile [1].center = (tile[2], tile[3])
 
    def draw(self, surface):
        for tile in self.maps_tile:
            surface.blit(tile[0], tile[1])
