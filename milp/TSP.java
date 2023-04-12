

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import ilog.concert.IloException;


public class TSP {
	private double[][] distances;
	private double[][] times;
	private Map<Position, Integer> posId;
	private OERPmin m;
	Position g = new Position(0.0, 0.0, 0.0, "bs");
	
	
	public TSP(OERPmin res) {
		m = res;
		distances = new double[m.g.positions.size()+1][m.g.positions.size()+1];
		times = new double[m.g.positions.size()+1][m.g.positions.size()+1];
		posId = new HashMap<Position, Integer>();
		posId.put(g, 0);
		int c=1;
		for (Position p : m.g.positions) {
			posId.put(p, c);
			c++;
		}
	}
	
	private void setDistances() {
		for (Position p : m.g.positions) {
			distances[0][posId.get(p)] = p.getDistance(g);
			distances[posId.get(p)][0] = p.getDistance(g);
			for (Position p2 : m.g.positions)
				distances[posId.get(p)][posId.get(p2)] = p.getDistance(p2);
		}
	}
	
	private void setTimes() {
		for (Position p : m.g.positions) {
			times[0][posId.get(p)] = p.getDistance(g)/10.2;
			times[posId.get(p)][0] = p.getDistance(g)/10.2;
			for (Position p2 : m.g.positions)
				times[posId.get(p)][posId.get(p2)] = p.getDistance(p2)/10.2;
		}
	}
	
	// Récupérer les données de OERPmin
	
	
	public static void main(String[] args) throws IloException, IOException{
		// INPUT values for topology
		double x=50, y=50; // Size of area
		Double[] h = {1.0, 2.0, 3.0, 4.0, 5.0}; // Possible altitudes
		double tau = 3600.0;
		int s=15, u=7; // #N = t, #P = u*u*|h|
		int maxP = 3; // Max number of available drones
		double time_limit = 1000;
		for(maxP = 3; maxP <=10;maxP++) {
			String dir= "D:\\dev\\d"+maxP+"_s"+s+"_p"+u;
			File f1 = new File(dir); 
			f1.mkdirs();
			for( int i = 0; i<100; i++) {
				Topology m = new Topology(x, y, h, s, u, maxP, tau);
				String resFile = "D:\\dev\\d"+maxP+"_s"+s+"_p"+u+"\\"  + i +".txt";
				long OERPminTime = System.currentTimeMillis();
				OERPmin c1 = new OERPmin(m, 0.1, time_limit);
				if (c1.cplex.solve()) {
					OERPminTime = System.currentTimeMillis() - OERPminTime;
					if(OERPminTime/1000 < time_limit) c1.printResults(resFile, OERPminTime);
					else {
						i = i - 1;
					}
				}
			}
		}
//		TSP algo = new TSP(c1);
//		algo.setDistances();
//		algo.setTimes();
//		System.out.println(Arrays.toString(algo.distances[0]));
//		System.out.println(Arrays.toString(algo.times[0]));
	}
	
}
