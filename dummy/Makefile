PIO_ENV ?= esp32

.PHONY: default
default:
	platformio run

.PHONY: firmware
firmware:
	platformio run -e $(PIO_ENV) --target upload

.PHONY: spiffs
spiffs:
	platformio run --target uploadfs

.PHONY: monitor
monitor:
	platformio device monitor -b 115200

.PHONY: flash
flash: firmware monitor;

.PHONY: esp32-flash
esp32-flash: PIO_ENV=esp32
esp32-flash: firmware monitor;

.PHONY: esp8266-flash
esp8266-flash: PIO_ENV=esp8266
esp8266-flash: firmware monitor;

.PHONY: flashall
flashall: firmware spiffs monitor;

.PHONY: clean
clean:
	platformio run --target clean
