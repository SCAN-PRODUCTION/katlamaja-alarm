# Katlamaja alarm
# Versioon: 1.0
# SCAN PRODUCTION OÜ

import RPi.GPIO as GPIO
import serial

# Jadapordi seadistamine GSM-mooduliga suhtlemiseks.
ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate = 9600,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

# Seadistan GPIO pini alarmi signaali saamiseks
signal_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(signal_pin, GPIO.IN)

# Telefoninumber, kuhu sõnum saata
phone_number = '+37200000000'

# SMS teksti sisu
sms_text = 'Katlamaja alarm'

# Kontrollin pidevalt turvasüsteemi signaali
while True:
    if GPIO.input(signal_pin):
        # Saadan sõnumi SMS-mooduli abil
        ser.write('AT+CMGS="{}"\r\n'.format(phone_number).encode())
        ser.write('{}\r\n'.format(sms_text).encode())
        ser.write(bytes([26]))
