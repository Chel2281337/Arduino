import sys
import random
import pygame
import pygame.gfxdraw

# ---------------------------- Parameters ----------------------------
FULLSCREEN = True
TITLE = "КОМАНДНАЯ КОНСОЛЬ"
BG_COLOR = (10, 15, 26)
CYAN = (222, 255, 255)
CONSOLE_FONT_SIZE = 32
INPUT_FONT_SIZE = 60
SELF_DESTRUCT_DURATION = 15000  # ms
PROMPT = "> "


def init_screen():
    pygame.init()
    flags = pygame.FULLSCREEN if FULLSCREEN else 0
    screen = (
        pygame.display.set_mode((0, 0), flags)
        if FULLSCREEN
        else pygame.display.set_mode((1280, 1024))
    )
    pygame.display.set_caption(TITLE)
    return screen


screen = init_screen()
WIDTH, HEIGHT = screen.get_size()
clock = pygame.time.Clock()

font_console = pygame.font.Font(None, CONSOLE_FONT_SIZE)
font_input = pygame.font.Font(None, INPUT_FONT_SIZE)
font_title = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 24)
font_key = pygame.font.Font(None, 36)
pygame.key.set_repeat(350, 40)

# onscreen keyboard layout
# preload backspace arrow image
ARROW_IMG = pygame.image.load("img/arrow.png").convert_alpha()

# onscreen keyboard layout
KEY_LAYOUT = [
    "1234567890_",
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM",
]
KEY_W = KEY_H = 90
keyboard_width = len(KEY_LAYOUT[0]) * KEY_W
keyboard_start_x = WIDTH // 2 - keyboard_width // 2

# main input box, backspace and enter buttons aligned with keyboard
INPUT_H = KEY_H
input_rect = pygame.Rect(
    keyboard_start_x,
    HEIGHT // 2 - INPUT_H - 20,
    keyboard_width - 2 * KEY_W - 20,
    INPUT_H,
    )
back_rect = pygame.Rect(input_rect.right + 10, input_rect.top, KEY_W, INPUT_H)
enter_rect = pygame.Rect(back_rect.right + 10, input_rect.top, KEY_W, INPUT_H)
INPUT_PADDING = 20
MAX_INPUT_W = input_rect.width - 2 * INPUT_PADDING

# build key rects
key_rects = []
start_y = input_rect.bottom + 20
for row_i, row in enumerate(KEY_LAYOUT):
    start_x = WIDTH // 2 - (len(row) * KEY_W) // 2
    for col_i, ch in enumerate(row):
        r = pygame.Rect(
            start_x + col_i * KEY_W,
            start_y + row_i * KEY_H,
            KEY_W - 4,
            KEY_H - 4,
            )
        key_rects.append((r, ch))

# ------------------------- Command handling -------------------------
console_lines = []
current_input = ""


def add_console_line(text: str) -> None:
    console_lines.append(text)
    if len(console_lines) > 40:
        console_lines.pop(0)

# ---------------------- Modal helpers -------------------------------

class TextPrompt:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.text = ""
        self.done = False
        self.accepted = False
        self.key_rects = key_rects
        self.back_hold = False
        self.back_last = 0

    def _append(self, ch: str):
        if font_input.size(self.text + ch)[0] <= MAX_INPUT_W:
            self.text += ch

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
            elif event.key == pygame.K_RETURN:
                self.accepted = True
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode and event.unicode.isprintable():
                self._append(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if enter_rect.collidepoint(event.pos):
                self.accepted = True
                self.done = True
            elif back_rect.collidepoint(event.pos):
                self.text = self.text[:-1]
                self.back_hold = True
                self.back_last = pygame.time.get_ticks()
            else:
                for r, ch in self.key_rects:
                    if r.collidepoint(event.pos):
                        self._append(ch)
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.back_hold = False

    def draw(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        title = font_title.render(self.prompt, True, CYAN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, input_rect.y - 70)))
        pygame.draw.rect(screen, CYAN, input_rect, 2, border_radius=6)
        txt = font_input.render(self.text, True, CYAN)
        screen.blit(txt, (input_rect.x + INPUT_PADDING, input_rect.centery - txt.get_height() / 2))
        pygame.draw.rect(screen, CYAN, back_rect, 2, border_radius=6)
        arrow_surf = pygame.transform.smoothscale(
            ARROW_IMG, (int(back_rect.width * 0.8), int(back_rect.height * 0.8))
        )
        screen.blit(arrow_surf, arrow_surf.get_rect(center=back_rect.center))
        pygame.draw.rect(screen, CYAN, enter_rect, 2, border_radius=6)
        tri = [
            (enter_rect.left + enter_rect.width * 0.25, enter_rect.top + enter_rect.height * 0.2),
            (enter_rect.right - enter_rect.width * 0.25, enter_rect.centery),
            (enter_rect.left + enter_rect.width * 0.25, enter_rect.bottom - enter_rect.height * 0.2),
        ]
        pygame.gfxdraw.filled_polygon(screen, tri, CYAN)
        pygame.gfxdraw.aapolygon(screen, tri, CYAN)
        for r, ch in self.key_rects:
            pygame.draw.rect(screen, CYAN, r, 2, border_radius=4)
            t = font_key.render(ch, True, CYAN)
            screen.blit(t, t.get_rect(center=r.center))

    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                self.handle_event(event)
            if self.back_hold and pygame.time.get_ticks() - self.back_last > 60:
                if self.text:
                    self.text = self.text[:-1]
                self.back_last = pygame.time.get_ticks()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        return self.text if self.accepted else None

def run_self_destruct(duration_ms=SELF_DESTRUCT_DURATION):
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
                "VENT FUEL", "ARM REACTOR", "SEAL BULKHEADS",
                "PURGE COOLANT", "DISENGAGE LOCKS", "CHARGE COILS"]))
            if len(console) > 12:
                console.pop(0)
            last_dot = (last_dot % 3) + 1
        screen.blit(overlay, (0, 0))
        dots = "." * last_dot
        title = font_input.render(f"{msg_base}{dots}", True, CYAN)
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
            txt = font_console.render(line, True, CYAN)
            screen.blit(txt, (bar_x, log_y))
            log_y += CONSOLE_FONT_SIZE + 4
        pygame.display.flip()
        clock.tick(30)
        if progress >= 1.0:
            break

# ----------------------------- Main loop ----------------------------

def execute_command(cmd: str):
    add_console_line(PROMPT + cmd)
    cmd = cmd.strip().upper()
    if cmd == "INITIATE_PROTOCOL":
        proto = TextPrompt("Введите номер протокола").run()
        if proto == "1234":
            pwd = TextPrompt("Введите пароль").run()
            if pwd == "1111":
                run_self_destruct()
            else:
                add_console_line("ОТКАЗ: неверный пароль")
        else:
            add_console_line("Неизвестный протокол")
    elif cmd:
        add_console_line("Неизвестная команда")


def main():
    global current_input
    back_hold = False
    back_last = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_RETURN:
                    execute_command(current_input)
                    current_input = ""
                elif event.unicode and event.unicode.isprintable():
                    if font_input.size(current_input + event.unicode)[0] <= MAX_INPUT_W:
                        current_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if enter_rect.collidepoint(event.pos):
                    execute_command(current_input)
                    current_input = ""
                elif back_rect.collidepoint(event.pos):
                    current_input = current_input[:-1]
                    back_hold = True
                    back_last = pygame.time.get_ticks()
                else:
                    for r, ch in key_rects:
                        if r.collidepoint(event.pos):
                            if font_input.size(current_input + ch)[0] <= MAX_INPUT_W:
                                current_input += ch
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                back_hold = False

        if back_hold and pygame.time.get_ticks() - back_last > 60:
            if current_input:
                current_input = current_input[:-1]
            back_last = pygame.time.get_ticks()

        screen.fill(BG_COLOR)

        # console log
        y = 40
        for line in console_lines[-20:]:
            txt = font_small.render(line, True, CYAN)
            screen.blit(txt, (40, y))
            y += font_small.get_height() + 4

        # title and input
        title = font_title.render("ВВЕДИТЕ КОМАНДУ", True, CYAN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, input_rect.y - 70)))
        pygame.draw.rect(screen, CYAN, input_rect, 2, border_radius=6)
        txt = font_input.render(current_input, True, CYAN)
        screen.blit(txt, (input_rect.x + INPUT_PADDING, input_rect.centery - txt.get_height() / 2))
        pygame.draw.rect(screen, CYAN, back_rect, 2, border_radius=6)
        arrow_surf = pygame.transform.smoothscale(
            ARROW_IMG, (int(back_rect.width * 0.8), int(back_rect.height * 0.8))
        )
        screen.blit(arrow_surf, arrow_surf.get_rect(center=back_rect.center))
        pygame.draw.rect(screen, CYAN, enter_rect, 2, border_radius=6)
        tri = [
            (enter_rect.left + enter_rect.width * 0.25, enter_rect.top + enter_rect.height * 0.2),
            (enter_rect.right - enter_rect.width * 0.25, enter_rect.centery),
            (enter_rect.left + enter_rect.width * 0.25, enter_rect.bottom - enter_rect.height * 0.2),
        ]
        pygame.gfxdraw.filled_polygon(screen, tri, CYAN)
        pygame.gfxdraw.aapolygon(screen, tri, CYAN)

        # draw keyboard
        for r, ch in key_rects:
            pygame.draw.rect(screen, CYAN, r, 2, border_radius=4)
            t = font_key.render(ch, True, CYAN)
            screen.blit(t, t.get_rect(center=r.center))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()