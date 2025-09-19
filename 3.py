import sys, os, random, math, pygame, pygame.gfxdraw

# ---------------------------- Параметры ----------------------------
FULLSCREEN = True
TITLE = "ФУНКЦИОНАЛЬНОЕ МЕНЮ"

BG_COLOR = (10, 15, 26)
CYAN = (222, 255, 255)
ALERT_RED = (255, 60, 0)

# размеры элементов первой панели
THERM_IMG_PATH = os.path.join("img", "term.png")
THERM_WIDTH = 220          # ширина изображения термометра
THERM_HEIGHT_RATIO = 0.95    # доля высоты ячейки, занимаемая термометром
RAD_CHART_SIZE = (380, 400)  # (ширина, высота) диаграммы радиации
GAS_CHART_SIZE = (380, 400)  # (ширина, высота) диаграммы газов

# смещения элементов первой панели относительно левого верхнего угла окна
THERM_POS = (35, -15)                             # (dx, dy) термометра
RAD_CHART_POS = (THERM_POS[0] + THERM_WIDTH + 25, -10)
GAS_CHART_POS = (RAD_CHART_POS[0] + RAD_CHART_SIZE[0] + 120, -10)

# регулировки отрисовки диаграмм и подписи температуры
GAS_LABEL_FONT_SIZE = 36         # размер текста подписей газов
GAS_CHART_H_OFFSET = -120         # сдвиг диаграммы газов по оси X
CHART_TITLE_GAP = 40             # отступ между названием и диаграммой
THERM_DEG_OFFSET = (0, -57)       # смещение подписи градусов

# параметры окна активации взрывных зарядов
ACTIVATE_PANEL_SIZE = (500, 360)      # (ширина, высота) окна
ACTIVATE_LABEL_FONT_SIZE = 56         # размер шрифта заголовка
ACTIVATE_BUTTON_SIZE = (300, 90)      # размер кнопки (w, h)
ACTIVATE_BUTTON_FONT_SIZE = 56        # размер шрифта на кнопке

# подписи и подсказки для зарядов
ZARYAD_ICON_SIZE = 150                # базовый размер иконки зарядов
ZARYAD_LABEL_FONT_SIZE = 29           # размер текста "Заряд N"
ZARYAD_LABEL_OFFSET = (0, 4)          # смещение подписи относительно иконки
ZARYAD_HINT_FONT_SIZE = 60            # размер текста подсказки под картой
ZARYAD_HINT_OFFSET = (0, -40)         # смещение подсказки относительно низа окна

# окно подтверждения активации
CONFIRM_PANEL_SIZE = (500, 220)       # (ширина, высота) окна подтверждения
CONFIRM_TITLE_FONT_SIZE = 40          # размер заголовка
CONFIRM_TEXT_FONT_SIZE = 28           # размер текста согласия
CONFIRM_BUTTON_SIZE = (250, 60)       # размер кнопки подтверждения
CONFIRM_BUTTON_FONT_SIZE = 48         # размер шрифта на кнопке

# размер шрифта обратного отсчёта перед самоуничтожением
COUNTDOWN_FONT_SIZE = 180

GAS_COMPOSITION = [
    ["Азот", 78.08, (80, 120, 150)],
    ["Кислород", 20.95, (100, 180, 200)],
    ["Аргон", 0.93, (160, 220, 240)],
    ["Углекислый газ", 0.04, (60, 90, 110)],
]

# шрифты
pygame.init()
flags = pygame.FULLSCREEN if FULLSCREEN else 0
screen = pygame.display.set_mode((0, 0), flags) if FULLSCREEN else pygame.display.set_mode((1280, 1024))
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

font_small = pygame.font.Font(None, 29)
font_diagram1 = pygame.font.Font(None, 38)
font_diagram2 = pygame.font.Font(None, 33)
font_diagram3 = pygame.font.Font(None, 28)
font_gas_label = pygame.font.Font(None, GAS_LABEL_FONT_SIZE)
font_therm = pygame.font.Font(None, 56)
font_energy = pygame.font.Font(None, 40)
font_energy2 = pygame.font.Font(None, 30)
font_enter = pygame.font.Font(None, 56)
font_activate_label = pygame.font.Font(None, ACTIVATE_LABEL_FONT_SIZE)
font_activate_btn = pygame.font.Font(None, ACTIVATE_BUTTON_FONT_SIZE)
font_zaryad_label = pygame.font.Font(None, ZARYAD_LABEL_FONT_SIZE)
font_zaryad_hint = pygame.font.Font(None, ZARYAD_HINT_FONT_SIZE)
font_confirm_title = pygame.font.Font(None, CONFIRM_TITLE_FONT_SIZE)
font_confirm_text = pygame.font.Font(None, CONFIRM_TEXT_FONT_SIZE)
font_confirm_btn = pygame.font.Font(None, CONFIRM_BUTTON_FONT_SIZE)
font_countdown = pygame.font.Font(None, COUNTDOWN_FONT_SIZE)
font_confirm_text2 = pygame.font.Font(None, 30)
# изображение энергетического статуса
ENERGY_IMG_PATH = os.path.join("img", "energy.png")
ENERGY_IMG_SIZE = (500, 500)
SUBSYS_BAR_WIDTH = 280

# смещения подписи состояний топливных баков и генераторов (dx, dy)
FUEL_STATUS_OFFSET = (-125, -170)
GEN_STATUS_OFFSET = (-150, -105)

# уровни подсистем
LIFE_SUPPORT_LEVEL = 10
AUX_SYSTEM_LEVEL = 10

THERM_IMG = pygame.image.load(THERM_IMG_PATH).convert_alpha()
ENERGY_IMG = pygame.image.load(ENERGY_IMG_PATH).convert_alpha()
WARN_IMG = pygame.image.load(os.path.join("img", "warn.png")).convert_alpha()

# изображения карт для нижних окон
MAP1_IMG_PATH = os.path.join("img", "map1.png")
MAP2_IMG_PATH = os.path.join("img", "map2.png")
MAP1_IMG = pygame.image.load(MAP1_IMG_PATH).convert()
MAP2_IMG = pygame.image.load(MAP2_IMG_PATH).convert()
MAP1_ORIG_W, MAP1_ORIG_H = MAP1_IMG.get_size()

# статические индикаторы для карты 1
STAT_ICON_PATH = os.path.join("img", "stat_off.png")
STAT_ICON_SIZE = 140
    STAT_POSITIONS = [
        (215, 220),
        (731, 180),
        (215, 520),
        (160, 800),
        (733, 545),
        (1230, 260),
        (1268, 670),
]
STAT_IMG = pygame.image.load(STAT_ICON_PATH).convert_alpha()

# прорисовываем индикаторы сразу на изображении MAP1
for px, py in STAT_POSITIONS:
    icon = pygame.transform.smoothscale(STAT_IMG, (STAT_ICON_SIZE, STAT_ICON_SIZE))
    MAP1_IMG.blit(icon, icon.get_rect(center=(px, py)))

# иконки зарядов на карте 2
ZARYAD_ICON_PATH = os.path.join("img", "zaryad.png")
ZARYAD_ACTIVE_ICON_PATH = os.path.join("img", "zaryad1.png")
# координаты зарядов в пикселях относительно исходного размера MAP2_IMG
ZARYAD_POSITIONS = [
    (215, 220),
    (731, 180),
    (215, 520),
    (733, 545),
    (1230, 260),
    (1268, 670),
]
ZARYAD_IMG = pygame.image.load(ZARYAD_ICON_PATH).convert_alpha()
ZARYAD_ACTIVE_IMG = pygame.image.load(ZARYAD_ACTIVE_ICON_PATH).convert_alpha()
MAP2_ORIG_W, MAP2_ORIG_H = MAP2_IMG.get_size()

# состояние зарядов
zaryads = [{"pos": pos, "activated": False, "anim_start": None} for pos in ZARYAD_POSITIONS]
zaryad_rects = []  # icon and label rectangles for кликов
map2_confirm = None

# обратный отсчёт после активации всех зарядов
countdown = None

# финальное подтверждение перед запуском обратного отсчёта
final_confirm = None

# изображения астероидов
ASTEROID_SIZE = 24
ASTEROID_IMAGES = [
    pygame.transform.smoothscale(
        pygame.image.load(os.path.join("img", f"asteroid{i}.png")).convert_alpha(),
        (ASTEROID_SIZE, ASTEROID_SIZE),
    )
    for i in range(1, 6)
]
# скорость полёта (пикселей в секунду), пауза между появлениями и максимум одновременно
ASTEROID_SPEED = 15
ASTEROID_SPAWN_INTERVAL = 800  # мс между появлениями
ASTEROID_MAX_COUNT = 4
ASTEROID_FADE_SPEED = 120  # скорость исчезновения рамки и координат

asteroids = []
last_asteroid_spawn = 0

# параметры радара
RADAR_SWEEP_SPEED = 1.5  # градусов за кадр
RADAR_TRAIL_LENGTH = 60  # длина хвоста в градусах
RADAR_TRAIL_STEP = 1     # шаг построения хвоста

# уровни подсистем корабля (проценты)
SUBSYSTEMS = [
    ("Главные двигатели", 95),
    ("Дополнительные двигатели", 88),
    ("Системы жизнеобеспечения", LIFE_SUPPORT_LEVEL),
    ("Вспомогательные системы", AUX_SYSTEM_LEVEL),
]

# ---------------------------- Диаграммы ----------------------------

def draw_pie(surface, center, radius, start_angle, end_angle, color):
    cx, cy = center
    points = [(cx, cy)]
    step = 1 if end_angle >= start_angle else -1
    for ang in range(int(start_angle), int(end_angle), step):
        rad = math.radians(ang)
        points.append((cx + radius * math.cos(rad), cy + radius * math.sin(rad)))
    rad = math.radians(end_angle)
    points.append((cx + radius * math.cos(rad), cy + radius * math.sin(rad)))
    if len(points) >= 3:
        pygame.gfxdraw.filled_polygon(surface, points, color)
        pygame.gfxdraw.aapolygon(surface, points, color)


def draw_gas_chart(surface, rect):
    caption_lines = [
        "Процент содержания газов",
        "в атмосфере корабля",
    ]
    caption_height = sum(font_diagram2.get_height() for _ in caption_lines) + 4
    max_radius = max(10, min(rect.width, rect.height - caption_height - CHART_TITLE_GAP) // 2)
    center = (rect.left + max_radius + 20 + GAS_CHART_H_OFFSET,
              rect.top + caption_height + CHART_TITLE_GAP + max_radius)
    start_angle = -90
    for name, pct, color in GAS_COMPOSITION:
        end_angle = start_angle + pct / 100 * 360
        draw_pie(surface, center, max_radius, start_angle, end_angle, color)
        start_angle = end_angle
    text_x = center[0] + max_radius + 30
    text_y = center[1] - max_radius + 70
    for name, pct, color in GAS_COMPOSITION:
        pygame.draw.rect(surface, color, (text_x, text_y, 18, 18))
        if name == "Кислород":
            label1 = font_gas_label.render(name, True, CYAN)
            label2 = font_gas_label.render(f"{pct:.2f}%", True, CYAN)
            surface.blit(label1, (text_x + 28, text_y - 2))
            surface.blit(label2, (text_x + 28, text_y - 2 + label1.get_height()))
            text_y += label1.get_height() + label2.get_height() + 8
        elif name == "Углекислый газ":
            label1 = font_gas_label.render("Углекислый", True, CYAN)
            label2 = font_gas_label.render(f"газ {pct:.2f}%", True, CYAN)
            surface.blit(label1, (text_x + 28, text_y - 2))
            surface.blit(label2, (text_x + 28, text_y - 2 + label1.get_height()))
            text_y += label1.get_height() + label2.get_height() + 8
        else:
            label = font_gas_label.render(f"{name} {pct:.2f}%", True, CYAN)
            surface.blit(label, (text_x + 28, text_y - 2))
            text_y += label.get_height() + 8
    y = rect.top
    for line in caption_lines:
        text = font_diagram2.render(line, True, CYAN)
        surface.blit(text, text.get_rect(midtop=(rect.centerx, y)))
        y += text.get_height() + 2
    pygame.gfxdraw.aacircle(surface, center[0], center[1], max_radius, CYAN)


def draw_radiation_chart(surface, rect, t):
    rad = 0.015 + 0.005 * math.sin(t / 90)
    caption_lines = ["Уровень ионизирующего", "излучения"]
    caption_height = sum(font_diagram2.get_height() for _ in caption_lines) + 4
    max_radius = max(10, min(rect.width, rect.height - caption_height - CHART_TITLE_GAP) // 2)
    center = (rect.centerx, rect.top + caption_height + CHART_TITLE_GAP + max_radius)
    sweep = max(1, 360 * rad / 100)
    end_angle = -90 + sweep
    draw_pie(surface, center, max_radius, -90, end_angle, (0, 255, 0))
    pygame.gfxdraw.aacircle(surface, center[0], center[1], max_radius, CYAN)
    value = font_diagram1.render(f"{rad:.2f} мкЗв/ч", True, CYAN)
    note = font_diagram3.render("(В пределах нормы)", True, CYAN)
    total_h = value.get_height() + note.get_height() + 4
    text_y = center[1] + max_radius - total_h - 67
    surface.blit(value, (center[0] - value.get_width() // 2, text_y))
    surface.blit(note, (center[0] - note.get_width() // 2, text_y + value.get_height() + 4))
    y = rect.top
    for line in caption_lines:
        text = font_diagram2.render(line, True, CYAN)
        surface.blit(text, text.get_rect(midtop=(rect.centerx, y)))
        y += text.get_height() + 2


def spawn_asteroid(center, radius):
    img = random.choice(ASTEROID_IMAGES)
    spawn = pygame.time.get_ticks()
    rot_speed = random.uniform(-30, 30)
    for _ in range(20):
        start_angle = random.uniform(0, 360)
        start = pygame.Vector2(center) + pygame.Vector2(radius + ASTEROID_SIZE, 0).rotate(start_angle)
        dir_angle = random.uniform(0, 360)
        vel = pygame.Vector2(1, 0).rotate(dir_angle)
        to_center = pygame.Vector2(center) - start
        if vel.dot(to_center) <= 0:
            continue
        if abs(to_center.cross(vel.normalize())) < ASTEROID_SIZE * 2:
            continue
        asteroids.append({
            "pos": start,
            "vel": vel.normalize() * ASTEROID_SPEED,
            "spawn": spawn,
            "rot_speed": rot_speed,
            "img": img,
            "last_detect": 0,
            "coord": "",
        })
        break


def draw_radar(surface, rect, t):
    center = rect.center
    radius = min(rect.width, rect.height) // 2 - 10
    local_center = (rect.width // 2, rect.height // 2)

    radar_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # grid circles
    for r in range(radius // 4, radius + 1, radius // 4):
        pygame.draw.circle(radar_surface, CYAN, local_center, r, 1)
    # cross lines
    pygame.draw.line(radar_surface, CYAN, (local_center[0] - radius, local_center[1]),
                     (local_center[0] + radius, local_center[1]), 1)
    pygame.draw.line(radar_surface, CYAN, (local_center[0], local_center[1] - radius),
                     (local_center[0], local_center[1] + radius), 1)

    angle = (t * RADAR_SWEEP_SPEED) % 360

    # хвост за линией сканирования
    trail = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for i in range(RADAR_TRAIL_STEP, RADAR_TRAIL_LENGTH + RADAR_TRAIL_STEP, RADAR_TRAIL_STEP):
        seg_start = angle - i
        seg_end = angle - i + RADAR_TRAIL_STEP
        alpha = max(0, 120 * (1 - i / RADAR_TRAIL_LENGTH))
        draw_pie(trail, local_center, radius, seg_start, seg_end, (*CYAN, int(alpha)))
    radar_surface.blit(trail, (0, 0))

    now = pygame.time.get_ticks()
    global last_asteroid_spawn
    if len(asteroids) < ASTEROID_MAX_COUNT and now - last_asteroid_spawn >= ASTEROID_SPAWN_INTERVAL:
        spawn_asteroid(center, radius)
        last_asteroid_spawn = now

    for a in asteroids[:]:
        dt = (now - a['spawn']) / 1000
        pos = a['pos'] + a['vel'] * dt
        dist = pygame.Vector2(pos).distance_to(center)
        if dist > radius + ASTEROID_SIZE:
            asteroids.remove(a)
            continue
        if dist <= radius:
            rot = a['rot_speed'] * dt
            img = pygame.transform.rotate(a['img'], rot)
            img_rect = img.get_rect(center=(int(pos.x - rect.left), int(pos.y - rect.top)))
            radar_surface.blit(img, img_rect)
            frame = img_rect.inflate(4, 4)

            angle_to = (math.degrees(math.atan2(pos.y - center[1], pos.x - center[0])) + 360) % 360
            diff = (angle - angle_to) % 360
            if diff < RADAR_SWEEP_SPEED or diff > 360 - RADAR_SWEEP_SPEED:
                a['last_detect'] = now
                a['coord'] = f"{dist:.2f}".replace('.', ',')

            fade = max(0, 255 - (now - a['last_detect']) * ASTEROID_FADE_SPEED / 1000)
            if fade > 0:
                overlay = pygame.Surface(radar_surface.get_size(), pygame.SRCALPHA)
                pygame.draw.rect(overlay, CYAN, frame, 1)
                start = (frame.centerx, frame.top)
                diag_end = (start[0] + 20, start[1] - 20)
                horiz_end = (diag_end[0] + 40, diag_end[1])
                pygame.draw.line(overlay, CYAN, start, diag_end, 1)
                pygame.draw.line(overlay, CYAN, diag_end, horiz_end, 1)
                txt = font_small.render(a['coord'], True, CYAN)
                txt_rect = txt.get_rect(midleft=(horiz_end[0] + 5, horiz_end[1]))
                overlay.blit(txt, txt_rect)
                overlay.set_alpha(int(fade))
                radar_surface.blit(overlay, (0, 0))

    # scanning line
    rad = math.radians(angle)
    end_x = local_center[0] + radius * math.cos(rad)
    end_y = local_center[1] + radius * math.sin(rad)
    pygame.draw.line(radar_surface, CYAN, local_center, (end_x, end_y), 2)

    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), local_center, radius)
    radar_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    pygame.draw.rect(surface, BG_COLOR, rect)
    surface.blit(radar_surface, rect.topleft)


def draw_energy_panel(surface, rect, t):
    img = pygame.transform.smoothscale(ENERGY_IMG, ENERGY_IMG_SIZE)
    img_rect = img.get_rect()
    img_rect.topleft = (rect.left - 85, rect.top - 100)
    surface.blit(img, img_rect)

    blink = (pygame.time.get_ticks() // 500) % 2 == 0
    blink_color = ALERT_RED if blink else CYAN

    # flashing warning icon over gauge
    warn_scaled = pygame.transform.smoothscale(WARN_IMG, (120, 120))
    warn_rect = warn_scaled.get_rect(center=(img_rect.centerx, img_rect.top + 250))
    warn_box = warn_rect.inflate(8, 8)
    if blink:
        surface.blit(warn_scaled, warn_rect)

    energy_label = font_energy.render("Энергия 4%", True, blink_color)
    surface.blit(energy_label, energy_label.get_rect(midtop=(img_rect.centerx + 5, img_rect.bottom - 160)))

    x = img_rect.right - 100
    y = img_rect.top + 145
    bar_h = 18
    for name, val in SUBSYSTEMS:
        text = font_small.render(name, True, CYAN)
        surface.blit(text, (x, y))
        bar_rect = pygame.Rect(x, y + text.get_height() + 4, SUBSYS_BAR_WIDTH, bar_h)
        if name in ("Главные двигатели", "Дополнительные двигатели"):
            pygame.draw.rect(surface, blink_color, bar_rect, 2)
            fail_txt = font_small.render("ОТКАЗ", True, blink_color)
            surface.blit(fail_txt, (bar_rect.centerx - fail_txt.get_width() // 2,
                                    bar_rect.centery - fail_txt.get_height() // 2))
        else:
            pygame.draw.rect(surface, CYAN, bar_rect, 2)
            inner_w = int((SUBSYS_BAR_WIDTH - 4) * val / 100)
            pygame.draw.rect(surface, CYAN,
                             (bar_rect.left + 2, bar_rect.top + 2,
                              inner_w, bar_rect.height - 4))
        y = bar_rect.bottom + 15

    pad = 6
    # fuel status split into two lines
    fuel_line1 = font_energy2.render("Состояние топливных баков:", True, CYAN)
    fuel_line2 = font_energy2.render("НОРМАЛЬНОЕ", True, CYAN)
    fuel_width = max(fuel_line1.get_width(), fuel_line2.get_width())
    fuel_height = fuel_line1.get_height() + fuel_line2.get_height()
    fuel_rect = pygame.Rect(0, 0, fuel_width, fuel_height)
    fuel_rect.centerx = rect.centerx + FUEL_STATUS_OFFSET[0]
    fuel_rect.bottom = rect.bottom + FUEL_STATUS_OFFSET[1]
    fuel_box = fuel_rect.inflate(pad * 2, pad * 2)
    pygame.draw.rect(surface, CYAN, fuel_box, 2)
    surface.blit(fuel_line1, (fuel_rect.centerx - fuel_line1.get_width() // 2, fuel_rect.top))
    surface.blit(fuel_line2, (fuel_rect.centerx - fuel_line2.get_width() // 2,
                              fuel_rect.top + fuel_line1.get_height()))

    # generator status split into two lines
    gen_line1 = font_energy2.render("Состояние генераторов:", True, blink_color)
    gen_line2 = font_energy2.render("КРИТИЧЕСКОЕ", True, blink_color)
    gen_width = max(gen_line1.get_width(), gen_line2.get_width())
    gen_height = gen_line1.get_height() + gen_line2.get_height()
    gen_rect = pygame.Rect(0, 0, gen_width, gen_height)
    gen_rect.centerx = rect.centerx + GEN_STATUS_OFFSET[0]
    gen_rect.bottom = rect.bottom + GEN_STATUS_OFFSET[1]
    gen_box = gen_rect.inflate(pad * 2, pad * 2)
    pygame.draw.rect(surface, blink_color, gen_box, 2)
    surface.blit(gen_line1, (gen_rect.centerx - gen_line1.get_width() // 2, gen_rect.top))
    surface.blit(gen_line2, (gen_rect.centerx - gen_line2.get_width() // 2,
                             gen_rect.top + gen_line1.get_height()))

# -------------------------- Разметка окон ---------------------------
MARGIN = 20
CELL_W = (WIDTH - MARGIN * 4) // 3
CELL_H = (HEIGHT - MARGIN * 3) // 2

combined = pygame.Rect(MARGIN, MARGIN, CELL_W * 2 + MARGIN, CELL_H)
top_right = pygame.Rect(MARGIN * 3 + CELL_W * 2, MARGIN, CELL_W, CELL_H)
bottom_left = pygame.Rect(MARGIN, MARGIN * 2 + CELL_H, CELL_W, CELL_H)
bottom_mid = pygame.Rect(MARGIN * 2 + CELL_W, MARGIN * 2 + CELL_H, CELL_W, CELL_H)
bottom_right = pygame.Rect(MARGIN * 3 + CELL_W * 2, MARGIN * 2 + CELL_H, CELL_W, CELL_H)
cells = [combined, top_right, bottom_left, bottom_mid, bottom_right]

enlarged_map = None  # 0 -> none, 1 -> map1, 2 -> map2
map_anim = None  # animation state for map expansion/collapse
map2_entry_visible = True
map2_btn_rect = None
map2_activation_visible = False
map2_act_btn_rect = None


def draw_layout(t):
    for idx, rect in enumerate(cells):
        pygame.draw.rect(screen, CYAN, rect, 2, border_radius=12)
        if idx == 0:
            therm_h = int(rect.height * THERM_HEIGHT_RATIO)
            therm_rect = pygame.Rect(
                rect.left + THERM_POS[0],
                rect.top + (rect.height - therm_h) // 2 + THERM_POS[1],
                THERM_WIDTH,
                therm_h,
                )
            rad_w, rad_h = RAD_CHART_SIZE
            rad_h = min(rad_h, rect.height)
            rad_rect = pygame.Rect(
                rect.left + RAD_CHART_POS[0],
                rect.top + (rect.height - rad_h) // 2 + RAD_CHART_POS[1],
                rad_w,
                rad_h,
                )
            gas_w, gas_h = GAS_CHART_SIZE
            gas_h = min(gas_h, rect.height)
            gas_rect = pygame.Rect(
                rect.left + GAS_CHART_POS[0],
                rect.top + (rect.height - gas_h) // 2 + GAS_CHART_POS[1],
                gas_w,
                gas_h,
                )
            update_gases()
            update_temp()
            therm_img = pygame.transform.smoothscale(THERM_IMG, therm_rect.size)
            screen.blit(therm_img, therm_rect)
            temp_text = font_therm.render(f"{current_temp}°C", True, CYAN)
            tx = therm_rect.centerx - temp_text.get_width() // 2 + THERM_DEG_OFFSET[0]
            ty = therm_rect.bottom + THERM_DEG_OFFSET[1]
            screen.blit(temp_text, (tx, ty))
            draw_radiation_chart(screen, rad_rect, t)
            draw_gas_chart(screen, gas_rect)
        elif idx == 1:
            draw_energy_panel(screen, rect, t)
        elif idx == 2:
            draw_radar(screen, rect, t)
            pygame.draw.rect(screen, CYAN, rect, 2, border_radius=12)
        elif idx == 3:
            hide = False
            if enlarged_map == 1:
                hide = True
            if map_anim and map_anim['which'] == 1:
                hide = True
            if not hide:
                inner = rect.inflate(-20, -20)
                img = pygame.transform.smoothscale(MAP1_IMG, inner.size)
                screen.blit(img, inner)
                draw_no_threat_box(screen, rect)
            pygame.draw.rect(screen, CYAN, rect, 2, border_radius=12)
        elif idx == 4:
            global map2_btn_rect
            hide = False
            if enlarged_map == 2 or (map_anim and map_anim['which'] == 2):
                hide = True
            if not hide:
                inner = rect.inflate(-20, -20)
                img = pygame.transform.smoothscale(MAP2_IMG, inner.size)
                screen.blit(img, inner)
                draw_zaryad_icons(screen, inner)
                if map2_entry_visible:
                    panel = inner.copy()
                    pygame.draw.rect(screen, BG_COLOR, panel)
                    pygame.draw.rect(screen, CYAN, panel, 2, border_radius=8)
                    label1 = font_therm.render("Вход в систему", True, CYAN)
                    label2 = font_therm.render("cамоуничтожения корабля", True, CYAN)
                    screen.blit(label1, label1.get_rect(midtop=(panel.centerx, panel.top + 140)))
                    screen.blit(label2, label2.get_rect(midtop=(panel.centerx, panel.top + 180)))
                    btn = pygame.Rect(0, 0, 210, 80)
                    btn.center = (panel.centerx, panel.centery + panel.height // 4 - 80)
                    pygame.draw.rect(screen, CYAN, btn, 2, border_radius=8)
                    btn_txt = font_enter.render("Войти", True, CYAN)
                    screen.blit(btn_txt, btn_txt.get_rect(center=btn.center))
                    map2_btn_rect = btn
                elif map2_activation_visible:
                    panel = pygame.Rect(0, 0, ACTIVATE_PANEL_SIZE[0], ACTIVATE_PANEL_SIZE[1])
                    panel.center = inner.center
                    pygame.draw.rect(screen, BG_COLOR, panel)
                    pygame.draw.rect(screen, CYAN, panel, 2, border_radius=8)
                    label1 = font_activate_label.render("Активация", True, CYAN)
                    label2 = font_activate_label.render("взрывных зарядов", True, CYAN)
                    screen.blit(label1, label1.get_rect(midtop=(panel.centerx, panel.top + 30)))
                    screen.blit(label2, label2.get_rect(midtop=(panel.centerx, panel.top + 30 + label1.get_height() + 10)))
                    btn = pygame.Rect(0, 0, ACTIVATE_BUTTON_SIZE[0], ACTIVATE_BUTTON_SIZE[1])
                    btn.center = (panel.centerx, panel.bottom - ACTIVATE_BUTTON_SIZE[1] // 2 - 20)
                    pygame.draw.rect(screen, CYAN, btn, 2, border_radius=8)
                    btn_txt = font_activate_btn.render("Активировать", True, CYAN)
                    screen.blit(btn_txt, btn_txt.get_rect(center=btn.center))
                    map2_act_btn_rect = btn
                    map2_btn_rect = None
                else:
                    map2_btn_rect = None
                    map2_act_btn_rect = None
            pygame.draw.rect(screen, CYAN, rect, 2, border_radius=12)

def draw_zaryad_icons(surface, map_rect, collect=False):
    scale_x = map_rect.width / MAP2_ORIG_W
    scale_y = map_rect.height / MAP2_ORIG_H
    if collect:
        zaryad_rects.clear()
    now = pygame.time.get_ticks()
    for i, z in enumerate(zaryads):
        px, py = z["pos"]
        icon_w = int(ZARYAD_ICON_SIZE * scale_x)
        icon_h = int(ZARYAD_ICON_SIZE * scale_y)
        base = pygame.transform.smoothscale(ZARYAD_IMG, (icon_w, icon_h))
        active = pygame.transform.smoothscale(ZARYAD_ACTIVE_IMG, (icon_w, icon_h))
        if z["anim_start"] is not None:
            pr = min(1, (now - z["anim_start"]) / 300)
            temp = base.copy()
            active_img = active.copy(); active_img.set_alpha(int(pr * 255))
            temp.blit(active_img, (0, 0))
            if pr >= 1:
                z["anim_start"] = None
                z["activated"] = True
            icon = temp
        else:
            icon = active if z["activated"] else base
        rect = icon.get_rect(center=(map_rect.left + px * scale_x, map_rect.top + py * scale_y))
        surface.blit(icon, rect)
        label = font_zaryad_label.render(f"Заряд {i+1}", True, CYAN)
        label_rect = label.get_rect(
            midtop=(rect.centerx + ZARYAD_LABEL_OFFSET[0], rect.bottom + ZARYAD_LABEL_OFFSET[1])
        )
        surface.blit(label, label_rect)
        if collect:
            zaryad_rects.append({"icon": rect, "label": label_rect})



def draw_no_threat_box(surface, rect):
    msg = font_small.render("Угроз не обнаружено", True, CYAN)
    box = msg.get_rect()
    box.inflate_ip(20, 10)
    box.midtop = (rect.centerx, rect.top + 10)
    pygame.draw.rect(surface, BG_COLOR, box)
    pygame.draw.rect(surface, CYAN, box, 2)
    surface.blit(msg, msg.get_rect(center=box.center))

def draw_enlarged_map(which):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    w = int(WIDTH * 0.8)
    h = int(HEIGHT * 0.8)
    rect = pygame.Rect(0, 0, w, h)
    rect.center = (WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, CYAN, rect, 2, border_radius=12)
    inner = rect.inflate(-20, -20)
    img = MAP1_IMG if which == 1 else MAP2_IMG
    img = pygame.transform.smoothscale(img, inner.size)
    screen.blit(img, inner)
    if which == 1:
        draw_no_threat_box(screen, rect)
    if which == 2:
        draw_zaryad_icons(screen, inner, collect=True)
        msg = font_zaryad_hint.render("Нажмите на заряд, чтобы активировать его", True, CYAN)
        box = msg.get_rect()
        box.inflate_ip(20, 10)
        box.midbottom = (
            inner.centerx + ZARYAD_HINT_OFFSET[0],
            rect.bottom + ZARYAD_HINT_OFFSET[1],
        )
        pygame.draw.rect(screen, BG_COLOR, box)
        pygame.draw.rect(screen, CYAN, box, 2)
        screen.blit(msg, msg.get_rect(center=box.center))
        if map2_confirm is not None:
            idx = map2_confirm["index"]
            icon_rect = zaryad_rects[idx]["icon"]
            panel_w, panel_h = CONFIRM_PANEL_SIZE
            panel = pygame.Rect(0, 0, panel_w, panel_h)
            panel.center = icon_rect.center
            pygame.draw.rect(screen, BG_COLOR, panel)
            pygame.draw.rect(screen, CYAN, panel, 2, border_radius=8)
            title = font_confirm_title.render("Подтвердите активацию заряда", True, CYAN)
            screen.blit(title, title.get_rect(midtop=(panel.centerx, panel.top + 15)))
            text1 = font_confirm_text.render("Я принимаю все риски и осознаю", True, CYAN)
            text2 = font_confirm_text.render("что произойдёт после активации", True, CYAN)
            chk_size = 24
            chk_rect = pygame.Rect(panel.left + 20, panel.top + 80, chk_size, chk_size)
            pygame.draw.rect(screen, CYAN, chk_rect, 2)
            if map2_confirm["checked"]:
                inner_chk = chk_rect.inflate(-8, -8)
                pygame.draw.rect(screen, CYAN, inner_chk)
            screen.blit(text1, (chk_rect.right + 10, chk_rect.top - 4))
            screen.blit(text2, (chk_rect.right + 10, chk_rect.top + text1.get_height() - 4))
            text_rect = pygame.Rect(
                chk_rect.right + 10,
                chk_rect.top - 4,
                max(text1.get_width(), text2.get_width()),
                text1.get_height() + text2.get_height(),
                )
            btn = pygame.Rect(0, 0, CONFIRM_BUTTON_SIZE[0], CONFIRM_BUTTON_SIZE[1])
            btn.center = (panel.centerx, panel.bottom - CONFIRM_BUTTON_SIZE[1] // 2 - 20)
            color = CYAN if map2_confirm["checked"] else (0, 100, 100)
            pygame.draw.rect(screen, color, btn, 2, border_radius=8)
            btn_txt = font_confirm_btn.render("Активировать", True, color if map2_confirm["checked"] else (100, 160, 160))
            screen.blit(btn_txt, btn_txt.get_rect(center=btn.center))
            map2_confirm["checkbox"] = chk_rect
            map2_confirm["text_rect"] = text_rect
            map2_confirm["button"] = btn
            map2_confirm["panel"] = panel


def get_small_map_rect(which):
    rect = cells[3] if which == 1 else cells[4]
    return rect.inflate(-20, -20)


def get_large_map_rects():
    w = int(WIDTH * 0.8)
    h = int(HEIGHT * 0.8)
    outer = pygame.Rect(0, 0, w, h)
    outer.center = (WIDTH // 2, HEIGHT // 2)
    inner = outer.inflate(-20, -20)
    return outer, inner


def lerp_rect(r1, r2, t):
    return pygame.Rect(
        r1.x + (r2.x - r1.x) * t,
        r1.y + (r2.y - r1.y) * t,
        r1.w + (r2.w - r1.w) * t,
        r1.h + (r2.h - r1.h) * t,
        )

# ------------------------- Логика газов -----------------------------
gas_toggle = False
gas_next_switch = 0

def update_gases():
    global gas_toggle, gas_next_switch, GAS_COMPOSITION
    now = pygame.time.get_ticks()
    if now >= gas_next_switch:
        gas_toggle = not gas_toggle
        if gas_toggle:
            GAS_COMPOSITION[0][1] = 78.09
            GAS_COMPOSITION[3][1] = 0.03
        else:
            GAS_COMPOSITION[0][1] = 78.08
            GAS_COMPOSITION[3][1] = 0.04
        gas_next_switch = now + random.randint(2000, 5000)

# ----------------------- Логика температуры ------------------------
current_temp = 21
temp_next_switch = 0

def update_temp():
    global current_temp, temp_next_switch
    now = pygame.time.get_ticks()
    if now >= temp_next_switch:
        current_temp = 22 if current_temp == 21 else 21
        temp_next_switch = now + random.randint(4000, 8000)


def run_self_destruct_animation(duration_ms=10000):
    msg_base = "Инициализация последовательности самоуничтожения корабля"
    start = pygame.time.get_ticks()
    last_update = start
    last_dot = 0
    console = []
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        now = pygame.time.get_ticks()
        elapsed = now - start
        progress = min(elapsed / duration_ms, 1.0)
        if now - last_update > 300:
            last_update = now
            console.append(random.choice([
                "VENT FUEL", "ARM REACTOR", "SYNC NODES",
                "PURGE COOLANT", "SEAL BULKHEADS", "CHARGE COILS"]))
            if len(console) > 12:
                console.pop(0)
            last_dot = (last_dot % 3) + 1
        screen.blit(overlay, (0, 0))
        dots = "." * last_dot
        title = font_confirm_title.render(f"{msg_base}{dots}", True, CYAN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
        bar_w = WIDTH * 0.6
        bar_h = 25
        bar_x = WIDTH * 0.2
        bar_y = HEIGHT // 2 - bar_h // 2
        pygame.draw.rect(screen, CYAN, (bar_x, bar_y, bar_w, bar_h), 2)
        fill_w = bar_w * progress
        pygame.draw.rect(screen, CYAN, (bar_x + 2, bar_y + 2, fill_w - 4, bar_h - 4))
        log_y = bar_y + bar_h + 40
        for line in console:
            txt = font_small.render(line, True, CYAN)
            screen.blit(txt, (bar_x, log_y))
            log_y += font_small.get_height() + 4
        pygame.display.flip()
        clock.tick(30)
        if progress >= 1.0:
            break

    show_game_over()


def show_game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
        screen.fill(BG_COLOR)
        txt = font_countdown.render("Игра окончена", True, CYAN)
        screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()
        clock.tick(60)
# ------------------------------ Main --------------------------------

def main():
    global enlarged_map, map_anim, map2_entry_visible, map2_btn_rect, map2_confirm, map2_activation_visible, map2_act_btn_rect, countdown, final_confirm
    t = 0
    anim_dur = 300
    while True:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if map_anim:
                    map_anim = None
                elif enlarged_map == 2 and map2_confirm is not None:
                    map2_confirm = None
                elif map2_activation_visible:
                    map2_activation_visible = False
                    map2_entry_visible = True
                elif enlarged_map is not None:
                    outer, inner = get_large_map_rects()
                    target = get_small_map_rect(enlarged_map)
                    map_anim = {
                        'which': enlarged_map,
                        'from_rect': inner,
                        'to_rect': target,
                        'start': now,
                        'dur': anim_dur,
                        'opening': False,
                    }
                    enlarged_map = None
                else:
                    pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if final_confirm:
                    for i, box in enumerate(final_confirm['boxes']):
                        if box.collidepoint(event.pos):
                            final_confirm['checked'][i] = not final_confirm['checked'][i]
                    if (
                            final_confirm['btn']
                            and final_confirm['btn'].collidepoint(event.pos)
                            and all(final_confirm['checked'])
                    ):
                        countdown = {'value': 20, 'last': now, 'flash': 0}
                        final_confirm = None
                    continue
                if map_anim:
                    continue
                if map2_entry_visible:
                    if map2_btn_rect and map2_btn_rect.collidepoint(event.pos):
                        map2_entry_visible = False
                        map2_activation_visible = True
                    continue
                if map2_activation_visible:
                    if map2_act_btn_rect and map2_act_btn_rect.collidepoint(event.pos):
                        map2_activation_visible = False
                        which = 2
                        start_rect = get_small_map_rect(which)
                        _, end_rect = get_large_map_rects()
                        map_anim = {
                            'which': which,
                            'from_rect': start_rect,
                            'to_rect': end_rect,
                            'start': now,
                            'dur': anim_dur,
                            'opening': True,
                        }
                        continue
                if enlarged_map is not None:
                    if enlarged_map == 2 and map2_confirm is not None:
                        if map2_confirm["checkbox"].collidepoint(event.pos) or (
                                map2_confirm.get("text_rect") and map2_confirm["text_rect"].collidepoint(event.pos)
                        ):
                            map2_confirm["checked"] = not map2_confirm["checked"]
                        elif map2_confirm["button"].collidepoint(event.pos) and map2_confirm["checked"]:
                            idx = map2_confirm["index"]
                            zaryads[idx]["anim_start"] = now
                            map2_confirm = None
                        elif not map2_confirm["panel"].collidepoint(event.pos):
                            map2_confirm = None
                    else:
                        clicked = False
                        if enlarged_map == 2:
                            for idx, r in enumerate(zaryad_rects):
                                if zaryads[idx]["activated"]:
                                    continue
                                if r["icon"].collidepoint(event.pos) or r["label"].collidepoint(event.pos):
                                    map2_confirm = {"index": idx, "checked": False}
                                    clicked = True
                                    break
                        if not clicked:
                            _, inner = get_large_map_rects()
                            if not inner.collidepoint(event.pos):
                                target = get_small_map_rect(enlarged_map)
                                map_anim = {
                                    'which': enlarged_map,
                                    'from_rect': inner,
                                    'to_rect': target,
                                    'start': now,
                                    'dur': anim_dur,
                                    'opening': False,
                                }
                                enlarged_map = None
                                map2_confirm = None
                else:
                    if cells[3].collidepoint(event.pos):
                        which = 1
                    elif cells[4].collidepoint(event.pos):
                        which = 2
                    else:
                        which = None
                    if which:
                        start_rect = get_small_map_rect(which)
                        _, end_rect = get_large_map_rects()
                        map_anim = {
                            'which': which,
                            'from_rect': start_rect,
                            'to_rect': end_rect,
                            'start': now,
                            'dur': anim_dur,
                            'opening': True,
                        }
        if countdown is None and final_confirm is None and all(z['activated'] for z in zaryads):
            final_confirm = {'checked': [False, False, False], 'boxes': [], 'btn': None}

        screen.fill(BG_COLOR)
        draw_layout(t)
        if map_anim:
            elapsed = now - map_anim['start']
            pr = min(1, elapsed / map_anim['dur'])
            rect = lerp_rect(map_anim['from_rect'], map_anim['to_rect'], pr)
            alpha = int(180 * (pr if map_anim['opening'] else 1 - pr))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            screen.blit(overlay, (0, 0))
            img = MAP1_IMG if map_anim['which'] == 1 else MAP2_IMG
            img = pygame.transform.smoothscale(img, rect.size)
            screen.blit(img, rect)
            pygame.draw.rect(screen, CYAN, rect.inflate(20, 20), 2, border_radius=12)
            if pr >= 1:
                if map_anim['opening']:
                    enlarged_map = map_anim['which']
                map_anim = None
        elif enlarged_map:
            draw_enlarged_map(enlarged_map)

        if final_confirm:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            panel = pygame.Rect(0, 0, ACTIVATE_PANEL_SIZE[0], ACTIVATE_PANEL_SIZE[1])
            panel.center = (WIDTH // 2, HEIGHT // 2)
            pygame.draw.rect(screen, BG_COLOR, panel)
            pygame.draw.rect(screen, CYAN, panel, 2, border_radius=8)
            texts = [
                "Я нахожусь в здравом уме",
                "Я осознаю все последствия",
                "Получать рассылку о новостях, акциях и релизах",
            ]
            final_confirm['boxes'] = []
            y = panel.top + 40
            for i, line in enumerate(texts):
                box = pygame.Rect(panel.left + 30, y, 30, 30)
                pygame.draw.rect(screen, CYAN, box, 2)
                if final_confirm['checked'][i]:
                    inner = box.inflate(-8, -8)
                    pygame.draw.rect(screen, CYAN, inner)
                txt = font_confirm_text2.render(line, True, CYAN)
                screen.blit(txt, (box.right + 10, box.centery - txt.get_height() // 2))
                final_confirm['boxes'].append(box)
                y += 40
            btn = pygame.Rect(0, 0, ACTIVATE_BUTTON_SIZE[0] + 100, ACTIVATE_BUTTON_SIZE[1])
            btn.center = (panel.centerx, panel.bottom - ACTIVATE_BUTTON_SIZE[1] // 2 - 20)
            color = CYAN if all(final_confirm['checked']) else (80, 80, 80)
            pygame.draw.rect(screen, color, btn, 2, border_radius=8)
            txt = font_activate_btn.render("Закончить миссию", True, color)
            screen.blit(txt, txt.get_rect(center=btn.center))
            final_confirm['btn'] = btn

        if countdown:
            if now - countdown['last'] >= 1000:
                countdown['value'] -= 1
                countdown['last'] = now
                countdown['flash'] = now + 200
                if countdown['value'] <= 0:
                    run_self_destruct_animation()
                    countdown = None
                    continue
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            color = ALERT_RED if countdown['flash'] > now else CYAN
            num = font_countdown.render(str(countdown['value']), True, color)
            screen.blit(num, num.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()
        clock.tick(60)
        t += 1

if __name__ == "__main__":
    main()