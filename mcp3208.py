#!/usr/bin/python

#Einfaches Pythonscript zum Auslesen von 2 MCP3208-ADC-Wandlern (insgesamt 16 Kanäle) per SPI-Interface (NICHT GPIO!)
#Ich habe als Referenzspannung 3,3V, die per Spannungsteiler von max. 10V heruntergebrochen werden. 

import spidev
import time
import math

spi = spidev.SpiDev()

#Frequenz des SPI-Busses. Maximal 5000000, geht man drüber, kommen unsinnige Werte heraus.

herz = 5000000



def eformat(f, prec, exp_digits):
    s = "%.*e"%(prec, f)
    mantissa, exp = s.split('e')
    # add 1 to digits as 1 is taken by sign +/-
    return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))


while True:

  for s in range (2):
     spi.open(0,s)  # öffnen des einen oder anderen MCP3208 
     spi.max_speed_hz=(herz)
     for c in range (8):
       #Bestimmung des Kommandos zum Empfangen der einzelnen Kanäle. Siehe dazu auch https://github.com/xaratustrah/rasdaq
       if c < 4:
          com1 = 0x06
          com2 = c * 0x40
       else: 
          com1 = 0x07
          com2 = (c-4) * 0x40
    
       antwort = spi.xfer([com1, com2, 0])


       val = ((antwort[1] << 8) + antwort[2])  # Interpretieren der Antwort
       val = int(val)
       u = val * 0.002441406                   # Umrechnen in Spannung: (10V/2¹²)
       u = round (u,2)
       print (str(u) + ' ', end="")
     spi.close() 
     if s == 1:
       print (' ')
