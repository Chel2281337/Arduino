import sys, os, pygame, serial, time

# ---------------------------- Параметры ----------------------------
IMAGE_PATH = "img/12345.png"
FULLSCREEN = True
TITLE = "ТЕРМИНАЛ ДОСТУПА"

BG_COLOR = (10, 15, 26)
CYAN = (222, 255, 255)
DOOR_COLOR_CLOSED = (255, 165, 0)
DOOR_COLOR_OPENED = (0, 255, 0)
ALERT_RED = (255, 60, 0)

ANIM_DURATION = 5500
OPEN_FRACTION = 1
USE_PASSWORDS = True

MAP_ORIGINAL_SIZE = (1024, 768)
# ширина области под легенду слева
LEGEND_WIDTH = 300
# размер шрифта легенды
LEGEND_FONT_SIZE = 33
LEGEND_LINE_SPACING = LEGEND_FONT_SIZE + 4
LEGEND_ICON_SIZE = 50
LEGEND_ICON_SPACING = 10
LEGEND_SCROLL_SPEED = 20
SCROLLBAR_WIDTH = 12

# заголовок сверху и его размер
HEADER_TEXT = "ПАНЕЛЬ УПРАВЛЕНИЯ"
HEADER_FONT_SIZE = 48

# дополнительная настраиваемая подпись
CUSTOM_LABEL_TEXT = ""
CUSTOM_LABEL_FONT_SIZE = 32
CUSTOM_LABEL_POS = (0, 0)

ERROR_DURATION = 4500
ERROR_BLINK_MS = 600

try:  # ???
    ser = serial.Serial('COM3', 9600)
    time.sleep(2)
except Exception:
    ser = None
serial_buffer = ""
# ------------------------------------------------------------------

pygame.init()
flags = pygame.FULLSCREEN if FULLSCREEN else 0
screen = pygame.display.set_mode((0, 0), flags) if FULLSCREEN else pygame.display.set_mode((1280, 1024))
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

font_big = pygame.font.Font(None, 56)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
legend_font = pygame.font.Font(None, LEGEND_FONT_SIZE)
font_number = pygame.font.Font(None, 90)
header_font = pygame.font.Font(None, HEADER_FONT_SIZE)
custom_label_font = pygame.font.Font(None, CUSTOM_LABEL_FONT_SIZE)

# элементы иконок легенды
legend_icon_items = [
    ("-  Терминал", "img/terminal.png"),
    ("-  Роборука", "img/ruki.png"),
    ("-  Сервер", "img/server.png"),
    ("-  Криокамера", "img/krio.png"),
    ("-  Управление кораблём", "img/rul.png"),
    ("-  Роборука", "img/ruki.png"),
    ("-  Сервер", "img/server.png"),
    ("-  Криокамера", "img/krio.png"),
]
legend_icons = [
    (name, pygame.transform.smoothscale(pygame.image.load(path).convert_alpha(),
                                        (LEGEND_ICON_SIZE, LEGEND_ICON_SIZE)))
    for name, path in legend_icon_items
]
icon_scroll = 0
legend_icons_rect = pygame.Rect(0, 0, 0, 0)
scroll_track_rect = pygame.Rect(0, 0, 0, 0)
scroll_thumb_rect = pygame.Rect(0, 0, 0, 0)
dragging_thumb = False

# размеры иконок
TERMINAL_ICON_SIZE = 40
RUKI_ICON_SIZE = 40
SERVER_ICON_SIZE = 40
KRIO_ICON_SIZE = 38
STOLOV_ICON_SIZE = 50
RUL_ICON_SIZE = 50
COM_ICON_SIZE = 50
LOCK_ICON_SIZE = 29

# вертикальные смещения замков относительно центра двери
LOCK_OFFSET_VERTICAL = 0
LOCK_OFFSET_HORIZONTAL = -6

WARN_IMG = pygame.image.load("img/warn.png").convert_alpha()


class MapIcon:
    def __init__(self, rel_pos, image_path, size):
        self.rel_pos = pygame.Vector2(rel_pos)
        self.image_path = image_path
        self.size = size
        self.img_raw = pygame.image.load(image_path).convert_alpha()
        self.img = pygame.transform.smoothscale(self.img_raw, (size, size))
        self.pos = self.rel_pos.copy()

    def update_pos(self, map_rect):
        sx = map_rect.width / MAP_ORIGINAL_SIZE[0]
        sy = map_rect.height / MAP_ORIGINAL_SIZE[1]
        self.pos.x = map_rect.left + self.rel_pos.x * sx
        self.pos.y = map_rect.top + self.rel_pos.y * sy
        scaled = int(self.size * (sx + sy) / 2)
        self.img = pygame.transform.smoothscale(self.img_raw, (scaled, scaled))

    def draw(self, surf):
        rect = self.img.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        surf.blit(self.img, rect)


def wrap_text(text, font, max_width):
    """Split text into at most two lines so that each fits max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if not current or font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
        if len(lines) == 2:
            break
    if len(lines) < 2 and current:
        lines.append(current)
    return lines


def draw_glow_rect(surf, rect, color, width=3, radius=10):
    pygame.draw.rect(surf, color, rect, width, border_radius=radius)

# ---------------------------- Пароль -------------------------------
class PasswordPrompt:
    def __init__(self):
        w, h = 720, 440
        self.rect = pygame.Rect(WIDTH // 2 - w // 2, HEIGHT // 2 - h // 2 - 120, w, h)
        self.text = ""
        self.done = False
        self.accepted = False
        bx = self.rect.x + 40
        by = self.rect.bottom - 120
        self.btn_ok = pygame.Rect(bx, by, 280, 80)
        self.btn_cancel = pygame.Rect(bx + 360, by, 280, 80)
        # экранная клавиатура в стиле QWERTY
        self.key_layout = [
            "1234567890←",
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM",
        ]
        self.key_rects = []
        key_w, key_h = 100, 100
        start_y = self.rect.bottom + 20
        for row_i, row in enumerate(self.key_layout):
            row_len = len(row)
            start_x = WIDTH // 2 - (row_len * key_w) // 2
            for col_i, ch in enumerate(row):
                r = pygame.Rect(start_x + col_i * key_w, start_y + row_i * key_h, key_w - 4, key_h - 4)
                self.key_rects.append((r, ch))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
            elif event.key == pygame.K_RETURN:
                self.accepted = True
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isalnum():
                self.text += event.unicode.upper()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_ok.collidepoint(event.pos):
                self.accepted = True
                self.done = True
            elif self.btn_cancel.collidepoint(event.pos):
                self.done = True
            else:
                for r, ch in self.key_rects:
                    if r.collidepoint(event.pos):
                        if ch == '←':
                            self.text = self.text[:-1]
                        else:
                            self.text += ch
                        break

    def draw(self, surf):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surf.blit(overlay, (0, 0))
        pygame.draw.rect(surf, CYAN, self.rect, 3, border_radius=12)
        label = font_medium.render("Введите пароль", True, CYAN)
        surf.blit(label, label.get_rect(center=(self.rect.centerx, self.rect.top + 40)))
        masked = "*" * len(self.text)
        txt = font_medium.render(masked, True, CYAN)
        surf.blit(txt, txt.get_rect(center=self.rect.center))
        pygame.draw.rect(surf, CYAN, self.btn_ok, 2, border_radius=8)
        pygame.draw.rect(surf, CYAN, self.btn_cancel, 2, border_radius=8)
        ok_txt = font_small.render("ОК", True, CYAN)
        cancel_txt = font_small.render("Отмена", True, CYAN)
        surf.blit(ok_txt, ok_txt.get_rect(center=self.btn_ok.center))
        surf.blit(cancel_txt, cancel_txt.get_rect(center=self.btn_cancel.center))
        for r, ch in self.key_rects:
            pygame.draw.rect(surf, CYAN, r, 2, border_radius=4)
            if ch == '←':
                cx, cy = r.center
                arrow = [
                    (cx + 20, cy - 20),
                    (cx - 10, cy - 20),
                    (cx - 10, cy - 35),
                    (cx - 40, cy),
                    (cx - 10, cy + 35),
                    (cx - 10, cy + 20),
                    (cx + 20, cy + 20),
                ]
                pygame.draw.polygon(surf, CYAN, arrow)
            else:
                t = font_small.render(ch, True, CYAN)
                surf.blit(t, t.get_rect(center=r.center))


def ask_password():
    prompt = PasswordPrompt()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            prompt.handle_event(event)
        draw_map_and_doors()
        prompt.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        if prompt.done:
            return prompt.text if prompt.accepted else None
# ------------------------------------------------------------------

# универсальный вывод ошибки
def show_error(message, draw_scene, blink_draw):
    err_rect = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 190, 600, 380)
    warn_img = pygame.transform.smoothscale(WARN_IMG, (180, 180))
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < ERROR_DURATION:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        draw_scene()
        blink = (pygame.time.get_ticks() // ERROR_BLINK_MS) % 2 == 0
        blink_draw(blink)
        if blink:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 0, 0, 80))
            screen.blit(flash, (0, 0))
        bg = (60, 0, 0) if blink else BG_COLOR
        pygame.draw.rect(screen, bg, err_rect)
        pygame.draw.rect(screen, ALERT_RED, err_rect, 3, border_radius=12)
        if blink:
            screen.blit(warn_img, warn_img.get_rect(center=(err_rect.centerx, err_rect.top + 140)))
        msg = font_small.render(message, True, ALERT_RED)
        screen.blit(msg, msg.get_rect(center=(err_rect.centerx, err_rect.bottom - 60)))
        pygame.display.flip()
        clock.tick(60)


def show_password_error(door):
    def draw_scene():
        draw_map_and_doors(exclude=door)

    def blink_draw(blink):
        color = ALERT_RED if blink else door.closed_color
        pygame.draw.rect(screen, color, door.rect)

        if door.lock_icon and door.lock_visible:
            if blink:
                tinted = door.lock_icon.img.copy()
                overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
                overlay.fill((*ALERT_RED, 255))
                tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(
                    tinted,
                    tinted.get_rect(center=(int(door.lock_icon.pos.x), int(door.lock_icon.pos.y)))
                )
            else:
                door.lock_icon.draw(screen)

    show_error("Неверный пароль", draw_scene, blink_draw)
# ------------------------------------------------------------------

# ----------------------------- Двери ---------------------------------
class Door:
    def __init__(self, rel_rect, orientation, password="", open_message="", close_message="",
                 closed_color=DOOR_COLOR_CLOSED, open_color=DOOR_COLOR_OPENED, has_lock=None,
                 lock_size=LOCK_ICON_SIZE):
        self.rel_rect = pygame.Rect(rel_rect)
        self.orientation = orientation  # 'h' or 'v'
        self.password = password
        self.open_message = close_message
        self.close_message = close_message
        self.closed_color = closed_color
        self.open_color = open_color
        self.open = False
        self.rect = self.rel_rect.copy()
        self.part_a = None
        self.part_b = None
        self.anim_state = None  # None, 'opening', 'closing'
        self.anim_start = 0
        self.shift_total = 0
        self.lock_size = lock_size
        if has_lock is None:
            has_lock = bool(password)
        if has_lock:
            if self.orientation == 'v':
                lock_pos = (self.rel_rect.centerx, self.rel_rect.centery + LOCK_OFFSET_VERTICAL)
            else:
                lock_pos = (self.rel_rect.centerx, self.rel_rect.centery + LOCK_OFFSET_HORIZONTAL)
            self.lock_icon = MapIcon(lock_pos, "img/lock.png", self.lock_size)
        else:
            self.lock_icon = None
        self.lock_visible = has_lock

    def update_rect(self, map_rect):
        sx = map_rect.width / MAP_ORIGINAL_SIZE[0]
        sy = map_rect.height / MAP_ORIGINAL_SIZE[1]
        self.rect = pygame.Rect(
            map_rect.left + self.rel_rect.x * sx,
            map_rect.top + self.rel_rect.y * sy,
            self.rel_rect.width * (sx if self.orientation == 'h' else sy),
            self.rel_rect.height * (sy if self.orientation == 'h' else sx)
        )
        if self.open:
            shift = self._compute_shift()
            self.part_a, self.part_b = self._parts_at(shift)
        if self.lock_icon:
            self.lock_icon.update_pos(map_rect)

    def draw(self, surf):
        if self.open or self.anim_state:
            color = self.open_color if (self.open or self.anim_state == 'closing') else self.closed_color
            if not self.part_a or not self.part_b:
                shift = self._compute_shift() if self.open else 0
                self.part_a, self.part_b = self._parts_at(shift)
            pygame.draw.rect(surf, color, self.part_a)
            pygame.draw.rect(surf, color, self.part_b)
        else:
            pygame.draw.rect(surf, self.closed_color, self.rect)

    def _compute_shift(self):
        base = self.rect.width // 2 if self.orientation == 'h' else self.rect.height // 2
        return int(base * OPEN_FRACTION)

    def _parts_at(self, shift):
        left = self.rect.copy()
        right = self.rect.copy()
        if self.orientation == 'h':
            left.width //= 2
            right.width //= 2; right.x = self.rect.centerx
            left.x -= shift
            right.x += shift
        else:
            left.height //= 2
            right.height //= 2; right.y = self.rect.centery
            left.y -= shift
            right.y += shift
        return left, right

    def start_open(self):
        if self.open or self.anim_state:
            return
        self.anim_state = 'opening'
        self.anim_start = pygame.time.get_ticks()
        self.shift_total = self._compute_shift()

    def start_close(self):
        if not self.open or self.anim_state:
            return
        self.anim_state = 'closing'
        self.anim_start = pygame.time.get_ticks()
        self.shift_total = self._compute_shift()
        self.part_a, self.part_b = self._parts_at(self.shift_total)

    def update_animation(self):
        if not self.anim_state:
            return
        elapsed = pygame.time.get_ticks() - self.anim_start
        pr = min(elapsed / ANIM_DURATION, 1.0)
        pr = pr * pr * (3 - 2 * pr)  # smoothstep
        if self.anim_state == 'opening':
            shift = int(self.shift_total * pr)
            self.part_a, self.part_b = self._parts_at(shift)
            if pr >= 1:
                self.open = True
                self.anim_state = None
        elif self.anim_state == 'closing':
            shift = int(self.shift_total * (1 - pr))
            self.part_a, self.part_b = self._parts_at(shift)
            if pr >= 1:
                self.open = False
                self.part_a = self.part_b = None
                self.anim_state = None
                if self.lock_icon:
                    self.lock_visible = True

    def handle_click(self):
        if self.open:
            if ser:
                ser.write(self.close_message.encode())
            self.start_close()
        else:
            if not USE_PASSWORDS or not self.password:
                if ser:
                    ser.write(self.open_message.encode())
                if self.lock_icon:
                    self.lock_visible = False
                self.start_open()
            else:
                pwd = ask_password()
                if pwd == self.password:
                    if ser:
                        ser.write(self.open_message.encode())
                    if self.lock_icon:
                        self.lock_visible = False
                    self.start_open()
                elif pwd is not None:
                    show_password_error(self)



# ------------------------------------------------------------------

# пример координат; замените на реальные
horizontal_doors = [
    Door((474, 249, 62, 13), 'h', password="",
         open_message="F",
         close_message="F",),
    Door((474, 344, 63, 13), 'h', password="",
         open_message="A",
         close_message="A"),
    Door((475, 523, 62, 13), 'h', password="",
         open_message="C",
         close_message="C"),
    Door((805, 371, 61, 13), 'h', password="",
         open_message="D1",
         close_message="D0"),
    Door((823, 430, 61, 13), 'h', password="",
         open_message="E1",
         close_message="E0"),
    Door((839, 87, 60, 13), 'h', password="",
         open_message="F1",
         close_message="F0"),
    Door((128, 302, 62, 13), 'h', password="",
         open_message="G1",
         close_message="G0"),
    Door((254, 710, 62, 13), 'h', password="1111",
         open_message="H1",
         close_message="H0",
         closed_color=(255, 0, 0),
         lock_size=LOCK_ICON_SIZE),
]

vertical_doors = [
    Door((280, 385, 13, 64), 'v', password="",
         open_message="I1",
         close_message="I0"),
    Door((280, 140, 13, 64), 'v', password="",
         open_message="J1",
         close_message="J0"),
    Door((200, 581, 13, 61), 'v', password="",
         open_message="K1",
         close_message="K0"),
    Door((365, 412, 13, 59), 'v', password="",
         open_message="L1",
         close_message="L0"),
    Door((649, 412, 13, 59), 'v', password="",
         open_message="B",
         close_message="B"),
    Door((745, 500, 13, 56), 'v', password="",
         open_message="N1",
         close_message="N0"),
    Door((730, 263, 13, 54), 'v', password="",
         open_message="O1",
         close_message="O0"),
    Door((931, 151, 13, 54), 'v', password="",
         open_message="P1",
         close_message="P0"),
]

doors = horizontal_doors + vertical_doors

SERIAL_DOOR_MAP = {chr(ord('A') + i): door for i, door in enumerate(doors)}
for letter, door in SERIAL_DOOR_MAP.items():
    door.serial_key = letter

icons = []
term_positions = [(70, 484), (418, 382), (418, 497), (607, 382), (607, 497)]
for p in term_positions:
    icons.append(MapIcon(p, "img/terminal.png", TERMINAL_ICON_SIZE))
ruki_positions = [(838, 176)]
for p in ruki_positions:
    icons.append(MapIcon(p, "img/ruki.png", RUKI_ICON_SIZE))
server_positions = [(70, 412)]
for p in server_positions:
    icons.append(MapIcon(p, "img/server.png", SERVER_ICON_SIZE))
'''term2_positions = [(500, 100)]
for p in term2_positions:
    icons.append(MapIcon(p, "img/term2.png", TERMINAL_ICON_SIZE))'''

# дополнительные иконки
krio_positions = [
    (959, 472), (959, 568),
    (959, 520), (959, 616),
    (845, 617),  (879, 617),
    (811, 617),
]
for p in krio_positions:
    icons.append(MapIcon(p, "img/krio.png", KRIO_ICON_SIZE))
    rul_positions = [(507, 100)]
for p in rul_positions:
    icons.append(MapIcon(p, "img/rul.png", RUL_ICON_SIZE))
'''stolov_positions = [(100, 100)]
for p in stolov_positions:
    icons.append(MapIcon(p, "img/table1.png", STOLOV_ICON_SIZE))
com_positions = [(135, 100)]
for p in com_positions:
    icons.append(MapIcon(p, "img/table2.png", COM_ICON_SIZE))'''

# номера комнат на карте (относительные координаты)
room_labels = [
    (507, 439, "А-1"),
    (507, 160, "А-2"),
    (160, 188, "С-1"),
    (160, 412, "С-2"),
    (119, 620, "С-3"),
    (839, 245, "Х-13"),
    (868, 543, "Х-2"),
]

# строки легенды слева
legend_lines = [
    "",
    "   А-1 - Командный пункт",
    "",
    "   А-2 - Пункт управления",
    "   кораблём",
    "",
    "   Х-13 - Лаборатория",
    "",
    "   Х-2 - Криокрамеры",
    "",
    "   С-1 - Столовая",
    "",
    "   С-2 - Серверная",
    "",
    "   С-3 - Эвакуационная",
    "   капсула",
    "",
    "",
]

# ----------------------- Загрузка карты -----------------------------
def load_map(path):
    if os.path.isfile(path):
        return pygame.image.load(path).convert()
    return pygame.Surface(MAP_ORIGINAL_SIZE)

ship_map_raw = load_map(IMAGE_PATH)


def scaled_map_surface(map_raw):
    map_w = WIDTH - LEGEND_WIDTH
    map_h = HEIGHT
    iw, ih = map_raw.get_size()
    scale = min(map_w / iw, map_h / ih)
    return pygame.transform.smoothscale(map_raw, (int(iw * scale), int(ih * scale)))

ship_map = scaled_map_surface(ship_map_raw)


def layout_map():
    rect = ship_map.get_rect(topright=(WIDTH, 0))
    if rect.left < LEGEND_WIDTH:
        rect.left = LEGEND_WIDTH
    return rect
# --------------------------------------------------------------------

def draw_legend():
    global legend_icons_rect
    legend_rect = pygame.Rect(0, 0, LEGEND_WIDTH, HEIGHT)
    top_height = 20 + len(legend_lines) * LEGEND_LINE_SPACING + 10
    top_rect = pygame.Rect(0, 0, LEGEND_WIDTH, top_height)
    bottom_rect = pygame.Rect(0, top_height, LEGEND_WIDTH, HEIGHT - top_height)
    legend_icons_rect = bottom_rect
    draw_glow_rect(screen, top_rect, CYAN, 3, 0)
    draw_glow_rect(screen, bottom_rect, CYAN, 3, 0)
    for i, line in enumerate(legend_lines):
        txt = legend_font.render(line, True, CYAN)
        screen.blit(txt, (10, 20 + i * LEGEND_LINE_SPACING))
    prev_clip = screen.get_clip()
    screen.set_clip(bottom_rect.inflate(-6, -6))
    y = bottom_rect.top + 10 + icon_scroll
    text_x = bottom_rect.left + LEGEND_ICON_SIZE + 10
    max_width = bottom_rect.width - (text_x - bottom_rect.left) - 10
    for name, img in legend_icons:
        lines = wrap_text(name, legend_font, max_width)
        line_height = legend_font.get_linesize()
        total_h = line_height * len(lines)
        ty = y + (LEGEND_ICON_SIZE - total_h) // 2
        for line in lines:
            text = legend_font.render(line, True, CYAN)
            screen.blit(text, (text_x, ty))
            ty += line_height
        screen.blit(img, (bottom_rect.left + 10, y))
        y += LEGEND_ICON_SIZE + LEGEND_ICON_SPACING
    screen.set_clip(prev_clip)

    global scroll_track_rect, scroll_thumb_rect
    track_margin = 8
    scroll_track_rect = pygame.Rect(
        bottom_rect.right - track_margin - SCROLLBAR_WIDTH,
        bottom_rect.top + track_margin,
        SCROLLBAR_WIDTH,
        bottom_rect.height - 2 * track_margin,
        )
    content_h = len(legend_icons) * (LEGEND_ICON_SIZE + LEGEND_ICON_SPACING)
    view_h = bottom_rect.height - 20
    ratio = view_h / content_h if content_h else 1
    thumb_h = max(20, scroll_track_rect.height * ratio)
    scroll_fraction = -icon_scroll / max(1, content_h - view_h)
    thumb_y = scroll_track_rect.y + (scroll_track_rect.height - thumb_h) * scroll_fraction
    scroll_thumb_rect = pygame.Rect(scroll_track_rect.x, thumb_y, SCROLLBAR_WIDTH, thumb_h)
    pygame.draw.rect(screen, (60, 60, 60), scroll_track_rect, border_radius=6)
    pygame.draw.rect(screen, CYAN, scroll_thumb_rect, border_radius=6)


def draw_map_and_doors(exclude=None):
    screen.fill(BG_COLOR)
    draw_legend()
    map_rect = layout_map()
    screen.blit(ship_map, map_rect)
    for x, y, num in room_labels:
        sx = map_rect.left + x * map_rect.width / MAP_ORIGINAL_SIZE[0]
        sy = map_rect.top + y * map_rect.height / MAP_ORIGINAL_SIZE[1]
        lbl = font_number.render(num, True, CYAN)
        screen.blit(lbl, lbl.get_rect(center=(sx, sy)))
    for d in doors:
        d.update_rect(map_rect)
        d.update_animation()
        if d is not exclude:
            d.draw(screen)
        if d.lock_icon and d.lock_visible:
            d.lock_icon.draw(screen)
    for icon in icons:
        icon.update_pos(map_rect)
        icon.draw(screen)
    header_txt = header_font.render(HEADER_TEXT, True, CYAN)
    screen.blit(header_txt, header_txt.get_rect(midtop=(WIDTH // 2, 10)))
    if CUSTOM_LABEL_TEXT:
        custom_txt = custom_label_font.render(CUSTOM_LABEL_TEXT, True, CYAN)
        screen.blit(custom_txt, custom_txt.get_rect(topleft=CUSTOM_LABEL_POS))
    return map_rect

def poll_serial_commands():
    if not ser:
        return
    global serial_buffer
    try:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            serial_buffer += data
        while '\n' in serial_buffer:
            line, serial_buffer = serial_buffer.split('\n', 1)
            cmd = line.strip()
            if len(cmd) >= 2:
                door_id = cmd[0].upper()
                state = cmd[1]
                door = SERIAL_DOOR_MAP.get(door_id)
                if door:
                    if state == '1':
                        if not door.open:
                            door.start_open()
                    elif state == '0':
                        if door.open:
                            door.start_close()
    except Exception:
        pass

# ------------------------------ Main loop ---------------------------
def main():
    global icon_scroll, dragging_thumb
    while True:
        poll_serial_commands()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if scroll_thumb_rect.collidepoint(event.pos):
                    dragging_thumb = True
                else:
                    for d in doors:
                        if d.rect.collidepoint(event.pos):
                            d.handle_click()
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_thumb = False
            elif event.type == pygame.MOUSEMOTION and dragging_thumb:
                track_top = scroll_track_rect.y
                track_bottom = scroll_track_rect.bottom - scroll_thumb_rect.height
                new_y = min(max(scroll_thumb_rect.y + event.rel[1], track_top), track_bottom)
                scroll_thumb_rect.y = new_y
                content = len(legend_icons) * (LEGEND_ICON_SIZE + LEGEND_ICON_SPACING)
                view = legend_icons_rect.height - 20
                max_scroll = max(0, content - view)
                fraction = (scroll_thumb_rect.y - track_top) / max(1, track_bottom - track_top)
                icon_scroll = -max_scroll * fraction
            elif event.type == pygame.MOUSEWHEEL:
                if legend_icons_rect.collidepoint(pygame.mouse.get_pos()):
                    content = len(legend_icons) * (LEGEND_ICON_SIZE + LEGEND_ICON_SPACING)
                    visible = legend_icons_rect.height - 20
                    max_scroll = max(0, content - visible)
                    icon_scroll = max(-max_scroll, min(0, icon_scroll + event.y * LEGEND_SCROLL_SPEED))

        draw_map_and_doors()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()