

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ParseResultsFromFile {

	public static void main(String[] args) throws Exception {
		File rep = new File("./data/oerpmin/150mJtemp/");
		File[] fichiers = rep.listFiles();
		//File[] fichiers = {new File("./data/oerpmin/results/resMin_10_10_125_5.txt")};
		
		String statFile = "./data/oerpmin/detailedStatsFile.txt";
		FileWriter output = new FileWriter(statFile);
        BufferedWriter wout = new BufferedWriter(output);
        wout.write("0LP1G\t#D\t #S\t #P\t #it\t obj\t rTime\t nbDused\t maxLocTime\t minLocTime\t meanLocTime\t maxPos\t minPos\t minPosNotNull\t meanNbPos\t maxAlt\t minAlt\t meanAlt\n");
		
		for (int i=0; i<fichiers.length; i++) {
			Scanner f = new Scanner(fichiers[i]);
			// Recup #D #N #P
			String fName = fichiers[i].getName();
			System.out.println(fName);
			fName = fName.substring(fName.indexOf("_")+1);
			int d = new Integer(fName.substring(0, fName.indexOf("_")));
			fName = fName.substring(fName.indexOf("_")+1);
			int s = new Integer(fName.substring(0, fName.indexOf("_")));
			fName = fName.substring(fName.indexOf("_")+1);
			int np = new Integer(fName.substring(0, fName.indexOf("_")));
			fName = fName.substring(fName.indexOf("_")+1);
			int it = new Integer(fName.substring(0, fName.indexOf(".")));
			
			
			int type = 0;
			double obj = 0.0;
			double time = 0.0; // in ms
			
			// Construct drones with associated positions
			List<Drone> drones = new ArrayList<Drone>();
			
			
			while(f.hasNextLine()) {
				Scanner l = new Scanner(f.nextLine());
				l.useDelimiter(" ");
				
				if (l.hasNext()) {
					String current = l.next();
					switch (current) {
					case "Greedy": type = 1; break;
					case "Obj": 
						l.next(); 
						obj = new Double(l.next()); 
						while (l.hasNext()) {
							String c = l.next();
							if (c.equals("time")) {
								l.next();
								time = new Double(l.next());
							}
						}
						break;
					case "Drone": 
						Drone n = new Drone(l.next());
						drones.add(n);
						break;
					case "located":
						while (l.hasNext()) {
							String element = l.next();
							if (element.startsWith("P")) {
								double alt = new Double(element.substring(element.indexOf("_")+1));
								l.next();l.next();l.next();l.next();l.next();
								double tp = new Double(l.next());
								Position p = new Position(0, 0, alt, element);
								drones.get(drones.size()-1).addPosition(p, tp);
							}
						}
						break;
					}
				
				}
				
			}
			
			/*System.out.println(obj+" "+time);
			for (Drone n : drones)
				System.out.println(n);*/
			
			// Location time
			double minLoc = 3600.0;
			double maxLoc = 0.0;
			double meanLoc = 0.0;
			for (Drone n : drones) {
				for (Position p : n.getPos().keySet()) {
					if (n.getPos().get(p) > maxLoc)
						maxLoc = n.getPos().get(p);
					if (n.getPos().get(p) < minLoc)
						minLoc = n.getPos().get(p);
					meanLoc += n.getPos().get(p);
				}
			}
			
			
			// Positions
			int minPos = 10;
			int minPosNN = 10;
			int maxPos = 0;
			int nbPos = 0;
			double nbD = 0.0;
			double meanPos = 0.0;
			for (Drone n : drones) {
				int nnp = n.getPos().keySet().size();
				nbPos += nnp;
				if (nnp == 0)
					minPos = nnp;
				if (nnp < minPosNN && nnp > 0)
					minPosNN = nnp;
				if (nnp > maxPos)
					maxPos = nnp;
				if (minPos > 0 && minPos > minPosNN)
					minPos = minPosNN;
				if (n.getPos().keySet().size() > 0)
					nbD += 1.0;	
			}
			
			meanPos = nbPos / nbD;
			//System.out.println(meanPos+" "+nbPos+" "+nbD);
			//System.exit(0);
			meanLoc /= nbPos;
			
			// Altitude
			double minAlt = 5.0;
			double maxAlt = 0.0;
			double meanAlt = 0.0;
			for (Drone n : drones) {
				for (Position p : n.getPos().keySet()) {
					if (p.getH() > maxAlt)
						maxAlt = p.getH();
					if (p.getH() < minAlt)
						minAlt = p.getH();
					meanAlt += p.getH();
				}
			}
			meanAlt /= nbPos;
			
			wout.write(type+"\t"+d+"\t"+s+"\t"+np+"\t"+it+"\t"+obj+"\t"+time+"\t"+nbD+"\t"+maxLoc+"\t"+minLoc+"\t"+meanLoc+"\t"+maxPos+"\t"+minPos+"\t"+minPosNN+"\t"+meanPos+"\t"+maxAlt+"\t"+minAlt+"\t"+meanAlt+"\n");			
			
			
		}

		wout.close();
		output.close();
		
	}

}
