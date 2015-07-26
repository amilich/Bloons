import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.FileWriter; 


public class Trim {
  public static void main(String[] args){
    try(BufferedReader br = new BufferedReader(new FileReader("/Users/Andrew/Downloads/datalog.txt"))) {
      int count = 0; 
	  FileWriter fw = new FileWriter("cleaned.txt");

      for(String line; (line = br.readLine()) != null; ) {
        String[] everything = line.split(" ");
        String alt = ""; 
        for (int ii = 0; ii < everything.length; ii++) {
          if(everything[ii].contains("Temperature") && !everything[ii].contains("asdf")){
            alt = /*everything[ii] +*/ everything[ii+1]; 
          }
        }
        if(alt.equals(""))
          continue; 
        if(!line.toLowerCase().contains("error"))//Double.parseDouble(alt) != -1. && Double.parseDouble(alt) != -0.01)
          fw.write(line + "\n"); 
          count ++; 
      }



      System.out.println();
	  fw.close();
      //System.out.println(count);
      // line is not visible here.
    } catch (FileNotFoundException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }


	try(BufferedReader br = new BufferedReader(new FileReader("/Users/Andrew/Downloads/cleaned.txt"))) {
	  int count = 0; 
	  int accelCount = 0; 

	  for(String line; (line = br.readLine()) != null; ) {
	    String[] everything = line.split(" ");
	    String alt = ""; 
		String temp = ""; 
		String pres = ""; 
		double altitude = 0; 
		double pressure = 0; 
		double temperature = 0; 
		String accelData = ""; 
	    for (int ii = 0; ii < everything.length; ii++) {
	      if(everything[ii].contains("Accelerometer") && !everything[ii].contains("GPS")){
	        temp = /*everything[ii] +*/ everything[ii+1]; 
			//temperature = Double.parseDouble(temp); 
			double accelX = 0; 
			double accelY = 0; 
			double accelZ = 0; 
			
			try{
				
				accelX = Double.parseDouble(everything[ii+4].substring(1, everything[ii+4].length()-1)); 
				accelY = Double.parseDouble(everything[ii+5].substring(0, everything[ii+5].length()-1)); 
				accelZ = Double.parseDouble(everything[ii+6].substring(0, everything[ii+6].length()-2)); 
			}
			catch(Exception e){
				//e.printStackTrace(); 
			}
			if(accelX + accelY + accelZ != 0){
				accelData += everything[ii+4];
				accelData += everything[ii+5];
				accelData += everything[ii+6];
			}
	        //System.out.println(accelData.substring(1, accelData.length()-1));
			if(accelData.length() != 0){
				System.out.println(accelCount + "," + accelData.substring(1, accelData.length()-1)); 
				accelCount ++; 
			}
			//count ++;  
	      }
		  if(everything[ii].contains("Altitude") && !everything[ii].contains("GPS")){
		        alt = /*everything[ii] +*/ everything[ii+1]; 
				altitude = Double.parseDouble(alt); 
		        //System.out.println(alt);
				//count ++;  
		  }
		  if(everything[ii].contains("Pressure") && !everything[ii].contains("GPS")){
			    pres = /*everything[ii] +*/ everything[ii+1]; 
				pressure = Double.parseDouble(pres);//*0.750061683; 
			      //System.out.println(pressure);
					//count ++;  
		  }
		  //altitude = -(1.38*Math.pow(10, -23))*temperature*Math.log(pressure/(731.160128))/(9.81*28.97); 
		  //System.out.println(altitude);
	    }
	  }
	  System.out.println();
	  //System.out.println(count);
	  // line is not visible here.
	} catch (FileNotFoundException e) {
	  // TODO Auto-generated catch block
	  e.printStackTrace();
	} catch (IOException e) {
	  // TODO Auto-generated catch block
	  e.printStackTrace();
	}
  }
}
