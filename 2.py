import pygame, sys, os, serial, time
import numpy as np

ser = serial.Serial('COM3', 9600)
time.sleep(2)
commands = ['C','D', 'A', 'B']

IMAGE_PATH = "img/12345.png"
IMAGE_PATH_MENU3 = "img/12345.png"
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
screen = pygame.display.set_mode((0, 0), flags) if FULLSCREEN else pygame.display.set_mode((1280, 800))
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

door_coordinates = np.array([[144, 929], [166, 403], [254, 590], [273, 783], [266, 219], [294, 588],
                             [358, 403], [390, 744], [389, 442], [383, 855], [418, 856], [491, 782],
                             [494, 589], [513, 403]])

door_positions = [pygame.Rect(x - 45, y - 30, 90, 15) for x, y in door_coordinates]

DOOR_WIDTH = 90
DOOR_HEIGHT = 15

# Цвет дверей
DOOR_COLOR_CLOSED = (255, 165, 0)  # Оранжевый (закрытая дверь)
DOOR_COLOR_OPENED = (0, 255, 0)  # Зеленый (открытая дверь)

# Массив с координатами дверей, создадим прямоугольники для каждой двери
door_positions = [pygame.Rect(x - 45, y - 30, DOOR_WIDTH, DOOR_HEIGHT) for x, y in door_coordinates]

# Функция для рисования дверей
def draw_door_buttons():
    for door_rect in door_positions:
        pygame.draw.rect(screen, DOOR_COLOR_CLOSED, door_rect, 0)  # Рисуем закрытые двери оранжевыми

def handle_door_animation(door_rect, door_index):
    # Анимация открытия двери
    opening_duration = 2000  # Время для завершения анимации (в миллисекундах)
    time_start = pygame.time.get_ticks()

    # Изначально дверь состоит из двух частей
    door_left = pygame.Rect(door_rect.left, door_rect.top, door_rect.width // 2, door_rect.height)
    door_right = pygame.Rect(door_rect.right - door_rect.width // 2, door_rect.top, door_rect.width // 2, door_rect.height)

    # Пока не завершится анимация
    while pygame.time.get_ticks() - time_start < opening_duration:
        elapsed_time = pygame.time.get_ticks() - time_start
        progress = elapsed_time / opening_duration  # Нормализованный прогресс

        # Сдвигаем двери в стороны
        left_shift = int(progress * (door_rect.width // 2))  # Двигаем влево
        right_shift = int(progress * (door_rect.width // 2))  # Двигаем вправо

        # Новые прямоугольники для двух частей двери
        door_left = pygame.Rect(door_rect.left - left_shift, door_rect.top, door_rect.width // 2, door_rect.height)
        door_right = pygame.Rect(door_rect.right + right_shift - door_rect.width // 2, door_rect.top, door_rect.width // 2, door_rect.height)

        # Рисуем разделенные двери
        pygame.draw.rect(screen, DOOR_COLOR_CLOSED, door_left, 0)
        pygame.draw.rect(screen, DOOR_COLOR_CLOSED, door_right, 0)

        pygame.display.flip()  # Обновление экрана

    # После завершения анимации, двери открыты и они становятся зеленые
    pygame.draw.rect(screen, DOOR_COLOR_OPENED, door_left, 0)  # Показываем открытую левую часть
    pygame.draw.rect(screen, DOOR_COLOR_OPENED, door_right, 0)

    # Отправляем сигнал на Arduino только для соответствующей двери
    send_signal_to_arduino(door_index)

def send_signal_to_arduino(door_index):
    # Отправка сигнала на Arduino
    signal = commands[door_index]  # Получаем соответствующую команду для двери
    ser.write(signal.encode())  # Отправляем команду для этой двери

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
    map_h = int(HEIGHT * 0.55)  # Высота карты на экране
    map_w = int(WIDTH * 0.8)    # Ширина карты на экране
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

# Координаты дверей
door_coordinates = np.array([[144, 929], [166, 403], [254, 590], [273, 783], [266, 219], [294, 588],
                             [358, 403], [390, 744], [389, 442], [383, 855], [418, 856], [491, 782],
                             [494, 589], [513, 403]])

door_buttons_state = ['closed'] * len(door_coordinates)  # Изначально все двери закрыты

# Рисуем кнопки
def draw_buttons_on_map(door_coordinates, door_buttons_state):
    for i, coord in enumerate(door_coordinates):
        # Увеличиваем размер кнопок до 100x100
        button_rect = pygame.Rect(coord[1] - 50, coord[0] - 50, 100, 100)  # Увеличены размеры кнопок
        print(f"Рисую кнопку на координатах: {coord}")  # Отладочное сообщение
        # Проверим, попадает ли кнопка на экран
        if 0 <= button_rect.left <= WIDTH and 0 <= button_rect.top <= HEIGHT:
            print(f"Кнопка {i} рисуется на экране с координатами: {button_rect}")

        if door_buttons_state[i] == 'opening':
            pygame.draw.rect(screen, (0, 255, 255), button_rect)  # Кнопка в процессе открытия
        elif door_buttons_state[i] == 'opened':
            pygame.draw.rect(screen, (0, 255, 0), button_rect)  # Кнопка после открытия (зеленая)
            pygame.draw.line(screen, (0, 255, 0), button_rect.midleft, button_rect.midright, 3)
        else:
            pygame.draw.rect(screen, (255, 165, 0), button_rect)  # Оранжевая кнопка (для закрытой двери)

# Обработка кликов по дверям
def handle_door_clicks(mouse_pos, door_buttons_state):
    for i, coord in enumerate(door_coordinates):
        button_rect = pygame.Rect(coord[1] - 50, coord[0] - 50, 100, 100)
        if button_rect.collidepoint(mouse_pos):
            if door_buttons_state[i] == 'closed':
                door_buttons_state[i] = 'opening'
                return i  # Возвращаем индекс кнопки, которая была нажата
    return None

# Функции для работы с меню
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
    map_rect, (btn1, btn2) = layout_menu1()
    screen.blit(ship_map, ship_map.get_rect(center=map_rect.center))  # Отображаем карту внутри рамки
    pygame.draw.rect(screen, CYAN, map_rect, 5, border_radius=12)

    caption = font_small.render("Карта корабля", True, CYAN)
    screen.blit(caption, (map_rect.left, map_rect.top - 28))

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

def draw_button(label, rect, hover=False):
    outline = CYAN
    draw_glow_rect(screen, rect, outline, 3, 10)
    if hover:
        pygame.draw.rect(screen, (0, 80, 80), rect.inflate(-6, -6), 0, border_radius=8)
    text = font_medium.render(label, True, CYAN)
    screen.blit(text, text.get_rect(center=rect.center))

def draw_glow_rect(surf, rect, color, width=3, radius=10):
    pygame.draw.rect(surf, color, rect, width, border_radius=radius)

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
                    goto_menu3  ()
            elif event.type == pygame.MOUSEBUTTONDOWN and state == STATE_MENU1:
                btn1, btn2 = layout_menu1()
                if btn1.collidepoint(event.pos):
                    goto_opening()
                elif btn2.collidepoint(event.pos):
                    goto_menu3()
                for i, door_rect in enumerate(door_positions):
                    if door_rect.collidepoint(event.pos):  # Проверка нажатия на дверь
                        handle_door_animation(door_rect, i)
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_button = handle_door_clicks(mouse_pos, door_buttons_state)
                if clicked_button is not None:
                    pygame.time.set_timer(pygame.USEREVENT, 2000)  # Анимация длится 2 секунды

            elif event.type == pygame.USEREVENT:
                # После завершения анимации, меняем состояние кнопки на 'opened'
                for i in range(len(door_buttons_state)):
                    if door_buttons_state[i] == 'opening':
                        door_buttons_state[i] = 'opened'
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Сбрасываем таймер

        # Рисуем карту и кнопки
        screen.fill(BG_COLOR)
        screen.blit(ship_map, (0, 0))  # Отображаем карту
        draw_buttons_on_map(door_coordinates, door_buttons_state)  # Рисуем кнопки на карте

        # Рисуем меню в зависимости от состояния
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
