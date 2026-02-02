# radio_minigame_blocking.py
import pygame
from pygame import Rect
from pathlib import Path

def run_radio_minigame(screen: pygame.Surface,
                       assets_dir: Path,
                       font_path: Path | None = None,
                       exit_on_win: bool = False,
                       exit_on_lose: bool = False) -> str:
    """
    Corre el minijuego de radio en modo bloqueante dentro de tu juego principal (Marce).
    Devuelve: "won" | "lost" | "cancelled"
    """
    # ------------------ CONFIG ------------------
    WINDOW_W, WINDOW_H = screen.get_size()
    PIXEL_W, PIXEL_H   = 320, 180
    SCALE_X, SCALE_Y   = WINDOW_W // PIXEL_W, WINDOW_H // PIXEL_H
    FPS = 60

    DIAL_MIN, DIAL_MAX = 88.0, 108.0
    PASO_GRUESO, PASO_FINO = 0.2, 0.05
    TOLERANCIA = 0.15
    MS_MENSAJE_ENCONTRADA = 1300
    VOLUMEN_ESTATICA_MAX = 0.35

    FONT_SIZE = 10
    STATIC_PATH = assets_dir / "images" / "interferencia_radio.mp3"

    # Estaciones: izquierda = perdés, medio = neutral, derecha = ganás
    STATIONS = [
        {"frecuencia": 90.5,  "nombre": "Radio mala FM",
         "sonido": str(assets_dir / "images" / "solito.mp3"),
         "comienzo": 8.0,   "duracion_ms": 5000, "volumen": 0.50, "mensaje_ms": 5000},
        {"frecuencia": 97.3,  "nombre": "Radio Chill 97.3",
         "sonido": str(assets_dir / "images" / "onda.mp3"),
         "comienzo": 0.0,    "duracion_ms": 5000, "volumen": 0.50, "mensaje_ms": 5000},
        {"frecuencia": 103.9, "nombre": "Radio buena FM",
         "sonido": str(assets_dir / "images" / "ruta1.mp3"),
         "comienzo": 0.0, "duracion_ms": 5000, "volumen": 0.50, "mensaje_ms": 5000},
    ]

    # ------------------ PALETA ------------------
    COL_SKY1   = (120, 174, 232); COL_SKY2   = (84, 132, 201); COL_NUBE   = (235, 245, 255)
    COL_TABLERO= (26, 28, 34);   COL_PARAB  = (40, 45, 54);   COL_MARCO  = (18, 20, 26)
    COL_VOLANTE= (20, 22, 28);   COL_VOL_BRD= (60, 65, 80)
    COL_RADIO_BG  = (18, 19, 23); COL_RADIO_FR  = (44, 47, 58); COL_RADIO_BRD = (190, 190, 210)
    COL_TEXT      = (240, 240, 255); COL_TEXT_DIM  = (210, 210, 230)
    COL_ACCENT    = (255, 230, 120)
    COL_SIGNAL    = (90, 200, 120); COL_SIGNAL_BG = (40, 40, 48)

    # ------------------ HELPERS ------------------
    def clamp(x,a,b): return max(a, min(b, x))
    def dentro_tolerancia(freq, objetivo): return abs(freq - objetivo) <= TOLERANCIA

    def fuerza_senal(freq, objetivos):
        if not objetivos: return 0.0
        dmin = min(abs(freq - f) for f in objetivos)
        if dmin <= TOLERANCIA: return 1.0
        maxd = TOLERANCIA * 5.0
        return clamp(1.0 - (dmin - TOLERANCIA)/maxd, 0.0, 1.0)

    def roles_por_posicion(stations):
        orden = sorted(stations, key=lambda s: s["frecuencia"])
        roles = {}
        if len(orden) >= 1: roles[orden[0]["frecuencia"]] = "bad"
        if len(orden) >= 2: roles[orden[1]["frecuencia"]] = "neutral"
        if len(orden) >= 3: roles[orden[2]["frecuencia"]] = "good"
        return roles

    def draw_pixel_text(surf, font, text, x, y, color=COL_TEXT, center=False):
        img = font.render(text, False, color)
        r = img.get_rect(center=(x,y)) if center else img.get_rect(topleft=(x,y))
        surf.blit(img, r)

    def draw_car_interior(world):
        W, H = world.get_size()
        pygame.draw.rect(world, COL_SKY1, Rect(0, 0, W, H//2))
        pygame.draw.rect(world, COL_SKY2, Rect(0, H//2 - 10, W, H//2 - 30))
        for x,y,w,h in [(30,18,28,10),(60,14,24,12),(120,20,38,12),(190,28,28,10),(230,16,26,10)]:
            pygame.draw.rect(world, COL_NUBE, Rect(x,y,w,h))
        pygame.draw.rect(world, COL_PARAB, Rect(0, 0, W, 20))
        pygame.draw.rect(world, COL_PARAB, Rect(0, H-60, W, 60))
        pygame.draw.rect(world, COL_PARAB, Rect(0, 0, 12, H))
        pygame.draw.rect(world, COL_PARAB, Rect(W-12, 0, 12, H))
        pygame.draw.rect(world, COL_TABLERO, Rect(0, H-48, W, 48))
        pygame.draw.rect(world, COL_MARCO, Rect(0, H-52, W, 4))
        cx, cy, r = 48, H-16, 40
        pygame.draw.circle(world, COL_VOLANTE, (cx, cy), r)
        pygame.draw.circle(world, COL_TABLERO, (cx, cy+6), r-8)
        pygame.draw.circle(world, COL_VOL_BRD, (cx, cy), r, 1)

    def draw_radio_module(world, font):
        W, H = world.get_size()
        radio_w, radio_h = 200, 80
        radio_x, radio_y = (W - radio_w)//2, H - 46 - radio_h
        body = Rect(radio_x, radio_y, radio_w, radio_h)

        pygame.draw.rect(world, COL_RADIO_FR, body)
        pygame.draw.rect(world, COL_RADIO_BRD, body, 1)

        disp = Rect(body.x+8, body.y+6, body.w-16, 16)
        pygame.draw.rect(world, COL_RADIO_BG, disp)
        pygame.draw.rect(world, COL_RADIO_BRD, disp, 1)

        knob_r = 6
        pygame.draw.circle(world, COL_RADIO_BG, (body.x+10, body.y+body.h-12), knob_r)
        pygame.draw.circle(world, COL_RADIO_BRD, (body.x+10, body.y+body.h-12), knob_r, 1)
        pygame.draw.circle(world, COL_RADIO_BG, (body.right-10, body.y+body.h-12), knob_r)
        pygame.draw.circle(world, COL_RADIO_BRD, (body.right-10, body.y+body.h-12), knob_r, 1)

        dial_y = disp.bottom + 12
        dial_x1, dial_x2 = body.x+12, body.right-12
        pygame.draw.line(world, COL_TEXT_DIM, (dial_x1, dial_y), (dial_x2, dial_y), 1)
        for i in range(int((DIAL_MAX - DIAL_MIN) / 2.0) + 1):
            f = DIAL_MIN + i*2.0
            t = (f - DIAL_MIN) / (DIAL_MAX - DIAL_MIN)
            x = int(dial_x1 + t*(dial_x2 - dial_x1))
            pygame.draw.line(world, COL_TEXT_DIM, (x, dial_y-4), (x, dial_y+4), 1)

        btn_w, btn_h = 44, 14
        btn_left  = Rect(body.x+20, body.bottom-18, btn_w, btn_h)
        btn_right = Rect(body.right-20-btn_w, body.bottom-18, btn_w, btn_h)
        pygame.draw.rect(world, COL_RADIO_BG, btn_left);  pygame.draw.rect(world, COL_RADIO_BRD, btn_left, 1)
        pygame.draw.rect(world, COL_RADIO_BG, btn_right); pygame.draw.rect(world, COL_RADIO_BRD, btn_right, 1)
        draw_pixel_text(world, font, "◀", btn_left.centerx, btn_left.centery-1, center=True)
        draw_pixel_text(world, font, "▶", btn_right.centerx, btn_right.centery-1, center=True)

        return {"body": body, "disp": disp, "dial_y": dial_y, "dial_x1": dial_x1, "dial_x2": dial_x2,
                "btn_left": btn_left, "btn_right": btn_right}

    # ------------------ AUDIO ------------------
    EVENT_STOP_MUSIC = pygame.USEREVENT + 77

    def start_static_loop(volume=0.3):
        try:
            pygame.mixer.music.load(str(STATIC_PATH))
            pygame.mixer.music.set_volume(clamp(volume, 0.0, 1.0))
            pygame.mixer.music.play(loops=-1)
        except Exception as e:
            print("[Radio] No pude iniciar estática:", e)

    def stop_music():
        try: pygame.mixer.music.stop()
        except Exception: pass

    def play_station_segment(st: dict):
        path = st.get("sonido")
        if not path: return 0
        start = float(st.get("comienzo", 0.0))
        if "duracion_ms" in st:
            dur_ms = int(st["duracion_ms"])
        elif "duracion_s" in st:
            dur_ms = int(float(st["duracion_s"]) * 1000)
        else:
            dur_ms = 0
        vol = float(st.get("volumen", 0.8))
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(clamp(vol, 0.0, 1.0))
            pygame.mixer.music.play(loops=0, start=start if start>0 else 0.0)
            if dur_ms > 0: pygame.time.set_timer(EVENT_STOP_MUSIC, dur_ms, True)
            return dur_ms
        except Exception as e:
            print(f"[Radio] Falló reproducir estación: {path} -> {e}")
            return 0

    # ---- LIMPIEZA DE AUDIO (PARA TODOS LOS RETURNS) ----
    def _cleanup_audio():
        try:
            pygame.time.set_timer(EVENT_STOP_MUSIC, 0)  # mata el timer
        except Exception:
            pass
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        try:
            pygame.mixer.music.unload()  # pygame 2.3+
        except Exception:
            pass

    # ------------------ ESTADO ------------------
    world = pygame.Surface((PIXEL_W, PIXEL_H))
    try:
        font = pygame.font.Font(str(font_path), FONT_SIZE) if font_path else pygame.font.SysFont("consolas", FONT_SIZE)
    except Exception:
        font = pygame.font.SysFont("consolas", FONT_SIZE)

    frecuencia = round((DIAL_MIN + DIAL_MAX)/2, 1)
    objetivos = [s["frecuencia"] for s in STATIONS]
    roles = roles_por_posicion(STATIONS)  # {freq: 'bad'|'neutral'|'good'}

    game_state = "playing"  # 'playing' | 'won' | 'lost'
    mostrando_mensaje_hasta = 0
    overlay_text_top = ""
    overlay_text_bottom = ""

    clock = pygame.time.Clock()
    start_static_loop(volume=0.25)

    # ------------------ LOOP BLOQUEANTE ------------------
    while True:
        dt = clock.tick(FPS)
        ahora = pygame.time.get_ticks()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                _cleanup_audio()
                return "cancelled"
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    _cleanup_audio()
                    return "cancelled"
                if game_state == "playing":
                    paso = PASO_FINO if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else PASO_GRUESO
                    if e.key in (pygame.K_LEFT, pygame.K_a):
                        frecuencia = max(DIAL_MIN, round(frecuencia - paso, 2))
                    elif e.key in (pygame.K_RIGHT, pygame.K_d):
                        frecuencia = min(DIAL_MAX, round(frecuencia + paso, 2))
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and game_state == "playing":
                pass
            elif e.type == EVENT_STOP_MUSIC:
                pygame.mixer.music.stop()

        # ----- DIBUJO -----
        world.fill((0,0,0))
        draw_car_interior(world)
        ui = draw_radio_module(world, font)

        # clicks en botones (después de tener rects)
        if game_state == "playing" and pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            mx //= SCALE_X; my //= SCALE_Y
            if ui["btn_left"].collidepoint((mx,my)):
                frecuencia = max(DIAL_MIN, round(frecuencia - PASO_GRUESO, 2))
            elif ui["btn_right"].collidepoint((mx,my)):
                frecuencia = min(DIAL_MAX, round(frecuencia + PASO_GRUESO, 2))

        # display + dial
        draw_pixel_text(world, font, f"{frecuencia:05.2f} MHz", ui["disp"].x+4, ui["disp"].y+3, COL_TEXT)
        t = clamp((frecuencia - DIAL_MIN) / (DIAL_MAX - DIAL_MIN), 0.0, 1.0)
        x_marker = int(ui["dial_x1"] + t*(ui["dial_x2"] - ui["dial_x1"]))
        pygame.draw.line(world, COL_ACCENT, (x_marker, ui["dial_y"]-7), (x_marker, ui["dial_y"]+7), 1)

        # señal
        fuerza = fuerza_senal(frecuencia, objetivos)
        sig_base = Rect(ui["body"].x+10, ui["body"].y+40, ui["body"].w-20, 8)
        pygame.draw.rect(world, COL_SIGNAL_BG, sig_base)
        sig_fill = Rect(sig_base.x+1, sig_base.y+1, int((sig_base.w-2)*fuerza), sig_base.h-2)
        pygame.draw.rect(world, COL_SIGNAL, sig_fill)

        # enganchar estación
        if game_state == "playing" and ahora >= mostrando_mensaje_hasta:
            for st in STATIONS:
                f = st["frecuencia"]
                if dentro_tolerancia(frecuencia, f):
                    rol = roles.get(f, "neutral")
                    stop_music()
                    dur_ms = play_station_segment(st)  # duración real del clip (si se pudo)
                    msg_ms = int(st.get("mensaje_ms", MS_MENSAJE_ENCONTRADA))
                    mostrando_mensaje_hasta = ahora + max(msg_ms, dur_ms)  # sincroniza audio/overlay
                    if rol == "good":
                        game_state = "won";  overlay_text_top, overlay_text_bottom = "¡GANASTE!", st["nombre"]
                    elif rol == "bad":
                        game_state = "lost"; overlay_text_top, overlay_text_bottom = "PERDISTE", st["nombre"]
                    else:
                        overlay_text_top, overlay_text_bottom = "ESTACIÓN", st["nombre"]
                    break

        # estática dinámica si se puede seguir jugando
        if game_state == "playing" and ahora >= mostrando_mensaje_hasta:
            vol_est = min(VOLUMEN_ESTATICA_MAX, 0.85*(1.0 - fuerza) + 0.10)
            if not pygame.mixer.music.get_busy():
                start_static_loop(volume=vol_est)
            else:
                pygame.mixer.music.set_volume(vol_est)

        # overlay de mensaje
        if mostrando_mensaje_hasta > ahora:
            overlay = pygame.Surface((PIXEL_W, PIXEL_H), pygame.SRCALPHA)
            overlay.fill((0,0,0,120))
            world.blit(overlay, (0,0))
            draw_pixel_text(world, font, overlay_text_top, PIXEL_W//2, PIXEL_H//2 - 10, COL_TEXT, center=True)
            draw_pixel_text(world, font, overlay_text_bottom, PIXEL_W//2, PIXEL_H//2 + 8, COL_ACCENT, center=True)

        # fin automático (y salida ordenada)
        if mostrando_mensaje_hasta <= ahora and game_state in ("won", "lost"):
            _cleanup_audio()
            if game_state == "won" and exit_on_win:
                pygame.quit(); return "won"
            if game_state == "lost" and exit_on_lose:
                pygame.quit(); return "lost"
            return game_state

        # escalar nearest
        scaled = pygame.transform.scale(world, (WINDOW_W, WINDOW_H))
        screen.blit(scaled, (0,0))
        pygame.display.flip()