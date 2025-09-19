import sys, os, random, pygame, textwrap, math, pygame.gfxdraw

# ---------------------------- Параметры ----------------------------
FULLSCREEN = True
TITLE = "ИНФОРМАЦИОННАЯ ПАНЕЛЬ"

BG_COLOR = (10, 15, 26)
CYAN = (222, 255, 255)
BLACK = (0, 0, 0)

# информация о корабле
SHIP_DATA = {
    "photo": "img/ship.png",  # заменить на реальное изображение корабля
    "tech": [
        "Длина: 134 м",
        "Ширина: 90 м",
        "Высота: 60 м",
        "Масса: 350,000 тонн",
        "Двигатель: Двигатели гиперпространственного типа",
    ],
    "description": [
        "Бортовая система: AI \"Мать\" (Mother)",
        "Система жизнеобеспечения: автоматизирована",
        "Основное назначение: транспортировка грузов",
        "История: корабль Ностромо участвовал в трагических событиях",
    ],
}

# список сотрудников с индивидуальными данными
CREW_DATA = [
    {
        "photo": "img/crew1.png",
        "name": "Элен Луиза Рипли",
        "code": "180924609",
        "desc": (
            "Описание:\n"
            "Элен — профессионал с многолетним опытом в управлении сложными проектами и командами в экстремальных"
            " условиях. Она проявила выдающиеся лидерские качества, обеспечивая безопасность команды и поддерживая"
            " порядок в критических ситуациях. Рипли обладает обширными знаниями в сфере управления и принятия"
            " решений в кризисных ситуациях, что делает её ценным специалистом в самых нестандартных ситуациях.\n\n"
            "Достижения:\n"
            "Руководила крупными проектами в условиях экстремальных рисков.\n"
            "Обладает обширным опытом в управлении персоналом и выполнении задач в кризисных ситуациях.\n"
            "Получила несколько наград за принятие быстрых и правильных решений в экстренных обстоятельствах.\n\n"
            "Роль: Командир, ответственный за координацию работы команды и безопасность.\n"
            "Откуда: Земля\n"
            "Срок службы: 3 года\n"
            "Почему выбрали: Рипли была выбрана за её способность сохранять хладнокровие в любых ситуациях и обеспечивать"
            " безопасность экипажа в условиях, требующих немедленного реагирования."
        ),
    },
    {
        "photo": "img/crew2.png",
        "name": "Джон Ричард Даллас",
        "code": "180924610",
        "desc": (
            "Описание:\n"
            "Опытный капитан с более чем 12-летним опытом в командовании и принятии стратегических решений. Даллас"
            " успешно разрабатывал стратегии для выполнения сложных миссий и эффективно управлял командой в нестабильных"
            " условиях. Его лидерские качества и способность сохранять спокойствие при высоких рисках помогли бы"
            " организовать стабильную работу команды в любых ситуациях.\n\n"
            "Достижения:\n"
            "12 лет успешной службы в различных командных и лидерских ролях.\n"
            "Разработал стратегии для успешного завершения нескольких сложных миссий, включая межпланетные транспортировки.\n"
            "Отличается выдающимися навыками по организации работы под давлением.\n\n"
            "Роль: Капитан, координатор всех операций и стратегий.\n"
            "Откуда: Земля\n"
            "Срок службы: 12 лет\n"
            "Почему выбрали: Даллас был выбран на должность капитана благодаря своему опыту управления людьми и организации"
            " безопасных и эффективных операций в условиях неопределенности."
        ),
    },
    {
        "photo": "img/crew3.png",
        "name": "Кэрол Ламберт",
        "code": "180924611",
        "desc": (
            "Описание:\n"
            "Ламберт — специалист по внешней связи и навигации, чьи аналитические навыки и способность быстро реагировать"
            " на изменения обстановки были признаны ценными для выполнения высокоскоростных и рискованных задач. Она"
            " демонстрирует уверенность в принятии решений, работая с критически важными коммуникационными и навигационными"
            " системами, всегда учитывая изменения внешних факторов.\n\n"
            "Достижения:\n"
            "Опыт работы в условиях высоконапряжённых ситуаций, где точность и быстрая реакция критичны.\n"
            "Отличная работа по организации внешней связи и логистики на длительных миссиях.\n"
            "Сертифицированный специалист по навигационным системам и экстренным коммуникациям.\n\n"
            "Роль: Офицер связи, координатор навигации и внешних коммуникаций.\n"
            "Откуда: Земля\n"
            "Срок службы: 4 года\n"
            "Почему выбрали: Ламберт была выбрана за её способность быстро реагировать на нестандартные ситуации и её опыт"
            " работы в сфере связи и навигации, что было критично для миссии."
        ),
    },
    {
        "photo": "img/crew4.png",
        "name": "Кейн Александр",
        "code": "180924612",
        "desc": (
            "Описание:\n"
            "Эксперт по экзобиологии, Кейн обладает уникальными знаниями в области биологических исследований и исследований"
            " экосистем. Он работал в самых сложных и экстремальных условиях, проводя эксперименты и анализируя новые формы"
            " жизни, что позволяет ему быстро принимать решения в условиях неопределенности и риска.\n\n"
            "Достижения:\n"
            "Международно признанный эксперт в области экзобиологии.\n"
            "Осуществил несколько успешных исследований в экстремальных условиях, связанных с новой формой жизни.\n"
            "Автор научных работ, опубликованных в престижных биологических изданиях.\n\n"
            "Роль: Эксперт по экзобиологии, проводит исследования и анализирует биологические системы.\n"
            "Откуда: Земля\n"
            "Срок службы: 5 лет\n"
            "Почему выбрали: Кейн был принят на корабль благодаря своему глубокому знанию экзобиологии и навыкам работы"
            " в полевых условиях для проведения исследований в условиях межпланетных миссий."
        ),
    },
    {
        "photo": "img/crew5.png",
        "name": "Вильям Томас Скеттс",
        "code": "180924613",
        "desc": (
            "Описание:\n"
            "Скеттс — высококвалифицированный инженер с многолетним опытом в обслуживании и поддержании технически сложных"
            " систем. Он проделал значительную работу по модернизации и оптимизации оборудования для межпланетных миссий,"
            " а также принимал участие в создании инновационных технических решений для долговечности оборудования.\n\n"
            "Достижения:\n"
            "Многолетний опыт работы инженером, включая обслуживание сложного оборудования в экстремальных условиях.\n"
            "Проводил технические исследования по модернизации систем обеспечения кораблей дальнего космоса.\n"
            "Ответственен за успешную модернизацию нескольких космических платформ и повышение их долговечности.\n\n"
            "Роль: Инженер, специалист по техническому обслуживанию оборудования.\n"
            "Откуда: Земля\n"
            "Срок службы: 6 лет\n"
            "Почему выбрали: Скеттс был выбран за его выдающиеся инженерные навыки и опыт в обслуживании высокотехнологичных"
            " систем, что требовалось для обеспечения надежной работы корабля."
        ),
    },
    {
        "photo": "img/crew6.png",
        "name": "Роберт Ретчед",
        "code": "180924614",
        "desc": (
            "Описание:\n"
            "Ретчед — слесарь с большим опытом в техническом обслуживании и ремонте оборудования. Его навыки в решении"
            " нестандартных задач и быстрая реакция в сложных ситуациях стали неоценимыми для поддержания работоспособности"
            " всех систем корабля.\n\n"
            "Достижения:\n"
            "Опыт в техническом обслуживании на множестве миссий с непредсказуемыми условиями.\n"
            "Специализируется на ремонте оборудования и систем, работы с большими нагрузками и ремонтном сложных механизмов.\n"
            "Обладает навыками быстрого выявления и устранения неисправностей в экстренных ситуациях.\n\n"
            "Роль: Слесарь, специалист по техническому обслуживанию и ремонту.\n"
            "Откуда: Земля\n"
            "Срок службы: 4 года\n"
            "Почему выбрали: Ретчед был принят на корабль за его технические навыки и способность быстро устранять поломки"
            " в любых условиях, что обеспечивало бесперебойную работу оборудования."
        ),
    },
    {
        "photo": "img/crew7.png",
        "name": "Джонси",
        "code": "N/A",
        "desc": (
            "Описание:\n"
            "Джонси — кот с выдающейся интуицией и умением адаптироваться к самым разным условиям. Его способность"
            " поддерживать моральный дух команды и сохранять спокойствие в стрессовых ситуациях оказалась исключительно"
            " важной для общего психологического состояния экипажа.\n\n"
            "Достижения:\n"
            "Обладает необычайной выносливостью и интуицией, что позволило ему выжить в самых сложных условиях.\n"
            "Джонси стал неотъемлемой частью команды, поддерживая моральный дух и снижая уровень стресса у экипажа.\n\n"
            "Роль: Питомец, который активно участвует в поддержке морального духа команды.\n"
            "Откуда: Земля\n"
            "Срок службы: 3 года (вместе с Рипли)\n"
            "Почему выбрали: Джонси был выбран за его способность приносить уют и спокойствие в сложных ситуациях, что"
            " играет важную роль в поддержке морального духа команды."
        ),
    },
]

# параметры корабля
SHIP_ITEM_WIDTH = 1840
SHIP_ITEM_HEIGHT = 230
SHIP_IMG_WIDTH = 160
SHIP_IMG_HEIGHT = 100
SHIP_IMAGE_MARGIN = 10

# размеры карточки сотрудника (горизонтальный список)
CREW_CARD_WIDTH = 500
CREW_CARD_HEIGHT = 380
CREW_IMAGE_SIZE = 230
PHOTO_CORNER_RADIUS = 12
CREW_CARD_SPACING = 20
CREW_FRAME_MARGIN = 20

# параметры горизонтального скроллбара
CREW_SCROLLBAR_HEIGHT = 18
CREW_SCROLL_THUMB_WIDTH = 60

# высота нижней панели состояния корабля
STATUS_PANEL_HEIGHT = 300  # нижняя панель статусов

# Состав газов (изменяемые проценты для анимации)
GAS_COMPOSITION = [
    ["Азот", 78.09, (135, 206, 235)],
    ["Кислород", 20.95, (0, 191, 255)],
    ["Аргон", 0.93, (255, 215, 0)],
    ["Углекислый газ", 0.03, (205, 133, 63)],
]

# таймер изменения концентраций азота и CO₂
gas_toggle = False
gas_next_switch = 0

# вертикальные отступы
HEADER_TOP = 40
HEADER_SHIP_SPACING = 20
CREW_TOP_MARGIN = 20
# ------------------------------------------------------------------

pygame.init()
flags = pygame.FULLSCREEN if FULLSCREEN else 0
screen = pygame.display.set_mode((0, 0), flags) if FULLSCREEN else pygame.display.set_mode((1280, 1024))
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

gas_next_switch = pygame.time.get_ticks() + random.randint(2000, 5000)

font_title = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
font_console = pygame.font.SysFont('courier', 30)
font_diagramm1 = pygame.font.Font(None, 36)
font_diagramm2 = pygame.font.Font(None, 33)
font_diagramm3 = pygame.font.Font(None, 28)


def load_image(path, size):
    if os.path.isfile(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, size)
    surf = pygame.Surface(size)
    surf.fill((30, 30, 30))
    pygame.draw.rect(surf, CYAN, surf.get_rect(), 2)
    return surf


def load_round_image(path, size, radius=12):
    """Загружает изображение нужного размера и закругляет углы."""
    img = load_image(path, size).convert_alpha()
    mask = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255), mask.get_rect(), border_radius=radius)
    img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pygame.draw.rect(img, CYAN, img.get_rect(), 2, border_radius=radius)
    return img


def draw_pie(surface, center, radius, start_angle, end_angle, color):
    """Draws a filled pie slice using basic polygons."""
    cx, cy = center
    # Begin with center and the starting edge so we always have at least
    # three points for the polygon, even for tiny slices.
    points = [(cx, cy)]
    rad = math.radians(start_angle)
    points.append((cx + radius * math.cos(rad), cy + radius * math.sin(rad)))

    step = 4 if end_angle >= start_angle else -4
    for ang in range(int(start_angle + step), int(end_angle), step):
        rad = math.radians(ang)
        points.append((cx + radius * math.cos(rad), cy + radius * math.sin(rad)))

    rad = math.radians(end_angle)
    points.append((cx + radius * math.cos(rad), cy + radius * math.sin(rad)))
    pygame.draw.polygon(surface, color, points)


def update_gases():
    """Периодически меняет проценты азота и CO₂."""
    global gas_toggle, gas_next_switch, GAS_COMPOSITION
    now = pygame.time.get_ticks()
    if now >= gas_next_switch:
        gas_toggle = not gas_toggle
        if gas_toggle:
            GAS_COMPOSITION[0][1] = 78.09
            GAS_COMPOSITION[3][1] = 0.03
        else:
            GAS_COMPOSITION[0][1] = 78.10
            GAS_COMPOSITION[3][1] = 0.02
        gas_next_switch = now + random.randint(2000, 5000)


def draw_gas_chart(surface, rect):
    """Рисует круговую диаграмму газов с подписями справа."""
    # оставляем место справа под подписи
    max_radius = min(rect.height - 60, rect.width - 120) // 2
    center = (rect.left + max_radius + 20, rect.top + rect.height // 2 - 15)

    start_angle = -90
    for name, pct, color in GAS_COMPOSITION:
        end_angle = start_angle + pct / 100 * 360
        draw_pie(surface, center, max_radius, start_angle, end_angle, color)
        start_angle = end_angle

    # подписи справа от диаграммы
    text_x = center[0] + max_radius + 33
    text_y = rect.top + 45
    for name, pct, color in GAS_COMPOSITION:
        pygame.draw.rect(surface, color, (text_x, text_y, 18, 18))
        label = font_diagramm1.render(f"{name} {pct:.2f}%", True, CYAN)
        surface.blit(label, (text_x + 28, text_y - 2))
        text_y += label.get_height() + 8

    caption = font_diagramm2.render(
        "Процент содержания газов в атмосфере корабля", True, CYAN
    )
    surface.blit(
        caption,
        (rect.left + (rect.width - caption.get_width()) / 2, center[1] + max_radius + 11),
    )

    pygame.gfxdraw.aacircle(surface, center[0], center[1], max_radius, CYAN)


def draw_text_block(surface, text, font, color, rect, line_spacing=5, width=60):
    """Рисует многострочный текст в пределах rect."""
    x, y = rect.topleft
    for paragraph in text.split("\n"):
        if not paragraph:
            y += font.get_height()
            continue
        for line in textwrap.wrap(paragraph, width=width):
            img = font.render(line, True, color)
            surface.blit(img, (x, y))
            y += img.get_height() + line_spacing


header_surface = font_title.render(TITLE, True, CYAN)

# подготовка изображений корабля
SHIP_DATA["img_small"] = load_round_image(
    SHIP_DATA["photo"], (SHIP_IMG_WIDTH, SHIP_IMG_HEIGHT), PHOTO_CORNER_RADIUS
)
SHIP_DATA["img_big"] = load_round_image(SHIP_DATA["photo"], (300, 200), PHOTO_CORNER_RADIUS)

ship_item_width = min(SHIP_ITEM_WIDTH, WIDTH - 80)
ship_item_rect = pygame.Rect(
    40,
    HEADER_TOP + header_surface.get_height() + HEADER_SHIP_SPACING,
    ship_item_width,
    SHIP_ITEM_HEIGHT,
    )
ship_img_rect = SHIP_DATA["img_small"].get_rect(
    topleft=(ship_item_rect.left + SHIP_IMAGE_MARGIN, ship_item_rect.top + SHIP_IMAGE_MARGIN)
)

# предварительно загрузим фото сотрудников
for m in CREW_DATA:
    m["img_small"] = load_round_image(
        m["photo"], (CREW_IMAGE_SIZE, CREW_IMAGE_SIZE), PHOTO_CORNER_RADIUS
    )
    m["img_big"] = load_round_image(m["photo"], (200, 200), PHOTO_CORNER_RADIUS)

crew_offset = 0
crew_start_y = ship_item_rect.bottom + CREW_TOP_MARGIN

view_width = WIDTH - 80
total_width = len(CREW_DATA) * (CREW_CARD_WIDTH + CREW_CARD_SPACING) - CREW_CARD_SPACING
max_scroll = min(0, view_width - total_width)


def draw_ship_info():
    pygame.draw.rect(screen, CYAN, ship_item_rect, 2, border_radius=12)
    screen.blit(SHIP_DATA["img_small"], ship_img_rect)
    tech_x = ship_img_rect.right + 20
    remaining = ship_item_rect.right - tech_x - 20
    col_w = remaining // 2

    title = font_medium.render("Технические характеристики:", True, CYAN)
    screen.blit(title, (tech_x, ship_img_rect.top))
    y = ship_img_rect.top + title.get_height() + 5
    for line in SHIP_DATA["tech"]:
        surf = font_small.render(line, True, CYAN)
        screen.blit(surf, (tech_x, y))
        y += surf.get_height() + 4

    desc_x = tech_x + col_w + 20
    title = font_medium.render("Описание:", True, CYAN)
    screen.blit(title, (desc_x, ship_img_rect.top))
    y = ship_img_rect.top + title.get_height() + 5
    for line in SHIP_DATA["description"]:
        surf = font_small.render(line, True, CYAN)
        screen.blit(surf, (desc_x, y))
        y += surf.get_height() + 4


def draw_crew_list():
    crew_rect = pygame.Rect(40, crew_start_y - 10, view_width, CREW_CARD_HEIGHT + 2 * CREW_FRAME_MARGIN + 16)
    pygame.draw.rect(screen, CYAN, crew_rect, 2, border_radius=12)
    inner_clip = crew_rect.inflate(-2 * CREW_FRAME_MARGIN, -2 * CREW_FRAME_MARGIN)
    screen.set_clip(inner_clip)
    thumb_rect = None
    for i, m in enumerate(CREW_DATA):
        x = 40 + CREW_FRAME_MARGIN + i * (CREW_CARD_WIDTH + CREW_CARD_SPACING) + crew_offset
        if x + CREW_CARD_WIDTH < inner_clip.left or x > inner_clip.right:
            continue
        item_rect = pygame.Rect(
            x, crew_start_y + CREW_FRAME_MARGIN, CREW_CARD_WIDTH, CREW_CARD_HEIGHT
        )
        pygame.draw.rect(screen, CYAN, item_rect, 2, border_radius=12)
        img_rect = m["img_small"].get_rect()
        img_rect.topleft = (item_rect.left + 10, item_rect.top + 10)
        screen.blit(m["img_small"], img_rect)
        name = font_small.render(m["name"], True, CYAN)
        code = font_small.render(f"Код сотрудника: {m['code']}", True, CYAN)
        screen.blit(name, (img_rect.right + 10, img_rect.top))
        screen.blit(code, (item_rect.left + 10, img_rect.bottom + 10))
        m["rect"] = item_rect

    screen.set_clip(None)

    scrollbar_rect = pygame.Rect(
        42,
        crew_start_y - 29 + CREW_FRAME_MARGIN * 2 + CREW_CARD_HEIGHT + 17,
        view_width - 4,
        CREW_SCROLLBAR_HEIGHT,
        )
    pygame.draw.rect(screen, CYAN, scrollbar_rect, 2, border_radius=6)
    if total_width > view_width:
        thumb_w = max(20, scrollbar_rect.width * view_width / total_width)
        ratio = -crew_offset / (total_width - view_width)
        thumb_x = scrollbar_rect.left + ratio * (scrollbar_rect.width - thumb_w)
        thumb_rect = pygame.Rect(
            int(thumb_x), scrollbar_rect.top, int(thumb_w), CREW_SCROLLBAR_HEIGHT
        )
        pygame.draw.rect(screen, CYAN, thumb_rect, 0, border_radius=6)
    return thumb_rect, scrollbar_rect


class ShipStatus:
    def __init__(self):
        self.t = 0
        self.log_lines = []
        self.last_cmd = 0
        self.start_time = pygame.time.get_ticks()

    def _update_commands(self, max_lines):
        now = pygame.time.get_ticks()
        if now - self.last_cmd > 1000:
            pool = [
                "SYSTEM_CHECK --ALL",
                "CREW_STATUS --ACTIVE",
                "MONITOR_HULL --INTEGRITY",
                "ENV_CHECK --STATUS",
                "ENERGY_CORE --READING",
                "LIFE_SUPPORT --MONITOR",
                "SCANNER --SCAN",
                "DATA_TRANSFER --SECURE",
                "ALERT_SYS --STATUS",
                "COMM_STATUS --CHECK",
                "CREW_ASSIGN --CURRENT",
                "SHIP_LOC --COORDS",
                "MAINT_CHECK --MODULE",
                "HEALTH_CHECK --CREW",
                "AIR_QUALITY --MEASURE",
                "OXYGEN_LEVEL --STATUS",
                "GRAVITY_CHECK --STATUS",
                "SHIP_SPEED --MONITOR",
                ""
            ]
            ts = ((now - self.start_time) / 1000) % 1000
            self.log_lines.append(f"{ts:.2f} {random.choice(pool)}")
            if len(self.log_lines) > max_lines:
                self.log_lines.pop(0)
            self.last_cmd = now

    def draw(self, surf, rect):
        self.t += 1
        third = rect.width // 3
        gas_rect = pygame.Rect(rect.left, rect.top, third, rect.height)
        rad_rect = pygame.Rect(rect.left + third, rect.top, third, rect.height)
        cmd_rect = pygame.Rect(rect.left + 2 * third, rect.top, rect.width - 2 * third, rect.height)

        self._update_commands(cmd_rect.height // (font_console.get_height() + 2))
        rad = 0.015 + 0.005 * math.sin(self.t / 90)

        pygame.draw.rect(surf, CYAN, gas_rect, 2, border_radius=12)
        pygame.draw.rect(surf, CYAN, rad_rect, 2, border_radius=12)
        pygame.draw.rect(surf, CYAN, cmd_rect, 2, border_radius=12)

        update_gases()
        draw_gas_chart(surf, gas_rect)

        max_radius = min(rad_rect.height - 60, rad_rect.width - 120) // 2
        center2 = (rad_rect.left + max_radius + 180, rad_rect.top + rad_rect.height // 2 - 15)
        end_angle = -90 + int(360 * rad / 100)
        draw_pie(surf, center2, max_radius, -90, end_angle, (0, 255, 0))
        pygame.gfxdraw.aacircle(surf, center2[0], center2[1], max_radius, CYAN)

        text_x = center2[0] + max_radius + 30
        text_y = rad_rect.top + 35
        pygame.draw.rect(surf, (0, 255, 0), (text_x - 228, text_y + 114, 18, 18))
        label = font_diagramm1.render(f"{rad:.2f} мкЗв/ч", True, CYAN)
        surf.blit(label, (text_x - 205, text_y + 112))
        label2 = font_diagramm3.render(f"(В пределах нормы)", True, CYAN)
        surf.blit(label2, (text_x - 247, text_y + 142))

        caption = font_diagramm2.render("Уровень ионизируещего излучения", True, CYAN)
        surf.blit(
            caption,
            (rad_rect.left + (rad_rect.width - caption.get_width()) / 2, center2[1] + max_radius + 11),
        )

        inner = cmd_rect.inflate(-4, -4)
        pygame.draw.rect(surf, BG_COLOR, inner, 0, border_radius=8)
        line_h = font_console.get_height()
        y = inner.bottom - line_h * len(self.log_lines) - 4
        for line in self.log_lines:
            surf.blit(font_console.render(line, True, CYAN), (inner.left + 30, y))
            y += line_h


status_panel = ShipStatus()


def draw_status_panel():
    rect = pygame.Rect(40, HEIGHT - STATUS_PANEL_HEIGHT, view_width, STATUS_PANEL_HEIGHT)
    status_panel.draw(screen, rect)


def _prepare_text_surfaces(text, font, max_width):
    """Wraps text to fit `max_width` and returns rendered line surfaces."""
    char_width = font.size("A")[0]
    max_chars = max(1, max_width // char_width)
    surfaces = []
    for paragraph in text.split("\n"):
        if not paragraph:
            surfaces.append(font.render("", True, CYAN))
            continue
        for line in textwrap.wrap(paragraph, width=max_chars):
            surfaces.append(font.render(line, True, CYAN))
    return surfaces


def show_member_info(member):
    w, h = int(WIDTH * 0.6), int(HEIGHT * 0.6)
    rect = pygame.Rect(WIDTH // 2 - w // 2, HEIGHT // 2 - h // 2, w, h)
    img = member["img_big"]
    img_rect = img.get_rect(topleft=(rect.left + 20, rect.top + 20))
    text_rect = pygame.Rect(
        rect.left + 20,
        img_rect.bottom + 20,
        rect.width - 40,
        rect.height - (img_rect.bottom - rect.top) - 40,
        )
    lines = _prepare_text_surfaces(member["desc"], font_small, text_rect.width)
    line_spacing = 5
    total_text_height = sum(s.get_height() + line_spacing for s in lines) - line_spacing
    offset = 0
    max_offset = min(0, text_rect.height - total_text_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    offset = min(offset + 20, 0)
                elif event.button == 5:
                    offset = max(offset - 20, max_offset)
                else:
                    return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        screen.blit(panel, rect.topleft)
        pygame.draw.rect(screen, CYAN, rect, 3, border_radius=12)

        screen.blit(img, img_rect)
        name = font_medium.render(member["name"], True, CYAN)
        code = font_small.render(f"Код сотрудника: {member['code']}", True, CYAN)
        screen.blit(name, (img_rect.right + 20, img_rect.top))
        screen.blit(code, (img_rect.right + 20, img_rect.top + 40))

        screen.set_clip(text_rect)
        y = text_rect.top + offset
        for surf in lines:
            screen.blit(surf, (text_rect.left, y))
            y += surf.get_height() + line_spacing
        screen.set_clip(None)

        pygame.display.flip()
        clock.tick(60)


def show_ship_details():
    w, h = int(WIDTH * 0.6), int(HEIGHT * 0.6)
    rect = pygame.Rect(WIDTH // 2 - w // 2, HEIGHT // 2 - h // 2, w, h)
    img = SHIP_DATA["img_big"]
    img_rect = img.get_rect(topleft=(rect.left + 20, rect.top + 20))
    text_rect = pygame.Rect(img_rect.right + 20, img_rect.top, rect.width - img_rect.width - 40, rect.height - 40)
    lines = _prepare_text_surfaces("\n".join(SHIP_DATA["tech"] + SHIP_DATA["description"]), font_small, text_rect.width)
    offset = 0
    total = sum(s.get_height() + 4 for s in lines)
    max_offset = min(0, text_rect.height - total)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    offset = min(offset + 20, 0)
                elif event.button == 5:
                    offset = max(offset - 20, max_offset)
                else:
                    return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        pygame.draw.rect(screen, CYAN, rect, 3, border_radius=12)
        screen.blit(img, img_rect)

        screen.set_clip(text_rect)
        y = text_rect.top + offset
        for surf in lines:
            screen.blit(surf, (text_rect.left, y))
            y += surf.get_height() + 4
        screen.set_clip(None)

        pygame.display.flip()
        clock.tick(60)


def main():
    global crew_offset
    header = header_surface
    dragging_thumb = False
    drag_offset = 0
    dragging_list = False
    drag_start_x = 0
    drag_start_offset = 0
    drag_moved = False
    clicked_member = None
    thumb_rect = None
    scrollbar_rect = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_RIGHT:
                    crew_offset = max(crew_offset - 40, max_scroll)
                elif event.key == pygame.K_LEFT:
                    crew_offset = min(crew_offset + 40, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                crew_rect = pygame.Rect(40, crew_start_y, view_width, CREW_CARD_HEIGHT + 2 * CREW_FRAME_MARGIN)
                if event.button == 4:
                    crew_offset = min(crew_offset + 40, 0)
                elif event.button == 5:
                    crew_offset = max(crew_offset - 40, max_scroll)
                elif ship_item_rect.collidepoint(event.pos):
                    show_ship_details()
                elif thumb_rect and thumb_rect.collidepoint(event.pos):
                    dragging_thumb = True
                    drag_offset = event.pos[0] - thumb_rect.x
                elif crew_rect.collidepoint(event.pos):
                    dragging_list = True
                    drag_start_x = event.pos[0]
                    drag_start_offset = crew_offset
                    drag_moved = False
                    clicked_member = None
                    for m in CREW_DATA:
                        if m.get("rect") and m["rect"].collidepoint(event.pos):
                            clicked_member = m
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_thumb:
                    dragging_thumb = False
                elif dragging_list:
                    if not drag_moved and clicked_member:
                        show_member_info(clicked_member)
                    dragging_list = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging_thumb and scrollbar_rect:
                    new_x = min(max(event.pos[0] - drag_offset, scrollbar_rect.left), scrollbar_rect.right - thumb_rect.width)
                    ratio = (new_x - scrollbar_rect.left) / (scrollbar_rect.width - thumb_rect.width)
                    crew_offset = -ratio * (total_width - view_width)
                elif dragging_list:
                    dx = event.pos[0] - drag_start_x
                    if abs(dx) > 5:
                        drag_moved = True
                    crew_offset = max(min(drag_start_offset + dx, 0), max_scroll)

        screen.fill(BG_COLOR)
        screen.blit(header, header.get_rect(midtop=(WIDTH // 2, HEADER_TOP)))
        draw_ship_info()
        thumb_rect, scrollbar_rect = draw_crew_list()
        draw_status_panel()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()