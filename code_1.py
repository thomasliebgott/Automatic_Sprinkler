import RPi.GPIO as GPIO
import time
import smbus
import datetime
import tkinter as tk
import threading

# Get I2C bus
bus = smbus.SMBus(1)
time.sleep(0.5)

v = False #test temperature boolean

#Pin setup 
btnOnPompe = 16
btnStopPompe = 10
btnStopLumiere = 18
ledRouge = 19
onRelayLumiere = 36
onRelayPompe = 38
ledJaune = 32
ledbleu = 37
ledVerte = 24
detectIR = 8 #detection IR

GPIO.setwarnings(False)

#setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(btnOnPompe, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(btnStopPompe, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(ledRouge, GPIO.OUT)
GPIO.setup(onRelayLumiere, GPIO.OUT)
GPIO.setup(onRelayPompe, GPIO.OUT)
GPIO.setup(ledVerte, GPIO.OUT)
GPIO.setup(ledbleu, GPIO.OUT)
GPIO.setup(ledJaune, GPIO.OUT)
GPIO.setup(detectIR, GPIO.IN)
GPIO.setup(btnStopLumiere, GPIO.IN , pull_up_down = GPIO.PUD_DOWN)


    
    
    
