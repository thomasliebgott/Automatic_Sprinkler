import RPi.GPIO as GPIO
import time
import smbus
import datetime


# Get I2C bus
bus = smbus.SMBus(1)
time.sleep(0.5)

v = False #test temperature boolean

#Pin setup 
ty = 12
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

#function 
def returnDate():
    x = datetime.datetime.now()
    time.sleep(1)
    return x 

def detectionLumiere():
    GPIO.setup(detectIR, GPIO.IN)
    dateAndHour = returnDate()
    dateAndHour= str(dateAndHour)
    month = dateAndHour[5:7]
    hour = dateAndHour[11:16]

    print(dateAndHour)
    print(month)
    print(hour)
    
    if GPIO.input(detectIR):
        if (hour > "15:00"):
            #allumage lampe detecteur
            #if (stopLumiere == 0):
            #allumage lampe detecteur
            print("Motion detected!")
            #allumange lumineres 
            GPIO.output(onRelayLumiere,GPIO.LOW)
            GPIO.output(ledJaune,GPIO.HIGH)
            time.sleep(120)
            GPIO.output(onRelayLumiere,GPIO.HIGH)
            GPIO.output(ledJaune,GPIO.LOW)

def arrosageRegu():
    GPIO.output(ledVerte,GPIO.HIGH)
    GPIO.output(onRelayPompe,GPIO.HIGH)
    time.sleep(tempAros)
    GPIO.output(ledVerte,GPIO.LOW)
    GPIO.output(onRelayPompe,GPIO.LOW)

#variable
c = 0
tempAros = 2000  
stop = False

while True:
    #init values 
    GPIO.output(onRelayPompe,GPIO.HIGH)
    print("boucle loop")
    
    #verification du code bouton avec allumage des Leds 
    bOnPompeEtat = GPIO.input(btnOnPompe)
    bStopPompeEtat = GPIO.input(btnStopPompe)
    bStopLumiereEtat = GPIO.input(btnStopLumiere)
    
    GPIO.output(onRelayLumiere,GPIO.HIGH)

    # capteur de temp
    data = bus.read_i2c_block_data(0x18, 0x05, 2)
    # Conversion des data en 13-bits
    ctemp = ((data[0] & 0x1F) * 256) + data[1]
    if ctemp > 4095 :
            ctemp -= 8192
    ctemp = ctemp * 0.0625
    print ("Temperature in Celsius is    : %.2f C" %ctemp)
    # verif validation temp
    if (ctemp > 8):
        v = True
    
    dateAndHour = returnDate()
    dateAndHour= str(dateAndHour)
    month = dateAndHour[5:7]
    hour = dateAndHour[11:16]

    print(dateAndHour)
    print(month)
    print(hour)

    detectionLumiere() 
  
    #Mai Juin
    if(month == "05" or month == "06" and ctemp > 0):
        if(hour == "04:00"):
            arrosageRegu()

    #Juillet aout 
    if(month == "07" or month == "08" and ctemp > 0):
        c += 1 
        if(hour == "04:00" and c == 1):
            arrosageRegu()
        if(hour == "23:00" and c == 1):
            arrosageRegu()
            c = 0
            
    #Septembre
    if(month == "09" and ctemp > 0 ):
        c += 1 
        if(hour == "04:00" and c == 2):
            arrosageRegu()
            c = 0
        
    #button On press
    if(bOnPompeEtat == 0 and ctemp > 0):
        go = True
        while(go == True):
            GPIO.output(ledVerte,GPIO.HIGH)
            GPIO.output(onRelayPompe,GPIO.LOW)
            print("bt on")
            detectionLumiere()
            bOnPompeEtat = GPIO.input(btnOnPompe)
            time.sleep(0.25)
            if(bOnPompeEtat == 1):
                GPIO.output(ledVerte,GPIO.LOW)
                GPIO.output(onRelayPompe,GPIO.HIGH)
                print("bt on out")
                time.sleep(0.25)
                break

    
    if(bStopPompeEtat == 0):
        stop = True
        GPIO.output(ledRouge,GPIO.HIGH)  
        while(stop == True):
            bStopPompeEtat = GPIO.input(btnStopPompe)
            GPIO.output(ledVerte,GPIO.LOW)
            GPIO.output(onRelayPompe,GPIO.HIGH)
            detectionLumiere()
            print("bt stop stop")
            time.sleep(0.25)
            if(bStopPompeEtat == 1):
                GPIO.output(ledRouge,GPIO.LOW)
                print("bt stop pompe out")
                time.sleep(0.25)
                break
        
    #GPIO.output(OffSystem,GPIO.LOW)   #garder bouton stop en off 
        
    while(bStopLumiereEtat == 0):
        GPIO.output(onRelayLumiere,GPIO.LOW)
        GPIO.output(ledJaune,GPIO.HIGH)
        bStopLumiereEtat = GPIO.input(btnStopLumiere)
        print("bt stop lumiere ")
        time.sleep(0.25)
    GPIO.output(ledJaune,GPIO.LOW)
    time.sleep(0.25)
        
    
    
    
