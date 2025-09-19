import pygame, sys, os, serial, time, numpy as np, threading, PyQt5

pygame.init()

lock = threading.Lock()

ser = serial.Serial('COM3', 9600)
time.sleep(2)
commands = ['A', 'C', 'B', 'D']

IMAGE_PATH = "img/12345.png"
IMAGE_PATH_MENU3 = "img/9876.png"
FULLSCREEN = True
TITLE = "ТЕРМИНАЛ ДОСТУПА"

BG_COLOR = (10, 15, 26)
CYAN = (0, 255, 255)
ALERT_RED = (255, 60, 0)

T_OPENING = 4000
T_ERROR = 3000
T_WARNING = 4000

pygame.init()
flags = pygame.FULLSCREEN if FULLSCREEN else 0
screen = pygame.display.set_mode((0, 0), flags) if FULLSCREEN else pygame.display.set_mode((1280, 1024))
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

font_big = pygame.font.Font(None, 56)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

STATE_MENU2, STATE_MENU1, STATE_MENU3, STATE_OPENING, STATE_ERROR, STATE_WARNING = range(6)
state = STATE_MENU2

EVT_OPENING_DONE = pygame.USEREVENT + 1
EVT_ERROR_DONE = pygame.USEREVENT + 2
EVT_WARNING_DONE = pygame.USEREVENT + 3

door_coordinates = np.array([[919, 256], [919, 329], [919, 468], [680, 783], [266, 219], [294, 588],
                             [358, 403], [390, 744], [389, 442], [383, 855], [418, 856], [491, 782],
                             [494, 589], [513, 403]])

DOOR_WIDTH = 70
DOOR_HEIGHT = 10.9

DOOR_COLOR_CLOSED = (255, 165, 0)
DOOR_COLOR_OPENED = (0, 255, 0)

door_positions = [pygame.Rect(x, y, DOOR_WIDTH, DOOR_HEIGHT) for x, y in door_coordinates]

def draw_door_buttons():
    for door_rect in door_positions:
        pygame.draw.rect(screen, DOOR_COLOR_CLOSED, door_rect, 0)

def handle_door_animation(door_rect, door_index):
    opening_duration = 2000
    time_start = pygame.time.get_ticks()
    send_signal_to_arduino(door_index)

    door_left = pygame.Rect(door_rect.left, door_rect.top, door_rect.width // 2, door_rect.height)
    door_right = pygame.Rect(door_rect.right - door_rect.width // 2, door_rect.top, door_rect.width // 2, door_rect.height)

    while pygame.time.get_ticks() - time_start < opening_duration:
        elapsed_time = pygame.time.get_ticks() - time_start
        progress = elapsed_time / opening_duration

        left_shift = int(progress * (door_rect.width // 2))
        right_shift = int(progress * (door_rect.width // 2))

        door_left = pygame.Rect(door_rect.left - left_shift, door_rect.top, door_rect.width // 2, door_rect.height)
        door_right = pygame.Rect(door_rect.right + right_shift - door_rect.width // 2, door_rect.top, door_rect.width // 2, door_rect.height)

        pygame.draw.rect(screen, DOOR_COLOR_CLOSED, door_left, 0)
        pygame.draw.rect(screen, DOOR_COLOR_CLOSED, door_right, 0)

        pygame.display.flip()

    pygame.draw.rect(screen, DOOR_COLOR_OPENED, door_left, 0)
    pygame.draw.rect(screen, DOOR_COLOR_OPENED, door_right, 0)


def send_signal_to_arduino(door_index):
    signal = commands[door_index]
    ser.write(signal.encode())

def load_map(image_path):
    if os.path.isfile(image_path):
        try:
            img = pygame.image.load(image_path).convert()
            return img
        except Exception as e:
            print("Не удалось загрузить изображение карты:", e)
    return None

ship_map_raw = load_map(IMAGE_PATH)
ship_map_menu3_raw = load_map(IMAGE_PATH_MENU3)

def scaled_map_surface(map_raw):
    map_h = int(HEIGHT * 0.55)
    map_w = int(WIDTH * 0.8)
    if map_raw is None:
        surf = pygame.Surface((map_w, map_h))
        surf.fill((8, 12, 22))
        step = 28
        for x in range(0, map_w, step):
            pygame.draw.line(surf, (20, 60, 80), (x, 0), (x, map_h), 1)
        for y in range(0, map_h, step):
            pygame.draw.line(surf, (20, 60, 80), (0, y), (map_w, y), 1)
        pygame.draw.rect(surf, CYAN, surf.get_rect(), 3, border_radius=12)
        txt = font_small.render("КАРТА НЕ НАЙДЕНА: проверь IMAGE_PATH", True, CYAN)
        surf.blit(txt, (20, 20))
        return surf
    iw, ih = map_raw.get_size()
    scale = min(map_w / iw, map_h / ih)
    new_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
    return pygame.transform.smoothscale(map_raw, new_size)

ship_map = scaled_map_surface(ship_map_raw)
ship_map_menu3 = scaled_map_surface(ship_map_menu3_raw)

def draw_glow_rect(surf, rect, color, width=3, radius=10):
    pygame.draw.rect(surf, color, rect, width, border_radius=radius)

def draw_button(label, rect, hover=False):
    outline = CYAN
    draw_glow_rect(screen, rect, outline, 3, 10)
    if hover:
        pygame.draw.rect(screen, (0, 80, 80), rect.inflate(-6, -6), 0, border_radius=8)
    text = font_medium.render(label, True, CYAN)
    screen.blit(text, text.get_rect(center=rect.center))

def layout_menu2():
    btn_w, btn_h = int(WIDTH * 0.48), int(HEIGHT * 0.48)
    left_x = 20
    right_x = WIDTH - btn_w - 20
    y = HEIGHT // 2 - btn_h // 2
    btn1 = pygame.Rect(left_x, y, btn_w, btn_h)
    btn2 = pygame.Rect(right_x, y, btn_w, btn_h)
    return btn1, btn2

def layout_menu1():
    map_rect = ship_map.get_rect(midtop=(WIDTH // 2, int(HEIGHT * 0.06)))
    btn_w = int(WIDTH * 0.8)
    btn_h = 64
    area_top = map_rect.bottom + int(HEIGHT * 0.05)
    x = WIDTH // 2 - btn_w // 2
    btn1 = pygame.Rect(x, area_top, btn_w, btn_h)
    btn2 = pygame.Rect(x, area_top + btn_h + 24, btn_w, btn_h)
    return map_rect, (btn1, btn2)

def layout_menu3():
    map_rect = ship_map_menu3.get_rect(midtop=(WIDTH // 2, int(HEIGHT * 0.06)))
    btn_w = int(WIDTH * 0.8)
    btn_h = 64
    area_top = map_rect.bottom + int(HEIGHT * 0.05)
    x = WIDTH // 2 - btn_w // 2
    btn1 = pygame.Rect(x, area_top, btn_w, btn_h)
    return map_rect, (btn1,)

def draw_menu2(mouse_pos):
    screen.fill(BG_COLOR)
    btn1, btn2 = layout_menu2()
    draw_button("Открытие/закрытие дверей", btn1, btn1.collidepoint(mouse_pos))
    draw_button("Включение/выключение света", btn2, btn2.collidepoint(mouse_pos))

def draw_menu1(mouse_pos):
    screen.fill(BG_COLOR)
    map_rect, btns = layout_menu1()
    btn1, btn2 = btns
    screen.blit(ship_map, ship_map.get_rect(center=map_rect.center))
    pygame.draw.rect(screen, CYAN, map_rect, 5, border_radius=12)
    caption = font_small.render("Карта корабля", True, CYAN)
    screen.blit(caption, (map_rect.left, map_rect.top - 28))
    draw_door_buttons()
    draw_button("Открыть/закрыть все двери", btn1, btn1.collidepoint(mouse_pos))

def draw_menu3(mouse_pos):
    screen.fill(BG_COLOR)
    map_rect, (btn1,) = layout_menu3()
    screen.blit(ship_map_menu3, ship_map_menu3.get_rect(center=map_rect.center))
    pygame.draw.rect(screen, CYAN, map_rect, 5, border_radius=12)

    caption = font_small.render("Карта корабля", True, CYAN)
    screen.blit(caption, (map_rect.left, map_rect.top - 28))

    draw_button("Включить/выключить свет", btn1, btn1.collidepoint(mouse_pos))

def draw_opening():
    screen.fill(BG_COLOR)
    msg = font_big.render(">> ОТКРЫТИЕ ДВЕРИ…", True, CYAN)
    screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))

def draw_error():
    screen.fill(BG_COLOR)
    msg = font_big.render("!! ОШИБКА: МЕХАНИЗМ ЗАСТРЯЛ", True, ALERT_RED)
    screen.blit(msg, msg.get_rect(center=(WIDTH//2, HEIGHT//2)))

def draw_warning():
    screen.fill(BG_COLOR)
    if (pygame.time.get_ticks() // 125) % 2 == 0:
        w1 = font_big.render("ВНИМАНИЕ! ГЕНЕРАТОРЫ ПОВРЕЖДЕНЫ.", True, ALERT_RED)
        w2 = font_big.render("ПЕРЕХОД НА АВАРИЙНУЮ СИСТЕМУ ПИТАНИЯ!", True, ALERT_RED)
        screen.blit(w1, w1.get_rect(center=(WIDTH//2, HEIGHT//2 - 32)))
        screen.blit(w2, w2.get_rect(center=(WIDTH//2, HEIGHT//2 + 32)))

def goto_menu2():
    global state
    state = STATE_MENU2

def goto_menu1():
    global state
    state = STATE_MENU1

def goto_menu3():
    global state
    state = STATE_MENU3

def goto_opening():
    global state
    state = STATE_OPENING
    pygame.time.set_timer(EVT_OPENING_DONE, T_OPENING, True)

def goto_error():
    global state
    state = STATE_ERROR
    pygame.time.set_timer(EVT_ERROR_DONE, T_ERROR, True)

def goto_warning():
    global state
    state = STATE_WARNING
    pygame.time.set_timer(EVT_WARNING_DONE, T_WARNING, True)

def main():
    global ship_map
    ship_map = scaled_map_surface(ship_map_raw)
    goto_menu2()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN and state == STATE_MENU2:
                btn1, btn2 = layout_menu2()
                if btn1.collidepoint(event.pos):
                    goto_menu1()
                elif btn2.collidepoint(event.pos):
                    goto_menu3()
            elif event.type == pygame.MOUSEBUTTONDOWN and state == STATE_MENU1:
                map_rect, btns = layout_menu1()
                btn1, btn2 = btns
                for i, door_rect in enumerate(door_positions):
                    if door_rect.collidepoint(event.pos):
                        handle_door_animation(door_rect, i)
                if btn1.collidepoint(event.pos):
                    goto_opening()
                elif btn2.collidepoint(event.pos):
                    goto_menu3()
            elif event.type == pygame.MOUSEBUTTONDOWN and state == STATE_MENU3:
                btn1, = layout_menu3()
                if btn1.collidepoint(event.pos):
                    print("Включение/выключение света")
            elif event.type == EVT_OPENING_DONE and state == STATE_OPENING:
                goto_error()
            elif event.type == EVT_ERROR_DONE and state == STATE_ERROR:
                goto_warning()
            elif event.type == EVT_WARNING_DONE and state == STATE_WARNING:
                goto_menu1()
            elif event.type == pygame.FINGERDOWN and state == STATE_MENU2:
                btn1, btn2 = layout_menu2()
                if btn1.collidepoint(event.pos):
                    goto_menu1()
                elif btn2.collidepoint(event.pos):
                    goto_menu3  ()
            elif event.type == pygame.FINGERDOWN and state == STATE_MENU1:
                btn1, btn2 = layout_menu1()
                if btn1.collidepoint(event.pos):
                    goto_opening()
                elif btn2.collidepoint(event.pos):
                    goto_menu3()
            elif event.type == pygame.FINGERDOWN and state == STATE_MENU3:
                btn1, = layout_menu3()
                if btn1.collidepoint(event.pos):
                    print("Включение/выключение света")


        if state == STATE_MENU2:
            draw_menu2(mouse_pos)
        elif state == STATE_MENU1:
            draw_menu1(mouse_pos)
        elif state == STATE_MENU3:
            draw_menu3(mouse_pos)
        elif state == STATE_OPENING:
            draw_opening()
        elif state == STATE_ERROR:
            draw_error()
        elif state == STATE_WARNING:
            draw_warning()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
