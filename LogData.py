import Adafruit_BMP.BMP085 as BMP085
from Adafruit_I2C import Adafruit_I2C
from Adafruit_LSM303 import * 
import time
import datetime
import gps

""" 

Revision 1.0: 5/4/15: Basic datalogging to print pressure, alt, temp and time. 
	TODO: add GPS loc, speed, etc. at time as well as accelerometer at the time. 

Revision 1.2: 5/5/15: Added GPS logging 
    TODO: add accelerometer data at the time. 

Revision 1.3: 5/6/15: New logging 
    TODO: test GPS 

GitHub Repo: 
    https://www.github.com/amilich/Bloons

"""

# Log data: http://www.instructables.com/id/Raspberry-Pi-Temperature-Logger/
# GPS tutorial: https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/using-your-gps

printData = True 

if __name__ == '__main__':
    #Balloon monitoring/logging data app 
    
    #initialize sensors
    sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)
    lsm = Adafruit_LSM303()
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    print("Balloon Data Logger\n")

    with open("datalog.txt", "a") as myFile:
        myFile = open("datalog.txt", "a")
        myFile.write("Initializing Data Logger")

    #if we don't have the current time, we can estimate it based on the number of readings and 
    #the python time module 
    readingNum = 0
    start_time = time.time()

    while True:
        readingNum += 1

        #update temperature readings 
        temp = sensor.read_temperature()
        pressure = sensor.read_pressure()
        altitude = sensor.read_altitude()

        with open("datalog.txt", "a") as myFile:
            #add reading # and then temperature data 
            myFile.write("****** READING #" + str(readingNum) + " ******")
            myFile.write("****** TIME ELAPSED: %s seconds ******" % (time.time() - start_time))


            tempLine =  "Temperature: %.2f C" % temp + " Pressure: %.2f hPa" % (pressure / 100.0) + "Altitude: %.2f" % altitude + "\n"
            
            myFile.write(tempLine)
            myFile.write("(Accel X,Y,Z), (Magnetometer X, Y, Z, orient)")
            myFile.write(str(lsm.read()).strip('[]'))

            if printData: 
                print tempLine
                print "[(Accelerometer X, Y, Z), (Magnetometer X, Y, Z, orientation)]"
                print str(lsm.read()).strip('[]')

            #gps data
            try: 
                report = session.next() #update GPS 
                if printData: 
                    print type(report)
                    print report
                myFile.write("GPS Report: ")
                #myFile.write(report)
            except KeyError:
                pass
            except KeyboardInterrupt:
                quit() #TODO: check this 
            except StopIteration:
                session = None
                if printData: 
                    print "GPSD has terminated"
                myFile.write("*** GPS FAIL ***")
    
            myFile.write("\n") #clean data with newline 

        time.sleep(10) #sleep for 10s
    