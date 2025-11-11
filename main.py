import pygame as pg
import constantes_varaibles as cons
import personaje as per
import weapon as wp
import os
import texto as tx
import items as ts
import mundo as md
import csv
import enemigo as ene
import utils 
pg.init()
pg.mixer.init()

ventana = pg.display.set_mode((cons.ANCHO_VENTANA, cons.ALTO_VENTANA))
pg. display.set_caption(cons.NOMBRE_JUEGO)

### variables ####
posicion_pantalla = [0, 0]
nivel = 1
multiplicador_dificultad = 1.0

# === MÚSICA ===
pg.mixer.music.set_volume(cons.MUSICA_VOLUMEN_NORMAL)  # volumen medio

# Cargar el sonido del disparo ---
sonido_disparo = pg.mixer.Sound(cons.SONIDO_DISPARO)  
sonido_disparo.set_volume(cons.SONIDO_DISPARO_NORMAL)  # Ajusto el volumen 


#######################  FUNCIONES  #######################

# pantalla de inicio
def pantalla_inicio():

    ventana.blit(imagen_fondo_inicio, (0, 0))

    # Creo el texto y obtengo su ancho
    texto_titulo_str = "S U R V I V O R"
    offset_sombra = 4
    y_pos_titulo = cons.ALTO_VENTANA/2 - 200 # Posición Y del texto

    # 1. Renderizar y posicionar la SOMBRA (NEGRA)
    sombra_surf = font_titulo.render(texto_titulo_str, True, cons.COLOR_NEGRO)
    ancho_sombra = sombra_surf.get_width()
    x_sombra = (cons.ANCHO_VENTANA // 2) - (ancho_sombra // 2)
    sombra_rect = sombra_surf.get_rect(topleft=(x_sombra + offset_sombra, y_pos_titulo + offset_sombra))

    # 2. Renderizar y posicionar el TEXTO PRINCIPAL (ROJO OSCURO)
    texto_surf = font_titulo.render(texto_titulo_str, True, cons.ROJO_OSCURO)
    ancho_texto = texto_surf.get_width()
    x_texto = (cons.ANCHO_VENTANA // 2) - (ancho_texto // 2)
    texto_rect = texto_surf.get_rect(topleft=(x_texto, y_pos_titulo))

    # 3. Dibujar (Sombra primero, luego Texto)
    ventana.blit(sombra_surf, sombra_rect)
    ventana.blit(texto_surf, texto_rect)

    # --- Botones (Texto Centrado) ---
    pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_jugar)
    rect_texto_jugar = texto_boton_jugar.get_rect(center=boton_jugar.center)
    ventana.blit(texto_boton_jugar, rect_texto_jugar)

    pg.draw.rect(ventana, cons.COLOR_ROJO, boton_salir)
    rect_texto_salir = texto_boton_salir.get_rect(center=boton_salir.center)
    ventana.blit(texto_boton_salir, rect_texto_salir)

    pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_menu)
    rect_texto_menu = texto_boton_menu.get_rect(center=boton_menu.center)
    ventana.blit(texto_boton_menu, rect_texto_menu
                 )
    pg.display.update()

def pantalla_menu():
    # 1. Dibujar el fondo
    ventana.blit(imagen_fondo_menu, (0, 0))

    # 2. Dibujar el título "MENU"
    ventana.blit(texto_titulo_menu, rect_titulo_menu)

    # 3. Dibujar botones del menú y centrar el texto
    
    # Botón DIFICULTAD
    pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_dificultad)
    rect_texto_dif = texto_boton_dificultad.get_rect(center=boton_dificultad.center)
    ventana.blit(texto_boton_dificultad, rect_texto_dif)

    # Botón RANKING
    pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_ranking)
    rect_texto_ranking = texto_boton_ranking.get_rect(center=boton_ranking.center)
    ventana.blit(texto_boton_ranking, rect_texto_ranking)

    # Botón VOLUMEN
    pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_volumen)
    rect_texto_vol = texto_boton_volumen.get_rect(center=boton_volumen.center)
    ventana.blit(texto_boton_volumen, rect_texto_vol)

    # Botón CONTROLES
    pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_controles)
    rect_texto_controles = texto_boton_controles.get_rect(center=boton_controles.center)
    ventana.blit(texto_boton_controles, rect_texto_controles)

    # Botón VOLVER (sigue en rojo)
    pg.draw.rect(ventana, cons.COLOR_ROJO, boton_volver) 
    rect_texto_volver = texto_boton_volver.get_rect(center=boton_volver.center)
    ventana.blit(texto_boton_volver, rect_texto_volver)

    # 4. Dibujar botones de volumen (SI ESTÁN ACTIVOS)
    if mostrar_opciones_volumen:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_vol_bajo)
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_vol_norm)
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_vol_fuerte)

        # Centrar texto "B", "N", "F"
        rect_vol_b = texto_vol_bajo.get_rect(center=boton_vol_bajo.center)
        ventana.blit(texto_vol_bajo, rect_vol_b)
        
        rect_vol_n = texto_vol_norm.get_rect(center=boton_vol_norm.center)
        ventana.blit(texto_vol_norm, rect_vol_n)
        
        rect_vol_f = texto_vol_fuerte.get_rect(center=boton_vol_fuerte.center)
        ventana.blit(texto_vol_fuerte, rect_vol_f)

    if mostrar_opciones_dificultad:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_dif_facil)
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_dif_norm)
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_dif_fuerte)
        
        # usamos los textos "Facil", "Normal", "Dificl"
        rect_dif_f = texto_dif_facil.get_rect(center=boton_dif_facil.center)
        ventana.blit(texto_dif_facil, rect_dif_f)
        
        rect_dif_n = texto_dif_norm.get_rect(center=boton_dif_norm.center)
        ventana.blit(texto_dif_norm, rect_dif_n)
        
        rect_dif_fu = texto_dif_fuerte.get_rect(center=boton_dif_fuerte.center)
        ventana.blit(texto_dif_fuerte, rect_dif_fu)

    # 5. Actualizar la pantalla
    pg.display.update()

def pantalla_ranking():
    # 1. Dibujar el fondo
    ventana.blit(imagen_fondo_menu, (0, 0)) # Reutiliza el fondo del menú

    # 2. Dibujar el título "RANKING"
    ventana.blit(texto_titulo_ranking, rect_titulo_ranking)

    # 3. Cargar y dibujar los puntajes
    scores = cargar_scores()
    base_y = (cons.ALTO_VENTANA // 2) - 150
    
    if not scores:
        # Mensaje si no hay puntajes
        no_scores_text = font_reinicio.render("No hay puntajes guardados", True, cons.COLOR_BLANCO)
        no_scores_rect = no_scores_text.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 - 20))
        ventana.blit(no_scores_text, no_scores_rect)
    else:
        # Dibujar encabezados
        header_name = font_reinicio.render("NOMBRE", True, cons.COLOR_AMARILLO)
        header_score = font_reinicio.render("PUNTAJE", True, cons.COLOR_AMARILLO)
        ventana.blit(header_name, (cons.ANCHO_VENTANA // 2 - 150, base_y))
        ventana.blit(header_score, (cons.ANCHO_VENTANA // 2 + 50, base_y))

        # Dibujar cada puntaje
        y_offset = 40
        for i, (nombre, score) in enumerate(scores):
            # Posición Y para esta fila
            y_pos = base_y + y_offset
            
            # Dibuja el Nombre
            score_name = font_reinicio.render(f"{i+1}. {nombre}", True, cons.COLOR_BLANCO)
            ventana.blit(score_name, (cons.ANCHO_VENTANA // 2 - 150, y_pos))
            
            # Dibuja el Puntaje
            score_val = font_reinicio.render(str(score), True, cons.COLOR_BLANCO)
            ventana.blit(score_val, (cons.ANCHO_VENTANA // 2 + 50, y_pos))
            
            y_offset += 40 # Aumenta el espacio para la siguiente fila

    # 4. Dibujar el botón "VOLVER" (Reutilizado del menú)
    pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_volver)
    rect_texto_volver = texto_boton_volver.get_rect(center=boton_volver.center)
    ventana.blit(texto_boton_volver, rect_texto_volver)

    # 5. Actualizar la pantalla
    pg.display.update()

def pantalla_controles():
    ventana.blit(imagen_fondo_menu, (0, 0)) # Reutiliza fondo
    ventana.blit(texto_titulo_controles, rect_titulo_controles) # Título

    # Dibujar los textos de ayuda (centrados)
    rect_texto_1 = texto_controles_1.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 - 50))
    rect_texto_2 = texto_controles_2.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2))
    rect_texto_3 = texto_controles_3.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 + 50))
    
    ventana.blit(texto_controles_1, rect_texto_1)
    ventana.blit(texto_controles_2, rect_texto_2)
    ventana.blit(texto_controles_3, rect_texto_3)
    
    # Reutiliza el botón VOLVER
    pg.draw.rect(ventana, cons.COLOR_ROJO, boton_volver)
    rect_texto_volver = texto_boton_volver.get_rect(center=boton_volver.center)
    ventana.blit(texto_boton_volver, rect_texto_volver)

    pg.display.update()

def pantalla_briefing():
    # 1. Dibujar el fondo (reutilizamos el del menú)
    ventana.blit(imagen_fondo_menu, (0, 0))

    # 2. Dibujar el título "SOBREVIVE"
    ventana.blit(texto_titulo_briefing, rect_titulo_briefing)

    # 3. Dibujar los textos de la historia (centrados)
    rect_historia_1 = texto_historia_1.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 - 150))
    rect_historia_2 = texto_historia_2.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 - 110))
    ventana.blit(texto_historia_1, rect_historia_1)
    ventana.blit(texto_historia_2, rect_historia_2)
    
    # 4. Dibujar los textos de controles (reutilizados)
    rect_texto_1 = texto_controles_1.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2))
    rect_texto_2 = texto_controles_2.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 + 40))
    rect_texto_3 = texto_controles_3.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 + 80))
    ventana.blit(texto_controles_1, rect_texto_1)
    ventana.blit(texto_controles_2, rect_texto_2)
    ventana.blit(texto_controles_3, rect_texto_3)
    
    # 5. Dibujar el botón "COMENZAR"
    pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_comenzar)
    rect_texto_comenzar = texto_boton_comenzar.get_rect(center=boton_comenzar.center)
    ventana.blit(texto_boton_comenzar, rect_texto_comenzar)

    # 6. Actualizar la pantalla
    pg.display.update()

def pantalla_selec_personaje():
    # Ya no necesitamos 'global', porque 'sets_anim_jugadores'
    # es una variable global que podemos leer y modificar (siendo una lista).
    
    ventana.fill(cons.COLOR_NEGRO) 
    ventana.blit(texto_titulo_personaje, rect_titulo_personaje)

    # 3. Dibujar y animar los 3 personajes
    botones_personaje = [boton_selec_p1, boton_selec_p2, boton_selec_p3]

    # Iteramos sobre la lista 'sets_anim_jugadores' directamente
    for i, anim_dict in enumerate(sets_anim_jugadores):
        
        # Leemos el estado actual
        frame_index = anim_dict["frame_index"]
        update_time = anim_dict["update_time"]
        cooldown = anim_dict["cooldown"]

        # 3.1. Actualizar la animación de IDLE
        if "idle" in anim_dict:
            current_idle_anim = anim_dict["idle"]
            
            if pg.time.get_ticks() - update_time >= cooldown:
                frame_index += 1
                update_time = pg.time.get_ticks()
                if frame_index >= len(current_idle_anim):
                    frame_index = 0
            
            # Guardamos el estado actualizado EN LA LISTA ORIGINAL
            anim_dict["frame_index"] = frame_index
            anim_dict["update_time"] = update_time

            # 3.2. Dibujar el sprite actual de IDLE
            sprite_actual = current_idle_anim[frame_index]
            rect_sprite = sprite_actual.get_rect(center=botones_personaje[i].center)
            ventana.blit(sprite_actual, rect_sprite)
        
        elif "run" in anim_dict:
            # Fallback para personajes sin 'idle' (dragon)
            sprite_actual = anim_dict["run"][0]
            rect_sprite = sprite_actual.get_rect(center=botones_personaje[i].center)
            ventana.blit(sprite_actual, rect_sprite)

    # 4. Dibujar un recuadro de selección
    if personaje_seleccionado_idx == 0:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_selec_p1, 4)
    elif personaje_seleccionado_idx == 1:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_selec_p2, 4)
    elif personaje_seleccionado_idx == 2:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_selec_p3, 4)

    # 5. Dibujar el botón "Siguiente"
    pg.draw.rect(ventana, cons.COLOR_AMARILLO, boton_comenzar)
    rect_texto_siguiente = texto_boton_siguiente.get_rect(center=boton_comenzar.center)
    ventana.blit(texto_boton_siguiente, rect_texto_siguiente)

    pg.display.update()
# ------------------------------------


def pantalla_fin_juego():
    # 2. Dibujar fondo y título (GAME OVER o ¡GANASTE!)
    if mensaje_fin_juego == "¡GANASTE!":
        ventana.blit(imagen_fondo_victoria, (0, 0)) 
    else: # Será "GAME OVER"
        ventana.blit(imagen_fondo_derrota, (0, 0))

    # Dibuja el texto (ya centrado)
    texto_renderizado = font_fin_juego.render(mensaje_fin_juego, True, cons.COLOR_BLANCO)
    text_rect = texto_renderizado.get_rect(center = (cons.ANCHO_VENTANA/2, cons.ALTO_VENTANA/2 - 100))
    ventana.blit(texto_renderizado, text_rect)

    # 4. Dibujar el input de nombre
    # Label
    x_label = input_rect.centerx - (label_nombre.get_width() // 2)
    ventana.blit(label_nombre, (x_label, input_rect.y - 30))

    # Campo de texto (color cambia si está activo o no)
    if input_activo:
        color_caja = color_activo
    else:
        color_caja = color_inactivo
    pg.draw.rect(ventana, color_caja, input_rect, width=2)
    texto_input = font_input.render(nombre_jugador, True, cons.COLOR_BLANCO)
    ventana.blit(texto_input, (input_rect.x + 10, input_rect.y + 7))

    # 5. Feedback de guardado Y MOSTRAR BOTONES
    if puntaje_guardado:
        msg_ok = font_input.render("¡Puntaje guardado!", True, cons.COLOR_BLANCO)
        x_texto_guardado = input_rect.centerx - (msg_ok.get_width() // 2)
        ventana.blit(msg_ok, (x_texto_guardado, input_rect.y + 45))

        # 6. Botón de reinicio (Y: +200)
        boton_reinicio = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 100, 200, 50)
        pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_reinicio)
        rect_texto_reinicio = texto_boton_reinicio.get_rect(center=boton_reinicio.center)
        ventana.blit(texto_boton_reinicio, rect_texto_reinicio)

        # 7. Botón Volver al Menú (Y: +260)
        boton_volver_menu = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 160, 200, 50)
        pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_volver_menu)
        rect_texto_volver = texto_boton_volver_menu.get_rect(center=boton_volver_menu.center)
        ventana.blit(texto_boton_volver_menu, rect_texto_volver)

        # 8. Botón de Salir (Final) (Y: +320)
        boton_salir_final = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 220, 200, 50)
        pg.draw.rect(ventana, cons.COLOR_ROJO, boton_salir_final) 
        rect_texto_salir = texto_boton_salir_final.get_rect(center=boton_salir_final.center)
        ventana.blit(texto_boton_salir_final, rect_texto_salir)

##########################     FUENTES     ###########################

# --- 1. Carga de Objetos de Fuente ---d

# Fuentes de Título (GOTHIC)
font_titulo = pg.font.Font(cons.FUENTE_GOTHIC, 100)
font_game_over = pg.font.Font(cons.FUENTE_GOTHIC, 110)
font_titulo_secundario = pg.font.Font(cons.FUENTE_TEXTO, 100)

# Fuentes de Texto (TEXTO)
font_inicio = pg.font.Font(cons.FUENTE_TEXTO, 30)
font_reinicio = pg.font.Font(cons.FUENTE_TEXTO, 30)
font_input = pg.font.Font(cons.FUENTE_TEXTO, 28)
font_volumen = pg.font.Font(cons.FUENTE_TEXTO, 20)
font_score = pg.font.Font(cons.FUENTE_TEXTO, cons.TAMANIO_FUENTE_SCORE)
font = pg.font.Font(cons.FUENTE_TEXTO, cons.TAMANIO_FUENTE_ENEMIGOS)

# --- 2. Renderizado de Textos Estáticos ---
# (Todos los textos que no cambian se definen aquí, usando las fuentes de arriba)

# Textos de Fin de Juego
game_over_text = font_game_over.render("GAME OVER", True, cons.COLOR_BLANCO)
texto_boton_reinicio = font_reinicio.render("Reiniciar", True, cons.COLOR_NEGRO)
texto_boton_salir_final = font_reinicio.render("Salir", True, cons.COLOR_BLANCO)
texto_boton_volver_menu = font_reinicio.render("Menu Principal", True, cons.COLOR_NEGRO)
label_nombre = font_input.render("Ingresá tus iniciales (3) y presiona ENTER:", True, cons.COLOR_BLANCO)

# Textos de Pantalla de Victoria
texto_ganaste = font_titulo.render("¡GANASTE!", True, cons.COLOR_BLANCO)
rect_ganaste = texto_ganaste.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2))

# Textos de Botones de Inicio
boton_jugar = pg.Rect(cons.ANCHO_VENTANA/2 -100, cons.ALTO_VENTANA/2 +15, 200, 50)
boton_menu = pg.Rect(cons.ANCHO_VENTANA/2 -100, cons.ALTO_VENTANA/2 +75, 200, 50)
boton_salir = pg.Rect(cons.ANCHO_VENTANA/2 -100, cons.ALTO_VENTANA/2 +135, 200, 50)
texto_boton_jugar = font_inicio.render("JUGAR", True, cons.COLOR_NEGRO)
texto_boton_menu = font_inicio.render("MENU", True, cons.COLOR_NEGRO)
texto_boton_salir = font_inicio.render("SALIR", True, cons.COLOR_BLANCO)


# Textos de Menú
texto_titulo_menu = font_titulo_secundario.render("M E N U", True, cons.COLOR_BLANCO)
rect_titulo_menu = texto_titulo_menu.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA/2 - 150))
y_base_menu = cons.ALTO_VENTANA / 2 - 60
espacio_menu = 60
boton_dificultad = pg.Rect(cons.ANCHO_VENTANA/2 - 100, y_base_menu, 200, 50)
boton_ranking = pg.Rect(cons.ANCHO_VENTANA/2 - 100, y_base_menu + espacio_menu, 200, 50)
boton_volumen = pg.Rect(cons.ANCHO_VENTANA/2 - 100, y_base_menu + (espacio_menu * 2), 200, 50)
boton_controles = pg.Rect(cons.ANCHO_VENTANA/2 - 100, y_base_menu + (espacio_menu * 3), 200, 50)
boton_volver = pg.Rect(cons.ANCHO_VENTANA/2 - 100, y_base_menu + (espacio_menu * 4), 200, 50)
texto_boton_dificultad = font_inicio.render("DIFICULTAD", True, cons.COLOR_NEGRO)
texto_boton_ranking = font_inicio.render("RANKING", True, cons.COLOR_NEGRO)
texto_boton_volumen = font_inicio.render("VOLUMEN", True, cons.COLOR_NEGRO)
texto_boton_controles = font_inicio.render("CONTROLES", True, cons.COLOR_NEGRO)
texto_boton_volver = font_inicio.render("VOLVER", True, cons.COLOR_NEGRO)

# Textos de Sub-menús (Volumen y Dificultad)
ancho_boton_vol = 60
espacio_boton_vol = 10
x_inicio_dif = cons.ANCHO_VENTANA/2 + 110
y_boton_dif = boton_dificultad.y
boton_dif_facil = pg.Rect(x_inicio_dif, y_boton_dif, ancho_boton_vol, 50)
boton_dif_norm = pg.Rect(x_inicio_dif + ancho_boton_vol + espacio_boton_vol, y_boton_dif, ancho_boton_vol, 50)
boton_dif_fuerte = pg.Rect(x_inicio_dif + (ancho_boton_vol + espacio_boton_vol) * 2, y_boton_dif, ancho_boton_vol, 50)

x_inicio_vol = cons.ANCHO_VENTANA/2 + 110 
y_boton_vol = boton_volumen.y 
boton_vol_bajo = pg.Rect(x_inicio_vol, y_boton_vol, ancho_boton_vol, 50)
boton_vol_norm = pg.Rect(x_inicio_vol + ancho_boton_vol + espacio_boton_vol, y_boton_vol, ancho_boton_vol, 50)
boton_vol_fuerte = pg.Rect(x_inicio_vol + (ancho_boton_vol + espacio_boton_vol) * 2, y_boton_vol, ancho_boton_vol, 50)

texto_vol_bajo = font_volumen.render("M I N", True, cons.COLOR_NEGRO)
texto_vol_norm = font_volumen.render("N O R", True, cons.COLOR_NEGRO)
texto_vol_fuerte = font_volumen.render("M A X", True, cons.COLOR_NEGRO)

# (Reutilizamos la fuente 'font_volumen')
texto_dif_facil = font_volumen.render("Facil", True, cons.COLOR_NEGRO)
texto_dif_norm = font_volumen.render("Normal", True, cons.COLOR_NEGRO)
texto_dif_fuerte = font_volumen.render("Dificil", True, cons.COLOR_NEGRO)

# Textos de Ranking
texto_titulo_ranking = font_titulo.render("RANKING", True, cons.COLOR_BLANCO)
rect_titulo_ranking = texto_titulo_ranking.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA/2 - 250))

# Textos de Controles
texto_titulo_controles = font_titulo_secundario.render("C O N T R O L E S", True, cons.COLOR_BLANCO)
rect_titulo_controles = texto_titulo_controles.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA/2 - 200))
texto_controles_1 = font_reinicio.render("W, A, S, D = Moverse", True, cons.COLOR_BLANCO)
texto_controles_2 = font_reinicio.render("Click Izquierdo = Disparar", True, cons.COLOR_BLANCO)
texto_controles_3 = font_reinicio.render("E = Abrir Puertas", True, cons.COLOR_BLANCO)

# Textos de Briefingd
texto_titulo_briefing = font_titulo_secundario.render("S O B R E V I V E", True, cons.COLOR_BLANCO)
rect_titulo_briefing = texto_titulo_briefing.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA/2 - 250))
texto_historia_1 = font_reinicio.render("Hordas de monstruos han invadido.", True, cons.COLOR_BLANCO)
texto_historia_2 = font_reinicio.render("¡Elimínalos a todos y encuentra la salida!", True, cons.COLOR_AMARILLO)
boton_comenzar = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA / 2 + 250, 200, 50)
texto_boton_comenzar = font_inicio.render("COMENZAR", True, cons.COLOR_NEGRO)

# --- Variables de la Pantalla de SELECCIÓN DE PERSONAJE ---
texto_titulo_personaje = font_titulo_secundario.render("ELIGE TU HEROE", True, cons.COLOR_BLANCO)
rect_titulo_personaje = texto_titulo_personaje.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA/2 - 250))

# Definimos los Rects donde haremos clic para seleccionar
boton_selec_p1 = pg.Rect(cons.ANCHO_VENTANA/2 - 200, cons.ALTO_VENTANA/2 - 100, 100, 150) # Izquierda
boton_selec_p2 = pg.Rect(cons.ANCHO_VENTANA/2 - 50, cons.ALTO_VENTANA/2 - 100, 100, 150) # Centro
boton_selec_p3 = pg.Rect(cons.ANCHO_VENTANA/2 + 100, cons.ALTO_VENTANA/2 - 100, 100, 150) # Derecha

texto_boton_siguiente = font_inicio.render("SIGUIENTE", True, cons.COLOR_NEGRO)
# --------------------------------------------------------

# --- Variables de Estado (Fin de Juego) ---
mensaje_fin_juego = "GAME OVER"
font_fin_juego = font_game_over
input_activo = False
nombre_jugador = ""
puntaje_guardado = False
t_fin_juego = 0
input_rect = pg.Rect(cons.ANCHO_VENTANA//2 - 80, cons.ALTO_VENTANA//2 , 160, 40)
color_inactivo = (cons.COLOR_NEGRO)
color_activo = (cons.COLOR_BLANCO)
# ------------------------------------------

##############importar imagenes#############

# Cargar y escalar imagen de fondo al tamaño de la ventana

imagen_fondo_inicio = pg.image.load("assets/images/fondos_de_pantalla/fondo_inicio.webp").convert()
imagen_fondo_inicio = pg.transform.scale(imagen_fondo_inicio, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))

imagen_fondo_menu = pg.image.load("assets/images/fondos_de_pantalla/imagen_fondo_menu.jpg").convert()
imagen_fondo_menu = pg.transform.scale(imagen_fondo_menu, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))

imagen_fondo_victoria = pg.image.load("assets/images/fondos_de_pantalla/imagen_fondo_victoria.png").convert()
imagen_fondo_victoria = pg.transform.scale(imagen_fondo_victoria, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))

imagen_fondo_derrota = pg.image.load("assets/images/fondos_de_pantalla/imagen_fondo_derrota.png").convert()
imagen_fondo_derrota = pg.transform.scale(imagen_fondo_derrota, (cons.ANCHO_VENTANA, cons.ALTO_VENTANA))

# energia
corazon_vacio = utils.cargar_imagen("assets/images/items/corazon_vacio_1.png", cons.ESCALA_CORAZONES)
corazon_medio = utils.cargar_imagen("assets/images/items/corazon_mitad_1.png", cons.ESCALA_CORAZONES)
corazon_lleno = utils.cargar_imagen("assets/images/items/corazon_lleno_1.png", cons.ESCALA_CORAZONES)

# --- Cargar animaciones de JUGADORES ---
directorio_jugadores = "assets/images/characters/players"
# Esto carga 'players
# también lo carga automáticamente.
sets_anim_jugadores = utils.cargar_set_animaciones(directorio_jugadores, cons.ESCALA_PERSONAJE)

# ---  ---
# (Preparamos los diccionarios con sus variables de estado)
for anim_dict in sets_anim_jugadores:
    anim_dict["frame_index"] = 0
    anim_dict["update_time"] = pg.time.get_ticks()
    anim_dict["cooldown"] = 150 # Cooldown para la pantalla de selección
# -------------------------

# --- Cargar animaciones de ENEMIGOS ---
directorio_enemigos = "assets/images/characters/enemigos"
animacion_enemigos = utils.cargar_set_animaciones(directorio_enemigos, cons.ESCALA_ENEMIGOS)

#armas
imagen_arma = utils.cargar_imagen("assets/images/weapons/vacio.png", cons.ESCALA_ARMA)

#balas
imagen_bala = utils.cargar_imagen("assets/images/weapons/bullets/fuego_1.png", cons.ESCALA_BALA)

#cargar imagenes del mundo
lista_tile = []
for x in range(cons.TIPOS_TILES):
    tile_image = pg.image.load(f"assets/images/tiles/tile_{x+1}.png").convert_alpha()
    tile_image = pg.transform.scale(tile_image, (int(cons.TAMANIO_TILES), int(cons.TAMANIO_TILES)))
    lista_tile.append(tile_image)

#cargar imagen de los items
posion_roja = utils.cargar_imagen("assets/images/items/posion/posion.png", cons.ESCALA_POSION_ROJA)


SCORES_FILE = "scores.csv"   # Archivo donde se guardará
monedas_imagen = []
ruta_imagen = "assets/images/items/moneda"
numero_monedas_imagen = utils.contar_elementos(ruta_imagen)
for i in range(numero_monedas_imagen):
    img = utils.cargar_imagen(f"assets/images/items/moneda/moneda_frame_{i+1}.png", cons.ESCALA_MONEDA)
    monedas_imagen.append(img)

item_imagenes = [monedas_imagen, [posion_roja]]

def dibujar_texto_pantalla(texto, fuente, color, x, y):
    img = fuente.render (texto, True, color)
    ventana.blit(img, (x, y))

def vida_jugador():
    corazon_mitad_dibujado = False
    for i in range(5):
        if jugador.energia >= ((i+1)*20):
            ventana.blit(corazon_lleno, (5+i*50, 5))
        elif jugador.energia % 20 > 0 and not corazon_mitad_dibujado:
            ventana.blit(corazon_medio, (5+i*50, 5))
            corazon_mitad_dibujado = True
        else: 
            ventana.blit(corazon_vacio, (5+i*50, 5))

            
def aplicar_volumen(vol_musica, vol_sonido):
    """
    Aplica el volumen seleccionado a la música y a todos los sonidos.
    """
    # 1. Aplica a la música (la que esté sonando)
    pg.mixer.music.set_volume(vol_musica)
    # 2. Aplica al sonido del disparo (que ya está creado)
    sonido_disparo.set_volume(vol_sonido)
    
    print(f"Volumen aplicado: Música={vol_musica}, Sonidos={vol_sonido}")

# funciones de nivel / mundo  

def cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos, multiplicador):
    # crea world + lista_enemigos sin tocar grupos (grupo_items se maneja afuera)
    world_data_local = utils.leer_csv_nivel(nivel) 
    world_local = md.Mundo()
    # Pasa el multiplicador a la siguiente función
    world_local.procesar_data(world_data_local, lista_tile, item_imagenes, animacion_enemigos, multiplicador)
    # ... (resto de la función) ...

    lista_enemigos_local = []
    for ene in world_local.lista_enemigo:
        lista_enemigos_local.append(ene)

    return world_local, lista_enemigos_local
# ... (después de la función cargar_world_y_enemigos) ...

def cargar_scores():
    scores_list = []
    # Primero, revisa si el archivo existe
    if not os.path.isfile(SCORES_FILE):
        return [] # Devuelve una lista vacía si no hay archivo

    try:
        with open(SCORES_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader) # Salta el encabezado ("nombre", "score")
            for row in reader:
                if row: # Asegura que la fila no esté vacía
                    scores_list.append((row[0], int(row[1]))) # Guarda (Nombre, Puntaje como NÚMERO)
    except Exception as e:
        print(f"Error al leer scores.csv: {e}")
        return [] # Devuelve vacío si hay un error

    # Ordena la lista. 
    # 'key=lambda item: item[1]' le dice que ordene usando el segundo elemento (el puntaje)
    # 'reverse=True' hace que el más alto quede primero
    scores_list.sort(key=lambda item: item[1], reverse=True)
    
    # Devuelve solo los 5 mejores puntajes
    return scores_list[:5]

# ... (después del final de 'cargar_scores()') ...

def iniciar_juego(nivel_a_cargar):
    """
    Prepara todas las variables y carga los assets para iniciar el juego.
    """
    global mostrar_inicio, mostrar_menu, mostrar_ranking, mostrar_selec_dificultad, evitar_click_fantasma
    global world, lista_enemigos, jugador # Hacemos globales las variables del juego
    
    # 1. Configura la música y los estados
    pg.mixer.music.load(cons.MUSICA_JUEGO)
    pg.mixer.music.play(-1)
    mostrar_inicio = False
    mostrar_menu = False
    mostrar_ranking = False
    evitar_click_fantasma = True # Activa el anti-click
    
    # 2. Resetea al jugador
    jugador.energia = 100
    jugador.vivo = True
    jugador.score = 0
    
    # 3. Limpia los grupos de sprites
    grupo_damage_text.empty()
    grupo_balas.empty()
    grupo_items.empty()
    
    # 4. Carga el mundo (¡PASANDO EL MULTIPLICADOR!)
    world, lista_enemigos = cargar_world_y_enemigos(nivel_a_cargar, lista_tile, item_imagenes, animacion_enemigos, multiplicador_dificultad)
    
    # 5. Crea el nuevo jugador seleccionado y lo coloca
    anim_dict_seleccionado = sets_anim_jugadores[personaje_seleccionado_idx]
    jugador = per.Personaje(80, 80, anim_dict_seleccionado, 100, 1) # reinicia energia a 100
    jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel_a_cargar)])
    for item in world.lista_item:
        grupo_items.add(item)

def reiniciar_juego_completo():
    """ Resetea todas las variables globales al estado de inicio. """
    global nivel, input_activo, nombre_jugador, puntaje_guardado, t_fin_juego
    global mensaje_fin_juego, font_fin_juego
    
    # Resetea estado del jugador
    jugador.vivo = True
    jugador.energia = 100
    jugador.score = 0
    nivel = 1
    
    # Resetea variables de input
    input_activo = False
    nombre_jugador = ""
    puntaje_guardado = False
    t_fin_juego = 0
    mensaje_fin_juego = "GAME OVER"
    font_fin_juego = font_game_over
    
    # Limpia grupos
    grupo_damage_text.empty()
    grupo_balas.empty()
    grupo_items.empty()


world_data = []

for fila in range(cons.FILAS):
    filas = [7] * cons.COLUMNAS
    world_data.append(filas)

#cargar el archivo con nivel
with open("niveles/nivel_1.csv", newline="") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data [x] [y] = int(columna)
world = md.Mundo()
world.procesar_data(world_data, lista_tile, item_imagenes, animacion_enemigos, multiplicador_dificultad) 


#crear una lista de enemigos
lista_enemigos = []
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)

#crear un arma de la clase weapon centrada en jugador
arma = wp.weapon(imagen_arma, imagen_bala, sonido_disparo)

#crear un grupo de sprites
grupo_damage_text = pg.sprite.Group()
grupo_balas = pg.sprite.Group()
grupo_items = pg.sprite.Group()

#añadir items de la data de world
for item in world.lista_item:
    grupo_items.add(item)



#variables de movimiento del jugador

mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

#conrolar el frame rate
reloj = pg.time.Clock()
prueba = True
run = True
mostrar_inicio = True
mostrar_menu = False
mostrar_opciones_volumen = False
mostrar_ranking = False
mostrar_opciones_dificultad = False
mostrar_selec_dificultad = False
mostrar_controles = False
mostrar_briefing = False
mostrar_selec_personaje = False
evitar_click_fantasma = False
personaje_seleccionado_idx = 1

#crear un jugador de la clase personaje en posicion x , y
jugador = per.Personaje (80, 80, sets_anim_jugadores[personaje_seleccionado_idx], 80, 1)

# estado de victoria
mostrar_ganaste = False
t_inicio_ganaste = 0

while run:
        # pantalla de victoria (3 segundos y volver al menú) 
    if mostrar_ganaste:
        ventana.fill(cons.COLOR_SUELO)
        ventana.blit(texto_ganaste, rect_ganaste)
        pg.display.update()

        # tras 3s, reset y volver al inicio
        if pg.time.get_ticks() - t_inicio_ganaste >= 3000:
            # resetear estado básico
            jugador.vivo = True
            jugador.energia = 100
            jugador.score = 0
            nivel = 1

            # limpiar grupos
            grupo_damage_text.empty()
            grupo_balas.empty()
            grupo_items.empty()

            # recargar nivel 1
            world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos)
            jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])
            for item in world.lista_item:
                grupo_items.add(item)

            # volver a pantalla de inicio
            mostrar_ganaste = False
            mostrar_inicio = True

        continue  # saltar el resto del frame mientras está la pantalla de victoria

    elif mostrar_inicio:
        pantalla_inicio()
        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(cons.MUSICA_PRINCIPAL)
            pg.mixer.music.play(-1)  # -1 = loop infinito

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                    mostrar_selec_personaje = True 
                elif boton_menu.collidepoint(event.pos):
                    pg.mixer.music.load(cons.MUSICA_MENU) # Carga la nueva música
                    pg.mixer.music.play(-1) # Reproduce en loop
                    mostrar_inicio = False
                    mostrar_menu = True # Activa el estado 'menu'
                elif boton_salir.collidepoint(event.pos):
                    run = False

    elif mostrar_menu:
        pantalla_menu() # Llama a la nueva función de DIBUJO

        # Bucle de eventos del menú
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                    # Lógica del botón VOLVER
                if boton_volver.collidepoint(event.pos):
                    pg.mixer.music.load(cons.MUSICA_PRINCIPAL) # Carga la música original del menú
                    pg.mixer.music.play(-1) # Reproduce en loop
                    mostrar_menu = False
                    mostrar_inicio = True # Vuelve al inicio
                    mostrar_opciones_volumen = False # Oculta el volumen al salir
                    mostrar_opciones_dificultad = False # oculta dificultad al salir
                    mostrar_controles = False
                # Lógica del botón VOLUMEN (mostrar/ocultar)
                elif boton_volumen.collidepoint(event.pos):
                    mostrar_opciones_volumen = not mostrar_opciones_volumen
                    mostrar_opciones_dificultad = False # Oculta el otro menú

                # Lógica del botón RANKING (no hace nada)
                elif boton_ranking.collidepoint(event.pos):
                    mostrar_menu = False
                    mostrar_ranking = True
                    mostrar_opciones_volumen = False # Oculta menús
                    mostrar_opciones_dificultad = False
                
                # Lógica del botón DIFICULTAD (mostrar/ocultar)
                elif boton_dificultad.collidepoint(event.pos): 
                    mostrar_opciones_dificultad = not mostrar_opciones_dificultad
                    mostrar_opciones_volumen = False # Oculta el otro menú

                elif boton_controles.collidepoint(event.pos):
                    mostrar_menu = False
                    mostrar_controles = True # <-- Activa la nueva pantalla
                    mostrar_opciones_volumen = False
                    mostrar_opciones_dificultad = False

                # Lógica de los botones B, N, F (si están visibles)
                elif mostrar_opciones_volumen:
                    if boton_vol_bajo.collidepoint(event.pos):
                        aplicar_volumen(cons.MUSICA_VOLUMEN_BAJO, cons.SONIDO_DISPARO_BAJO)
                        mostrar_opciones_volumen = False

                    elif boton_vol_norm.collidepoint(event.pos):
                        aplicar_volumen(cons.MUSICA_VOLUMEN_NORMAL, cons.SONIDO_DISPARO_NORMAL)
                        mostrar_opciones_volumen = False

                    elif boton_vol_fuerte.collidepoint(event.pos):
                        aplicar_volumen(cons.MUSICA_VOLUMEN_FUERTE, cons.SONIDO_DISPARO_FUERTE)
                        mostrar_opciones_volumen = False

                # Lógica de los botones F, N, D (Dificultad)
                elif mostrar_opciones_dificultad:
                    if boton_dif_facil.collidepoint(event.pos):
                        multiplicador_dificultad = 0.7
                        print("Dificultad: FÁCIL (0.7)")
                        mostrar_opciones_dificultad = False

                    elif boton_dif_norm.collidepoint(event.pos):
                        multiplicador_dificultad = 1.0
                        print("Dificultad: NORMAL (1.0)")
                        mostrar_opciones_dificultad = False

                    elif boton_dif_fuerte.collidepoint(event.pos):
                        multiplicador_dificultad = 1.5
                        print("Dificultad: DIFÍCIL (1.5)")
                        mostrar_opciones_dificultad = False
    
    elif mostrar_ranking:
        pantalla_ranking() # Llama a la función de DIBUJO

        # Bucle de eventos del ranking
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                # Lógica del botón VOLVER (reutilizado)
                if boton_volver.collidepoint(event.pos):
                    mostrar_ranking = False
                    mostrar_menu = True

    elif mostrar_controles:
        pantalla_controles() # Llama a la función de DIBUJO

        # Bucle de eventos de controles
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                # Lógica del botón VOLVER (reutilizado)
                if boton_volver.collidepoint(event.pos):
                    mostrar_controles = False
                    mostrar_menu = True # Vuelve al menú
    # ----------------------------------------

    elif mostrar_briefing:
        pantalla_briefing() # Llama a la función de DIBUJO

        # Bucle de eventos del briefing
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                # Lógica del botón COMENZAR
                if boton_comenzar.collidepoint(event.pos):
                    mostrar_briefing = False
                    iniciar_juego(nivel) # <-- ¡AHORA SÍ EMPIEZA EL JUEGO!
    # ----------------------------------------

    elif mostrar_selec_personaje:
        pantalla_selec_personaje() # Llama a la función de DIBUJO

        # Bucle de eventos de selección de personaje
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
 
                # Clic en "Siguiente" (reutiliza 'boton_comenzar')
                if boton_comenzar.collidepoint(event.pos):
                    mostrar_selec_personaje = False
                    mostrar_briefing = True # Pasa a la pantalla de briefing

                # Clics para seleccionar personaje
                elif boton_selec_p1.collidepoint(event.pos):
                    personaje_seleccionado_idx = 0 # caballero
                elif boton_selec_p2.collidepoint(event.pos):
                    personaje_seleccionado_idx = 1 # heroina
                elif boton_selec_p3.collidepoint(event.pos):
                    personaje_seleccionado_idx = 2 # Necro
        # ----------------------------------------

    else:
            
        #que valla a 60 fps
        reloj.tick(cons.FPS)


        ventana.fill(cons.COLOR_SUELO)

        if jugador.vivo:



            #calcular movimiento del jugador
            delta_x = 0
            delta_y = 0

            if mover_derecha == True:
                delta_x = cons.VELOCIDAD_PERSONAJE
            if mover_izquierda == True:
                delta_x = -cons.VELOCIDAD_PERSONAJE
            if mover_abajo == True:
                delta_y = cons.VELOCIDAD_PERSONAJE
            if mover_arriba == True:
                delta_y = -cons.VELOCIDAD_PERSONAJE

                #mover al jugador
            posicion_pantalla, nivel_completo = jugador.movimiento(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)

            # actualiza el mapa
            world.update(posicion_pantalla)

            #actualiza estado de jugador
            jugador.update()

            #actualiza estado de enemigo
            for ene_data in lista_enemigos:
                ene_obj = ene_data[0] # Saca el objeto Enemigo de la tupla
                ene_obj.update() # Llama a .update() sobre el objeto
        

            #actualiza el esatdo del arma
            bala = None
            
            # Revisamos la bandera (tu "retardo")
            if evitar_click_fantasma:
                # Si está activa, la consumimos y no hacemos nada.
                # El click se ignora este frame.
                if not pg.mouse.get_pressed()[0]:
                    evitar_click_fantasma = False
            else:
                # Si la bandera está inactiva, actualizamos el arma normalmente.
                bala = arma.update(jugador)

            if bala:
                grupo_balas.add(bala)

            # "Desempaquetamos" la lista de enemigos (de tuplas)
            # para pasarle solo los OBJETOS a la bala.
            lista_de_objetos_enemigos = [ene_data[0] for ene_data in lista_enemigos]

            for bala in grupo_balas:
                # Ahora le pasamos la lista de OBJETOS, no la de tuplas
                damage, post_damage = bala.update(lista_de_objetos_enemigos, world.obstaculos_tiles)
                if damage:
                    damage_text = tx.Damage_text(post_damage.centerx, post_damage.centery, "-" + str(damage), font, cons.COLOR_ROJO)
                    grupo_damage_text.add(damage_text)



            # actualizar el daño
            grupo_damage_text.update(posicion_pantalla)

            #actualizar items
            grupo_items.update(posicion_pantalla, jugador)

            #dibujar mundo
            world.draw(ventana)
        
            #dibujar al jugador
            jugador.dibujar(ventana)
        
            #dibujar al enemigo

            for ene_data in lista_enemigos.copy():
                
                # "Desempaquetamos"
                ene = ene_data[0]

                if ene.energia <= 0:
                    jugador.score += ene.score_value
                    lista_enemigos.remove(ene_data) # Removemos la tupla entera
                    continue

                # update IA / colisiones / etc
                ene.ia(jugador, world.obstaculos_tiles, posicion_pantalla,)
                # dibujar sprite
                ene.dibujar(ventana)

            #dibujar el arma
            arma.dibujar(ventana)

            #dibujar balas
            for bala in grupo_balas:
                bala.dibujar(ventana)

            #dibujar corazones
            vida_jugador()

            #dibujar textos
            grupo_damage_text.draw(ventana)
            dibujar_texto_pantalla(f"SCORE : {jugador.score}", font_score, cons.COLOR_AMARILLO, cons.POSICION_TEXTO_SCORE_X, cons.POSICION_TEXTO_SCORE_Y)

            # nivel
            dibujar_texto_pantalla(f"N I V E L: " + str(nivel), font, cons.COLOR_BLANCO, cons.ANCHO_VENTANA / 2, 5)

            #dibujar items
            grupo_items.draw(ventana)

            # chuequear si el nivel esta completo
            if nivel_completo:
                if nivel < cons.NIVEL_MAXIMO:
                    nivel += 1
                    # cargar mundo y enemigos con función
                    world, lista_enemigos = cargar_world_y_enemigos(nivel, lista_tile, item_imagenes, animacion_enemigos, multiplicador_dificultad)
                    # reposicionar jugador según config
                    jugador.actualizar_coordenadas(cons.COORDENADAS_ENEMIGO_NIVEL[str(nivel)])
                    # 1. Vacía los ítems del nivel anterior
                    grupo_items.empty()
                    # 2. Carga los ítems del nuevo nivel
                    for item in world.lista_item:
                        grupo_items.add(item)
                else:
                    # detener música del juego al ganar
                    if pg.mixer.music.get_busy():
                        pg.mixer.music.stop()

                    # Preparamos la pantalla de ingreso ---
                    mensaje_fin_juego = "¡GANASTE!"
                    font_fin_juego = font_titulo # Usamos la fuente de título
                    
                    jugador.vivo = False # Usamos la misma pantalla de "muerto"
                    t_fin_juego = pg.time.get_ticks() # Inicia el timer
                    pg.event.clear() # Limpia teclas 

        # LÓGICA DE FIN DE JUEGO (SI NO ESTÁ VIVO)
        else:
            # --- LÓGICA DE FIN DE JUEGO (GAME OVER O VICTORIA) ---

            # 1. Iniciar temporizador (Esto es LÓGICA, se queda aquí)
            if t_fin_juego == 0:
                t_fin_juego = pg.time.get_ticks()
                pg.event.clear() # Limpia teclas 
                if pg.mixer.music.get_busy(): # Parar música
                    pg.mixer.music.stop()

            # 3. Activar el input (Esto es LÓGICA, se queda aquí)
            if not input_activo and (pg.time.get_ticks() - t_fin_juego > 1000): # 1000ms = 1 seg
                input_activo = True

            # 4. Llamar a la función de DIBUJO
            pantalla_fin_juego()

        #  BUCLE DE EVENTOS ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            # --- LÓGICA DE TECLADO (KEYDOWN) ---
            if event.type == pg.KEYDOWN:

                if jugador.vivo:
                    if event.key == pg.K_w:
                        mover_arriba = True
                    elif event.key == pg.K_s:
                        mover_abajo = True
                    elif event.key == pg.K_d:
                        mover_derecha = True
                    elif event.key == pg.K_a:
                        mover_izquierda = True
                    elif event.key == pg.K_e:
                        if world.cambiar_puerta(jugador, lista_tile):
                            print("puerta cambiada")
                else:
                # --- Eventos de INPUT (solo si está muerto/ganó y el input está activo) ---
                    if input_activo:
                        if event.key == pg.K_BACKSPACE:
                            nombre_jugador = nombre_jugador[:-1]
                        
                        elif event.key == pg.K_RETURN:
                            # Guardar puntaje si tiene 3 letras y no se guardó
                            if len(nombre_jugador.strip()) == 3 and not puntaje_guardado:
                                try:
                                    file_existe = os.path.isfile(SCORES_FILE)
                                    with open(SCORES_FILE, "a", newline="", encoding="utf-8") as f:
                                        writer = csv.writer(f)
                                        if not file_existe:
                                            writer.writerow(["nombre", "score"]) # Encabezado
                                        writer.writerow([nombre_jugador.strip().upper(), jugador.score])
                                    puntaje_guardado = True
                                except Exception as e:
                                    print("[ERROR guardando score]", e)

                        # Añadir letra (solo si es alfa, < 3 letras y no guardó)
                        elif event.unicode.isalpha() and len(nombre_jugador) < 3 and not puntaje_guardado:
                            nombre_jugador += event.unicode.upper()

            # LÓGICA DE TECLA LEVANTADA (KEYUP) 
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    mover_arriba = False
                elif event.key == pg.K_s:
                    mover_abajo = False
                elif event.key == pg.K_d:
                    mover_derecha = False
                elif event.key == pg.K_a:
                    mover_izquierda = False

            # LÓGICA DE CLICKS (MOUSEBUTTONDOWN) 
            if event.type == pg.MOUSEBUTTONDOWN:
                
                # --- Lógica de Clics si el JUGADOR ESTÁ MUERTO/GANÓ ---
                if not jugador.vivo:
                    
                    # --- CASO 1: El puntaje YA se guardó (Muestra "Reiniciar", "Volver", "Salir") ---
                    if puntaje_guardado:
                        # Definir los Rects aquí para chequear los clics
                        boton_reinicio = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 100, 200, 50)
                        boton_volver_menu = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 160, 200, 50)
                        boton_salir_final = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 220, 200, 50)

                        # 1. Click en el botón REINICIAR
                        if boton_reinicio.collidepoint(event.pos):
                            reiniciar_juego_completo() 
                            iniciar_juego(nivel) 
                        
                        # 1b. Click en el botón VOLVER AL MENÚ
                        elif boton_volver_menu.collidepoint(event.pos):
                            reiniciar_juego_completo()
                            mostrar_inicio = True
                            pg.mixer.music.load(cons.MUSICA_PRINCIPAL)
                            pg.mixer.music.play(-1)
                        
                        # 1c. Click en el botón SALIR (Final)
                        elif boton_salir_final.collidepoint(event.pos):
                            run = False
                    
                    # --- CASO 2: El puntaje NO se ha guardado (Muestra el Input) ---
                    else:
                        # 2a. Click en la CAJA de input
                        if input_rect.collidepoint(event.pos):
                            if pg.time.get_ticks() - t_fin_juego > 1000:
                                input_activo = True
                        
                        # 2b. Click FUERA de la caja
                        else:
                            input_activo = False
                
                # --- Lógica de Clics si el JUGADOR ESTÁ VIVO ---
                else:
                    pass


        pg.display.update()

pg.quit()


