# bus_runner_mod.py
import pygame, random
from typing import Callable

def bus_runner(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    load_img: Callable[..., pygame.Surface],
    font: pygame.font.Font,
    font_big: pygame.font.Font,
    fps: int = 60,
    duration_ms: int = 30_000,
) -> dict:
    """
    Minijuego del bus con 3 carriles durante 'duration_ms' milisegundos.
    Colisión: pixel-perfect con máscaras (ignora transparencias).
    Controles: ← / → (o A / D) para cambiar de carril.
    Devuelve: {"win": bool, "tiempo_ms": int}
    """
    WIDTH, HEIGHT = screen.get_size()
    carriles_x = [int(WIDTH * 0.25), int(WIDTH * 0.5), int(WIDTH * 0.75)]

    # Tamaños relativos
    bus_w = max(60, int(WIDTH * 0.10))
    bus_h = max(90, int(HEIGHT * 0.22))
    obs_w = bus_w
    obs_h = bus_h

    # Fondo e imágenes (con fallback)
    try:
        fondo = load_img("rutas.png", scale=(WIDTH, HEIGHT), alpha=False)
    except Exception:
        fondo = pygame.Surface((WIDTH, HEIGHT))
        fondo.fill((30, 30, 30))
        lane_w = WIDTH // 3
        for i in range(3):
            x0 = i * lane_w
            pygame.draw.rect(fondo, (40, 40, 40), (x0 + 8, 0, lane_w - 16, HEIGHT), 2)

    try:
        bus_img = load_img("bus.png", scale=(bus_w, bus_h), alpha=True)
    except Exception:
        bus_img = pygame.Surface((bus_w, bus_h), pygame.SRCALPHA)
        pygame.draw.rect(bus_img, (50, 140, 240), bus_img.get_rect(), border_radius=10)

    try:
        auto_img = load_img("autobus.png", scale=(obs_w, obs_h), alpha=True)
    except Exception:
        auto_img = pygame.Surface((obs_w, obs_h), pygame.SRCALPHA)
        pygame.draw.rect(auto_img, (220, 80, 80), auto_img.get_rect(), border_radius=10)

    # --- Máscaras pixel-perfect (solo una vez) ---
    bus_mask  = pygame.mask.from_surface(bus_img)
    auto_mask = pygame.mask.from_surface(auto_img)

    # Estado del jugador
    lane = 1  # carril medio (objetivo)
    bus_rect = pygame.Rect(0, 0, bus_w, bus_h)
    bus_rect.midbottom = (carriles_x[lane], HEIGHT - 30)

    # Para animación suave
    bus_speed_x = 1000  # px/s velocidad de cambio lateral
    target_x = carriles_x[lane]

    # Obstáculos
    obstaculos: list[dict] = []  # {"rect": Rect, "surf": Surface}

    # Dificultad
    vel_ini = max(250.0, HEIGHT / 2.0)   # px/s
    vel_max = vel_ini * 2.2
    vel = vel_ini
    spawn_ms = 1100
    spawn_min = 420
    spawn_timer = 0

    transcurrido = 0
    perdiste = False

    def spawn_obstaculo():
        cx = random.choice(carriles_x)
        r = pygame.Rect(0, 0, obs_w, obs_h)
        r.midtop = (cx, -obs_h)
        obstaculos.append({"rect": r, "surf": auto_img})

    while transcurrido < duration_ms and not perdiste:
        dt = clock.tick(fps)
        transcurrido += dt
        spawn_timer += dt

        # Aumentar dificultad
        prog = min(1.0, transcurrido / duration_ms)
        vel = vel_ini + (vel_max - vel_ini) * prog
        spawn_ms = max(spawn_min, 1100 - int(600 * prog))

        # Eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return {"win": False, "tiempo_ms": transcurrido}
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_LEFT, pygame.K_a):
                    lane = max(0, lane - 1)
                    target_x = carriles_x[lane]
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    lane = min(2, lane + 1)
                    target_x = carriles_x[lane]

        # Movimiento suave hacia el carril objetivo
        diff = target_x - bus_rect.centerx
        if abs(diff) > 2:  # umbral mínimo para no vibrar
            move = bus_speed_x * (dt / 1000.0)
            if diff > 0:
                bus_rect.centerx += min(move, diff)
            else:
                bus_rect.centerx += max(-move, diff)
        else:
            bus_rect.centerx = target_x

        bus_rect.bottom = HEIGHT - 30

        # Spawning
        if spawn_timer >= spawn_ms:
            spawn_obstaculo()
            spawn_timer = 0

        # Mover obstáculos
        for o in obstaculos:
            o["rect"].y += int(vel * (dt / 1000.0))

        # Limpiar los que salen
        obstaculos = [o for o in obstaculos if o["rect"].top <= HEIGHT]

        # --- Colisión pixel-perfect ---
        for o in obstaculos:
            if bus_rect.colliderect(o["rect"]):
                offset = (o["rect"].x - bus_rect.x, o["rect"].y - bus_rect.y)
                if bus_mask.overlap(auto_mask, offset):
                    perdiste = True
                    break

        # Dibujo
        screen.blit(fondo, (0, 0))

        # HUD: cuenta regresiva
        restante = max(0, duration_ms - transcurrido)
        seg = restante // 1000
        shadow = font_big.render(f"{seg}", True, (0, 0, 0))
        srect = shadow.get_rect(topright=(WIDTH - 26, 26))
        screen.blit(shadow, srect)
        text = font_big.render(f"{seg}", True, (255, 255, 255))
        screen.blit(text, srect.move(-2, -2))

        # Obstáculos y jugador
        for o in obstaculos:
            screen.blit(o["surf"], o["rect"])
        screen.blit(bus_img, bus_rect)

        tip = font.render("← / → para cambiar de carril", True, (255, 255, 255))
        screen.blit(tip, (20, HEIGHT - tip.get_height() - 16))

        pygame.display.flip()

    return {"win": not perdiste and transcurrido >= duration_ms, "tiempo_ms": transcurrido}