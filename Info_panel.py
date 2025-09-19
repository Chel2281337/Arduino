import sys, os, pygame, textwrap

BASE_DIR = os.path.dirname(__file__)


def asset(*parts):
    return os.path.join(BASE_DIR, *parts)

# ---------------------------- Parameters ----------------------------
FULLSCREEN = True
TITLE = "ИНФОРМАЦИОННАЯ ПАНЕЛЬ"

BG_COLOR = (10, 15, 26)
CYAN = (222, 255, 255)

RIGHT_PANEL_WIDTH = 360  # width of section menu on the right
SECTION_BUTTON_HEIGHT = 100
SECTION_TITLES = [
    "Информация о корабле",
    "Информация о сотрудниках",
    "Система навигации",
]
SHIP_SCHEMATIC = asset("img", "ship_schematic.png")
NAVIGATION_MAP = asset("img", "starmap.png")

# rotating icons over the ship schematic
TOCHKA_ICON = asset("img", "tochka.png")
TOCHKA_ICON2 = asset("img", "tochka2.png")
# pulsating icons for navigation map
PULSE_ICON = asset("img", "pulse.png")
# ship marker on navigation map
SPACEMAP_SHIP_ICON = asset("img", "spacemapship.png")

# each dict: position (x, y) in pixels relative to the schematic area,
# size in px, clockwise rotation speed in degrees per second,
# popup_pos and popup_size define location and size of the info window
TOCHKA_ICONS = [
    {"pos": (526, 560), "size": 100, "speed": 60,
     "popup_pos": (60, 60), "popup_size": (350, 462)},
    {"pos": (802, 147), "size": 120, "speed": 60,
     "popup_pos": (940, 20), "popup_size": (550, 310)},
    {"pos": (802, 548), "size": 150, "speed": 60,
     "popup_pos": (1176, 350), "popup_size": (350, 470)},
    {"pos": (800, 856), "size": 120, "speed": 60,
     "popup_pos": (60, 560), "popup_size": (360, 462)},
    {"pos": (1050, 923), "size": 110, "speed": 60,
     "popup_pos": (1175, 835), "popup_size": (350, 210)},
]

# textual information for each tochka popup; each entry is a list of
# (line, bold) tuples where *line* is a string and *bold* is a boolean
# indicating whether the line should be rendered in bold font
TOCHKA_INFO = [
    [
        ("Общие характеристики:", False),
        ("Тип: Многоуровневые топливные баки для хранения жидких и газообразных топливных компонентов", False),
        ("Материал: Специально разработанные сплавы, устойчивые к экстремальным температурным и давлениям, с использованием технологий из сверхпрочных композитных материалов для минимизации веса и повышения прочности.", False),
        ("Мощность и ёмкость: Баки разработаны для обеспечения работы всех систем корабля, включая двигатели и реактор, в условиях длительных межпланетных путешествий.", False),
        ("", False),
        ("Дейтерий и тритий (для термоядерного реактора)", True),
        ("Тип топлива: Дейтерий и тритий — изотопы водорода, используемые для термоядерного синтеза в реакторах. Эти изотопы обеспечивают высокую плотность энергии и являются основой термоядерного топлива.", False),
        ("Ёмкость: Хранятся в сжиженном или газообразном виде в специально герметичных резервуарах. Ёмкость зависит от продолжительности миссии, с возможностью хранения нескольких тысяч литров.", False),
        ("Особенности: Высокая эффективность синтеза при слиянии. Требуют строгого контроля температуры и давления для предотвращения утечек и обеспечения стабильности реакции.", False),
        ("", False),
        ("Двигательное топливо для дозвуковых и маневровых двигателей", True),
        ("Тип топлива: Гидразин или его производные, а также гипергорючие смеси для двигателей типа «Rolls-Royce N66 Cyclone» и маневровых двигателей «Weyland L46».", False),
        ("Ёмкость: Эти баки имеют высокий коэффициент сжимаемости и предназначены для хранения топлива под давлением, необходимого для маневрирования в космосе.", False),
        ("Особенности: Каждая из топливных смесей имеет точное количество резервуаров для обеспечения сбалансированного расхода топлива при высоких тяговых усилиях.", False),
        ("", False),
        ("Запасное топливо для сверхсветовых двигателей", True),
        ("Тип топлива: Жидкие и газообразные углеводородные смеси с высокой плотностью энергии, используемые для питания сверхсветовых тахионных двигателей «Yutani T7A NLS».", False),
        ("Ёмкость: Баки предназначены для хранения топлива при экстремально низких температурах и высоком давлении, что важно для работы в сверхсветовом режиме.", False),
        ("Особенности: Для работы сверхсветовых двигателей топливо должно быть стабилизировано и обеспечено высокое качество, что требует специализированных фильтров и контроля в реальном времени.", False),
    ],
    [
        ("Основной управляющий компьютер MU/TH/UR 182", True),
        ("Тип: Искусственный интеллект, управляющий всеми основными процессами корабля", False),
        ("Объем памяти: 2,1 ТБ", False),
        ("Функции: Управление навигацией, анализ данных с сенсоров, контроль всех систем корабля, включая двигатели, системы жизнеобеспечения и безопасность. AI отвечает за принятие решений и оптимизацию работы корабля в реальном времени.", False),
        ("Особенности: Искусственный интеллект с возможностью обучаться и адаптироваться в условиях экстремальной эксплуатации, что делает его ключевым элементом управления кораблем в условиях дальнего космоса.", False),
        ("Резервный мэйнфрейм: Дополнительный компьютер с 2 ТБ памяти, обеспечивающий резервное управление и сохранение данных в случае отказа основного блока.", False),
        ("", False),
        ("Операционная система OAM (Overmonitoring Address Matrix) версии 2.2.2120", True),
        ("Тип: Системное ПО", False),
        ("Функции: Координирует работу всех подсистем и датчиков, анализирует данные и оптимизирует работу оборудования в реальном времени, включая обработку сенсорной информации и управление ресурсами корабля.", False),
        ("Особенности: Высокая степень надежности и устойчивости в условиях длительных межпланетных путешествий и автономных миссий.", False),
        ("", False),
        ("Оборудование и датчики", False),
        ("Телескопы (оптический и инфракрасный диапазоны):", False),
        ("Тип: Два телескопа", False),
        ("Функции: Обнаружение космических объектов на дальних дистанциях, исследование небесных тел, а также анализ атмосферы и поверхности планет.", False),
        ("Размер: Каждый телескоп имеет диаметр 2 метра и способен работать в оптическом и инфракрасном диапазоне, а также в спектрографическом режиме.", False),
        ("", False),
        ("Газовый хроматограф:", False),
        ("Тип: Анализатор химического состава атмосферы и поверхности.", False),
        ("Функции: Применяется для точного анализа состава газов и других химических веществ, которые могут быть обнаружены во время исследования планет и спутников.", False),
        ("", False),
        ("Радар навигации и посадки:", False),
        ("Тип: Система навигации с радиолокацией", False),
        ("Диапазон: Работает в сантиметровом диапазоне", False),
        ("Функции: Обеспечивает точную навигацию и помощь при посадке, сканируя поверхность планеты или спутника.", False),
        ("", False),
        ("Радар сканирования поверхности с синтезированной апертурой:", False),
        ("Тип: Радар с синтезированной апертурой", False),
        ("Функции: Используется для детального сканирования поверхности планет и спутников, что позволяет создавать высококачественные карты местности и изучать возможные аномалии.", False),
        ("", False),
        ("Счётчик массы в гиперпространстве:", False),
        ("Тип: Метрическая система", False),
        ("Функции: Используется для измерения массы объектов, находящихся в гиперпространстве, что критично для расчётов в сверхсветовых путешествиях.", False),
    ],
    [
        ("Термоядерный реактор «Laratel WF-15»", True),
        ("Тип: Дейтериево-тритиевый термоядерный реактор", False),
        ("Мощность: 2,8 ТВт", False),
        ("Принцип работы: Реактор использует термоядерный синтез между изотопами водорода (дейтерий и тритий) для генерации высокоэффективной энергии. Этот процесс обеспечивает непрерывную и мощную энергию для работы всех систем корабля, включая двигатели и научное оборудование.", False),
        ("Особенности: Обеспечивает стабильное энергоснабжение на протяжении длительных межпланетных путешествий и является основным источником энергии для сверхсветовых и дозвуковых двигателей.", False),
        ("", False),
        ("Технические характеристики космического корабля", False),
        ("Масса:", False),
        ("Пустой корабль — 45 000 тонн", False),
        ("Нормальная загрузка — 50 000 тонн", False),
        ("Полная загрузка — 63 000 тонн", False),
        ("Платформа: Масса платформы свыше 20 миллионов тонн", False),
        ("", False),
        ("Автономность:", False),
        ("Стандартная — 14 месяцев", False),
        ("Максимальная — 24 месяца", False),
        ("", False),
        ("Вооружение: Отсутствует", False),
        ("Вспомогательные космические корабли: Один челнок класса «Starcab»", False),
    ],
    [
        ("Сверхсветовые тахионные двигатели «Yutani T7A NLS»", True),
        ("Тип: Сверхсветовые тахионные двигатели", False),
        ("Количество: 4 двигателя", False),
        ("Принцип работы: Используют тахионное излучение для создания сверхсветового движения, позволяя кораблю достигать скорости, превышающие скорость света.", False),
        ("Мощность: Позволяют кораблю разгоняться до 153-кратной скорости света в условиях максимальной загрузки, обеспечивая чрезвычайно высокую эффективность и дальность перемещения.", False),
        ("Особенности: Высокая степень стабильности при переходе в сверхсветовой режим и управление реактивным тяговым усилием на различных уровнях скорости.", False),
        ("", False),
        ("Внешний модуль малой тяги «Yutani J38»", True),
        ("Тип: Модуль малой тяги", False),
        ("Количество: 1 модуль", False),
        ("Мощность: Два комплекса двигателей «Lockheed Martin TL-30»", False),
        ("Принцип работы: Этот внешний модуль используется для корректировки движения при мелких маневрах, например, для стабилизации на орбите, и предназначен для точных, локальных изменений в траектории движения при минимальных расходах энергии.", False),
        ("Особенности: Система позволяет поддерживать стабильность на малых дистанциях и идеально подходит для малых маневров, таких как стоянка на орбите.", False),
    ],
    [
        ("Досветовые двигатели «Rolls-Royce N66 Cyclone»", True),
        ("Тип: Трубные двигатели с двунаправленным вектором тяги", False),
        ("Количество: 2 двигателя", False),
        ("Тяга: 7,29 млн тонн (64,9 гиганьютонов) на двигатель", False),
        ("Принцип работы: Используют комбинированные потоки газа и плазмы, обеспечивая высокую степень маневренности и эффективности на дозвуковых и гиперзвуковых скоростях. Двухвекторная тяга позволяет изменять направление полета для более точной навигации и маневров.", False),
        ("Особенности: Рекомендованы для работы на межпланетных расстояниях и эффективны для работы с высокими грузами, поскольку обладают мощным тяговым усилием при низких расходах топлива.", False),
        ("", False),
        ("Маневровые двигатели «Weyland L46»", True),
        ("Тип: Маневровые двигатели", False),
        ("Количество: 2 двигателя", False),
        ("Тяга: 850 тыс. тонн (7,6 гиганьютонов) на двигатель", False),
        ("Принцип работы: Маневровые двигатели позволяют плавно изменять траекторию корабля и обеспечивают точную посадку и орбитальное маневрирование. Используют высокоэффективный реактивный принцип работы с возможностью быстрой корректировки вектора тяги.", False),
        ("Особенности: Подходят для низкоскоростных маневров в пределах орбиты, а также для точных входов в атмосферу планет.", False),
    ],
]

# pulsating icons: position relative to navigation map area,
# minimal size, maximal size, scale speed and popup window parameters
PULSE_ICONS = [
    {"pos": (338, 842), "min": 50, "max": 150, "speed": 40,
     "popup_pos": (480, 620), "popup_size": (530, 400)},
    {"pos": (1240, 280), "min": 50, "max": 150, "speed": 50,
     "popup_pos": (1230, 380), "popup_size": (530, 400)},
]

TOCHKA_ANIM_MS = 80

# ship icon parameters on navigation map
SPACEMAP_SHIP_POS = (790, 570)
SPACEMAP_SHIP_SIZE1 = 110
SPACEMAP_SHIP_SIZE2 = 120
SPACEMAP_SHIP_ANGLE = -57

# status panel on navigation map
SPACEMAP_PANEL_POS = (40, 40)
SPACEMAP_PANEL_SIZE = (400, 460)
SPACEMAP_PANEL_FONT_SIZE = 40
SPACEMAP_PANEL_TEXT_OFFSET = (20, 20)
SPACEMAP_PANEL_LINE_GAP = 4
SPACEMAP_PANEL_PARAM_GAP = 28
SPACEMAP_PANEL_BOLD_LABELS = [True, True, True, True, True]

# per-tochka animation state: icon cross-fade progress, popup fade and rotation angle
tochka_states = [{"progress": 0.0, "target": 0,
                  "popup": 0.0, "popup_target": 0,
                  "rect": pygame.Rect(0, 0, 0, 0),
                  "center": (0, 0),
                  "angle": 0.0,
                  "offset": 0,
                  "max_offset": 0} for _ in TOCHKA_ICONS]
active_tochka = None
dt = 0

# ship and crew data reused from previous panel
SHIP_DATA = {
    "photo": asset("img", "ship.png"),
}

CREW_DATA = [
    {
        "photo": asset("img", "crew1.png"),
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
        "photo": asset("img", "crew2.png"),
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
        "photo": asset("img", "crew3.png"),
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
        "photo": asset("img", "crew4.png"),
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
        "photo": asset("img", "crew5.png"),
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
        "photo": asset("img", "crew6.png"),
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
        "photo": asset("img", "crew7.png"),
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

# crew list layout
CREW_ITEM_HEIGHT = 180
CREW_IMG_SIZE = 140
CREW_SPACING = 20
SCROLLBAR_WIDTH = 20
SCROLL_THUMB_WIDTH = 16

pygame.init()
flags = pygame.FULLSCREEN if FULLSCREEN else 0
screen = pygame.display.set_mode((0, 0), flags) if FULLSCREEN else pygame.display.set_mode((1280, 1024))
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

font_title = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_medium_bold = pygame.font.Font(None, 36)
font_medium_bold.set_bold(True)
font_small = pygame.font.Font(None, 24)
font_navpanel = pygame.font.Font(None, SPACEMAP_PANEL_FONT_SIZE)


def load_image(path, size=None):
    if os.path.isfile(path):
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    if size is None:
        size = (100, 100)
    surf = pygame.Surface(size)
    surf.fill((30, 30, 30))
    pygame.draw.rect(surf, CYAN, surf.get_rect(), 2)
    return surf


def load_round_image(path, size, radius=12):
    img = load_image(path, size).convert_alpha()
    mask = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255), mask.get_rect(), border_radius=radius)
    img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pygame.draw.rect(img, CYAN, img.get_rect(), 2, border_radius=radius)
    return img


for m in CREW_DATA:
    m["img_small"] = load_round_image(m["photo"], (CREW_IMG_SIZE, CREW_IMG_SIZE))
    m["img_big"] = load_round_image(m["photo"], (200, 200))

# information for pulsating icons on navigation map
PULSE_INFO = [
    {
        "photo": asset("img", "LV-426.png"),
        "title": "LV-426",
        "blurb": "Планета LV-426 является природным спутником газового гиганта, расположенным в системе Калпам.",
        "desc": (
            "Орбитальные характеристики:\n"
            "Тип объекта: Естественный спутник.\n"
            "Размеры: Диаметр планеты составляет порядка 10 500 километров, что относит её к категории спутников средней величины.\n"
            "Орбитальная характеристика: LV-426 имеет элиптическую орбиту вокруг своего родительского газового гиганта, с периодом обращения, приблизительно равным 16 земным суткам. Это накладывает определённые климатические особенности, связанные с сезонными изменениями температуры и радиации.\n\n"
            "Атмосферные характеристики:\n"
            "Состав атмосферы: Атмосфера LV-426 состоит преимущественно из углекислого газа (CO₂) с присутствием азота (N₂) и следовых количеств аммиака (NH₃). Метан (CH₄) также присутствует, что свидетельствует о возможных геохимических процессах, связанных с метаболической активностью местных микроорганизмов или геотермальными источниками.\n"
            "Давление: Атмосферное давление на поверхности составляет около 0,5 атмосферы (приблизительно 50% от земного), что требует использования специализированной защитной экипировки для дыхания живыми существами земного происхождения.\n"
            "Климат: Планета характеризуется переменным климатом, включающим экстремальные колебания температур, часто сопровождающиеся кислотными дождями, образующимися в результате химических реакций между компонентами атмосферы и минералами поверхности.\n\n"
            "Геологические особенности:\n"
            "Геология: Поверхность LV-426 состоит из разнообразных геологических форм, включая высокогорья, равнины, вулканические кратеры и огромные каньоны. Преобладающие породы — это древние базальтовые и андезитовые образования, свидетельствующие о тектонической активности в прошлом. Эти особенности предполагают, что планета может иметь неактивное тектоническое строение на данный момент, но сохранившиеся следы вулканизма указывают на более динамичные геологические процессы в её ранней истории.\n"
            "Минеральные ресурсы: Исследования показывают наличие редких минералов и металлов, таких как сера, сульфиды и карбонаты, которые могли бы быть продуктом гипотетической геотермальной активности. Эти материалы могут быть источниками энергии или участниками биохимических циклов, если таковые существуют на планете.\n\n"
            "Биосфера:\n"
            "Биологическая активность: По имеющимся данным, планета не поддерживает сложные формы жизни, аналогичные земным, однако наблюдаются следы биохимической активности. Это может включать экстремофильные микроорганизмы, способные выживать в условиях высокой кислотности, низких температур и ограниченного кислорода. Возможные биохимические пути метаболизма включают использование серы и аммиака в качестве источников энергии.\n"
            "Экологическая структура: Несмотря на неблагоприятные условия для жизнедеятельности, на планете могут существовать устойчивые экосистемы, основанные на гипотетических формах жизни, адаптированных к экстремальным экологическим условиям. Эти формы жизни могли бы быть адаптированы к существованию в условиях, где традиционные молекулы, такие как углеводы или белки, маловероятны."
        ),
    },
    {
        "photo": asset("img", "earth.png"),
        "title": "Земля",
        "blurb": "Земля — это планета земного типа, являющаяся родным домом человечества и важным объектом в контексте научных, экономических и технологических разработок. Она обладает уникальной экосистемой, поддерживающей разнообразие жизни, и играют важную роль в Солнечной системе как центр цивилизации и ключевая точка для исследовательской и промышленной деятельности.",
        "desc": (
            "Орбитальные характеристики:\n"
            "Тип объекта: Планета земного типа.\n"
            "Размеры: Диаметр Земли составляет около 12 742 километров, масса — 5,97 × 10²⁴ кг.\n"
            "Орбитальная характеристика: Земля обращается вокруг Солнца по эллиптической орбите с периодом 365,25 суток, "
            "что приводит к сезонным изменениям и стабилизации климатических условий.\n\n"
            "Атмосферные характеристики:\n"
            "Состав атмосферы: Атмосфера Земли включает 78% азота, 21% кислорода и следовые количества углекислого газа и "
            "других газов, создающих условия, подходящие для поддержания жизни.\n"
            "Климат: Земля обладает разнообразными климатическими зонами, от тропических до полярных регионов, что способствует "
            "экосистемному разнообразию.\n\n"
            "Геологические характеристики:\n"
            "Геология: Планета имеет активную тектоническую структуру, где действуют процессы горообразования, вулканизма и "
            "сейсмической активности. Земля состоит из континентов и океанов, что способствует формированию различных ландшафтов.\n"
            "Минеральные ресурсы: Земля богата минеральными ресурсами, такими как уголь, нефть, металлы, редкоземельные элементы "
            "и другие материалы, необходимые для промышленности и высоких технологий.\n\n"
            "Биосфера:\n"
            "Жизнь на Земле: Земля является домом для миллиардов видов живых существ. Она поддерживает уникальную и "
            "разнообразную биосферу, включая растения, животных, микроорганизмы и человека.\n"
            "Экосистемы: Разнообразие экосистем Земли включает в себя тропические леса, пустыни, океаны, горные регионы и "
            "другие биомы, каждый из которых поддерживает различные формы жизни."
        ),
    },
]

for p in PULSE_INFO:
    p["img_big"] = load_round_image(p["photo"], (300, 200))

# base image for rotating icons
TOCHKA_IMAGE = load_image(TOCHKA_ICON)
TOCHKA_IMAGE2 = load_image(TOCHKA_ICON2)
PULSE_IMAGE = load_image(PULSE_ICON)
SPACEMAP_SHIP_IMAGE = load_image(SPACEMAP_SHIP_ICON)

ship_schematic_img = load_image(SHIP_SCHEMATIC)
navigation_map_img = load_image(NAVIGATION_MAP)

scroll_offset = 0
active_section = 0

# animation state for pulsating icons and ship marker
pulse_states = [{"size": icon["min"], "dir": 1, "paused": False,
                 "popup": 0.0, "popup_target": 0,
                 "rect": pygame.Rect(0, 0, 0, 0), "center": (0, 0)}
                for icon in PULSE_ICONS]


def update_pulse_icons():
    for icon, state in zip(PULSE_ICONS, pulse_states):
        if not state["paused"]:
            state["size"] += state["dir"] * icon["speed"] * dt / 1000.0
            if state["size"] >= icon["max"]:
                state["size"] = icon["max"]
                state["dir"] = -1
            elif state["size"] <= icon["min"]:
                state["size"] = icon["min"]
                state["dir"] = 1
        if state["popup_target"] > state["popup"]:
            state["popup"] = min(state["popup_target"], state["popup"] + dt / TOCHKA_ANIM_MS)
        elif state["popup_target"] < state["popup"]:
            state["popup"] = max(state["popup_target"], state["popup"] - dt / TOCHKA_ANIM_MS)


def _prepare_text_surfaces(text, font, max_width):
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


def show_pulse_info(index):
    info = PULSE_INFO[index]
    cfg = PULSE_ICONS[index]
    popup_rect = pygame.Rect(cfg["popup_pos"], cfg["popup_size"])
    img = info["img_big"]
    img_w = popup_rect.width - 20
    img_h = int(img_w * img.get_height() / img.get_width())
    if img_h > popup_rect.height // 2:
        img_h = popup_rect.height // 2
        img_w = int(img.get_width() * img_h / img.get_height())
    img = pygame.transform.smoothscale(img, (img_w, img_h))
    img_rect = img.get_rect(topleft=(popup_rect.left + 10, popup_rect.top + 10))

    right_rect = pygame.Rect(
        img_rect.right + 10,
        img_rect.top,
        popup_rect.right - img_rect.right - 20,
        img_rect.height,
        )
    title = font_medium_bold.render(info["title"], True, CYAN)
    blurb_lines = _prepare_text_surfaces(info.get("blurb", ""), font_small, right_rect.width)

    text_rect = pygame.Rect(
        popup_rect.left + 10,
        img_rect.bottom + 10,
        popup_rect.width - 20,
        popup_rect.bottom - img_rect.bottom - 20,
        )
    lines = _prepare_text_surfaces(info["desc"], font_small, text_rect.width)
    line_spacing = 5
    total_text_height = sum(s.get_height() + line_spacing for s in lines) - line_spacing
    offset = 0
    max_offset = min(0, text_rect.height - total_text_height)

    prev = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()
        global dt
        dt = now - prev
        prev = now

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
                elif not popup_rect.collidepoint(event.pos):
                    return

        update_pulse_icons()
        screen.fill(BG_COLOR)
        draw_navigation_section()
        draw_right_panel(pygame.mouse.get_pos())
        draw_navigation_panel()

        cx, cy = pulse_states[index]["center"]
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        midpoints = [
            (popup_rect.centerx, popup_rect.top),
            (popup_rect.centerx, popup_rect.bottom),
            (popup_rect.left, popup_rect.centery),
            (popup_rect.right, popup_rect.centery),
        ]
        line_end = min(midpoints, key=lambda p: (p[0]-cx)**2 + (p[1]-cy)**2)
        pygame.draw.line(overlay, CYAN, (cx, cy), line_end, 2)
        panel = pygame.Surface(popup_rect.size, pygame.SRCALPHA)
        panel.fill((*BG_COLOR, 230))
        pygame.draw.rect(panel, CYAN, panel.get_rect(), 2, border_radius=12)
        panel.blit(img, img_rect.move(-popup_rect.left, -popup_rect.top))

        rel = popup_rect.topleft
        panel.blit(title, (right_rect.left - rel[0], right_rect.top - rel[1]))
        y_text = right_rect.top - rel[1] + title.get_height() + 5
        for surf in blurb_lines:
            if y_text + surf.get_height() > right_rect.bottom - rel[1]:
                break
            panel.blit(surf, (right_rect.left - rel[0], y_text))
            y_text += surf.get_height() + 5

        clip = text_rect.move(-popup_rect.left, -popup_rect.top)
        panel.set_clip(clip)
        y = clip.top + offset
        for surf in lines:
            panel.blit(surf, (clip.left, y))
            y += surf.get_height() + line_spacing
        panel.set_clip(None)
        overlay.blit(panel, popup_rect.topleft)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def draw_right_panel(mouse_pos):
    panel_rect = pygame.Rect(WIDTH - RIGHT_PANEL_WIDTH, 0, RIGHT_PANEL_WIDTH, HEIGHT)
    pygame.draw.rect(screen, CYAN, panel_rect, 2)
    btn_rects = []
    y = 0
    for i, title in enumerate(SECTION_TITLES):
        r = pygame.Rect(panel_rect.left, y, RIGHT_PANEL_WIDTH, SECTION_BUTTON_HEIGHT)
        btn_rects.append(r)
        if i == active_section:
            pygame.draw.rect(screen, (0, 80, 80), r)
        pygame.draw.rect(screen, CYAN, r, 2)
        text = font_medium.render(title, True, CYAN)
        screen.blit(text, text.get_rect(center=r.center))
        y += SECTION_BUTTON_HEIGHT
    return btn_rects


def draw_ship_section():
    area = pygame.Rect(0, 0, WIDTH - RIGHT_PANEL_WIDTH, HEIGHT)
    pygame.draw.rect(screen, CYAN, area, 2)
    if ship_schematic_img:
        inner = area.inflate(-4, -4)
        img = pygame.transform.smoothscale(ship_schematic_img, inner.size)
        screen.blit(img, inner.topleft)
        if TOCHKA_IMAGE and TOCHKA_IMAGE2:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            for i, cfg in enumerate(TOCHKA_ICONS):
                state = tochka_states[i]
                # update icon crossfade
                if state["target"] > state["progress"]:
                    state["progress"] = min(state["target"], state["progress"] + dt / TOCHKA_ANIM_MS)
                elif state["target"] < state["progress"]:
                    state["progress"] = max(state["target"], state["progress"] - dt / TOCHKA_ANIM_MS)
                # update popup fade
                if state["popup_target"] > state["popup"]:
                    state["popup"] = min(state["popup_target"], state["popup"] + dt / TOCHKA_ANIM_MS)
                elif state["popup_target"] < state["popup"]:
                    state["popup"] = max(state["popup_target"], state["popup"] - dt / TOCHKA_ANIM_MS)
                if active_tochka != i:
                    state["angle"] = (state["angle"] + cfg["speed"] * dt / 1000) % 360
                angle = state["angle"]
                size = cfg["size"]
                img1 = pygame.transform.smoothscale(TOCHKA_IMAGE, (size, size))
                img2 = pygame.transform.smoothscale(TOCHKA_IMAGE2, (size, size))
                rot1 = pygame.transform.rotate(img1, -angle)
                rot2 = pygame.transform.rotate(img2, -angle)
                rot1.set_alpha(int(255 * (1 - state["progress"])))
                rot2.set_alpha(int(255 * state["progress"]))
                blended = pygame.Surface(rot1.get_size(), pygame.SRCALPHA)
                blended.blit(rot1, (0, 0))
                blended.blit(rot2, (0, 0))
                rect = blended.get_rect(center=(inner.left + cfg["pos"][0],
                                                inner.top + cfg["pos"][1]))
                screen.blit(blended, rect)
                state["rect"] = rect
                state["center"] = rect.center

                if state["popup"] > 0:
                    popup_rect = pygame.Rect(cfg["popup_pos"], cfg["popup_size"])
                    cx, cy = state["center"]
                    midpoints = [
                        (popup_rect.centerx, popup_rect.top),
                        (popup_rect.centerx, popup_rect.bottom),
                        (popup_rect.left, popup_rect.centery),
                        (popup_rect.right, popup_rect.centery),
                    ]
                    line_end = min(midpoints, key=lambda p: (p[0]-cx)**2 + (p[1]-cy)**2)
                    alpha = int(255 * state["popup"])
                    pygame.draw.line(overlay, (*CYAN, alpha), state["center"], line_end, 2)
                    popup_surf = pygame.Surface(popup_rect.size, pygame.SRCALPHA)
                    popup_surf.fill((*BG_COLOR, alpha))
                    pygame.draw.rect(popup_surf, (*CYAN, alpha), popup_surf.get_rect(), 2, border_radius=12)

                    info = TOCHKA_INFO[i]
                    text_rect = popup_surf.get_rect().inflate(-20, -20)
                    lines = []
                    for text, bold in info:
                        font = font_medium_bold if bold else font_small
                        lines.extend(_prepare_text_surfaces(text, font, text_rect.width))
                        lines.append(None)
                    total_h = sum((font_small.get_height() + 5) if s is None else (s.get_height() + 5) for s in lines) - 5
                    state["max_offset"] = min(0, text_rect.height - total_h)
                    y_text = text_rect.top + state["offset"]
                    for surf in lines:
                        if surf is None:
                            y_text += font_small.get_height() + 5
                        else:
                            popup_surf.blit(surf, (text_rect.left, y_text))
                            y_text += surf.get_height() + 5

                    overlay.blit(popup_surf, popup_rect.topleft)

            screen.blit(overlay, (0, 0))


def draw_crew_section():
    global scroll_offset
    area = pygame.Rect(0, 0, WIDTH - RIGHT_PANEL_WIDTH, HEIGHT)
    pygame.draw.rect(screen, CYAN, area, 2)
    clip = area.inflate(-20, -20)
    screen.set_clip(clip)
    item_width = clip.width - SCROLLBAR_WIDTH - 10
    y_start = clip.top + scroll_offset
    thumb_rect = None
    for i, m in enumerate(CREW_DATA):
        y = y_start + i * (CREW_ITEM_HEIGHT + CREW_SPACING)
        if y + CREW_ITEM_HEIGHT < clip.top or y > clip.bottom:
            continue
        item_rect = pygame.Rect(clip.left, y, item_width, CREW_ITEM_HEIGHT)
        pygame.draw.rect(screen, CYAN, item_rect, 2, border_radius=12)
        img_rect = m["img_small"].get_rect()
        img_rect.topleft = (item_rect.left + 10, item_rect.top + (CREW_ITEM_HEIGHT - CREW_IMG_SIZE) // 2)
        screen.blit(m["img_small"], img_rect)
        name = font_medium.render(m["name"], True, CYAN)
        code = font_small.render(f"Код сотрудника: {m['code']}", True, CYAN)
        ty = item_rect.top + (CREW_ITEM_HEIGHT - (name.get_height() + code.get_height() + 10)) // 2
        screen.blit(name, (img_rect.right + 20, ty))
        screen.blit(code, (img_rect.right + 20, ty + name.get_height() + 10))
        m["rect"] = item_rect
    screen.set_clip(None)

    content_h = len(CREW_DATA) * (CREW_ITEM_HEIGHT + CREW_SPACING) - CREW_SPACING
    view_h = clip.height
    scrollbar_rect = pygame.Rect(clip.right - SCROLLBAR_WIDTH, clip.top, SCROLLBAR_WIDTH, clip.height)
    pygame.draw.rect(screen, CYAN, scrollbar_rect, 2, border_radius=6)
    if content_h > view_h:
        thumb_h = max(20, scrollbar_rect.height * view_h / content_h)
        ratio = -scroll_offset / (content_h - view_h)
        thumb_y = scrollbar_rect.top + ratio * (scrollbar_rect.height - thumb_h)
        thumb_rect = pygame.Rect(scrollbar_rect.centerx - SCROLL_THUMB_WIDTH // 2,
                                 int(thumb_y), SCROLL_THUMB_WIDTH, int(thumb_h))
        pygame.draw.rect(screen, CYAN, thumb_rect, border_radius=6)
    return thumb_rect, scrollbar_rect


def draw_navigation_section():
    area = pygame.Rect(0, 0, WIDTH - RIGHT_PANEL_WIDTH, HEIGHT)
    if navigation_map_img:
        img = pygame.transform.smoothscale(navigation_map_img, area.size)
        screen.blit(img, area)
    if SPACEMAP_SHIP_IMAGE:
        ship_img = pygame.transform.smoothscale(
            SPACEMAP_SHIP_IMAGE, (SPACEMAP_SHIP_SIZE1, SPACEMAP_SHIP_SIZE2))
        ship_img = pygame.transform.rotate(ship_img, SPACEMAP_SHIP_ANGLE)
        ship_rect = ship_img.get_rect(center=(area.left + SPACEMAP_SHIP_POS[0],
                                              area.top + SPACEMAP_SHIP_POS[1]))
        screen.blit(ship_img, ship_rect)
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for icon, state in zip(PULSE_ICONS, pulse_states):
        size = int(state["size"])
        img = pygame.transform.smoothscale(PULSE_IMAGE, (size, size))
        rect = img.get_rect(center=(area.left + icon["pos"][0], area.top + icon["pos"][1]))
        screen.blit(img, rect)
        state["rect"] = rect
        state["center"] = rect.center
        if state["popup"] > 0:
            popup_rect = pygame.Rect(icon.get("popup_pos", (0, 0)),
                                     icon.get("popup_size", (260, 160)))
            cx, cy = state["center"]
            midpoints = [
                (popup_rect.centerx, popup_rect.top),
                (popup_rect.centerx, popup_rect.bottom),
                (popup_rect.left, popup_rect.centery),
                (popup_rect.right, popup_rect.centery),
            ]
            line_end = min(midpoints, key=lambda p: (p[0]-cx)**2 + (p[1]-cy)**2)
            alpha = int(255 * state["popup"])
            pygame.draw.line(overlay, (*CYAN, alpha), state["center"], line_end, 2)
            popup_surf = pygame.Surface(popup_rect.size, pygame.SRCALPHA)
            popup_surf.fill((*BG_COLOR, alpha))
            pygame.draw.rect(popup_surf, (*CYAN, alpha), popup_surf.get_rect(), 2, border_radius=12)
            overlay.blit(popup_surf, popup_rect.topleft)
    screen.blit(overlay, (0, 0))
    pygame.draw.rect(screen, CYAN, area, 2)


def draw_navigation_panel():
    panel_rect = pygame.Rect(SPACEMAP_PANEL_POS, SPACEMAP_PANEL_SIZE)
    pygame.draw.rect(screen, BG_COLOR, panel_rect)
    pygame.draw.rect(screen, CYAN, panel_rect, 2, border_radius=12)
    tx = panel_rect.left + SPACEMAP_PANEL_TEXT_OFFSET[0]
    ty = panel_rect.top + SPACEMAP_PANEL_TEXT_OFFSET[1]
    lines = [
        ("Время до прибытия:", "НЕОПРЕДЕЛЕНО"),
        ("Оставшееся расстояние:", "78,3 световых лет."),
        ("Текущая скорость:", "0 св. л./сут."),
        ("Направление:", "57° к Солнечной системе."),
        ("Запасы топлива:", "73%"),
    ]
    for (label, value), bold in zip(lines, SPACEMAP_PANEL_BOLD_LABELS):
        font_navpanel.set_bold(bold)
        surf = font_navpanel.render(label, True, CYAN)
        screen.blit(surf, (tx, ty))
        ty += surf.get_height() + SPACEMAP_PANEL_LINE_GAP
        font_navpanel.set_bold(False)
        surf = font_navpanel.render(value, True, CYAN)
        screen.blit(surf, (tx, ty))
        ty += surf.get_height() + SPACEMAP_PANEL_PARAM_GAP


# ------------------------------ Main loop ---------------------------
def main():
    global scroll_offset, active_section
    thumb_rect = None
    scrollbar_rect = None
    dragging = False
    drag_offset = 0
    prev_time = pygame.time.get_ticks()

    while True:
        global dt, active_tochka
        now = pygame.time.get_ticks()
        dt = now - prev_time
        prev_time = now
        update_pulse_icons()
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if active_section == 1:
                        scroll_offset = min(scroll_offset + 40, 0)
                    elif active_section == 0 and active_tochka is not None:
                        st = tochka_states[active_tochka]
                        st["offset"] = min(st["offset"] + 20, 0)
                elif event.button == 5:
                    if active_section == 1:
                        content_h = len(CREW_DATA) * (CREW_ITEM_HEIGHT + CREW_SPACING) - CREW_SPACING
                        view_h = HEIGHT - 40
                        max_scroll = min(0, view_h - content_h)
                        scroll_offset = max(scroll_offset - 40, max_scroll)
                    elif active_section == 0 and active_tochka is not None:
                        st = tochka_states[active_tochka]
                        st["offset"] = max(st["offset"] - 20, st.get("max_offset", 0))
                else:
                    btns = draw_right_panel(mouse_pos)
                    for i, r in enumerate(btns):
                        if r.collidepoint(event.pos):
                            active_section = i
                            break
                    if active_section == 0:
                        handled = False
                        for i, st in enumerate(tochka_states):
                            if st["rect"].collidepoint(event.pos):
                                if active_tochka == i:
                                    st["target"] = 0
                                    st["popup_target"] = 0
                                    active_tochka = None
                                else:
                                    active_tochka = i
                                    for j, st2 in enumerate(tochka_states):
                                        st2["target"] = 1 if j == i else 0
                                        st2["popup_target"] = 1 if j == i else 0
                                handled = True
                                break
                        if not handled and active_tochka is not None:
                            cfg = TOCHKA_ICONS[active_tochka]
                            popup_rect = pygame.Rect(cfg["popup_pos"], cfg["popup_size"])
                            if not popup_rect.collidepoint(event.pos):
                                tochka_states[active_tochka]["target"] = 0
                                tochka_states[active_tochka]["popup_target"] = 0
                                active_tochka = None
                    elif active_section == 1:
                        if thumb_rect and thumb_rect.collidepoint(event.pos):
                            dragging = True
                            drag_offset = event.pos[1] - thumb_rect.y
                        else:
                            for m in CREW_DATA:
                                if m.get("rect") and m["rect"].collidepoint(event.pos):
                                    show_member_info(m)
                                    break
                    else:
                        handled = False
                        for i, st in enumerate(pulse_states):
                            if st["rect"].collidepoint(event.pos):
                                for j, st2 in enumerate(pulse_states):
                                    st2["paused"] = False
                                st["size"] = PULSE_ICONS[i]["max"]
                                st["dir"] = -1
                                st["paused"] = True
                                show_pulse_info(i)
                                st["paused"] = False
                                st["dir"] = -1
                                prev_time = pygame.time.get_ticks()
                                handled = True
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                if scrollbar_rect:
                    new_y = min(max(event.pos[1] - drag_offset, scrollbar_rect.top),
                                scrollbar_rect.bottom - thumb_rect.height)
                    ratio = (new_y - scrollbar_rect.top) / (scrollbar_rect.height - thumb_rect.height)
                    content_h = len(CREW_DATA) * (CREW_ITEM_HEIGHT + CREW_SPACING) - CREW_SPACING
                    view_h = HEIGHT - 40
                    max_scroll = min(0, view_h - content_h)
                    scroll_offset = -ratio * (content_h - view_h)

        screen.fill(BG_COLOR)
        if active_section == 0:
            draw_ship_section()
        elif active_section == 1:
            thumb_rect, scrollbar_rect = draw_crew_section()
        else:
            draw_navigation_section()
        draw_right_panel(mouse_pos)
        if active_section == 2:
            draw_navigation_panel()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()