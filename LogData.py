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

Revision 1.4 (final): 5/14/15 (updated later)
    Added try except error catching. 

GitHub Repo: 
    https://www.github.com/amilich/Bloons

Must Run Before Can Use GPS:
    sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
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

        try:

            temp = sensor.read_temperature()
            pressure = sensor.read_pressure()
            altitude = sensor.read_altitude()

            LSM303_Output = lsm.read()
            accelerometerInfo=LSM303_Output[0]
            magnetometerInfo=LSM303_Output[1]

        except:
            temp = "Error"
            pressure = "Error"
            altitude = "Error"
            accelerometerInfo = "Error"
            magnetometerInfo = "Error"
        with open("datalog.txt", "a") as myFile:
            #add reading # and then temperature data 
            myFile.write("****** READING #" + str(readingNum) + " ******")
            myFile.write("****** TIME ELAPSED: %s seconds ******" % (time.time() - start_time))


            tempLine =  "Temperature: %.2f C" % temp + " Pressure: %.2f hPa" % (pressure / 100.0) + "Altitude: %.2f" % altitude
            accelLine= "Accelerometer X, Y, Z: " + str(accelerometerInfo)
            magLine = "Magnetometer X, Y, Z, orientation: " + str(magnetometerInfo)
            

            myFile.write(tempLine)
            myFile.write(accelLine)
            myFile.write(magLine)

            if printData: 
                print tempLine
                print accelLine
                print magLine

            #gps data
            try: 
                report = session.next() #update GPS 

                if hasattr(report, 'time'):
                    myFile.write("GPS Time: " + str(report.time))

                if hasattr(report, 'lat'):
                    myFile.write("GPS Lat: " + str(report.lat))

                if hasattr(report, 'lon'):
                    myFile.write("GPS Lon: " + str(report.lon))

                if hasattr(report, 'alt'):
                    myFile.write("GPS Alt: " + str(report.alt))

                if hasattr(report, 'climb'):
                    myFile.write("GPS Climb: " + str(report.climb))

                if hasattr(report, 'speed'):
                    myFile.write("GPS Speed: " + str(report.speed))


                if printData: 

                    if hasattr(report, 'time'):
                        print "GPS Time: " + str(report.time)

                    if hasattr(report, 'lat'):
                        print "GPS Lat: " + str(report.lat)

                    if hasattr(report, 'lon'):
                        print "GPS Lon: " + str(report.lon)

                    if hasattr(report, 'alt'):
                        print "GPS Alt: " + str(report.alt)

                    if hasattr(report, 'climb'):
                        print "GPS Climb: " + str(report.climb)

                    if hasattr(report, 'speed'):
                        print "GPS Speed: " + str(report.speed)

                    #print "\n"
                    #print "GPS Report: " + str(report)
                    #print "Report Attributes: " + str(dir(report))
                    print "\n \n"
            except KeyError:
                pass
            except KeyboardInterrupt:
                quit() #TODO: check this 
            except StopIteration:
                session = None
                if printData: 
                    print "GPSD has terminated"
                myFile.write("*** GPS FAIL ***")
    
            myFile.write("\n \n") #clean data with newline 

        time.sleep(2) #sleep for 2s - this may be causing i2c problems?
            #no errors for time.sleep(5) 
    