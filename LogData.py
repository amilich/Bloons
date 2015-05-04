import Adafruit_BMP.BMP085 as BMP085
import time
import datetime

""" 

Revision 1.0: 5/4/15: Basic datalogging to print pressure, alt, temp and time. 
	TODO: add GPS loc, speed, etc. at time as well as accelerometer at the time. 

"""

#Balloon monitoring/logging data app 

sensor = BMP085.BMP085()
 
# From Adafruit example: 
# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode
 
temp = sensor.read_temperature()
pressure = sensor.read_pressure()
altitude = sensor.read_altitude()
 
print "Temperature: %.2f C" % temp
print "Pressure:    %.2f hPa" % (pressure / 100.0)
print "Altitude:    %.2f" % altitude

# log data: http://www.instructables.com/id/Raspberry-Pi-Temperature-Logger/

print("Balloon Data Logger\n")

readingNum = 1

while True:
    readingNum += 1
    with open("datalog.txt", "a") as myFile:
        now = datetime.datetime.now()
        #add all data together
        outvalue =  "Temperature: %.2f C" % temp + " Pressure:    %.2f hPa" % (pressure / 100.0) + "Altitude:    %.2f" % altitude + "\n"
        outstring = "Reading #: " + "%i" % readingNum + ": " + str(outvalue)
        print outstring
        myFile.write(outstring)

    #log temperature every 60 seconds
    time.sleep(10)
    
