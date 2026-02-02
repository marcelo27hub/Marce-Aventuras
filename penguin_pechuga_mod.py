# pollos_runner_mod.py
import pygame, random
from typing import Callable

def pollo_runner(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    load_img: Callable[..., pygame.Surface],
    font: pygame.font.Font,
    font_big: pygame.font.Font,
    *,
    fps: int = 60,
    duration_s: int = 30,         # duración máxima del minijuego (segundos)
    target: int = 15,             # pollos requeridos para ganar
    # ---- tuning ----
    player_speed_px_s: int = 520, # velocidad del jugador (px/seg)
    speed_scale: float = 1.2,     # multiplica la caída de los ítems
    spawn_initial_ms: int = 900,  # intervalo inicial de spawn (ms)
    spawn_min_ms: int = 250,      # intervalo mínimo de spawn (ms)
    spawn_diff_period_ms: int = 4500,  # cada cuánto acelera el spawn (ms)
    spawn_shrink_factor: float = 0.82  # cuánto reduce el intervalo en cada tick
) -> dict:
    """
    Minijuego: atrapar 'target' pollos antes de 'duration_s' segundos.
    Evitá la basura (te aturde 1s).
    Devuelve: {"win": bool, "pollos": int, "tiempo_ms": int}
    Usa la misma pantalla/clock del juego principal (no hace pygame.init ni set_mode).
    """

    WIDTH, HEIGHT = screen.get_size()

    # --- Cargar imágenes desde /images con tu helper ---
    def safe_img(name, scale, alpha=True, fallback_color=(200,200,200)):
        try:
            return load_img(name, scale=scale, alpha=alpha)
        except Exception:
            surf = pygame.Surface(scale, pygame.SRCALPHA if alpha else 0)
            surf.fill(fallback_color)
            return surf

    try:
        fondo = load_img("fondo_penguin_pechuga.png", scale=(WIDTH, HEIGHT), alpha=False)
    except Exception:
        fondo = pygame.Surface((WIDTH, HEIGHT))
        fondo.fill((30, 32, 36))

    marce_der = safe_img("marce_derecha.png",   (120,140), True, (180,220,255))
    marce_izq = safe_img("marce_izquierda.png", (120,140), True, (180,220,255))
    pollo_img = safe_img("pollo.png",           (60, 60),  True, (255,230,120))
    basura_img= safe_img("basura.png",          (80, 80),  True, (120,120,120))

    # --- Helpers UI ---
    def draw_text_center(text, fnt, color, x, y):
        s = fnt.render(text, True, color)
        screen.blit(s, s.get_rect(center=(x, y)))

    # --- Sprites ---
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.img_right = marce_der
            self.img_left  = marce_izq
            self.image = self.img_right
            self.rect  = self.image.get_rect()
            self.rect.centerx = WIDTH // 2
            self.rect.bottom  = HEIGHT - 10
            self.speed = player_speed_px_s  # px/seg
            self.stunned = False
            self.stun_until_ms = 0
            self.mask  = pygame.mask.from_surface(self.image)

        def update(self, dt):
            if self.stunned:
                return
            keys = pygame.key.get_pressed()
            dx = 0
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= self.speed * dt
                self.image = self.img_left
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += self.speed * dt
                self.image = self.img_right

            self.rect.x = int(self.rect.x + dx)
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.right > WIDTH: self.rect.right = WIDTH
            self.mask = pygame.mask.from_surface(self.image)

        def set_stun(self, ms=1000):
            self.stunned = True
            self.stun_until_ms = pygame.time.get_ticks() + ms

        def check_recover(self):
            if self.stunned and pygame.time.get_ticks() >= self.stun_until_ms:
                self.stunned = False

    class FallingObject(pygame.sprite.Sprite):
        def __init__(self, obj_type):
            super().__init__()
            self.obj_type = obj_type
            self.image = pollo_img if obj_type == "pollo" else basura_img
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -60)
            base = random.uniform(180, 360)
            self.speed = base * speed_scale  # caen más rápido
            self.mask = pygame.mask.from_surface(self.image)

        def update(self, dt):
            self.rect.y = int(self.rect.y + self.speed * dt)
            if self.rect.top > HEIGHT:
                self.kill()

    # --- Estado ---
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    falling = pygame.sprite.Group()

    chickens = 0
    start_ms = pygame.time.get_ticks()
    duration_ms = int(duration_s * 1000)

    # Spawning (agresivo)
    last_spawn_ms   = pygame.time.get_ticks()
    spawn_rate_ms   = spawn_initial_ms
    min_spawn_ms    = spawn_min_ms
    diff_period_ms  = spawn_diff_period_ms
    last_diffup_ms  = pygame.time.get_ticks()  # <-- CORRECTO

    # --- Loop ---
    while True:
        dt = clock.tick(fps) / 1000.0
        now = pygame.time.get_ticks()

        # Eventos
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return {"win": False, "pollos": chickens, "tiempo_ms": now - start_ms}
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return {"win": False, "pollos": chickens, "tiempo_ms": now - start_ms}

        # Recuperación de stun
        player.check_recover()

        # Dificultad dinámica (spawn cada vez más rápido)
        if now - last_diffup_ms >= diff_period_ms:
            spawn_rate_ms = max(min_spawn_ms, int(spawn_rate_ms * spawn_shrink_factor))
            last_diffup_ms = now

        # Spawn
        if now - last_spawn_ms >= spawn_rate_ms:
            kind = "pollo" if random.random() < 0.7 else "basura"
            obj = FallingObject(kind)
            all_sprites.add(obj); falling.add(obj)
            last_spawn_ms = now

        # Updates
        for spr in list(all_sprites):
            spr.update(dt)

        # Colisiones
        hits = pygame.sprite.spritecollide(player, falling, True, pygame.sprite.collide_mask)
        for h in hits:
            if h.obj_type == "pollo":
                chickens += 1
                # Victoria inmediata
                if chickens >= target:
                    return {"win": True, "pollos": chickens, "tiempo_ms": now - start_ms}
            else:  # basura
                if not player.stunned:
                    player.set_stun(1000)  # 1s aturdido

        # Tiempo (si no ganó antes)
        elapsed_ms = now - start_ms
        if elapsed_ms >= duration_ms:
            win = chickens >= target
            return {"win": win, "pollos": chickens, "tiempo_ms": elapsed_ms}

        # --- DRAW ---
        screen.blit(fondo, (0, 0))
        all_sprites.draw(screen)

        # HUD
        draw_text_center(f"Pollos: {chickens}/{target}", font, (255, 80, 80), 150, 30)
        draw_text_center(f"Tiempo: {int((duration_ms - elapsed_ms)/1000)}", font, (255, 80, 80), WIDTH - 120, 30)
        draw_text_center("Atrapa los pollos", font, (255,255,255), WIDTH // 2, 30)

        # Aviso de stun
        if player.stunned:
            aviso = font_big.render("¡ATURDIDO!", True, (255,215,0))
            w, h = aviso.get_size()
            aviso = pygame.transform.smoothscale(aviso, (int(w*1.05), int(h*1.05)))
            screen.blit(aviso, aviso.get_rect(center=(WIDTH//2, int(HEIGHT*0.85))))

        pygame.display.flip()