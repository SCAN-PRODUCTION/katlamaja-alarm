# Katlamaja alarm
# Versioon: 1.1
# SCAN PRODUCTION OÜ

import serial
import time
import RPi.GPIO as GPIO

# Seadistan serial porti ja baud rate SIM7600 mooduli jaoks.
port = '/dev/ttyUSB0'
baud = 115200

# Seadistan numbri, kuhu helistada
phone_number = "Sisesta number siia"

# Määran SIM7600 mooduli RX ja TX pinid
rx_pin = 26
tx_pin = 19

# Seadistan debounce time sisendsignaali jaoks
debounce_time = 0.5

# Käivitan GPIO library
GPIO.setmode(GPIO.BCM)

# Seadistan RX ja TX pins sisenditeks
GPIO.setup(rx_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(tx_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Avan serial porti, et ühenduda SIM7600 mooduliga
ser = serial.Serial(port, baud, timeout=5)

# Seadistan booleani, kas alarm on käivitatud või mitte.
alarm_triggered = False

# Jätkan sisendi kontrollimist SIM7600 mooduli RX pinil.
while True:
    # Loen signaali RX pinil.
    signal = GPIO.input(rx_pin)

    # Kontrollin, kas signaal on käivitatud pärast signaali kättesaamist RX pinilt.
    if signal == 0 and not alarm_triggered:
        # Määran booleani, et alarm on käivitatud.
        alarm_triggered = True

        # Jätkan pidevalt helistamist, kuni kõnele vastatakse.
        while True:
            # Saadan AT käsu, et teha kõne
            ser.write(f'ATD{phone_number};\r\n'.encode())

            # Ootan vastust SIM7600 moodulilt
            response = ser.readline().decode().strip()

            # Kontrollin kas kõnele vastati, või kõnest keelduti
            if "NO ANSWER" in response or "BUSY" in response or "NO CARRIER" in response:
                # Kõnele ei vastatud ja kõnest ei keeldutud, seega saame loopist välja
                break

            # Kõnele vastati, seega ootame signaali SIM7600 mooduli RX pinilt.
            while True:
                # Loen signaali RX-pinilt
                signal = GPIO.input(rx_pin)

                # Kontrollin kas kõnest keelduti
                if signal == 1:
                    # Kõnest keelduti, seega saame loopist välja
                    break

        # Lähtestan muutuja, mis näitab, et alarm on käivitatud.
        alarm_triggered = False

    # Ootan debounce aja enne signaali kontrollimist.
    time.sleep(debounce_time)

# Sulgen serial port.
ser.close()
