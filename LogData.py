import Adafruit_BMP.BMP085 as BMP085
from Adafruit_I2C import Adafruit_I2C
from Adafruit_LSM303.py import * 
import time
import datetime
import gps

""" 

Revision 1.0: 5/4/15: Basic datalogging to print pressure, alt, temp and time. 
	TODO: add GPS loc, speed, etc. at time as well as accelerometer at the time. 

Revision 1.2: 5/5/15: Added GPS logging 
    TODO: add accelerometer data at the time. 

"""

if __name__ == '__main__':
    #Balloon monitoring/logging data app 
    
    sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
     
    temp = sensor.read_temperature()
    pressure = sensor.read_pressure()
    altitude = sensor.read_altitude()
    lsm = Adafruit_LSM303()
    # log data: http://www.instructables.com/id/Raspberry-Pi-Temperature-Logger/

    print("Balloon Data Logger\n")
    
    readingNum = 1
    
    while True:
        readingNum += 1
        try: 
            report = session.next()
            print report 
            #if report['class'] == 'TPV':
            #    if hasattr(report, 'time'):
            #        print report.time
        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print "GPSD has terminated"
        with open("datalog.txt", "a") as myFile:
            now = datetime.datetime.now()
            #add all data together
            outvalue =  "Temperature: %.2f C" % temp + " Pressure:    %.2f hPa" % (pressure / 100.0) + "Altitude:    %.2f" % altitude + "\n"
            outstring = "Reading #: " + "%i" % readingNum + ": " + str(outvalue)
            print outstring
            myFile.write(outstring)
        print '[(Accelerometer X, Y, Z), (Magnetometer X, Y, Z, orientation)]'
        print lsm.read()
        #log temperature every 60 seconds
        time.sleep(10)
    