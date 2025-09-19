#include <SoftwareSerial.h>
#include <EEPROM.h>
#include <avr/wdt.h>   

//
// Пины
//
const uint8_t BTN = A0;   
const uint8_t P10 = 9;
const uint8_t P9  = 10;
const uint8_t P8  = 8;   
const uint8_t P7  = 7;   

//
// Тайминги
//
const unsigned long T_TOTAL = 5500;  
const unsigned long T_P9    = 500;  
const unsigned long DEBOUNCE_MS = 25;

//
// 
//
SoftwareSerial Master(4, 11);

//
// Состояния
//
enum Phase { PH_IDLE, PH_ACTIVE };
Phase phase = PH_IDLE;

unsigned long tStart = 0;
bool p9Released = false;

bool btnStable = false, btnPrev = false;
unsigned long tEdge = 0;

// какой из (P8|P7) использовать в СЛЕДУЮЩЕМ запуске по кнопке.
// Храним в EEPROM по адресу 0: 1 = P8, 0 = P7
bool nextUseP8 = true;

// кто запустил: кнопка (чередуем) или команда (не чередуем)
bool lastStartedByButton = false;

void setAllHigh() {
  digitalWrite(P10, HIGH);
  digitalWrite(P9,  HIGH);
  digitalWrite(P8,  HIGH);
  digitalWrite(P7,  HIGH);
}

void drainSerial() { while (Master.available()) Master.read(); }

void updateButton() {
  bool raw = (digitalRead(BTN) == LOW); // LOW = нажата
  unsigned long now = millis();
  if (raw != btnStable) {
    if (now - tEdge >= DEBOUNCE_MS) {
      btnStable = raw;
      tEdge = now;
    }
  } else {
    tEdge = now;
  }
}

void resetNow() {
  // Перезапуск через watchdog (~15 мс)
  wdt_enable(WDTO_15MS);
  while (true) { } // ждём reset
}

void startCycle(uint8_t pinAlt, bool byButton) {
  lastStartedByButton = byButton;
  p9Released = false;
  tStart = millis();
  phase = PH_ACTIVE;

  // старт: сразу LOW на D10 и выбранный (P8|P7), и LOW на P9
  digitalWrite(P10, LOW);
  digitalWrite(pinAlt, LOW);
  digitalWrite(P9, LOW);

  // Сохраним, какой альтернативный пин активен сейчас, в статике,
  // чтобы знать, что поднять по завершении.
  static uint8_t activePin = P8;
  activePin = pinAlt;

  // Привяжем его к локальной "форточке" через lambda:
  // (в конце цикла обратимся через getter)
  auto getActivePin = []() -> uint8_t {
    extern uint8_t __activePin_backdoor; return __activePin_backdoor;
  };

  if (getActivePin() == P8) {
    // Дверь открыта, отправляем A1 через пин 11
    Master.write('A'); Master.write('1');
  } else {
    // Дверь закрыта, отправляем A0 через пин 11
    Master.write('A'); Master.write('0');
  }
  delay(15);
}

// Хак-поле для getActivePin()
uint8_t __activePin_backdoor = P8; // инициализация не критична

// Обновим backdoor каждый старт
void __attribute__((always_inline)) setActivePin(uint8_t p) { __activePin_backdoor = p; }

void startCycle_wrap(uint8_t pinAlt, bool byButton) {
  setActivePin(pinAlt);
  startCycle(pinAlt, byButton);
}

uint8_t getActivePin() { return __activePin_backdoor; }

void finishCycleAndReset() {
  // Поднимаем всё в HIGH на момент перед reset
  digitalWrite(P10, HIGH);
  digitalWrite(getActivePin(), HIGH);
  digitalWrite(P9, HIGH);

  // Если старт был кнопкой — записываем в EEPROM, какой пин использовать в СЛЕДУЮЩИЙ раз
  if (lastStartedByButton) {
    bool newNext = (getActivePin() == P8) ? false : true; // если был P8, следующий P7; и наоборот
    EEPROM.update(0, newNext ? 1 : 0);
  }
  // Жёсткий перезапуск
  resetNow();
}

void setup() {
  wdt_disable();             // на всякий случай отключим WDT после загрузчика
  Master.begin(9600);
  Serial.begin(9600);

  pinMode(P10, OUTPUT);
  pinMode(P9,  OUTPUT);
  pinMode(P8,  OUTPUT);
  pinMode(P7,  OUTPUT);
  setAllHigh();

  pinMode(BTN, INPUT_PULLUP);
  btnStable = (digitalRead(BTN) == LOW);
  btnPrev   = btnStable;
  tEdge     = millis();

  // Загрузим направление чередования из EEPROM
  uint8_t v = EEPROM.read(0);
  nextUseP8 = (v == 0 || v == 1) ? (v == 1) : true; // по умолчанию P8
}

void loop() {
  unsigned long now = millis();
  updateButton();

  if (phase == PH_IDLE) {
    // --- запуск по кнопке (фронт) ---
    if (btnStable && !btnPrev) {
      startCycle_wrap(nextUseP8 ? P8 : P7, true);
    }
    btnPrev = btnStable;

    if (Master.available() >= 1) {
      char c = Master.read();
      if (c == 'A') {
        startCycle_wrap(nextUseP8 ? P8 : P7, true);
      }
      drainSerial();
    }
  } else { 
    drainSerial();

    if (!p9Released && (now - tStart >= T_P9)) {
      digitalWrite(P9, HIGH);
      p9Released = true;
    }

    // через 5.5 c завершаем и перезапускаем МК
    if (now - tStart >= T_TOTAL) {
      finishCycleAndReset();
      // дальше управление не дойдёт — будет reset
    }
  }
}
