import sys, os, pygame, serial, time

# ---------------------------- Параметры ----------------------------
IMAGE_PATH = "img/12345.png"
FULLSCREEN = True
TITLE = "ПАНЕЛЬ ОСВЕЩЕНИЯ"

BG_COLOR = (10, 15, 26)
CYAN = (222, 255, 255)
ALERT_RED = (255, 60, 0)
DOOR_MARKER_COLOR = (29, 84, 73)

ANIM_DURATION = 800
MAP_ORIGINAL_SIZE = (1024, 768)
LEGEND_WIDTH = 300
LEGEND_FONT_SIZE = 33
LEGEND_LINE_SPACING = LEGEND_FONT_SIZE + 4
MAP_SCALE = 1
MINI_MAP_SCALE = 2.2
MINI_MAP_MAX_RATIO = 0.8
MINI_MENU_DIM_PERCENT = 75
ROOM_TOGGLE_BUTTON_HEIGHT = 60
ROOM_TOGGLE_BUTTON_FONT_SIZE = 31

# заголовок сверху и его размер
HEADER_TEXT = "ПАНЕЛЬ УПРАВЛЕНИЯ"
HEADER_FONT_SIZE = 48

# дополнительная настраиваемая подпись
CUSTOM_LABEL_TEXT = ""
CUSTOM_LABEL_FONT_SIZE = 32
CUSTOM_LABEL_POS = (0, 0)

ERROR_DURATION = 4500
ERROR_BLINK_MS = 600
GENERATOR_ERROR_LINES = [
    "Ошибка! Генераторы повреждены.",
    "Невозможно включить свет в данной области.",
]

LIGHT_IMAGE_PATH = "img/light1.png"
LIGHT_ON_IMAGE_PATH = "img/light1_on.png"
LIGHT_ICON_SIZE = 48

TERMINAL_ICON_SIZE = 40
RUKI_ICON_SIZE = 40
SERVER_ICON_SIZE = 40
KRIO_ICON_SIZE = 40
STOLOV_ICON_SIZE = 40
RUL_ICON_SIZE = 40
COM_ICON_SIZE = 40
MINI_LEGEND_ICON_BASE = 50
MINI_LEGEND_SPACING = 10
MINI_LEGEND_TEXT_GAP = 10
MINI_LEGEND_ITEM_SCALE = 1.0
DEFAULT_MINI_LEGEND_SCALE = 1.3
ICON_NAMES = {
    "img/mini_icon_1": " - Стол",
    "img/mini_icon_2": "Иконка 2",
    "img/mini_icon_3": "Иконка 3",
    "img/mini_icon_4": "Иконка 4",
    "img/mini_icon_5": "Иконка 5",
    "img/mini_icon_6": "Иконка 6",
    "img/mini_icon_7": "Иконка 7",
    "img/terminal": " - Терминал",
    "img/rul": " - Управление кораблём",
    "img/server": " - Сервер",
}
# ------------------------------------------------------------------

pygame.init()
flags = pygame.FULLSCREEN if FULLSCREEN else 0
screen = pygame.display.set_mode((0, 0), flags) if FULLSCREEN else pygame.display.set_mode((1280, 1024))
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

WARN_IMG = pygame.image.load("img/warn.png").convert_alpha()

'''ser = serial.Serial('COM3', 9600)
time.sleep(2)'''

font_big = pygame.font.Font(None, 56)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
legend_font = pygame.font.Font(None, LEGEND_FONT_SIZE)
font_number = pygame.font.Font(None, 90)
header_font = pygame.font.Font(None, HEADER_FONT_SIZE)
custom_label_font = pygame.font.Font(None, CUSTOM_LABEL_FONT_SIZE)


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


class RoomLight:
    def __init__(
            self,
            rel_pos,
            label,
            mini_image,
            mini_icons=None,
            legend_scale=DEFAULT_MINI_LEGEND_SCALE,
            legend_width_scale=1.0,
            icon_path=LIGHT_IMAGE_PATH,
            room_icon_base=None,
            room_icon_size=(MINI_LEGEND_ICON_BASE, MINI_LEGEND_ICON_BASE),
            room_icon_rel=None,
            room_error=False,
            icon_size=LIGHT_ICON_SIZE,
    ):
        self.icon = MapIcon(rel_pos, icon_path, icon_size)
        self.label = label
        self.mini_img_raw = pygame.image.load(mini_image).convert()
        # список внутренних иконок: (rel_pos, base_path, size, text)
        self.mini_icons = mini_icons or []
        self.icon_states = [False] * len(self.mini_icons)
        self.legend_scale = legend_scale
        # дополнительный множитель ширины легенды для этой мини-карты
        self.legend_width_scale = legend_width_scale
        self.icon_rect = pygame.Rect(0, 0, 0, 0)
        self.label_surf = None
        self.label_rect = None
        self.room_icon_base = room_icon_base
        self.room_icon_size = room_icon_size
        self.room_icon_rel = room_icon_rel
        if room_icon_base:
            self.room_off_raw = pygame.image.load(f"{room_icon_base}_off.png").convert_alpha()
            self.room_on_raw = pygame.image.load(f"{room_icon_base}_on.png").convert_alpha()
        else:
            self.room_off_raw = self.room_on_raw = None
        self.room_state = False
        self.room_anim = None
        self.room_anim_start = 0
        self.room_error = room_error

    def update_pos(self, map_rect):
        self.icon.update_pos(map_rect)
        self.icon_rect = self.icon.img.get_rect(center=(int(self.icon.pos.x), int(self.icon.pos.y)))
        self.label_surf = font_number.render(self.label, True, CYAN)
        self.label_rect = self.label_surf.get_rect(midtop=(self.icon.pos.x, self.icon_rect.bottom + 5))

    def draw(self, surf):
        self.icon.draw(surf)
        surf.blit(self.label_surf, self.label_rect)

    def open_menu(self):
        iw, ih = self.mini_img_raw.get_size()
        scale = MINI_MAP_SCALE
        img_w = int(iw * scale)
        img_h = int(ih * scale)
        max_w = int(WIDTH * MINI_MAP_MAX_RATIO)
        max_h = int(HEIGHT * MINI_MAP_MAX_RATIO)
        if img_w > max_w or img_h > max_h:
            scale = min(max_w / iw, max_h / ih)
            img_w = int(iw * scale)
            img_h = int(ih * scale)
        map_img = pygame.transform.smoothscale(self.mini_img_raw, (img_w, img_h))
        rect = map_img.get_rect()

        # масштабирование легенды (одинаковый размер для всех мини-карт)
        legend_scale = self.legend_scale * MINI_LEGEND_ITEM_SCALE
        legend_w = int(LEGEND_WIDTH * self.legend_width_scale) + 100
        icon_size = int(MINI_LEGEND_ICON_BASE * legend_scale)
        btn_size = icon_size
        legend_font_scaled = pygame.font.Font(None, int(LEGEND_FONT_SIZE * legend_scale))
        room_btn_font = pygame.font.Font(None, int(ROOM_TOGGLE_BUTTON_FONT_SIZE * legend_scale))
        total_w = rect.width + legend_w + 20
        rect.left = WIDTH // 2 - total_w // 2 + legend_w + 20
        rect.top = HEIGHT // 2 - rect.height // 2
        legend_rect = pygame.Rect(rect.left - legend_w - 20, rect.top, legend_w, rect.height)

        # кнопка включения/выключения света в комнате
        room_btn_h = int(ROOM_TOGGLE_BUTTON_HEIGHT * legend_scale)
        room_btn_rect = pygame.Rect(legend_rect.left + 10, legend_rect.top + 10,
                                    legend_rect.width - 20, room_btn_h)

        # иконка состояния света в комнате
        room_icon_w = int(self.room_icon_size[0] * scale)
        room_icon_h = int(self.room_icon_size[1] * scale)
        if self.room_icon_rel:
            room_icon_pos = (
                rect.left + self.room_icon_rel[0] * scale - room_icon_w // 2,
                rect.top + self.room_icon_rel[1] * scale - room_icon_h // 2,
            )
        else:
            room_icon_pos = (
                rect.left + rect.width - room_icon_w - 10,
                rect.top + 10,
            )
        room_rect = pygame.Rect(room_icon_pos, (room_icon_w, room_icon_h))
        if self.room_off_raw:
            room_off = pygame.transform.smoothscale(self.room_off_raw, (room_icon_w, room_icon_h))
            room_on = pygame.transform.smoothscale(self.room_on_raw, (room_icon_w, room_icon_h))
        else:
            room_off = room_on = None

        # подготовка иконок: легенда, кнопки и мини-карта связаны между собой
        icon_entries = []
        y = room_btn_rect.bottom + 10
        text_gap = int(MINI_LEGEND_TEXT_GAP * legend_scale)

        def wrap_text(text, font, max_width):
            words = text.split()
            lines = []
            cur = ""
            for word in words:
                test = (cur + " " + word).strip()
                if not cur or font.size(test)[0] <= max_width:
                    cur = test
                else:
                    lines.append(cur)
                    cur = word
                if len(lines) == 1 and font.size(cur)[0] > max_width:
                    lines.append(cur)
                    cur = ""
                    break
            if cur:
                lines.append(cur)
            return [font.render(line, True, CYAN) for line in lines[:2]]

        for idx, (rel, base, size, text, animated, show, error) in enumerate(self.mini_icons):
            scaled_sz = int(size * scale)
            mini_pos = (
                rect.left + rel[0] * scale - scaled_sz // 2,
                rect.top + rel[1] * scale - scaled_sz // 2,
            )
            mini_rect = pygame.Rect(mini_pos, (scaled_sz, scaled_sz))

            if show:
                entry_y = y
                legend_pos = (legend_rect.left + 10, entry_y)
                button_rect = None
                text_x = legend_pos[0] + icon_size + text_gap
                if animated:
                    button_rect = pygame.Rect(legend_rect.right - btn_size - 10, entry_y, btn_size, btn_size)
                    max_text_w = button_rect.left - text_gap - text_x
                else:
                    max_text_w = legend_rect.right - 10 - text_x

                text_lines = wrap_text(text, legend_font_scaled, max_text_w)
                text_height = sum(t.get_height() for t in text_lines)
                entry_h = max(icon_size, text_height)
                legend_pos = (legend_pos[0], entry_y + (entry_h - icon_size) // 2)
                legend_rect_icon = pygame.Rect(legend_pos, (icon_size, icon_size))
                if button_rect:
                    button_rect.y = entry_y + (entry_h - btn_size) // 2
                text_pos_y = entry_y + (entry_h - text_height) // 2

                if animated:
                    off_raw = pygame.image.load(f"{base}_off.png").convert_alpha()
                    on_raw = pygame.image.load(f"{base}_on.png").convert_alpha()
                    legend_off = pygame.transform.smoothscale(off_raw, (icon_size, icon_size))
                    legend_on = pygame.transform.smoothscale(on_raw, (icon_size, icon_size))
                    mini_off = pygame.transform.smoothscale(off_raw, (scaled_sz, scaled_sz))
                    mini_on = pygame.transform.smoothscale(on_raw, (scaled_sz, scaled_sz))
                    icon_entries.append(
                        {
                            "legend_off": legend_off,
                            "legend_on": legend_on,
                            "text_lines": text_lines,
                            "text_height": text_height,
                            "text_pos_y": text_pos_y,
                            "legend_pos": legend_pos,
                            "legend_rect": legend_rect_icon,
                            "button_rect": button_rect,
                            "mini_off": mini_off,
                            "mini_on": mini_on,
                            "mini_pos": mini_pos,
                            "mini_rect": mini_rect,
                            "state": self.icon_states[idx],
                            "anim": None,
                            "anim_start": 0,
                            "animated": True,
                            "show": True,
                            "error": bool(error),
                        }
                    )
                else:
                    img_raw = pygame.image.load(f"{base}.png").convert_alpha()
                    legend_img = pygame.transform.smoothscale(img_raw, (icon_size, icon_size))
                    mini_img = pygame.transform.smoothscale(img_raw, (scaled_sz, scaled_sz))
                    icon_entries.append(
                        {
                            "legend_img": legend_img,
                            "text_lines": text_lines,
                            "text_height": text_height,
                            "text_pos_y": text_pos_y,
                            "legend_pos": legend_pos,
                            "mini_img": mini_img,
                            "mini_pos": mini_pos,
                            "animated": False,
                            "show": True,
                            "error": bool(error),
                        }
                    )
                y += entry_h + int(MINI_LEGEND_SPACING * legend_scale)
            else:
                if animated:
                    off_raw = pygame.image.load(f"{base}_off.png").convert_alpha()
                    on_raw = pygame.image.load(f"{base}_on.png").convert_alpha()
                    mini_off = pygame.transform.smoothscale(off_raw, (scaled_sz, scaled_sz))
                    mini_on = pygame.transform.smoothscale(on_raw, (scaled_sz, scaled_sz))
                    icon_entries.append(
                        {
                            "mini_off": mini_off,
                            "mini_on": mini_on,
                            "mini_pos": mini_pos,
                            "mini_rect": mini_rect,
                            "state": self.icon_states[idx],
                            "anim": None,
                            "anim_start": 0,
                            "animated": True,
                            "show": False,
                            "legend_rect": None,
                            "button_rect": None,
                            "error": bool(error),
                        }
                    )
                else:
                    img_raw = pygame.image.load(f"{base}.png").convert_alpha()
                    mini_img = pygame.transform.smoothscale(img_raw, (scaled_sz, scaled_sz))
                    icon_entries.append(
                        {
                            "mini_img": mini_img,
                            "mini_pos": mini_pos,
                            "animated": False,
                            "show": False,
                            "error": bool(error),
                        }
                    )

        light_off = pygame.transform.smoothscale(
            pygame.image.load(LIGHT_IMAGE_PATH).convert_alpha(), (btn_size - 4, btn_size - 4)
        )
        light_on = pygame.transform.smoothscale(
            pygame.image.load(LIGHT_ON_IMAGE_PATH).convert_alpha(), (btn_size - 4, btn_size - 4)
        )

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    handled = False
                    for i, entry in enumerate(icon_entries):
                        if entry.get("animated"):
                            br = entry.get("button_rect")
                            lr = entry.get("legend_rect")
                            if (
                                    (br and br.collidepoint(event.pos))
                                    or entry["mini_rect"].collidepoint(event.pos)
                                    or (lr and lr.collidepoint(event.pos))
                            ):
                                if entry.get("error"):
                                    show_error(GENERATOR_ERROR_LINES, draw_map_and_lights, lambda blink: None)
                                elif entry["anim"] is None:
                                    # toggle state immediately, then animate
                                    entry["state"] = not entry["state"]
                                    entry["anim"] = 'on' if entry["state"] else 'off'
                                    entry["anim_start"] = pygame.time.get_ticks()
                                    print(f"Icon {i}")
                                # mark as handled whether or not we started an animation
                                handled = True
                                break
                    if not handled and (room_btn_rect.collidepoint(event.pos) or (room_rect and room_rect.collidepoint(event.pos))):
                        if self.room_error:
                            show_error(GENERATOR_ERROR_LINES, draw_map_and_lights, lambda blink: None)
                        elif self.room_anim is None:
                            # switch state immediately, animation just shows transition
                            self.room_state = not self.room_state
                            self.room_anim = 'on' if self.room_state else 'off'
                            self.room_anim_start = pygame.time.get_ticks()
                        # ignore clicks while animation is active
                        handled = True
                    if not handled:
                        done = True
            draw_map_and_lights()
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, int(255 * MINI_MENU_DIM_PERCENT / 100)))
            screen.blit(overlay, (0, 0))

            pygame.draw.rect(screen, BG_COLOR, legend_rect)
            draw_glow_rect(screen, legend_rect, CYAN, 2, 0)
            btn_label = (
                "Выключить свет в комнате" if self.room_state else "Включить свет в комнате"
            )
            btn_surf = room_btn_font.render(btn_label, True, CYAN)
            pygame.draw.rect(screen, CYAN, room_btn_rect, 2, border_radius=6)
            screen.blit(btn_surf, btn_surf.get_rect(center=room_btn_rect.center))
            cur_time = pygame.time.get_ticks()
            mini_draw = []
            room_draw = None
            if room_off:
                if self.room_anim:
                    pr = min((cur_time - self.room_anim_start) / ANIM_DURATION, 1.0)
                    pr = pr * pr * (3 - 2 * pr)
                    alpha = int(pr * 255) if self.room_anim == 'on' else int((1 - pr) * 255)
                    temp = room_off.copy()
                    img = room_on.copy()
                    img.set_alpha(alpha)
                    temp.blit(img, (0, 0))
                    room_img = temp
                    if pr >= 1:
                        self.room_anim = None
                else:
                    room_img = room_on if self.room_state else room_off
                # draw room light icon before other mini icons so they appear above it
                room_draw = (room_img, room_icon_pos)
            for entry in icon_entries:
                if entry.get("animated"):
                    if entry["anim"]:
                        pr = min((cur_time - entry["anim_start"]) / ANIM_DURATION, 1.0)
                        pr = pr * pr * (3 - 2 * pr)
                        alpha = int(pr * 255) if entry["anim"] == 'on' else int((1 - pr) * 255)
                        if entry.get("show"):
                            temp_leg = entry["legend_off"].copy()
                            img_leg = entry["legend_on"].copy()
                            img_leg.set_alpha(alpha)
                            temp_leg.blit(img_leg, (0, 0))
                            legend_img = temp_leg
                            temp_btn = light_off.copy()
                            img_btn = light_on.copy()
                            img_btn.set_alpha(alpha)
                            temp_btn.blit(img_btn, (0, 0))
                            button_img = temp_btn
                        temp_mini = entry["mini_off"].copy()
                        img_mini = entry["mini_on"].copy()
                        img_mini.set_alpha(alpha)
                        temp_mini.blit(img_mini, (0, 0))
                        mini_img = temp_mini
                        if pr >= 1:
                            entry["anim"] = None
                    else:
                        if entry.get("show"):
                            legend_img = entry["legend_on"] if entry["state"] else entry["legend_off"]
                            button_img = light_on if entry["state"] else light_off
                        mini_img = entry["mini_on"] if entry["state"] else entry["mini_off"]

                    if entry.get("show"):
                        screen.blit(legend_img, entry["legend_pos"])
                        text_x = entry["legend_pos"][0] + icon_size + text_gap
                        ty = entry["text_pos_y"]
                        for ts in entry["text_lines"]:
                            screen.blit(ts, (text_x, ty))
                            ty += ts.get_height()
                        if entry.get("button_rect"):
                            pygame.draw.rect(screen, CYAN, entry["button_rect"], 2, border_radius=6)
                            screen.blit(button_img, button_img.get_rect(center=entry["button_rect"].center))
                    mini_draw.append((mini_img, entry["mini_pos"]))
                else:
                    if entry.get("show"):
                        screen.blit(entry["legend_img"], entry["legend_pos"])
                        text_x = entry["legend_pos"][0] + icon_size + text_gap
                        ty = entry["text_pos_y"]
                        for ts in entry["text_lines"]:
                            screen.blit(ts, (text_x, ty))
                            ty += ts.get_height()
                    mini_draw.append((entry["mini_img"], entry["mini_pos"]))

            screen.blit(map_img, rect)
            if room_off:
                # draw room light icon first so subsequent icons layer on top
                screen.blit(room_draw[0], room_draw[1])
            for img, pos in mini_draw:
                screen.blit(img, pos)
            pygame.draw.rect(screen, CYAN, rect, 3, border_radius=12)
            pygame.display.flip()
            clock.tick(60)

        self.icon_states = [entry.get("state", False) for entry in icon_entries]
        self.room_anim = None


def draw_glow_rect(surf, rect, color, width=3, radius=10):
    pygame.draw.rect(surf, color, rect, width, border_radius=radius)


# --------------------------- Лампочки -------------------------------
class Light:
    def __init__(self, rel_pos, on_message="", off_message="", size=LIGHT_ICON_SIZE,
                 off_image=LIGHT_IMAGE_PATH, on_image=LIGHT_ON_IMAGE_PATH, error=False):
        self.rel_pos = pygame.Vector2(rel_pos)
        self.on_message = on_message
        self.off_message = off_message
        self.size = size
        self.off_raw = pygame.image.load(off_image).convert_alpha()
        self.on_raw = pygame.image.load(on_image).convert_alpha()
        self.off_img = pygame.transform.smoothscale(self.off_raw, (size, size))
        self.on_img = pygame.transform.smoothscale(self.on_raw, (size, size))
        self.pos = self.rel_pos.copy()
        self.size_px = size
        self.on = False
        self.anim_state = None  # None, 'on', 'off'
        self.anim_start = 0
        self.temp_img = None
        self.error = error

    def update_pos(self, map_rect):
        sx = map_rect.width / MAP_ORIGINAL_SIZE[0]
        sy = map_rect.height / MAP_ORIGINAL_SIZE[1]
        self.pos.x = map_rect.left + self.rel_pos.x * sx
        self.pos.y = map_rect.top + self.rel_pos.y * sy
        self.size_px = int(self.size * (sx + sy) / 2)
        self.off_img = pygame.transform.smoothscale(self.off_raw, (self.size_px, self.size_px))
        self.on_img = pygame.transform.smoothscale(self.on_raw, (self.size_px, self.size_px))
        self.rect = self.on_img.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def draw(self, surf):
        img = self.temp_img if self.anim_state else (self.on_img if self.on else self.off_img)
        rect = img.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        surf.blit(img, rect)

    def start_on(self):
        if self.on or self.anim_state:
            return
        self.anim_state = 'on'
        self.anim_start = pygame.time.get_ticks()

    def start_off(self):
        if not self.on or self.anim_state:
            return
        self.anim_state = 'off'
        self.anim_start = pygame.time.get_ticks()

    def update_animation(self):
        if not self.anim_state:
            return
        pr = min((pygame.time.get_ticks() - self.anim_start) / ANIM_DURATION, 1.0)
        pr = pr * pr * (3 - 2 * pr)
        if self.anim_state == 'on':
            alpha = int(pr * 255)
            temp = self.off_img.copy()
            img = self.on_img.copy()
            img.set_alpha(alpha)
            temp.blit(img, (0, 0))
            self.temp_img = temp
            if pr >= 1:
                self.on = True
                self.anim_state = None
                self.temp_img = None
        else:
            alpha = int((1 - pr) * 255)
            temp = self.off_img.copy()
            img = self.on_img.copy()
            img.set_alpha(alpha)
            temp.blit(img, (0, 0))
            self.temp_img = temp
            if pr >= 1:
                self.on = False
                self.anim_state = None
                self.temp_img = None

    def handle_click(self):
        if self.error:
            show_light_error(self)
            return
        if self.on:
            '''ser.write(self.off_message.encode())'''
            self.start_off()
        else:
            '''ser.write(self.on_message.encode())'''
            self.start_on()
# ------------------------------------------------------------------


def show_error(message_lines, draw_scene, blink_draw):
    err_rect = pygame.Rect(WIDTH // 2 - 380, HEIGHT // 2 - 240, 760, 480)
    warn_img = pygame.transform.smoothscale(WARN_IMG, (180, 180))
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < ERROR_DURATION:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        draw_scene()
        blink = (pygame.time.get_ticks() // ERROR_BLINK_MS) % 2 == 0
        blink_draw(blink)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 60) if blink else (0, 0, 0, 60))
        screen.blit(overlay, (0, 0))
        bg = (60, 0, 0) if blink else BG_COLOR
        border_color = ALERT_RED if blink else CYAN
        pygame.draw.rect(screen, bg, err_rect)
        pygame.draw.rect(screen, border_color, err_rect, 3, border_radius=12)
        if blink:
            screen.blit(warn_img, warn_img.get_rect(center=(err_rect.centerx, err_rect.top + 110)))
        line_height = font_medium.get_height()
        start_y = err_rect.bottom - 80 - (len(message_lines) - 1) * line_height
        for i, line in enumerate(message_lines):
            msg = font_medium.render(line, True, ALERT_RED)
            screen.blit(msg, msg.get_rect(center=(err_rect.centerx, start_y + i * line_height)))
        pygame.display.flip()
        clock.tick(60)


def show_light_error(light):
    def draw_scene():
        draw_map_and_lights()

    def blink_draw(blink):
        if blink:
            base = light.on_img if light.on else light.off_img
            rect = base.get_rect(center=(int(light.pos.x), int(light.pos.y)))
            temp = base.copy()
            temp.fill(ALERT_RED, special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(temp, rect)

    show_error(GENERATOR_ERROR_LINES, draw_scene, blink_draw)



# статичные двери (без анимации и паролей)
class DoorMarker:
    def __init__(self, rel_rect, orientation):
        self.rel_rect = pygame.Rect(rel_rect)
        self.orientation = orientation
        self.rect = self.rel_rect.copy()

    def update_rect(self, map_rect):
        sx = map_rect.width / MAP_ORIGINAL_SIZE[0]
        sy = map_rect.height / MAP_ORIGINAL_SIZE[1]
        self.rect = pygame.Rect(
            map_rect.left + self.rel_rect.x * sx,
            map_rect.top + self.rel_rect.y * sy,
            self.rel_rect.width * (sx if self.orientation == 'h' else sy),
            self.rel_rect.height * (sy if self.orientation == 'h' else sx)
        )

    def draw(self, surf):
        pygame.draw.rect(surf, DOOR_MARKER_COLOR, self.rect)

horizontal_doors = [
    DoorMarker((474, 249, 62, 13), 'h'),
    DoorMarker((474, 344, 63, 13), 'h'),
    DoorMarker((475, 523, 62, 13), 'h'),
    DoorMarker((805, 371, 61, 13), 'h'),
    DoorMarker((823, 430, 61, 13), 'h'),
    DoorMarker((839, 87, 60, 13), 'h'),
    DoorMarker((128, 302, 62, 13), 'h'),
    DoorMarker((254, 710, 62, 13), 'h'),
]

vertical_doors = [
    DoorMarker((280, 385, 13, 64), 'v'),
    DoorMarker((280, 140, 13, 64), 'v'),
    DoorMarker((200, 581, 13, 61), 'v'),
    DoorMarker((365, 412, 13, 59), 'v'),
    DoorMarker((649, 412, 13, 59), 'v'),
    DoorMarker((745, 500, 13, 56), 'v'),
    DoorMarker((730, 263, 13, 54), 'v'),
    DoorMarker((931, 151, 13, 54), 'v'),
]

door_markers = horizontal_doors + vertical_doors

room_labels = [
    (507, 439, "А-1"),
    (507, 160, "А-2"),
    (160, 188, "С-1"),
    (160, 412, "С-2"),
    (119, 620, "С-3"),
    (839, 235, "Х-13"),
    (868, 543, "Х-2"),
]

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
]

mini_icon_sets_raw = [
    [
        ((220, 145), "img/mini_icon_1", 60, True, 1),
        ((95, 60), "img/terminal", 55, False, 1),
        ((360, 60), "img/terminal", 55, False, 0),
        ((95, 225), "img/terminal", 55, False, 0),
        ((360, 225), "img/terminal", 55, False, 0),
    ],
    [
        ((80, 80), "img/rul", 30, False, 1),
    ],
    [
        ((60, 40), "img/mini_icon_3", 30, True, 1),
        ((130, 70), "img/mini_icon_3", 30, True, 1),
        ((90, 110), "img/mini_icon_3", 30, True, 1),
    ],
    [
        ((75, 170), "img/server", 75, False, 1),
        ((75, 263), "img/terminal", 55, False, 1),
    ],
    [
        ((30, 40), "img/mini_icon_5", 30, True, 1),
        ((140, 90), "img/mini_icon_5", 30, True, 1),
        ((90, 60), "img/mini_icon_5", 30, True, 1),
    ],
    [
        ((80, 40), "img/mini_icon_6", 30, True, 1),
        ((150, 80), "img/mini_icon_6", 30, True, 1),
        ((60, 110), "img/mini_icon_6", 30, True, 1),
    ],
    [
        ((40, 40), "img/mini_icon_7", 30, True, 1),
        ((100, 70), "img/mini_icon_7", 30, True, 1),
        ((150, 100), "img/mini_icon_7", 30, True, 1),
    ],
]


GENERATOR_ERROR_BUTTONS = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

MINI_ROOM_ERRORS = [
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]


MINI_ROOM_ICON_POSITIONS = [
    (233, 141),
    None,
    None,
    (212, 168),
    None,
    None,
    None,
]


MINI_ROOM_ICON_SIZES = [
    (410, 225),
    (410, 225),
    (410, 225),
    (99, 269),
    (410, 225),
    (410, 225),
    (MINI_LEGEND_ICON_BASE, MINI_LEGEND_ICON_BASE),
]

mini_icon_sets = []
for room_idx, icon_list in enumerate(mini_icon_sets_raw):
    error_indices = set(GENERATOR_ERROR_BUTTONS[room_idx])
    processed = []
    for j, (pos, base, size, anim, show) in enumerate(icon_list):
        err = j in error_indices
        processed.append(
            (pos, base, size, ICON_NAMES.get(base, f"Иконка {j+1}"), anim, show, err)
        )
    mini_icon_sets.append(processed)

room_lights = []
for idx, (
        (x, y, label),
        icons,
        err,
        room_icon_pos,
        room_icon_size,
) in enumerate(
    zip(
        room_labels,
        mini_icon_sets,
        MINI_ROOM_ERRORS,
        MINI_ROOM_ICON_POSITIONS,
        MINI_ROOM_ICON_SIZES,
    ),
    start=1,
):
    mini = f"img/ship_mini_{idx}.png"
    room_lights.append(
        RoomLight(
            (x, y - 40),
            label,
            mini,
            mini_icons=icons,
            icon_path=LIGHT_IMAGE_PATH,
            room_icon_base=f"img/room_{idx}",
            room_icon_rel=room_icon_pos,
            room_icon_size=room_icon_size,
            room_error=err,
        )
    )


# ----------------------- Загрузка карты -----------------------------
def load_map(path):
    if os.path.isfile(path):
        return pygame.image.load(path).convert()
    return pygame.Surface(MAP_ORIGINAL_SIZE)

ship_map_raw = load_map(IMAGE_PATH)


def scaled_map_surface(map_raw):
    map_w = (WIDTH - LEGEND_WIDTH) * MAP_SCALE
    map_h = HEIGHT * MAP_SCALE
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
    legend_rect = pygame.Rect(0, 0, LEGEND_WIDTH, HEIGHT)
    pygame.draw.rect(screen, BG_COLOR, legend_rect)
    draw_glow_rect(screen, legend_rect, CYAN, 3, 0)
    for i, line in enumerate(legend_lines):
        txt = legend_font.render(line, True, CYAN)
        screen.blit(txt, (10, 20 + i * LEGEND_LINE_SPACING))


def draw_map_and_lights():
    screen.fill(BG_COLOR)
    draw_legend()
    map_rect = layout_map()
    screen.blit(ship_map, map_rect)
    for d in door_markers:
        d.update_rect(map_rect)
        d.draw(screen)
    for rl in room_lights:
        rl.update_pos(map_rect)
        rl.draw(screen)

# ------------------------------ Main loop ---------------------------
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rl in room_lights:
                    if rl.icon_rect.collidepoint(event.pos) or rl.label_rect.collidepoint(event.pos):
                        rl.open_menu()

        draw_map_and_lights()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()