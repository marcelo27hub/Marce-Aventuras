# cartas_game_mod.py
import pygame, random
from typing import Callable

def cartas_game(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    load_img: Callable[..., pygame.Surface],
    font: pygame.font.Font,
    font_big: pygame.font.Font,
    *,
    filas: int = 4,
    columnas: int = 4,
    tam_carta: int = 100,
    margen: int = 10,
    tiempo_total_ms: int = 40_000
) -> bool:
    """Juego de memoria: devuelve True si gana dentro del tiempo, False si no."""

    WIDTH, HEIGHT = screen.get_size()
    COLOR_TXT   = (255,255,255)
    COLOR_ROJO  = (255, 80, 80)
    COLOR_VERDE = (80, 255, 120)

    # --- assets (usa tu helper; las rutas son relativas a IMAGES_DIR) ---
    IMAGENES_CARTAS = {
        1: "imagenes/luji_cartas.png",
        2: "imagenes/tobi_cartas.png",
        3: "imagenes/maxi_cartas.png",
        4: "imagenes/edu_cartas.png",
        5: "imagenes/abi_cartas.png",
        6: "imagenes/marce_cartas.png",
        7: "imagenes/bici_cartas.png",
        8: "imagenes/pingu_cartas.png",
    }
    IMAGEN_DORSO = "imagenes/back_cartas.png"

    # Fondo (opcional)
    try:
        fondo = load_img("imagenes/fondo_cartas.png", scale=(WIDTH, HEIGHT), alpha=False)
    except Exception:
        fondo = pygame.Surface((WIDTH, HEIGHT)); fondo.fill((30, 30, 30))

    # Cargar imágenes y escalar
    def escalar(img: pygame.Surface) -> pygame.Surface:
        return pygame.transform.smoothscale(img, (tam_carta, tam_carta))

    try:
        dorso = escalar(load_img(IMAGEN_DORSO, alpha=True))
    except Exception:
        dorso = pygame.Surface((tam_carta, tam_carta), pygame.SRCALPHA)
        dorso.fill((60,60,60))

    imagenes = {}
    for k, ruta in IMAGENES_CARTAS.items():
        try:
            imagenes[k] = escalar(load_img(ruta, alpha=True))
        except Exception:
            imagenes[k] = dorso

    # Crear tablero
    num_pares = filas * columnas // 2
    claves = list(IMAGENES_CARTAS.keys())
    while len(claves) < num_pares:
        claves *= 2
    cartas = (claves[:num_pares]) * 2
    random.shuffle(cartas)

    tablero = []
    it = iter(cartas)
    for _ in range(filas):
        tablero.append([next(it) for __ in range(columnas)])

    descubiertas = [[False]*columnas for _ in range(filas)]

    # Layout
    ancho_tablero = columnas * tam_carta + (columnas + 1) * margen
    alto_tablero  = filas * tam_carta + (filas + 1) * margen
    offx = (WIDTH - ancho_tablero) // 2
    offy = (HEIGHT - alto_tablero) // 2
# cartas_game_mod.py
import pygame, random
from typing import Callable

def cartas_game(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    load_img: Callable[..., pygame.Surface],
    font: pygame.font.Font,
    font_big: pygame.font.Font,
    *,
    filas: int = 4,
    columnas: int = 4,
    tam_carta: int = 100,
    margen: int = 10,
    tiempo_total_ms: int = 40_000
) -> bool:
    """Juego de memoria: devuelve True si gana dentro del tiempo, False si no."""
    WIDTH, HEIGHT = screen.get_size()
    COLOR_TXT   = (255,255,255)
    COLOR_ROJO  = (255, 80, 80)
    COLOR_VERDE = (80, 255, 120)

    # --- RUTAS RELATIVAS A IMAGES_DIR (SIN SUBCARPETAS) ---
    IMAGENES_CARTAS = {
        1: "luji_cartas.png",
        2: "tobi_cartas.png",
        3: "maxi_cartas.png",
        4: "edu_cartas.png",
        5: "abi_cartas.png",
        6: "marce_cartas.png",
        7: "bici_cartas.png",
        8: "pingu_cartas.png",
    }
    IMAGEN_DORSO = "back_cartas.png"
    FONDO_CARTAS = "fondo_cartas.png"

    # Fondo (opcional)
    try:
        fondo = load_img(FONDO_CARTAS, scale=(WIDTH, HEIGHT), alpha=False)
    except Exception:
        fondo = pygame.Surface((WIDTH, HEIGHT)); fondo.fill((30, 30, 30))

    def escalar(img: pygame.Surface) -> pygame.Surface:
        return pygame.transform.smoothscale(img, (tam_carta, tam_carta))

    # Dorso
    try:
        dorso = escalar(load_img(IMAGEN_DORSO, alpha=True))
    except Exception:
        dorso = pygame.Surface((tam_carta, tam_carta), pygame.SRCALPHA)
        dorso.fill((60,60,60))

    # Cartas
    imagenes = {}
    for k, ruta in IMAGENES_CARTAS.items():
        try:
            imagenes[k] = escalar(load_img(ruta, alpha=True))
        except Exception:
            imagenes[k] = dorso  # fallback si falta alguna carta

    # --- Crear tablero ---
    num_pares = filas * columnas // 2
    claves = list(IMAGENES_CARTAS.keys())
    while len(claves) < num_pares:
        claves *= 2
    mazo = (claves[:num_pares]) * 2
    random.shuffle(mazo)

    tablero = []
    it = iter(mazo)
    for _ in range(filas):
        tablero.append([next(it) for __ in range(columnas)])

    descubiertas = [[False]*columnas for _ in range(filas)]

    # Layout
    ancho_tablero = columnas * tam_carta + (columnas + 1) * margen
    alto_tablero  = filas * tam_carta + (filas + 1) * margen
    offx = (WIDTH - ancho_tablero) // 2
    offy = (HEIGHT - alto_tablero) // 2

    def rect_celda(f, c):
        x = offx + margen + c * (tam_carta + margen)
        y = offy + margen + f * (tam_carta + margen)
        return pygame.Rect(x, y, tam_carta, tam_carta)

    def gano():
        return all(all(f) for f in descubiertas)

    seleccion = []
    esperando = False
    espera_ms = 0

    t0 = pygame.time.get_ticks()
    juego_terminado = False
    victoria = False

    while True:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not esperando and not juego_terminado:
                mx, my = e.pos
                # ¿qué celda tocó?
                for f in range(filas):
                    for c in range(columnas):
                        r = rect_celda(f, c)
                        if r.collidepoint(mx, my) and not descubiertas[f][c]:
                            descubiertas[f][c] = True
                            seleccion.append((f, c))
                            if len(seleccion) == 2:
                                esperando = True
                                espera_ms = 500
                            break

        if esperando:
            espera_ms -= dt
            if espera_ms <= 0:
                (f1, c1), (f2, c2) = seleccion
                if tablero[f1][c1] != tablero[f2][c2]:
                    descubiertas[f1][c1] = False
                    descubiertas[f2][c2] = False
                seleccion.clear()
                esperando = False

        # Tiempo
        t_rest = max(0, tiempo_total_ms - (pygame.time.get_ticks() - t0))
        if not juego_terminado:
            if gano():
                juego_terminado = True
                victoria = True
            elif t_rest <= 0:
                juego_terminado = True
                victoria = False

        # ---------- DRAW ----------
        screen.blit(fondo, (0, 0))

        # Título
        title = font.render("Encuentra los pares", True, COLOR_TXT)
        screen.blit(title, title.get_rect(midtop=(WIDTH//2, 18)))

        # Temporizador
        seg = t_rest // 1000
        tmp = font.render(f"Tiempo: {seg}", True, COLOR_TXT)
        screen.blit(tmp, tmp.get_rect(topright=(WIDTH-20, 18)))

        # Tablero
        for f in range(filas):
            for c in range(columnas):
                r = rect_celda(f, c)
                img = imagenes[tablero[f][c]] if descubiertas[f][c] else dorso
                screen.blit(img, r.topleft)
                pygame.draw.rect(screen, (255,255,255), r, 2)

        # Mensaje final
        if juego_terminado:
            color = COLOR_VERDE if victoria else COLOR_ROJO
            msg = "¡Felicidades, has ganado!" if victoria else "Se acabó tu tiempo, perdiste"
            label = font_big.render(msg, True, color)
            screen.blit(label, label.get_rect(midbottom=(WIDTH//2, HEIGHT-24)))

        pygame.display.flip()

        if juego_terminado:
            pygame.time.delay(1200)
            return victoria