# gana_juego.py  — versión simple
import pygame, random
from pathlib import Path

# Carpeta de imágenes local (cambia esto si tus PNG están en otro lado)
IMAGES_DIR = Path(__file__).resolve().parent / "images"

def _load_or_placeholder(nombre: str, escala=(180, 180)) -> pygame.Surface:
    """Carga una imagen; si no existe, devuelve un recuadro gris (no rompe)."""
    p = IMAGES_DIR / nombre
    if p.exists():
        img = pygame.image.load(str(p))
        img = img.convert_alpha()
        if escala: img = pygame.transform.smoothscale(img, escala)
        return img
    # placeholder muy simple
    surf = pygame.Surface(escala, pygame.SRCALPHA)
    surf.fill((60, 60, 60))
    pygame.draw.rect(surf, (10,10,10), surf.get_rect(), 4)
    return surf

def _build_animaciones(escala=(180, 180)):
    """6 sprites; cada uno usa 2 frames: movimiento(2i-1).png y movimiento(2i).png"""
    anims = []
    for i in range(1, 7):
        a = _load_or_placeholder(f"movimiento{2*i-1}.png", escala)
        b = _load_or_placeholder(f"movimiento{2*i}.png",   escala)
        anims.append([a, b])
    return anims

def Pantala_final_gano(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    font_big: pygame.font.Font,
    background: pygame.Surface,
    *,
    frame_ms: int = 200,
    escala_frames=(180,180),
    gap: int = 220,
    fila_y_offset: int = 180,
    overlay_alpha: int = 60,   # 0 = sin oscurecer
):
    """Pantalla de victoria: 6 muñecos animados en fila y dos textos."""
    W, H = screen.get_size()

    # Posiciones: fila centrada
    start_x = W//2 - (gap * (6-1))//2
    posiciones = [(start_x + i*gap, H//2 + fila_y_offset) for i in range(6)]

    # Animaciones (2 frames por sprite)
    anims = _build_animaciones(escala_frames)
    num_frames = 2
    estados = [{"idx": random.randrange(num_frames), "timer": random.randrange(frame_ms)} for _ in range(6)]

    # Textos
    titulo   = font_big.render("¡Marce llegó a CODE PRO!", True, (255,255,255))
    subtitulo= font_big.render("Hiciste que llegue a su destino BROO.", True, (255,255,255))
    sep = 20
    t_rect = titulo.get_rect(center=(W//2, H//2 - 300))
    s_rect = subtitulo.get_rect(center=(W//2, t_rect.bottom + sep))

    # Loop principal: sale con tecla o click
    while True:
        dt = clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return {'closed': True}
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return {'closed': False}

        # Avance de frames (independiente por sprite)
        for st in estados:
            st["timer"] += dt
            if st["timer"] >= frame_ms:
                st["timer"] = 0
                st["idx"] = (st["idx"] + 1) % num_frames

        # DIBUJO
        screen.blit(background, (0, 0))
        if overlay_alpha > 0:
            capa = pygame.Surface((W, H), pygame.SRCALPHA)
            capa.fill((0,0,0, max(0, min(255, overlay_alpha))))
            screen.blit(capa, (0,0))

        for i, frames in enumerate(anims):
            img = frames[estados[i]["idx"]]
            screen.blit(img, img.get_rect(center=posiciones[i]))

        screen.blit(titulo, t_rect)
        screen.blit(subtitulo, s_rect)
        pygame.display.flip()