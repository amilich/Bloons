import Adafruit_BMP085.BMP085 as BMP085
import smbus
import time
import datetime

""" 

Revision 1.0: 5/4/15: Basic datalogging to print pressure, alt, temp and time. 
	TODO: add GPS loc, speed, etc. at time as well as accelerometer at the time. 

"""

#Balloon monitoring/logging data app 

bmp = BMP085(0x77)
 
# From Adafruit example: 
# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode
 
temp = bmp.readTemperature()
pressure = bmp.readPressure()
altitude = bmp.readAltitude()
 
print "Temperature: %.2f C" % temp
print "Pressure:    %.2f hPa" % (pressure / 100.0)
print "Altitude:    %.2f" % altitude

# log data: http://www.instructables.com/id/Raspberry-Pi-Temperature-Logger/

print("Balloon Data Logger\n")

while True:
    f=open('datalog.txt','a') #read/write to file 
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y/%m/%d %H:%M")
    #add all data together
    outvalue =  "Temperature: %.2f C" % temp + " Pressure:    %.2f hPa" % (pressure / 100.0) + "Altitude:    %.2f" % altitude
    outstring = str(timestamp)+"  "+str(outvalue)
    print outstring
    f.write(outstring)
    f.close()

    #log temperature every 60 seconds
    time.sleep(60)
    
