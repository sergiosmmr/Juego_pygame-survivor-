import pygame as pg
import constantes_varaibles as cons
import items as itm
import personaje as per
import enemigo as ene

# usar sets para consultas O(1)
obstaculos = {0, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50, 51, 52, 53, 54, 55}
puertas_cerradas = {36, 37, 66, 67}

# mapeo de puertas cerradas → abiertas 
PUERTAS_MAP = {
    36: 57,  # tipo A
    66: 57,  # tipo A
    37: 58,  # tipo B
    67: 58,  # tipo B
}

class Mundo():
    def __init__(self):
        self.maps_tile = []
        self.obstaculos_tiles = []
        self.exit_tile = None
        self.lista_item = []
        self.lista_enemigo = []
        self.puertas_cerradas_tiles = []

    def procesar_data(self, data, lista_tile, item_imagenes, animacion_enemigos):
        self.level_lenght = len(data)

        # mapeos 
        ITEM_BY_TILE = {
            86: ("moneda", 0),  # (nombre, índice en item_imagenes)
            89: ("posion", 1),
        }
        ENEMIGO_BY_TILE = {
            #(índice animación, energía, velocidad)
            90: (0,  80, 2),   #  sapo
            91: (1, 110, 2),   # mosca
            92: (2, 150, 2),   # dragon
        }
        TILE_TRANSPARENTE = 22  # tile “vacío” que usás para limpiar donde había un objeto/enemigo

        tile_size = cons.TAMANIO_TILES
        obst_append = self.obstaculos_tiles.append
        mapa_append = self.maps_tile.append
        items_append = self.lista_item.append
        enemigos_append = self.lista_enemigo.append

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = lista_tile[tile]
                image_rect = image.get_rect()
                image_x = x * tile_size
                image_y = y * tile_size
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y, tile]

                # agregar tiles de obstáculo o puerta
                if tile in obstaculos or tile in puertas_cerradas:
                    obst_append(tile_data)

                # tile de salida
                if tile == 84:
                    self.exit_tile = tile_data

                # crear items (moneda o posión)
                elif tile in ITEM_BY_TILE:
                    nombre_item, idx_item = ITEM_BY_TILE[tile]
                    nuevo_item = itm.Item(image_x, image_y, idx_item, item_imagenes[idx_item])
                    items_append(nuevo_item)
                    tile_data[0] = lista_tile[TILE_TRANSPARENTE]

                # crear enemigos
                elif tile in ENEMIGO_BY_TILE:
                    indice_anim, energia, velocidad = ENEMIGO_BY_TILE[tile]
                    nuevo_enemigo = ene.Enemigo(image_x, image_y, animacion_enemigos[indice_anim], energia, velocidad)
                    enemigos_append(nuevo_enemigo)
                    tile_data[0] = lista_tile[TILE_TRANSPARENTE]

                # guardar el tile en el mapa
                mapa_append(tile_data)



    def cambiar_puerta(self, jugador, lista_tile):
        buffer = 50
        # rect de proximidad alrededor del jugador
        proximidad_rect = pg.Rect(
            jugador.forma.x - buffer,
            jugador.forma.y - buffer,
            jugador.forma.width + 2 * buffer,
            jugador.forma.height + 2 * buffer
        )

        for tile_data in self.maps_tile:
            imagen_tile, rect_tile, pos_x_tile, pos_y_tile, tipo_tile = tile_data

            # si no está cerca, seguí con el próximo
            if not proximidad_rect.colliderect(rect_tile):
                continue

            # si es una puerta cerrada, la mapeamos a su tile "abierta"
            if tipo_tile in puertas_cerradas:
                nuevo_tipo_puerta = PUERTAS_MAP.get(tipo_tile)
                if nuevo_tipo_puerta is None:
                    continue  # seguridad por si falta algo en el mapeo

                # actualizar tipo y sprite del tile
                tile_data[-1] = nuevo_tipo_puerta
                tile_data[0] = lista_tile[nuevo_tipo_puerta]

                # sacar este tile de la lista de colisiones si estaba (ya no bloquea)
                if tile_data in self.obstaculos_tiles:
                    self.obstaculos_tiles.remove(tile_data)

                return True

        return False
    
    def update(self, posicion_pantalla):
        for tile in self.maps_tile:
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.maps_tile:
            surface.blit(tile[0], tile[1])

