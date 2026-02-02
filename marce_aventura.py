
import pygame, sys, math, random
from typing import List, Tuple
from pathlib import Path
from gana_juego import Pantala_final_gano
from pierde_juego import Pantala_final_perdio

#inicializar el mixer 
pygame.mixer.init()

#crear variable de sonidos
click_sonido = pygame.mixer.Sound('sonidos/click_sonido.wav')
golpe_sonido = pygame.mixer.Sound('sonidos/sonido_golpe.mp3')
game_over_sonido = pygame.mixer.Sound('sonidos/sonido_game_over.wav')
lluvia_sonido= pygame.mixer.Sound('sonidos/marce_sonido_lluvia.mp3')
#pollos_sonido_intro= pygame.mixer.Sound('sonidos/marce_pollos_minijuego_intro.wav')
lluvia_sonido= pygame.mixer.Sound('sonidos/marce_pollos_minijuego.wav')
musica_win = pygame.mixer.Sound('sonidos/musica_victoria.mp3')

#Funciones para reproducir MUSICAS
# --- Cargar la música principal ---
def play_main_music():
    # Detener cualquier música o sonido que se esté reproduciendo
    pygame.mixer.music.stop()
    game_over_sonido.stop()
    try:
        # Cargar y reproducir la música principal en un bucle
        pygame.mixer.music.load('sonidos/marce_inicio.wav') 
        pygame.mixer.music.play(-1)
        print("Reproduciendo música principal...")
    except pygame.error as e:
        print(f"No se pudo cargar la música principal: {e}")

# --- Cargar la música del minijuego ---
def play_bici_music():
    # Detener la música principal
    pygame.mixer.music.stop()
    try:
        # Cargar y reproducir la música del minijuego
        pygame.mixer.music.load('sonidos/marce_bici_minijuego.wav')
        pygame.mixer.music.play(-1)
        print("Reproduciendo música del minijuego...")
    except pygame.error as e:
        print(f"No se pudo cargar la música del minijuego: {e}")

#cargar la musica de victoria
def play_musica_win():
    # Detener cualquier música o sonido que se esté reproduciendo
    pygame.mixer.music.stop()
    try:
        # Cargar y reproducir la música principal en un bucle
        pygame.mixer.music.load('sonidos/musica_victoria.mp3') 
        pygame.mixer.music.play(-1)
        print("Reproduciendo música de victoria...")
    except pygame.error as e:
        print(f"No se pudo cargar la música de victoria: {e}")

#cargar la musica de la lluvia
def play_lluvia_music():
    # Detener cualquier música o sonido que se esté reproduciendo
    pygame.mixer.music.stop()
    game_over_sonido.stop()
    try:
        # Cargar y reproducir la música principal en un bucle
        pygame.mixer.music.load('sonidos/marce_sonido_lluvia.mp3') 
        pygame.mixer.music.play(-1)
        print("Reproduciendo música de lluvia...")
    except pygame.error as e:
        print(f"No se pudo cargar la música principal: {e}")

#musica minijuego pollos
def play_pollos_music():
    # Detener cualquier música o sonido que se esté reproduciendo
    pygame.mixer.music.stop()
    #reproducir el sonido de la intro
    #pollos_sonido_intro.play()
    try:
        # Cargar y reproducir la música principal en un bucle
        pygame.mixer.music.load('sonidos/marce_pollos_minijuego.wav') 
        pygame.mixer.music.play(-1)
        print("Reproduciendo música principal...")
    except pygame.error as e:
        print(f"No se pudo cargar la música principal: {e}")

#ganar minijuego pollos
def play_pollos_win_music():
    # Detener cualquier música o sonido que se esté reproduciendo
    pygame.mixer.music.stop()
    try:
        # Cargar y reproducir la música principal en un bucle
        pygame.mixer.music.load('sonidos/marce_pollos_minijuego_win.ogg') 
        pygame.mixer.music.play(-1)
        print("Reproduciendo música de pollos win...")
    except pygame.error as e:
        print(f"No se pudo cargar la música pollos win: {e}")

#musica bus minijuego
def play_bus_minijuego():
    # Detener cualquier música o sonido que se esté reproduciendo
    pygame.mixer.music.stop()
    try:
        # Cargar y reproducir la música principal en un bucle
        pygame.mixer.music.load('sonidos/marce_bus_minijuego.wav') 
        pygame.mixer.music.play(-1)
        print("Reproduciendo música de bus...")
    except pygame.error as e:
        print(f"No se pudo cargar la música bus: {e}")

def play_bus_descompuesto():
    # Detener cualquier música o sonido que se esté reproduciendo
    pygame.mixer.music.stop()
    try:
        # Cargar y reproducir la música principal en un bucle
        pygame.mixer.music.load('sonidos/marce_bus_descompuesto.mp3') 
        pygame.mixer.music.play(-1)
        print("Reproduciendo música de bus descompuesto...")
    except pygame.error as e:
        print(f"No se pudo cargar la música bus descompuesto: {e}")

# --------------- Paths base (una sola vez) --------------------
BASE_DIR   = Path(__file__).resolve().parent 
IMAGES_DIR = BASE_DIR / "images"
FONTS_DIR  = BASE_DIR / "fuentes"

def load_img(name: str, scale: tuple[int,int] | None = None, alpha: bool = True):
    """
    Carga una imagen desde IMAGES_DIR de forma segura, opcionalmente escalada.
    alpha=True -> convert_alpha(); alpha=False -> convert()
    """
    p = IMAGES_DIR / name
    if not p.exists():
        # mensaje útil para depurar
        raise FileNotFoundError(f"No se encontró la imagen: {p}\nCWD: {Path.cwd()}\nIMAGES_DIR: {IMAGES_DIR}")
    surf = pygame.image.load(str(p))
    surf = surf.convert_alpha() if alpha else surf.convert()
    if scale is not None:
        surf = pygame.transform.smoothscale(surf, scale)
    return surf


# ------------------ Utilidades UI ------------------

WIDTH, HEIGHT = 1370, 720
FPS = 60

pygame.init()
pygame.display.set_caption("Marce Aventure - Pygame")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Fuente pixel
FONT_FILE = FONTS_DIR / "fuente_pixel.ttf"   

if not FONT_FILE.exists():
    raise FileNotFoundError(f"No encuentro la fuente: {FONT_FILE}")

# Cargar la misma fuente en tres tamaños
FONT      = pygame.font.Font(str(FONT_FILE), 23)
FONT_BIG  = pygame.font.Font(str(FONT_FILE), 10)
FONT_SMALL= pygame.font.Font(str(FONT_FILE), 5)
FONT_grandote= pygame.font.Font(str(FONT_FILE), 40)
FONT_HUGE = pygame.font.Font(str(FONT_FILE), 35)

#---------------- Sector Imagenes -----------------------------
#Cargar la imagen en la pantalla principal
IMG_PATH = IMAGES_DIR / "fondo_inicio.png"

pantalla_inicio = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
pantalla_inicio = pygame.transform.scale(pantalla_inicio, (WIDTH, HEIGHT))

#Cargar el fondo predeterminado del juego
IMG_PATH = IMAGES_DIR / "fondo_juego.png"

pantalla = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
pantalla = pygame.transform.scale(pantalla, (WIDTH, HEIGHT))

#Fondos especificos
IMG_PATH = IMAGES_DIR/ "fondo_bici.png"

fondo_bici = pygame.image.load(str(IMG_PATH))
fondo_bici = pygame.transform.scale(fondo_bici, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_lluvioso.png"

fondo_lluvioso = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_lluvioso = pygame.transform.scale(fondo_lluvioso, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR / "robo.png"

robo = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
robo = pygame.transform.scale(robo, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "parada_autobus.png"

parada_autobus = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
parada_autobus = pygame.transform.scale(parada_autobus, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "anciana.png"

anciana = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
anciana = pygame.transform.scale(anciana, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "bus_descompuesto.png"

bus_descompuesto = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
bus_descompuesto = pygame.transform.scale(bus_descompuesto, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "arreglar_bici.png"

arreglar_bici = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
arreglar_bici = pygame.transform.scale(arreglar_bici, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_llamada.png"

fondo_llamada = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_llamada = pygame.transform.scale(fondo_llamada, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "penguin_pechuga.png"

penguin_pechuga = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
penguin_pechuga = pygame.transform.scale(penguin_pechuga, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_gana.png"

fondo_ganar = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_ganar = pygame.transform.scale(fondo_ganar, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_acertijo_2.png"

fondo_acertijo2 = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_acertijo2 = pygame.transform.scale(fondo_acertijo2, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "juego_maxi_fondo.png"

juego_maxi_fondo = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
juego_maxi_fondo = pygame.transform.scale(juego_maxi_fondo, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "maxi2_fondo.png"

maxi2_fondo = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
maxi2_fondo = pygame.transform.scale(maxi2_fondo, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_juego2.png"

fondo_juego2 = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_juego2 = pygame.transform.scale(fondo_juego2, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "abi_tobi_fondo.png"

abi_tobi_fondo = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
abi_tobi_fondo = pygame.transform.scale(abi_tobi_fondo, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "abi_tobi_radio.png"

abi_tobi_radio = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
abi_tobi_radio = pygame.transform.scale(abi_tobi_radio, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "marce_heroe.png"

marce_heroe = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
marce_heroe = pygame.transform.scale(marce_heroe, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "penguin_pechuga2.png"

penguin_pechuga2 = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
penguin_pechuga2 = pygame.transform.scale(penguin_pechuga2, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "abi_tobi_fondo_pierde.png"

abi_tobi_fondo_pierde = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
abi_tobi_fondo_pierde = pygame.transform.scale(abi_tobi_fondo_pierde, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "off_puente_fondo.png"

off_puente_fondo = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
off_puente_fondo = pygame.transform.scale(off_puente_fondo, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_robo.png"

fondo_robo = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_robo = pygame.transform.scale(fondo_robo, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_maxi.png"

fondo_maxi = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_maxi = pygame.transform.scale(fondo_maxi, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_instr_radio.png"

fondo_instr_radio = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_instr_radio = pygame.transform.scale(fondo_instr_radio, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "marce_villano.png"

marce_villano = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
marce_villano = pygame.transform.scale(marce_villano, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "marce_maxi.jpeg"

marce_maxi = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
marce_maxi = pygame.transform.scale(marce_maxi, (WIDTH, HEIGHT))

IMG_PATH = IMAGES_DIR/ "fondo_cartas.png"

fondo_cartas = pygame.image.load(str(IMG_PATH))# para que cubra toda la pantalla
fondo_cartas = pygame.transform.scale(fondo_cartas, (WIDTH, HEIGHT))



#-----------------------------------------------------------------

def draw_text(surf, text, x, y, font=FONT, color=(230,230,230), center=True, center_screen=False):
    render = font.render(text, True, color)
    rect = render.get_rect()
    
    if center_screen:
        rect.center = (WIDTH // 2, HEIGHT // 2)
    elif center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    
    surf.blit(render, rect)
    return rect

class Button:
    def __init__(self, rect: pygame.Rect, label: str, key_hint: str = ""):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.key_hint = key_hint

    def draw(self, surf):
        #recuadro de los botones
        pygame.draw.rect(surf, (78, 152, 216), self.rect)
        pygame.draw.rect(surf, (10,10,10), self.rect, 2)
        txt = f"{self.key_hint} {self.label}".strip()

        #texto de los botones
        draw_text(surf, txt, self.rect.centerx, self.rect.centery, FONT_BIG, (0,0,0), center=True)

    def hit(self, pos):
        return self.rect.collidepoint(pos)

def wait_keypress(pred=None):
    """Bloquea hasta recibir un evento de teclado o cerrar."""
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if pred is None or pred(e):
                    return e
            if e.type == pygame.MOUSEBUTTONDOWN:
                return e
        clock.tick(60)

# ------------------ Estados de historia ------------------

karma = 0
finales_ganados = 0
finales_perdidos = 0

# ------------------ Pantallas auxiliares --------------------
def show_message(
    lines: List[str],
    buttons: List[Tuple[str,str]] = None,
    bg=None,
    *,
    y_anchor: str = "center",   # "center" | "top" | "bottom"
    y: int = 0,                 # offset en píxeles según el ancla
    spacing: int = 45,          # separación entre líneas
    font=FONT,
    color=(0,0,0),
):
    if buttons is None:
        buttons = [("ENTER", "Continuar")]

    if isinstance(bg, pygame.Surface):
        fondo = bg
    elif bg == "menu":
        fondo = pantalla_inicio
    else:
        fondo = pantalla

    while True:
        screen.blit(fondo, (0, 0))

        # --- bloque de texto centrado en X, con control de altura ---
        total_h = len(lines) * spacing
        if y_anchor == "center":
            start_y = HEIGHT // 2 - total_h // 2 + y
        elif y_anchor == "top":
            start_y = 0 + y
        elif y_anchor == "bottom":
            start_y = HEIGHT - total_h - y
        else:
            start_y = HEIGHT // 2 - total_h // 2  # fallback

        for line in lines:
            draw_text(screen, line, WIDTH // 2, start_y, font, color, center=True, center_screen=False)
            start_y += spacing

        # Botones
        btn_objs = []
        BTN_W, BTN_H = 260, 50
        if len(buttons) == 2:
            (hot1, label1), (hot2, label2) = buttons
            rect_left  = pygame.Rect(60, HEIGHT - 100, BTN_W, BTN_H)
            rect_right = pygame.Rect(WIDTH - 60 - BTN_W, HEIGHT - 100, BTN_W, BTN_H)
            btn_left  = Button(rect_left,  label1, f"[1]")
            btn_right = Button(rect_right, label2, f"[2]")
            btn_left.draw(screen); btn_right.draw(screen)
            btn_objs = [btn_left, btn_right]
        else:
            total_h = len(buttons) * (BTN_H + 12) - 12
            start_y = HEIGHT - total_h - 60
            for i, (hot, label) in enumerate(buttons):
                rect = pygame.Rect(WIDTH//2 - BTN_W//2, start_y + i*(BTN_H+12), BTN_W, BTN_H)
                btn = Button(rect, label, f"[{i+1}]")
                btn.draw(screen)
                btn_objs.append(btn)

        pygame.display.flip()

        # ----- EVENTOS -----
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if (e.key in (pygame.K_RETURN, pygame.K_KP_ENTER)) and len(buttons) == 1:
                    return 0
                if pygame.K_1 <= e.key <= pygame.K_9:
                    idx = e.key - pygame.K_1
                    if idx < len(buttons): return idx
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                for i, b in enumerate(btn_objs):
                    if b.hit((mx, my)): return i

        clock.tick(60)

# ------------------ Minijuego: Bici Runner ------------------

from bici_runner_mod import bici_runner
from acertijos_game_mod import acertijos_game
from penguin_pechuga_mod import pollo_runner

#------------------- Pantalla de cargando --------------------

def pantalla_cargando(duracion_ms: int = 2500, usar_fondo_menu: bool = True, fondo: str = fondo_juego2):
    """
    Muestra una pantalla de 'Cargando...' con una mini-animación por 'duracion_ms' milisegundos
    o hasta que el usuario presione una tecla/click (lo que ocurra primero).
    Requiere: screen, clock, WIDTH, HEIGHT, FPS, FONT (globales).
    """
    # --- prepara frames ---
    frames = []
    for i in range(1, 5):
        # ajusta la ruta/nombre exactamente a tus archivos
        # si usás nuestra helper:
        frame = load_img(f"imagen{i}.png", scale=(250, 250), alpha=True)
        frames.append(frame)

    # Texto
    texto = FONT.render("Cargando...", True, (255, 255, 255))

    # Opcional: fondo borroso/oscurecido (usamos tu 'pantalla' si querés)
    fondo_base = None
    if usar_fondo_menu:
        try:
            # reutilizamos 'pantalla' si existe, si no, dejamos negro
            fondo_base = fondo.copy()
        except Exception:
            fondo_base = None

    # Timers
    elapsed = 0
    frame_timer = 0
    frame_idx = 0
    FRAME_MS = 140  # velocidad de animación

    # Permitir salir antes si el user toca algo
    salir_antes = False

    while elapsed < duracion_ms and not salir_antes:
        dt_ms = clock.tick(FPS)
        elapsed += dt_ms
        frame_timer += dt_ms

        # Eventos (permitimos cerrar o saltar)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                salir_antes = True

        # Avance de animación
        if frame_timer >= FRAME_MS:
            frame_idx = (frame_idx + 1) % len(frames)
            frame_timer = 0

        # DIBUJO
        if fondo_base is not None:
            screen.blit(fondo_base, (0, 0))
            # oscurecer un toque para que resalte el loader
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 140))
            screen.blit(s, (0, 0))
        else:
            screen.fill((0, 0, 0))


        img = frames[frame_idx]
        # Posicionar imagen abajo a la izquierda
        img_rect = img.get_rect()
        img_rect.bottomleft = (50, HEIGHT + 10)  # 50 px desde izquierda y abajo
        screen.blit(img, img_rect)

        # Posicionar texto a la derecha de la imagen, alineado verticalmente al centro de la imagen
        text_rect = texto.get_rect()
        text_rect.midleft = (img_rect.right - 10, img_rect.centery + 60)
        screen.blit(texto, text_rect)

        pygame.display.flip()

# ------------------ Minijuego: Bus Runner ------------------
from bus_runner_mod import bus_runner
from cartas_games_mod import cartas_game
from radio_minijuego import run_radio_minigame


# ------------------ Flujo principal (Historia) ------------------

def main_menu():
    # Botones a los costados
    BTN_W, BTN_H = 260, 56
    jugar_btn = Button(pygame.Rect(60, HEIGHT - 100, BTN_W, BTN_H), "Jugar", "[1]")
    salir_btn = Button(pygame.Rect(WIDTH - 60 - BTN_W, HEIGHT - 100, BTN_W, BTN_H), "Salir", "[2]")

    while True:
        # ---- Eventos ----
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_1, pygame.K_RETURN, pygame.K_KP_ENTER):
                    return True
                if e.key in (pygame.K_2, pygame.K_ESCAPE):
                    pygame.quit(); sys.exit(0)
            if e.type == pygame.MOUSEBUTTONDOWN:
                click_sonido.play()
                if jugar_btn.hit(e.pos):
                    return True
                if salir_btn.hit(e.pos):
                    pygame.quit(); sys.exit(0)

        # ---- Dibujo ----
        screen.blit(pantalla_inicio, (0, 0))              # fondo completo

        # sin caja, sin párrafos — solo botones
        jugar_btn.draw(screen)
        salir_btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

def intro_historia():

    show_message([
        "Prepárate para acompañar a Marce,","un joven de 21 años con más energía que una","laptop recién cargada y más determinación que un","programador antes de un deadline..."])
    click_sonido.play()
    show_message(["Tiene un solo objetivo: llegar a ","CodePRO."])
    click_sonido.play()
    show_message(["Ubicación: New Italy. ","¿Listo para acompañarlo en esta ","travesía épica?"],[("1","Listo")])
    click_sonido.play()

def elegir_transporte():
    idx = show_message(["¿Cómo viajamos?"], [("1","Ir en bicicleta"), ("2","Ir en colectivo")])
    click_sonido.play()
    return idx  # 0 bici, 1 bus

def ruta_bici():
    global karma, finales_ganados, finales_perdidos
    show_message(["Minijuego: Bici Runner (30s).", "Salta con ESPACIO o ↑."])
    click_sonido.play()
    # >>> NUEVO: loader <<<
    pantalla_cargando(duracion_ms=2200, fondo=fondo_bici)
    play_bici_music()
    r = bici_runner(screen, clock, load_img, FONT, FONT, fps=FPS, duration_ms=30_000)
    if not r["win"]:
        pygame.mixer.music.stop()
        game_over_sonido.play()
        finales_perdidos += 1
        show_message(["Te chocaste en la bici.","Marce decide volver y pierde tiempo.", "Fin del juego."], y=-230)
        click_sonido.play()
        Pantala_final_perdio(
                screen, clock, FONT_HUGE, fondo_bici,
                frame_ms=220,           # más lento el “parpadeo”
                escala_frames=(240,240),
                gap=220,
                fila_y_offset=220,
                overlay_alpha=120,       # 0 si no querés oscurecer el fondo
            )
        return False

    idx = show_message(["En el camino, la bici de Marce llanta...","¿Arreglar solo o pedir ayuda?"], [("1","Arreglar solo"), ("2","Pedir ayuda")],fondo_bici,y=-200)
    click_sonido.play()
    if idx == 0:
        karma += 1
        show_message(["Marce arregla la bici con su mini-kit","y sigue."],bg = arreglar_bici, y=-260)
        click_sonido.play()
        show_message(["Otra sección del Bici Runner (15s). ","¡A pedalear de nuevo!"],bg = fondo_bici, y=-230)
        click_sonido.play()
        pantalla_cargando(duracion_ms=2200, fondo=fondo_bici)
        play_bici_music()
        r2 = bici_runner(screen, clock, load_img, FONT, FONT, fps=FPS, duration_ms=15_000)
        if not r2["win"]:
            pygame.mixer.music.stop()
            game_over_sonido.play()
            finales_perdidos += 1
            show_message(["Uy, otro tortazo. Marce pierde tiempo.", "Fin del juego."],bg = fondo_bici,y=-230)
            click_sonido.play()
            Pantala_final_perdio(
                screen, clock, FONT_HUGE, fondo_bici,
                frame_ms=220,           # más lento el “parpadeo”
                escala_frames=(240,240),
                gap=220,
                fila_y_offset=220,
                overlay_alpha=120,       # 0 si no querés oscurecer el fondo
            )
            return False

        play_lluvia_music()
        idx2 = show_message(["En el camino, empieza una fuerte lluvia...:","¿Seguir o resguardarse?"], [("1","Seguir"), ("2","Resguardarse")], fondo_lluvioso,y=-200)
        click_sonido.play()
        if idx2 == 0:
            finales_ganados += 1
            # Minijuego del acertijo
            try:
                fondo_acertijos = load_img("fondo_acertijo.png", scale=(WIDTH, HEIGHT), alpha=False)
            except Exception:
                fondo_acertijos = pantalla  # fallback

            show_message([
                           "Marce sigue su camino bajo la lluvia",
                           "Llega a un viejo puente de madera",
                           "cubierto por una neblina misteriosa"], bg=fondo_acertijos, color=(0,0,0))
            click_sonido.play()
            show_message(["Aparece Luji “la guardiana del puente” y le dice:",
                           "“Para cruzar este puente debes responder","al menos 2 acertijos.",
                           "Si respondes bien, podrás pasar.",
                           "Si fallas… bueno, mejor que te guste nadar.”"], bg=fondo_acertijo2, color=(0,0,0))
            click_sonido.play()
            
            pantalla_cargando(duracion_ms=2200, fondo=fondo_acertijo2)
            ok = acertijos_game(screen, clock, load_img, FONT, FONT_BIG)
            if ok:
                finales_ganados += 1
                show_message(["Luji sonríe  y el puente se ilumina.","Marce cruza sin problemas y sigue su camino","hacia CoderPRO.","Felicidades Ganaste."], bg=fondo_acertijo2)
                click_sonido.play()
                play_musica_win()
                Pantala_final_gano(
                    screen, clock, FONT_HUGE, fondo_ganar,
                    frame_ms=220,           # más lento el “parpadeo”
                    escala_frames=(240,240),
                    gap=220,
                    fila_y_offset=220,
                    overlay_alpha=120,       # 0 si no querés oscurecer el fondo
                )
                return True
            else:
                pygame.mixer.music.stop()
                game_over_sonido.play()
                finales_perdidos += 1
                show_message(["Luji saca la lengua, el puente se vuelve invisible","y Marce cae al río.","Pierde tiempo, se moja más, y cuando logra salir ","ya es demasiado tarde para llegar.","Pierde y Fin del Juego"], bg=off_puente_fondo)
                click_sonido.play()
                Pantala_final_perdio(
                    screen, clock, FONT_HUGE, fondo_acertijos,
                    frame_ms=220,           # más lento el “parpadeo”
                    escala_frames=(240,240),
                    gap=220,
                    fila_y_offset=220,
                    overlay_alpha=120,       # 0 si no querés oscurecer el fondo
                )
                return False
            return True
        else:
        # === Evento lluvia: Penguin Pechugas ===
            try:
                fondo_pp = load_img("fondo_penguin_pechuga.png", scale=(WIDTH, HEIGHT), alpha=False)
            except Exception:
                fondo_pp = pantalla  # fallback

            # Mensajes previos en BLANCO
            show_message(["Encuentra Penguin Pechugas,  Marce decide resguardarse"], bg=penguin_pechuga, y=-200, color=(255,255,255))
            click_sonido.play()
            show_message([
                "Allí encuentra a su amigo Edu, quien le dice:",
                "“Si me ayudas un rato te daré una recompensa",
                "si lo haces mal te echo de nuevo a la calle”."
            ], bg=fondo_pp, color=(255,255,255))
            click_sonido.play()
            show_message([
                "Marce debe atrapar 15 pollos en un tiempo de 30 segundos.",
                "Evitá atrapar la basura o te traerá problemas.",
                "¿Listo?"
            ], bg=fondo_pp, y=-150, color=(255,255,255))
            click_sonido.play()
            # (Opcional) pequeña pantalla de carga
            pantalla_cargando(duracion_ms=1200, usar_fondo_menu=False, fondo=fondo_pp)

            # Minijuego: 30s, meta 15
            play_pollos_music()
            r_pp =  pollo_runner(screen, clock, load_img, FONT, FONT_BIG, duration_s=30, target=15)

            if r_pp["win"]:
                pygame.mixer.music.stop()
                play_pollos_win_music()
                finales_perdidos += 1  # final perdedor por historia
                show_message([
                    "Lo hace bien y Edu le ofrece trabajar en “Penguin Pechugas”",
                    "Marce se queda feliz comiendo pechugas y alitas ",
                    "Nunca llega a codePRO por el amor a la comida.",
                    "Pierde y fin del juego."
                ], bg=fondo_pp, color=(255,255,255))
                click_sonido.play()
                Pantala_final_perdio(
                    screen, clock, FONT_HUGE, penguin_pechuga2,
                    frame_ms=220,           # más lento el “parpadeo”
                    escala_frames=(240,240),
                    gap=220,
                    fila_y_offset=220,
                    overlay_alpha=120,       # 0 si no querés oscurecer el fondo
                )
                return False
            else:
                pygame.mixer.music.stop()
                game_over_sonido.play()
                finales_perdidos += 1
                show_message([
                    "Marce no atrapa la cantidad de pollos requeridos.",
                    "Edu lo echa del local",
                    "lo deja afuera bajo la lluvia y Marce se queda triste.",
                    "Nada salió bien.",
                    "Marce se queda sin comida, sin trabajo y sin codePRO.",
                    "Pierde y fin del juego."
                ], bg=fondo_pp, color=(255,255,255))
                click_sonido.play()
                Pantala_final_perdio(
                    screen, clock, FONT_HUGE, penguin_pechuga2,
                    frame_ms=220,           # más lento el “parpadeo”
                    escala_frames=(240,240),
                    gap=220,
                    fila_y_offset=220,
                    overlay_alpha=120,       # 0 si no querés oscurecer el fondo
                )
                return False
    else:
        pygame.mixer.music.stop()
        game_over_sonido.play()
        finales_perdidos += 1
        show_message(["Le pidió ayuda a un 'señor'.","Plot twist: era un ladrón. Chau bici, chau CodePRO.","Pierde y fin del juego."], bg=robo, y=-240)
        click_sonido.play()
        Pantala_final_perdio(
            screen, clock, FONT_HUGE, fondo_robo,
            frame_ms=220,           # más lento el “parpadeo”
            escala_frames=(240,240),
            gap=220,
            fila_y_offset=220,
            overlay_alpha=120,       # 0 si no querés oscurecer el fondo
        )
        return False

def ruta_bus():
    global karma, finales_ganados, finales_perdidos

    show_message(["Viaje en colectivo..."],bg=parada_autobus,y=-163)
    click_sonido.play()
    show_message(["Manejar el Colectivo. ¡Evita chocar por 30 segundos!"],bg=parada_autobus, y=-163)
    click_sonido.play()
    # >>> NUEVO: loader <<<
    pantalla_cargando(duracion_ms=2200, fondo=parada_autobus)
    play_bus_minijuego()
    result = bus_runner(screen, clock, load_img, FONT, FONT_grandote, fps=FPS, duration_ms=30_000) 
    if not result["win"]:
        pygame.mixer.music.stop()
        game_over_sonido.play()
        finales_perdidos += 1
        show_message(["Te la diste contra otro auto. CodePRO queda lejos.", "Pierde y fin del juego."], bg=parada_autobus, y=-230)
        click_sonido.play()
        Pantala_final_perdio(
            screen, clock, FONT_HUGE, parada_autobus,
            frame_ms=220,           # más lento el “parpadeo”
            escala_frames=(240,240),
            gap=220,
            fila_y_offset=220,
            overlay_alpha=120,       # 0 si no querés oscurecer el fondo
        )
        return False
    else:
        show_message(['GANASTE'],bg=parada_autobus)
        click_sonido.play()

    
    idx = show_message(["El colectivo se llena y una anciana queda de pie junto a ti","¿Actúas como un héroe… o como un cojín egoísta?"], [("1","Héroe"), ("2","Egoísta")],bg=anciana, y=-240,font=FONT)
    click_sonido.play()
    if idx == 0:
        karma += 1
        show_message(["Marce, héroe del día."],bg=marce_heroe, y=-230)
        click_sonido.play()
    else:
        karma -= 1
        show_message(["Marce, villano del día."], bg=marce_villano, y=-230)
        click_sonido.play()

    play_bus_descompuesto()
    show_message(["El colectivo se descompone.","Marce tiene que pedir ayuda."],bg=bus_descompuesto,y=-250)
    click_sonido.play()
    idx2 = show_message(["¿A quién llama?"], [("1","Llamar a Maxi"), ("2","Llamar a Tobi")],bg=fondo_llamada, y=-300)
    click_sonido.play()
    if idx2 == 0:
        # Mensaje previo antes del juego de cartas
        show_message([
            "Desesperado por el calor en medio de la calle",
            "decide llamar a Maxi para que lo recoja y",
            "lleguen juntos a CodePRO"
        ],bg=juego_maxi_fondo, y=-230)
        click_sonido.play()
        show_message(["Pero Maxi con una sonrisa le dice:",
            "“Tendrás que ganarte mi ayuda.","Te propongo un pequeño juego de cartas.",
            "Si logras vencerme, iré de inmediato a recogerte.”"], bg=maxi2_fondo, y=-230)
        click_sonido.play()

        # JUEGO DE CARTAS
        pantalla_cargando(duracion_ms=2200, fondo=fondo_cartas)
        cartas = cartas_game(screen, clock, load_img, FONT, FONT_BIG)

        if cartas:
            finales_ganados += 1
            show_message([
                "¡Lo logra y sube al auto de Maxi!",
                "Entre risas llegan a CodePRO, listos para","la hackaton que se viene.",
                "Marce logra llegar a CodePRO. ¡Gana y fin del juego!"
            ],bg=marce_maxi, color=(255,255,255), y=-240)
            click_sonido.play()
            play_musica_win()
            Pantala_final_gano(
                screen, clock, FONT_HUGE, fondo_ganar,
                frame_ms=220,           # más lento el “parpadeo”
                escala_frames=(240,240),
                gap=220,
                fila_y_offset=220,
                overlay_alpha=120,       # 0 si no querés oscurecer el fondo
            )
            click_sonido.play()
            return True
        else:
            pygame.mixer.music.stop()
            game_over_sonido.play()
            finales_perdidos += 1
            show_message([
                "No lo consigue y Maxi le dice:",
                "“Tranqui, la próxima te llevo… si barajas mejor.”",
                "Marce pierde tiempo bajo el sol y no llega a CodePRO.",
                "Pierde y fin del juego."
            ])
            click_sonido.play()
            Pantala_final_perdio(
                screen, clock, FONT_HUGE, fondo_maxi,
                frame_ms=220,           # más lento el “parpadeo”
                escala_frames=(240,240),
                gap=220,
                fila_y_offset=220,
                overlay_alpha=120,       # 0 si no querés oscurecer el fondo
            )
            return False
    else:
        show_message(["Tobi y Abi llegan para buscar a Marce"], bg=abi_tobi_fondo, y=-300)
        click_sonido.play()
        show_message(["Tobi le dice a Marce que debe elegir una canción","que le guste, así para continuar el camino."], bg=abi_tobi_radio, y=-280,color=(255,255,255))
        click_sonido.play()
        show_message(["Marce debe de sintonizar una emisora de radio,","puede encontrar 3: ","Radio Chill: Música extra"," Radio Buena: Música correcta","Radio Mala: Te hará perder."],bg=fondo_instr_radio, y=-100)
        click_sonido.play()
        pygame.mixer.stop()  # por si tenés música sonando en Marce
        pantalla_cargando(duracion_ms=2200, fondo=fondo_instr_radio)
        resultado_radio = run_radio_minigame(
            screen,
            BASE_DIR,                     # carpeta donde están tus assets
            FONTS_DIR / "fuente_pixel.ttf" # fuente pixel
        )

        # Después decidís qué hacer según el resultado
        if resultado_radio == "won":
            show_message(["Lo lograste, pusiste la musica que a tobi le agrada"])
            click_sonido.play()
            finales_ganados += 1
            play_musica_win()
            Pantala_final_gano(
                screen, clock, FONT_HUGE, fondo_ganar,
                frame_ms=220,           # más lento el “parpadeo”
                escala_frames=(240,240),
                gap=220,
                fila_y_offset=220,
                overlay_alpha=120,       # 0 si no querés oscurecer el fondo
            )

        elif resultado_radio == "lost":
            game_over_sonido.play()
            show_message(["A tobi no le gustó la cación y lo echó..."])
            click_sonido.play()
            Pantala_final_perdio(
                screen, clock, FONT_HUGE, abi_tobi_fondo_pierde,
                frame_ms=220,           # más lento el “parpadeo”
                escala_frames=(240,240),
                gap=220,
                fila_y_offset=220,
                overlay_alpha=120,       # 0 si no querés oscurecer el fondo
            )
        elif resultado_radio == "cancelled":
            print("El jugador salió del minijuego")

def resumen_final():
    lines = [
        f"Finales ganados: {finales_ganados}",
        f"Finales perdidos: {finales_perdidos}",
    ]
    show_message(lines, [("ENTER","Salir")])
    click_sonido.play()

def main():
    while True:
        if not main_menu(): return
        intro_historia()
        elec = elegir_transporte()
        if elec == 0:
            ruta_bici()
        else:
            ruta_bus()
        resumen_final()
        # ¿Reintentar?
        idx = show_message(["¿Querés volver al menú?"], [("1","Sí"), ("2","No, cerrar")])
        play_main_music()
        if idx == 1:
            pygame.quit(); sys.exit(0)

if __name__ == "__main__":
    play_main_music()
    try:
        main()
    finally:
        pygame.quit()
        
