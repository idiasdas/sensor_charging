

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import ilog.concert.IloException;
import ilog.concert.IloLinearNumExpr;
import ilog.concert.IloNumVar;
import ilog.cplex.IloCplex;

public class OERPmin {
	static final double eps = 1.0e-7;
	static final double threshold = 0.000063095734448;
	double a;
	
	Topology g;
	IloCplex cplex;
	Map<Drone, IloNumVar> x = new HashMap<Drone, IloNumVar>();
	Map<Drone, Map<Position, IloNumVar>> y = new HashMap<Drone, Map<Position, IloNumVar>>();
	Map<Drone, Map<Position, IloNumVar>> t = new HashMap<Drone, Map<Position, IloNumVar>>();
	IloNumVar lambda1, lambda2;
	
	public OERPmin(Topology g, double a, double time_limit) throws IloException {
		// Init topology and power values
		this.g = g;
		this.a = a;
		
		// Init ILP
		cplex = new IloCplex();
		cplex.setParam(IloCplex.Param.TimeLimit, time_limit);
		//cplex.setWarning(null);
		//cplex.setOut(null);
		lambda1 = cplex.numVar(0, g.getTau(), "lambda1");
		lambda2 = cplex.numVar(0, g.positions.size()*g.drones.size(), "lambda2");
		for (Drone n : g.drones) {
			x.put(n, cplex.intVar(0, 1, "x_"+n.getName()));
			Map<Position, IloNumVar> tn = new HashMap<Position, IloNumVar>();
			Map<Position, IloNumVar> yn = new HashMap<Position, IloNumVar>();
			
			for (Position j : g.positions) {
				tn.put(j, cplex.numVar(0.0, g.getTau(), "t_"+n.getName()+"_"+j.getName()));
				yn.put(j, cplex.intVar(0, 1, "y_"+n.getName()+"_"+j.getName()));
			}			
			t.put(n, tn);
			y.put(n, yn);			
		}
		
		setObjective(a);
		setConstraints();		
	}
	
	public void setObjective(double a) throws IloException {
		for (Drone n : g.drones) {
			IloLinearNumExpr lCstrLeft = cplex.linearNumExpr(); // min max_n sum_j t^n_j
			IloLinearNumExpr posCstr = cplex.linearNumExpr(); // sum_j y^n_j <= lambda2			
			
			for (Position j : g.positions) {
				lCstrLeft.addTerm(1.0, t.get(n).get(j));
				posCstr.addTerm(1.0, y.get(n).get(j));
			}
			
			cplex.addLe(lCstrLeft, lambda1);
			cplex.addLe(posCstr, lambda2);
		}
		
		cplex.addMinimize(cplex.sum(cplex.prod(a, lambda1), cplex.prod(1.0-a, lambda2)));
	}
	
	public void setConstraints() throws IloException {
		IloLinearNumExpr budget = cplex.linearNumExpr();
		for (Drone n : g.drones) {
			// sum_n x_n <= B
			budget.addTerm(1.0, x.get(n));
			
			// sum_j t^n_j <= tau*x_n
			IloLinearNumExpr timeLeft = cplex.linearNumExpr();
			IloLinearNumExpr timeRight = cplex.linearNumExpr();
			timeRight.addTerm(g.getTau(), x.get(n));
			// sum_j y^n_j >= x_n
			IloLinearNumExpr unusedCstr = cplex.linearNumExpr();
			for (Position j : g.positions) {
				timeLeft.addTerm(1.0, t.get(n).get(j));
				
				IloLinearNumExpr tpCstrLeft = cplex.linearNumExpr();
				IloLinearNumExpr tpCstrRight = cplex.linearNumExpr(); // t^n_j <= tau y^n_j
				tpCstrLeft.addTerm(1.0, t.get(n).get(j));
				tpCstrRight.addTerm(g.getTau(), y.get(n).get(j));
				cplex.addLe(tpCstrLeft, tpCstrRight);
				
				unusedCstr.addTerm(1.0, y.get(n).get(j));
			}
			
			cplex.addLe(timeLeft, timeRight);
			cplex.addGe(unusedCstr, x.get(n));
			
		}
		cplex.addLe(budget, g.getB());
		
		for (Position j : g.positions) {
			IloLinearNumExpr altCstr = cplex.linearNumExpr(); // sum_n t^n_j + sum_j' sum_n' t^n'_j' <= lambda1
			
			for (Drone n : g.drones) {
				altCstr.addTerm(1.0, t.get(n).get(j));
			}
			
			for (Position j2 : g.positions) {
				if (!j.equals(j2) && Math.abs(j.getX()-j2.getX()) < eps && Math.abs(j.getY()-j2.getY()) < eps)
					for (Drone n : g.drones)
						altCstr.addTerm(1.0, t.get(n).get(j2));
			}
			
			cplex.addLe(altCstr, lambda1);
			
		}
		
		// y^n_j <= x_n	
		for (Drone n : g.drones)
			for (Position j : g.positions)
				cplex.addLe(y.get(n).get(j), x.get(n));
		
		for (Sensor i : g.sensors) {
			IloLinearNumExpr energyCstr = cplex.linearNumExpr(); // sum_n sum_j Phi t^n_j >= E_i
			IloLinearNumExpr newCstr = cplex.linearNumExpr(); // sum_n sum_j t^n_j <= lambda1
			
			for (Drone n : g.drones)
				for (Position j : g.positions)
					if (g.Ph.get(j).get(i)-threshold >= eps) {
						energyCstr.addTerm(g.Ph.get(j).get(i), t.get(n).get(j));
						newCstr.addTerm(1.0, t.get(n).get(j));
					}
			
			cplex.addGe(energyCstr, i.getCost());
			cplex.addLe(newCstr, lambda1);
		}
	}
	
	// Print results in a file
	// Get value of objective function, resolution time, # of deployed drones, data about altitudes, ...
	public void printResults(String file, long time) throws IOException, IloException {
		FileWriter output = new FileWriter(file);
        BufferedWriter wout = new BufferedWriter(output);
        wout.write("LP RESULTS :\n Obj = "+a+"*lambda1+"+(1-a)+"*lambda2 = "+cplex.getObjValue()+" (lambda1 = "+cplex.getValue(lambda1)+", lambda2 = "+cplex.getValue(lambda2)+") Resol time = "+time+" ms\n\n");
        int task_id = 0;
        for (Drone n : g.drones) {
        	if (Math.abs(cplex.getValue(x.get(n))) > eps) {
//        		wout.write("Drone "+n.getName()+" used : \n");
        		
        		for (Position j : g.positions) {
        			double tnj = Math.abs(cplex.getValue(t.get(n).get(j)));
        			if (tnj > eps) {
        				//n.addPosition(j, tnj);
        				wout.write("{\"id\": " + task_id + ", \"drone\": " + n.getName() + ", \"position\":(" + j.getX() + "," + j.getY() + "," + j.getH() + "), \"time\":" + tnj + ",\"sensors\":[");
//        				wout.write("located at "+j+" during "+tnj+" s\n");
        				
        				boolean comma = false;
        				for (Sensor i : g.sensors) {
        					if (g.Ph.get(j).get(i) > threshold) {
        						if(comma)wout.write(",");
        						wout.write(i.getName());
        						comma = true;
//        						wout.write("\t\t recharging sensor "+i+" d = "+j.getDistance(i)+" Prx = "+g.Prx.get(j).get(i)+" Ph = "+g.Ph.get(j).get(i)+" H^t_i = "+g.Ph.get(j).get(i)*tnj+"\n");
        					} 
        				}
        				wout.write("],\"power\":[");
        				comma = false;
        				for (Sensor i : g.sensors) {
        					if (g.Ph.get(j).get(i) > threshold) {
        						if(comma)wout.write(",");
        						wout.write("" + g.Ph.get(j).get(i)*tnj);
        						comma = true;
//        						wout.write("\t\t recharging sensor "+i+" d = "+j.getDistance(i)+" Prx = "+g.Prx.get(j).get(i)+" Ph = "+g.Ph.get(j).get(i)+" H^t_i = "+g.Ph.get(j).get(i)*tnj+"\n");
        					} 
        				}
        				
        				wout.write("]}\n");
        				task_id ++;
        			}
        		}
        	}
        	
        }
        
        wout.close();
		output.close();
	}
}
