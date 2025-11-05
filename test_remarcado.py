import pygame

# === Inicialización ===
pygame.init()
ANCHO, ALTO = 600, 300
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Texto con Contorno en Pygame")

# === Fuente y colores ===
fuente = pygame.font.SysFont("arial", 72, bold=True)
COLOR_TEXTO = (255, 255, 255)  # blanco
COLOR_BORDE = (0, 0, 0)        # negro
COLOR_FONDO = (100, 150, 255)  # celeste

def render_texto_con_borde(texto, fuente, color_texto, color_borde, grosor=2):
    """
    Renderiza texto con contorno dibujando varias copias desplazadas.

    Args:
        texto (str): Texto a renderizar.
        fuente (pygame.font.Font): Fuente a utilizar.
        color_texto (tuple): Color del texto principal (R, G, B).
        color_borde (tuple): Color del contorno (R, G, B).
        grosor (int): Grosor del borde en píxeles.

    Returns:
        pygame.Surface: Superficie con el texto contorneado.
    """
    texto_base = fuente.render(texto, True, color_texto)
    texto_rect = texto_base.get_rect()

    superficie = pygame.Surface((texto_rect.width + grosor * 2, texto_rect.height + grosor * 2), pygame.SRCALPHA)

    # Dibujar el borde (desplazamientos alrededor)
    for dx in range(-grosor, grosor + 1):
        for dy in range(-grosor, grosor + 1):
            if dx != 0 or dy != 0:
                superficie.blit(fuente.render(texto, True, color_borde), (dx + grosor, dy + grosor))

    # Dibujar el texto principal encima
    superficie.blit(texto_base, (grosor, grosor))
    return superficie


# === Bucle principal ===
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ventana.fill(COLOR_FONDO)

    texto_render = render_texto_con_borde("Pygame!", fuente, COLOR_TEXTO, COLOR_BORDE, grosor=3)
    ventana.blit(texto_render, (ANCHO//2 - texto_render.get_width()//2, ALTO//2 - texto_render.get_height()//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
