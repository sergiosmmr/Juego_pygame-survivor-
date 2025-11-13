
import pygame as pg
import constantes_varaibles as cons
import utils  


########### PANTALLA DE INICIO ###########
def pantalla_inicio(ventana, assets):
    """ Dibuja la pantalla de inicio """
    ventana.blit(assets["imagen_fondo_inicio"], (0, 0))

    texto_titulo_str = "S U R V I V O R"
    offset_sombra = 4
    y_pos_titulo = cons.ALTO_VENTANA / 2 - 200

    # sombra
    sombra_surf = assets["font_titulo"].render(texto_titulo_str, True, cons.COLOR_NEGRO)
    ancho_sombra = sombra_surf.get_width()
    x_sombra = (cons.ANCHO_VENTANA // 2) - (ancho_sombra // 2)
    sombra_rect = sombra_surf.get_rect(topleft=(x_sombra + offset_sombra, y_pos_titulo + offset_sombra))

    # texto principal
    texto_surf = assets["font_titulo"].render(texto_titulo_str, True, cons.ROJO_OSCURO)
    ancho_texto = texto_surf.get_width()
    x_texto = (cons.ANCHO_VENTANA // 2) - (ancho_texto // 2)
    texto_rect = texto_surf.get_rect(topleft=(x_texto, y_pos_titulo))

    ventana.blit(sombra_surf, sombra_rect)
    ventana.blit(texto_surf, texto_rect)

    # botones
    pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_jugar"])
    rect_texto_jugar = assets["texto_boton_jugar"].get_rect(center=assets["boton_jugar"].center)
    ventana.blit(assets["texto_boton_jugar"], rect_texto_jugar)

    pg.draw.rect(ventana, cons.COLOR_ROJO, assets["boton_salir"])
    rect_texto_salir = assets["texto_boton_salir"].get_rect(center=assets["boton_salir"].center)
    ventana.blit(assets["texto_boton_salir"], rect_texto_salir)

    pg.draw.rect(ventana, cons.COLOR_BLANCO, assets["boton_menu"])
    rect_texto_menu = assets["texto_boton_menu"].get_rect(center=assets["boton_menu"].center)
    ventana.blit(assets["texto_boton_menu"], rect_texto_menu)
    
    pg.display.update()


    ########### PANTALLA DE MENÚ ###########

def pantalla_menu(ventana, assets, estado):
    """ Dibuja la pantalla de menú """
    ventana.blit(assets["imagen_fondo_menu"], (0, 0))
    ventana.blit(assets["texto_titulo_menu"], assets["rect_titulo_menu"])

    # botones principales
    pg.draw.rect(ventana, cons.COLOR_BLANCO, assets["boton_dificultad"])
    rect_texto_dif = assets["texto_boton_dificultad"].get_rect(center=assets["boton_dificultad"].center)
    ventana.blit(assets["texto_boton_dificultad"], rect_texto_dif)

    pg.draw.rect(ventana, cons.COLOR_BLANCO, assets["boton_ranking"])
    rect_texto_ranking = assets["texto_boton_ranking"].get_rect(center=assets["boton_ranking"].center)
    ventana.blit(assets["texto_boton_ranking"], rect_texto_ranking)

    pg.draw.rect(ventana, cons.COLOR_BLANCO, assets["boton_volumen"])
    rect_texto_vol = assets["texto_boton_volumen"].get_rect(center=assets["boton_volumen"].center)
    ventana.blit(assets["texto_boton_volumen"], rect_texto_vol)

    pg.draw.rect(ventana, cons.COLOR_BLANCO, assets["boton_controles"])
    rect_texto_controles = assets["texto_boton_controles"].get_rect(center=assets["boton_controles"].center)
    ventana.blit(assets["texto_boton_controles"], rect_texto_controles)

    pg.draw.rect(ventana, cons.COLOR_ROJO, assets["boton_volver"])
    rect_texto_volver = assets["texto_boton_volver"].get_rect(center=assets["boton_volver"].center)
    ventana.blit(assets["texto_boton_volver"], rect_texto_volver)

    # botones de volumen (si estan activos)
    if estado["mostrar_opciones_volumen"]:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_vol_bajo"])
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_vol_norm"])
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_vol_fuerte"])

        rect_vol_b = assets["texto_vol_bajo"].get_rect(center=assets["boton_vol_bajo"].center)
        ventana.blit(assets["texto_vol_bajo"], rect_vol_b)
        
        rect_vol_n = assets["texto_vol_norm"].get_rect(center=assets["boton_vol_norm"].center)
        ventana.blit(assets["texto_vol_norm"], rect_vol_n)
        
        rect_vol_f = assets["texto_vol_fuerte"].get_rect(center=assets["boton_vol_fuerte"].center)
        ventana.blit(assets["texto_vol_fuerte"], rect_vol_f)

    # botones de dificultad (si estan activos)
    if estado["mostrar_opciones_dificultad"]:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_dif_facil"])
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_dif_norm"])
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_dif_fuerte"])
        
        rect_dif_f = assets["texto_dif_facil"].get_rect(center=assets["boton_dif_facil"].center)
        ventana.blit(assets["texto_dif_facil"], rect_dif_f)
        
        rect_dif_n = assets["texto_dif_norm"].get_rect(center=assets["boton_dif_norm"].center)
        ventana.blit(assets["texto_dif_norm"], rect_dif_n)
        
        rect_dif_fu = assets["texto_dif_fuerte"].get_rect(center=assets["boton_dif_fuerte"].center)
        ventana.blit(assets["texto_dif_fuerte"], rect_dif_fu)

    pg.display.update()


    ########### PANTALLA DE RANKING ###########

def pantalla_ranking(ventana, assets):
    """ Dibuja la pantalla de ranking """
    ventana.blit(assets["imagen_fondo_menu"], (0, 0))
    ventana.blit(assets["texto_titulo_ranking"], assets["rect_titulo_ranking"])

    # cargar y dibujar los puntajes
    scores = utils.cargar_scores(cons.SCORES_FILE)  # usamos la funcion de utils
    base_y = (cons.ALTO_VENTANA // 2) - 150
    
    if not scores:
        no_scores_text = assets["font_reinicio"].render("No hay puntajes guardados", True, cons.COLOR_BLANCO)
        no_scores_rect = no_scores_text.get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 - 20))
        ventana.blit(no_scores_text, no_scores_rect)
    else:
        # encabezados
        header_name = assets["font_reinicio"].render("NOMBRE", True, cons.COLOR_AMARILLO)
        header_score = assets["font_reinicio"].render("PUNTAJE", True, cons.COLOR_AMARILLO)
        ventana.blit(header_name, (cons.ANCHO_VENTANA // 2 - 150, base_y))
        ventana.blit(header_score, (cons.ANCHO_VENTANA // 2 + 50, base_y))

        # puntajes
        y_offset = 40
        for i, (nombre, score) in enumerate(scores):
            y_pos = base_y + y_offset
            
            score_name = assets["font_reinicio"].render(f"{i+1}. {nombre}", True, cons.COLOR_BLANCO)
            ventana.blit(score_name, (cons.ANCHO_VENTANA // 2 - 150, y_pos))
            
            score_val = assets["font_reinicio"].render(str(score), True, cons.COLOR_BLANCO)
            ventana.blit(score_val, (cons.ANCHO_VENTANA // 2 + 50, y_pos))
            
            y_offset += 40

    # boton "VOLVER"
    pg.draw.rect(ventana, cons.COLOR_BLANCO, assets["boton_volver"])
    rect_texto_volver = assets["texto_boton_volver"].get_rect(center=assets["boton_volver"].center)
    ventana.blit(assets["texto_boton_volver"], rect_texto_volver)

    pg.display.update()


    ########### PANTALLA DE CONTROLES ###########

def pantalla_controles(ventana, assets):
    """ Dibuja la pantalla de controles """
    ventana.blit(assets["imagen_fondo_menu"], (0, 0))
    ventana.blit(assets["texto_titulo_controles"], assets["rect_titulo_controles"])

    # textos de ayuda
    rect_texto_1 = assets["texto_controles_1"].get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 - 50))
    rect_texto_2 = assets["texto_controles_2"].get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2))
    rect_texto_3 = assets["texto_controles_3"].get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 + 50))
    
    ventana.blit(assets["texto_controles_1"], rect_texto_1)
    ventana.blit(assets["texto_controles_2"], rect_texto_2)
    ventana.blit(assets["texto_controles_3"], rect_texto_3)
    
    # boton VOLVER
    pg.draw.rect(ventana, cons.COLOR_ROJO, assets["boton_volver"])
    rect_texto_volver = assets["texto_boton_volver"].get_rect(center=assets["boton_volver"].center)
    ventana.blit(assets["texto_boton_volver"], rect_texto_volver)

    pg.display.update()


    ########### PANTALLA DE HISTORIA ###########

def pantalla_historia(ventana, assets):
    """ Dibuja la pantalla de historia """
    ventana.blit(assets["imagen_fondo_menu"], (0, 0))
    ventana.blit(assets["texto_titulo_briefing"], assets["rect_titulo_briefing"])

    # textos de historia
    rect_historia_1 = assets["texto_historia_1"].get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 - 150))
    rect_historia_2 = assets["texto_historia_2"].get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 - 110))
    ventana.blit(assets["texto_historia_1"], rect_historia_1)
    ventana.blit(assets["texto_historia_2"], rect_historia_2)
    
    # textos de controles
    rect_texto_1 = assets["texto_controles_1"].get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2))
    rect_texto_2 = assets["texto_controles_2"].get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 + 40))
    rect_texto_3 = assets["texto_controles_3"].get_rect(center=(cons.ANCHO_VENTANA // 2, cons.ALTO_VENTANA // 2 + 80))
    ventana.blit(assets["texto_controles_1"], rect_texto_1)
    ventana.blit(assets["texto_controles_2"], rect_texto_2)
    ventana.blit(assets["texto_controles_3"], rect_texto_3)
    
    # boton "COMENZAR"
    pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_comenzar"])
    rect_texto_comenzar = assets["texto_boton_comenzar"].get_rect(center=assets["boton_comenzar"].center)
    ventana.blit(assets["texto_boton_comenzar"], rect_texto_comenzar)

    pg.display.update()


    ########### PANTALLA DE SELECCIÓN DE PERSONAJE ###########

def pantalla_selec_personaje(ventana, assets, estado):
    """ Dibuja la pantalla de selección de personaje """
    ventana.fill(cons.COLOR_NEGRO)
    ventana.blit(assets["texto_titulo_personaje"], assets["rect_titulo_personaje"])

    botones_personaje = [assets["boton_selec_p1"], assets["boton_selec_p2"], assets["boton_selec_p3"]]

    # iteramos sobre la lista 'sets_anim_jugadores'
    for i, anim_dict in enumerate(assets["sets_anim_jugadores"]):
        
        frame_index = anim_dict["frame_index"]
        update_time = anim_dict["update_time"]
        cooldown = anim_dict["cooldown"]

        # actualizar animacion
        if "idle" in anim_dict:
            current_idle_anim = anim_dict["idle"]
            
            if pg.time.get_ticks() - update_time >= cooldown:
                frame_index += 1
                update_time = pg.time.get_ticks()
                if frame_index >= len(current_idle_anim):
                    frame_index = 0
            
            # guardamos el estado actualizado
            anim_dict["frame_index"] = frame_index
            anim_dict["update_time"] = update_time

            # dibujar el sprite
            sprite_actual = current_idle_anim[frame_index]
            rect_sprite = sprite_actual.get_rect(center=botones_personaje[i].center)
            ventana.blit(sprite_actual, rect_sprite)
        
        elif "run" in anim_dict: # sino tiene idle
            sprite_actual = anim_dict["run"][0]
            rect_sprite = sprite_actual.get_rect(center=botones_personaje[i].center)
            ventana.blit(sprite_actual, rect_sprite)

    # recuadro de seleccion
    idx = estado["personaje_seleccionado_idx"]
    if idx == 0:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_selec_p1"], 4)
    elif idx == 1:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_selec_p2"], 4)
    elif idx == 2:
        pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_selec_p3"], 4)

    # boton "Siguiente"
    pg.draw.rect(ventana, cons.COLOR_AMARILLO, assets["boton_comenzar"])
    rect_texto_siguiente = assets["texto_boton_siguiente"].get_rect(center=assets["boton_comenzar"].center)
    ventana.blit(assets["texto_boton_siguiente"], rect_texto_siguiente)

    pg.display.update()


    ########### PANTALLA DE FIN DE JUEGO ###########

def pantalla_fin_juego(ventana, assets, estado):
    """ Dibuja la pantalla de fin de juego (Game Over o Victoria) """
    
    mensaje_fin = estado["mensaje_fin_juego"]
    
    if mensaje_fin == "¡GANASTE!":
        ventana.blit(assets["imagen_fondo_victoria"], (0, 0))
    else:
        ventana.blit(assets["imagen_fondo_derrota"], (0, 0))

    # titulo (GAME OVER o ¡GANASTE!)
    texto_renderizado = estado["font_fin_juego"].render(mensaje_fin, True, cons.COLOR_BLANCO)
    text_rect = texto_renderizado.get_rect(center=(cons.ANCHO_VENTANA / 2, cons.ALTO_VENTANA / 2 - 100))
    ventana.blit(texto_renderizado, text_rect)

    # input de nombre
    input_rect = assets["input_rect"]
    x_label = input_rect.centerx - (assets["label_nombre"].get_width() // 2)
    ventana.blit(assets["label_nombre"], (x_label, input_rect.y - 30))

    color_caja = assets["color_activo"] if estado["input_activo"] else assets["color_inactivo"]
    pg.draw.rect(ventana, color_caja, input_rect, width=2)
    
    texto_input = assets["font_input"].render(estado["nombre_jugador"], True, cons.COLOR_BLANCO)
    ventana.blit(texto_input, (input_rect.x + 10, input_rect.y + 7))

    # feedback y botones (si guardo)
    if estado["puntaje_guardado"]:
        msg_ok = assets["font_input"].render("¡Puntaje guardado!", True, cons.COLOR_BLANCO)
        x_texto_guardado = input_rect.centerx - (msg_ok.get_width() // 2)
        ventana.blit(msg_ok, (x_texto_guardado, input_rect.y + 45))

        # boton de reinicio
        boton_reinicio = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 100, 200, 50)
        pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_reinicio)
        rect_texto_reinicio = assets["texto_boton_reinicio"].get_rect(center=boton_reinicio.center)
        ventana.blit(assets["texto_boton_reinicio"], rect_texto_reinicio)

        # boton Volver al menu
        boton_volver_menu = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 160, 200, 50)
        pg.draw.rect(ventana, cons.COLOR_BLANCO, boton_volver_menu)
        rect_texto_volver = assets["texto_boton_volver_menu"].get_rect(center=boton_volver_menu.center)
        ventana.blit(assets["texto_boton_volver_menu"], rect_texto_volver)

        # boton de salir 
        boton_salir_final = pg.Rect(cons.ANCHO_VENTANA/2 - 100, cons.ALTO_VENTANA/2 + 220, 200, 50)
        pg.draw.rect(ventana, cons.COLOR_ROJO, boton_salir_final)
        rect_texto_salir = assets["texto_boton_salir_final"].get_rect(center=boton_salir_final.center)
        ventana.blit(assets["texto_boton_salir_final"], rect_texto_salir)