# bici_runner_mod.py
import pygame, random
from typing import Callable

def make_cloud_surface(w, h, color, edge=(200,210,220), block=8, seed=None):
    """Construye UNA Surface de nube con borde y la devuelve lista para blitear."""
    sw = max(8, w // block)
    sh = max(6, h // block)
    small = pygame.Surface((sw, sh), pygame.SRCALPHA)

    rnd = random.Random(seed)
    num_blobs = rnd.randint(3, 5)
    for _ in range(num_blobs):
        bw = int(rnd.uniform(0.35, 0.75) * sw)
        bh = int(rnd.uniform(0.45, 0.85) * sh)
        cx = int(rnd.uniform(0.2, 0.8) * sw)
        cy = int(rnd.uniform(0.25, 0.55) * sh)
        rect = pygame.Rect(0, 0, bw, bh)
        rect.center = (cx, cy)
        pygame.draw.ellipse(small, color, rect)

    # base más plana
    pygame.draw.rect(small, color, pygame.Rect(0, int(sh*0.55), sw, int(sh*0.5)))

    # escalar a tamaño final y dibujar borde UNA VEZ
    big = pygame.transform.scale(small, (w, h))
    mask = pygame.mask.from_surface(big)
    outline = mask.outline()
    if outline:
        pygame.draw.polygon(big, edge, outline, 2)

    return big.convert_alpha()

def bici_runner(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    load_img: Callable[..., pygame.Surface],
    font: pygame.font.Font,
    font_big: pygame.font.Font,
    fps: int = 60,
    duration_ms: int = 1_000,
) -> dict:
    """
    Runner de bici. Devuelve {"win": bool, "tiempo_ms": int}.
    Requiere que le pases screen, clock, load_img, font y font_big.
    """

    WIDTH, HEIGHT = screen.get_size()

    # ====== Config ======
    CESPED = 6
    PLANTA_BAJA = HEIGHT - 60
    PIE = 10

    VEL_INI = 250.0
    VEL_MAX = 430.0

    SPAWN_MIN, SPAWN_MAX = 1.10, 1.80
    MIN_GAP_PX = 280

    SCALE_PLAYER = 0.32
    SCALE_OBS = 0.35

    # ====== Fondo ======
    try:
        fondo = load_img("fondo_bici.png", scale=(WIDTH, HEIGHT), alpha=False)
    except Exception:
        fondo = None

    # ====== Jugador ======
    frames = []
    i = 1
    while True:
        try:
            raw = load_img(f"marce_bici_{i}.png", alpha=True)
        except Exception:
            break
        w = int(raw.get_width() * SCALE_PLAYER)
        h = int(raw.get_height() * SCALE_PLAYER)
        frames.append(pygame.transform.smoothscale(raw, (w, h)))
        i += 1

    if not frames:
        # fallback para no crashear
        dummy = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.rect(dummy, (200, 60, 60), dummy.get_rect(), border_radius=8)
        frames = [dummy]

    SPR_W, SPR_H = frames[0].get_size()
    frame_idx, frame_timer, frame_delay = 0, 0.0, 0.12

    rider_x = 200.0
    y_bottom = float(PLANTA_BAJA + PIE)
    rider_vy = 0.0
    on_ground = True

    # ====== Obstáculos ======
    obst_imgs = []
    idx = 1
    while True:
        try:
            raw = load_img(f"obst_{idx}.png", alpha=True)
        except Exception:
            break
        ow = int(raw.get_width() * SCALE_OBS)
        oh = int(raw.get_height() * SCALE_OBS)
        obst_imgs.append(pygame.transform.smoothscale(raw, (ow, oh)))
        idx += 1
    use_rect_fallback = (len(obst_imgs) == 0)

    # ====== Nubes (pre-render con cache) ======
    CLOUD_BLOCK = 8
    CLOUD_COLORS = [(236,243,252), (225,235,245), (255,255,255)]
    CLOUD_LAYERS = [0.25, 0.35, 0.50]
    nubes = []
    for _ in range(7):
        w = random.randint(80, 150)
        h = random.randint(26, 48)
        color = random.choice(CLOUD_COLORS)
        layer = random.choice(CLOUD_LAYERS)
        seed  = random.randint(0, 999999)
        surf  = make_cloud_surface(w, h, color, edge=(200,210,220), block=CLOUD_BLOCK, seed=seed)
        nubes.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(40, 180),
            "w": w, "h": h,
            "layer": layer,
            "color": color,
            "seed": seed,
            "surf": surf
        })

    # ====== Mundo / loop ======
    obstacles = []
    spawn_cd = 0.0
    start_ms = pygame.time.get_ticks()
    finished = False
    win = False

    while True:
        dt = clock.tick(fps) / 1000.0
        now = pygame.time.get_ticks()
        elapsed = now - start_ms

        # Velocidad progresiva
        p = max(0.0, min(1.0, elapsed / float(duration_ms)))
        vel_mov = VEL_INI + (VEL_MAX - VEL_INI) * p

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return {"win": False, "tiempo_ms": elapsed}
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return {"win": False, "tiempo_ms": elapsed}
                if e.key in (pygame.K_SPACE, pygame.K_UP) and on_ground:
                    rider_vy = -600.0
                    on_ground = False

        # Fondo
        if fondo:
            screen.blit(fondo, (0, 0))
        else:
            screen.fill((180,210,245))

        # Suelo
        pygame.draw.rect(screen, (90,180,90),  pygame.Rect(0, PLANTA_BAJA, WIDTH, CESPED))
        pygame.draw.rect(screen, (150,120,90), pygame.Rect(0, PLANTA_BAJA+CESPED, WIDTH, HEIGHT-(PLANTA_BAJA+CESPED)))

        # Nubes (parallax + respawn con pre-render)
        for c in nubes:
            c["x"] -= vel_mov * c["layer"] * dt
            if c["x"] + c["w"] < 0:
                c["x"] = WIDTH + random.randint(20, 220)
                c["y"] = random.randint(40, 180)
                c["w"] = random.randint(80, 150)
                c["h"] = random.randint(26, 48)
                c["layer"] = random.choice(CLOUD_LAYERS)
                c["color"] = random.choice(CLOUD_COLORS)
                c["seed"]  = random.randint(0, 999999)
                c["surf"]  = make_cloud_surface(c["w"], c["h"], c["color"], edge=(200,210,220), block=CLOUD_BLOCK, seed=c["seed"])
            screen.blit(c["surf"], (int(c["x"]), int(c["y"])))

        # Física jugador
        rider_vy += 1600.0 * dt
        y_bottom += rider_vy * dt
        if y_bottom >= PLANTA_BAJA + PIE:
            y_bottom = float(PLANTA_BAJA + PIE)
            rider_vy = 0.0
            on_ground = True

        sx = int(rider_x) - SPR_W // 2
        sy = int(y_bottom) - SPR_H

        # Spawns
        spawn_cd -= dt
        can_time = (spawn_cd <= 0.0)
        can_gap  = (not obstacles) or (obstacles[-1]["x"] < WIDTH - MIN_GAP_PX)
        if can_time and can_gap:
            if use_rect_fallback:
                w = random.randint(14, 24)
                h = random.randint(34, 56)
                obstacles.append({"x": WIDTH + 20, "y": PLANTA_BAJA - h + PIE, "w": w, "h": h, "img": None})
            else:
                img = random.choice(obst_imgs)
                w, h = img.get_width(), img.get_height()
                obstacles.append({"x": WIDTH + 20, "y": PLANTA_BAJA - h + PIE, "w": w, "h": h, "img": img})
            spawn_cd = random.uniform(SPAWN_MIN, SPAWN_MAX)

        # Mover/limpiar obs
        kept = []
        for ob in obstacles:
            ob["x"] -= vel_mov * dt
            if ob["x"] + ob["w"] > -40:
                kept.append(ob)
        obstacles = kept

        # Dibujar obs
        if use_rect_fallback:
            for ob in obstacles:
                pygame.draw.rect(screen, (60,60,60), pygame.Rect(int(ob["x"]), int(ob["y"]), ob["w"], ob["h"]))
        else:
            for ob in obstacles:
                screen.blit(ob["img"], (int(ob["x"]), int(ob["y"])))

        # Colisión
        margin = int(min(SPR_W, SPR_H) * 0.12)
        player_rect = pygame.Rect(sx + margin, sy + margin, SPR_W - 2*margin, SPR_H - 2*margin)
        for ob in obstacles:
            if player_rect.colliderect(pygame.Rect(int(ob["x"]), int(ob["y"]), ob["w"], ob["h"])):
                finished = True; win = False
                break

        if elapsed >= duration_ms:
            finished = True; win = True

        # Animación jugador
        if on_ground and len(frames) > 1:
            frame_timer += dt
            if frame_timer >= frame_delay:
                frame_timer = 0.0
                frame_idx = (frame_idx + 1) % len(frames)

        # Dibujo jugador
        screen.blit(frames[frame_idx], (sx, sy))

        # Barra de tiempo
        total_w = WIDTH - 40
        fill_w  = int(total_w * (elapsed/float(duration_ms)))
        pygame.draw.rect(screen, (30,30,30), pygame.Rect(20,16,total_w,12))
        pygame.draw.rect(screen, (70,200,80), pygame.Rect(20,16,fill_w,12))
        pygame.draw.rect(screen, (10,10,10), pygame.Rect(20,16,total_w,12), 2)

        if finished:
            msg = "¡GANASTE!" if win else "Game Over"
            label = font_big.render(msg, True, (15,15,15))
            screen.blit(label, label.get_rect(center=(WIDTH//2, HEIGHT//2 - 10)))
            pygame.display.flip()
            pygame.time.delay(800)
            return {"win": win, "tiempo_ms": elapsed}

        pygame.display.flip()