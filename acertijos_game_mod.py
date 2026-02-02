# acertijos_game_mod.py
import pygame
import random
from typing import Callable

def acertijos_game(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    load_img: Callable[..., pygame.Surface],
    font: pygame.font.Font,
    font_big: pygame.font.Font
) -> bool:
    """
    Minijuego de 3 acertijos. Devuelve True si aciertas >= 2, False si no.
    """
    WIDTH, HEIGHT = screen.get_size()

    # Fondo desde /images
    try:
        bg = load_img("fondo_acertijo_2.png", scale=(WIDTH, HEIGHT), alpha=False)
    except Exception:
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill((18, 22, 28))

    # Pool de preguntas
    pool = [
        {"texto": "Vuelo sin alas, lloro sin ojos. ¿Qué soy?",
         "opciones": ["nube", "pájaro", "avión"], "respuesta": "nube"},

        {"texto": "Cuanto más me quitas, más grande soy. ¿Qué soy?",
         "opciones": ["agujero", "huella", "sombra"], "respuesta": "agujero"},

        {"texto": "No tengo vida, pero crezco; no tengo pulmones, pero necesito aire. ¿Qué soy?",
         "opciones": ["fuego", "planta", "roca"], "respuesta": "fuego"},

        {"texto": "Si me nombras, desaparezco. ¿Qué soy?",
         "opciones": ["silencio", "sombra", "eco"], "respuesta": "silencio"},

        {"texto": "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera.",
            "opciones": ["pera", "kiwi", "manzana"], "respuesta": "pera"},

        {"texto": "Tengo ciudades pero no casas, montañas pero no árboles y agua pero no peces. ¿Qué soy?",
            "opciones": ["mapa", "planeta", "maqueta"], "respuesta": "mapa"},

        {"texto": "Siempre está por venir, pero nunca llega. ¿Qué es?",
            "opciones": ["mañana", "futuro", "trenes"], "respuesta": "mañana"},

        {"texto": "Tiene dientes pero no muerde. ¿Qué es?",
            "opciones": ["peine", "llave", "sierra"], "respuesta": "peine"},

        {"texto": "Corre sin piernas y murmura sin boca. ¿Qué es?",
            "opciones": ["río", "sueño", "sombra"], "respuesta": "río"},

        {"texto": "La ves una vez en un minuto, dos veces en un momento y nunca en cien años. ¿Qué es?",
            "opciones": ["la letra m", "la luna", "el tiempo"], "respuesta": "la letra m"},

        {"texto": "Cuanto más seco, más me mojo. ¿Qué soy?",
            "opciones": ["toalla", "esponja", "arena"], "respuesta": "toalla"},
    ]

    # Elegimos 3 preguntas random y barajamos orden
    preguntas = random.sample(pool, 3)
    for q in preguntas:
        opts = q["opciones"][:]
        random.shuffle(opts)
        q["opciones"] = opts
    random.shuffle(preguntas)

    def draw_typewriter_text(surface, texto, tfnt, color, center_x, start_y, max_w, start_time, chars_per_sec):
        """Dibuja texto centrado con efecto máquina de escribir."""
        # Calcular cuántos caracteres mostrar
        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        num_chars = int(elapsed * chars_per_sec)
        visible_text = texto[:num_chars]

        # Partir en líneas respetando el ancho
        palabras = visible_text.split(" ")
        lineas = []
        linea = ""
        for p in palabras:
            test = (linea + p + " ").strip()
            if tfnt.size(test)[0] <= max_w:
                linea = test + " "
            else:
                lineas.append(linea.strip())
                linea = p + " "
        if linea:
            lineas.append(linea.strip())

        # Dibujar cada línea centrada
        y = start_y
        for l in lineas:
            render = tfnt.render(l, True, color)
            rect = render.get_rect(center=(center_x, y))
            surface.blit(render, rect)
            y += tfnt.get_linesize()

        # ¿Terminó?
        terminado = len(visible_text) >= len(texto)
        return terminado

    def crear_botones(opciones):
        botones = []
        w, h = 260, 64
        gap = 36
        total = len(opciones) * w + (len(opciones) - 1) * gap
        start_x = (WIDTH - total) // 2
        y = int(HEIGHT * 0.62)
        for i, txt in enumerate(opciones):
            rect = pygame.Rect(start_x + i * (w + gap), y, w, h)
            botones.append((rect, txt))
        return botones

    # Estado inicial
    idx = 0
    aciertos = 0
    mostrando = False
    mensaje = ""
    hasta_ms = 0

    start_time = pygame.time.get_ticks()
    texto_completo = preguntas[idx]["texto"]
    texto_terminado = False
    botones = crear_botones(preguntas[idx]["opciones"])

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not mostrando:
                mx, my = e.pos
                for rect, txt in botones:
                    if rect.collidepoint((mx, my)):
                        if txt.lower() == preguntas[idx]["respuesta"].lower():
                            mensaje = "¡Correcto!"
                            aciertos += 1
                        else:
                            mensaje = f"Incorrecto. Era: {preguntas[idx]['respuesta']}"
                        mostrando = True
                        hasta_ms = pygame.time.get_ticks() + 1500  # 1.5s de feedback

        # Avance a la siguiente pregunta (cuando termina el feedback)
        if mostrando and pygame.time.get_ticks() >= hasta_ms:
            mostrando = False
            idx += 1

            # ¿Se acabaron?
            if idx >= len(preguntas):
                success = aciertos >= 2
                msg = "¡GANASTE!" if success else "PERDISTE"
                color = (255, 215, 0) if success else (255, 80, 80)

                screen.blit(bg, (0, 0))
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                screen.blit(overlay, (0, 0))

                label = font_big.render(msg, True, color)
                scale = 1.9
                w, h = label.get_size()
                big_label = pygame.transform.smoothscale(label, (int(w * scale), int(h * scale)))
                screen.blit(big_label, big_label.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

                pygame.display.flip()
                pygame.time.delay(1600)
                return success

            # Preparar siguiente (AHORA sí es seguro acceder a preguntas[idx])
            start_time = pygame.time.get_ticks()
            texto_completo = preguntas[idx]["texto"]
            texto_terminado = False
            botones = crear_botones(preguntas[idx]["opciones"])

        # ----------------- DRAW -----------------
        screen.blit(bg, (0, 0))

        # Título
        titulo = font.render(f"Acertijo {idx+1} de {len(preguntas)}", True, (255,255,255))
        trect = titulo.get_rect(midtop=(WIDTH//2, 24))
        panel = pygame.Surface((trect.width+18, trect.height+12), pygame.SRCALPHA)
        panel.fill((0,0,0,160))
        screen.blit(panel, (trect.x-9, trect.y-6))
        screen.blit(titulo, trect)

        # Pregunta (NO resetees start_time acá)
        texto_terminado = draw_typewriter_text(
            screen,
            texto_completo,
            font,
            (255,255,255),
            WIDTH // 2,   # centro horizontal
            180,          # Y inicial
            WIDTH - 120,  # ancho máximo
            start_time,
            chars_per_sec=25
        )

        # Botones
        for rect, txt in botones:
            pygame.draw.rect(screen, (78, 152, 216), rect)
            pygame.draw.rect(screen, (10,10,10), rect, 3)
            label = font.render(txt, True, (0,0,0))
            screen.blit(label, label.get_rect(center=rect.center))

        # Feedback temporal
        if mostrando:
            aviso = font_big.render(mensaje, True, (255,215,0))
            w, h = aviso.get_size()
            aviso_big = pygame.transform.smoothscale(aviso, (int(w*1.25), int(h*1.25)))
            screen.blit(aviso_big, aviso_big.get_rect(center=(WIDTH//2, int(HEIGHT*0.85))))

        pygame.display.flip()
        clock.tick(60)