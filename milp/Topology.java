

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;


public class Topology {
	static final double eps = 1.0e-7;
	static final double threshold = 0.000063095734448;
	
	private double xmax; // Area width
	private double ymax; // Area height
	private Double[] h; // Set of possible altitudes for drones
	private double tau;
	private int B;
	
	Set<Position> positions = new HashSet<Position>();
	Set<Drone> drones = new HashSet<Drone>();
	Set<Sensor> sensors = new HashSet<Sensor>();
	
	Map<Position, Map<Sensor, Double>> Prx = new HashMap<Position, Map<Sensor, Double>>();
	Map<Position, Map<Sensor, Double>> Ph = new HashMap<Position, Map<Sensor, Double>>();
	
	
	public Topology(double xmax, double ymax, Double[] alt, int nbs, int u, int m, double tau) {
		this.xmax = xmax;
		this.ymax = ymax;
		h = alt;
		B = m;
		this.tau = tau;
		this.setDrones();
		this.setSensors(nbs);
		this.setRegularPositions(u);
		this.setSensorCost();
		this.setPrx();
		this.setPh();
		this.setPositionCost();
	}
	
	public double getTau() {
		return tau;
	}
	
	public int getB() {
		return B;
	}
	
	/* ************************************************************************************
	 * ************************************************************************************
	 */
	
	public void setDrones() {
		for (int i=0; i< B; i++) {
			Drone temp = new Drone(""+i);
			drones.add(temp);
		}
	}
	
	
	public void setSensors(int s) {
		// Generate Target positions randomly on the area
		for (int i=0; i<s; i++) {
			sensors.add(new Sensor(Math.random()*xmax, Math.random()*ymax, i + ""));
		}
	}
	
	// Generate regular possible locations for drones
	public void setRegularPositions(int nb_positions) {		
		// Divide the area into regular squares and place a possible location at the center of each square
		for (int i=0; i<nb_positions; i++) {
			for (int j=0; j<nb_positions; j++) {
				double xtemp = (i+1)*xmax/(nb_positions+1);
				double ytemp = (j+1)*ymax/(nb_positions+1);
				// For each possible altitude, add a location
				for (Double htemp : h) 
					positions.add(new Position(xtemp, ytemp, htemp, "P"+i+"_"+j+"_"+htemp.toString().substring(0, htemp.toString().indexOf("."))));
			}
			
		}
	}
	
	public void setRandomSensorCost() {
		// Random priority
		for (Sensor i : sensors) {
			i.setCost((Math.random()*0.01+threshold)*120); // 2 minutes of random harvested power
			//System.out.println(i.getCost());
		}
	}
	
	public void setSensorCost() {
		// Random priority
		for (Sensor i : sensors) {
			i.setCost(0.15); // 150 mJ for all the nodes
			//System.out.println(i.getCost());
		}
	}
	
	public void setPositionCost() {
		// sum_i C_i * Phi
		for (Position j : positions) {
			double cj = 0.0;
			Map<Sensor, Double> Phj = Ph.get(j);
			for (Sensor i : Phj.keySet())
				if (Phj.get(i) > threshold)
					cj += (i.getCost() * Phj.get(i));
			j.setCost(cj);
		}
	}
	
	public void setPrx() {
		for (Position j : positions) {
			Map<Sensor, Double> Prxj = new HashMap<Sensor, Double>();
			for (Sensor i : sensors) {
				Prxj.put(i, receivedPower(j, i));
			}
			Prx.put(j, Prxj);
		}
	}
	
	
	public void setPh() {
		for (Position j : positions) {
			Map<Sensor, Double> Phj = new HashMap<Sensor, Double>();
			for (Sensor i : sensors) {
				double phi = Prx.get(j).get(i)*harvestGain(j, i);
				//System.out.println("Position "+j.getName()+" Sensor "+i.getName()+" Ph = "+phi);
				if (phi > 0.01) {
					Phj.put(i, 0.01);
					//System.err.println("Position "+j.getName()+" Sensor "+i.getName()+" Ph = "+phi);
				}
				else if (phi < threshold)
					Phj.put(i, 0.0);
				else
					Phj.put(i, phi);
				
				
			}
			Ph.put(j, Phj);
		}
		//System.exit(0);
	}
	
	// Print in file the generated topology
	public void printTopo(String f) throws IOException {
		FileWriter output = new FileWriter(f);
        BufferedWriter wout = new BufferedWriter(output);
        
        for (Drone d : drones) {
        	wout.write(d.toString()+"\n");
        }
        
        for (Sensor i: sensors) {
        	wout.write(i.toString()+"\n");
        }
        for (Position j: positions) {
        	wout.write(j.toString()+"\n");
        }
		
		wout.close();
		output.close();
	}
	
	public String toString() {
		String res="";
        for (Drone d : drones) {
        	res += d.toString()+"\n";
        }
        
        for (Sensor t: sensors) {
        	res += t.toString()+"\n";
        }
        for (Position d: positions) {
        	res += d.toString()+"\n";
        }
		
		return res;
	}
	
	
	/* ************************************************************************************
	 * ************************************************************************************
	 */
	
	// HARVESTING MODEL
		public double receivedPower(Position j, Sensor i) {
			double P0 = 10;
			double Grx = 6;
			double lambda = 3*Math.pow(10, 8)/915000000;
			Grx = Math.pow(10, Grx/10);
			double P1 = P0*Grx*Math.pow((lambda/(4*Math.PI*1)), 2);
			double G = Math.abs(new Random().nextGaussian());
			double sigma = 0.01;
			double I = P1*Math.exp(2*sigma*G)/Math.pow(j.getDistance(i), 2);
			return I;
		}
		
		
		public double harvestGain(Position j, Sensor i) {
			double x = Prx.get(j).get(i) * 1000;
			double y = 0.52;
			if (x < 0.04)
				y = 0;
			else if ((x >= 0.04) && (x < 0.08))
				y = Math.exp(-Math.pow(x-1.114, 28));
			else if ((x >= 0.08) && (x < 0.2))
				y = Math.pow(x-0.078, 0.5) * Math.pow(1.38-x, 2.1);
			else if ((x>= 0.2) && (x < 0.35))
				y = Math.exp(-Math.pow(x-0.32, 2)/Math.pow(0.35, 2))/1.795;
			else if ((x >= 0.35) && (x < 0.6))
				y = Math.exp(-Math.pow(x-0.32, 2)/Math.pow(1.1, 2))/1.795;
			else if ((x >= 0.6) && (x < 0.8))
				y = Math.pow(1.7, Math.pow(x-0.7,2)) - 0.48;
			else if ((x >= 0.8) && (x < 2.5))
				y = Math.exp(-Math.pow(x-2.5, 2)/Math.pow(3.75, 2))/1.555;
			else if ((x >= 2.5) && (x <= 10))
				y = Math.exp(-Math.pow(x-2.5, 2)/Math.pow(17, 2))/1.555;
			
			return y;
		}
		
		
		
		/* ************************************************************************************
		 * ************************************************************************************
		 */
}
