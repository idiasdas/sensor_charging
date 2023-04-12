

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import ilog.concert.IloException;
import ilog.concert.IloLinearNumExpr;
import ilog.concert.IloNumVar;
import ilog.cplex.IloCplex;

public class OERPmin_nodrone {
	static final double eps = 1.0e-7;
	static final double threshold = 0.000063095734448;
	double a;
	
	Topology g;
	IloCplex cplex;
	
	Map<Position, IloNumVar> y = new HashMap<Position, IloNumVar>(); // binary variable to indicate if a position is used or not.
	Map<Position, IloNumVar> t = new HashMap<Position, IloNumVar>(); // real variable to indicate for how  long a position is used.
	IloNumVar lambda1, lambda2;
	double fixed_lambda2;
	
	public OERPmin_nodrone(Topology g, double a, double time_limit, double fixed_lambda2) throws IloException {
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
		this.fixed_lambda2 = fixed_lambda2;
			
		for (Position j : g.positions) {
			t.put(j, cplex.numVar(0.0, g.getTau(), "t_"+j.getName()));
			y.put(j, cplex.intVar(0, 1, "y_"+j.getName()));
		}						

		setObjective(a);
		setConstraints();		
	}
	
	public void setObjective(double a) throws IloException {
		IloLinearNumExpr obj = cplex.linearNumExpr();
		obj.addTerm(a , this.lambda1);
		obj.addTerm(1 - a, this.lambda2);
		cplex.addMinimize(obj);
	}
	
	//---------------------------------------------------------- CONSTRAINT 1 ----------------------------------------------------------
	// Sum tp <= lambda1 for all sensors
	public void set_constraint_1() throws IloException{
		IloLinearNumExpr left;
		for (Sensor s : g.sensors){
			left = cplex.linearNumExpr();
			for (Position j : g.positions){
				if (g.Ph.get(j).get(s)-threshold >= eps){
					left.addTerm(1.0,t.get(j));	
				}
			}
			cplex.addLe(left, this.lambda1,"c1_s" + s.getName());
		}
	}
	//---------------------------------------------------------- CONSTRAINT 2 ----------------------------------------------------------
	// Sum yp <= lambda2 for all sensors
	public void set_constraint_2() throws IloException{
		IloLinearNumExpr left;
		for (Sensor s : g.sensors){
			left = cplex.linearNumExpr();
			for (Position j : g.positions){
				if (g.Ph.get(j).get(s)-threshold >= eps){
					left.addTerm(1.0,y.get(j));	
				}
			}
			// cplex.addLe(left, this.fixed_lambda2);
			cplex.addLe(left, this.lambda2, "c2_s"+ s.getName());
		}
	}
	//---------------------------------------------------------- CONSTRAINT 3 ----------------------------------------------------------
	public void set_constraint_3() throws IloException{
		IloLinearNumExpr right;
		for (Position j : g.positions){
			right = cplex.linearNumExpr();
			right.addTerm(g.getTau(),this.y.get(j));
			cplex.addLe(this.t.get(j), right, "c3_p" + j.getName());
		}
	}
	//---------------------------------------------------------- CONSTRAINT 4 ----------------------------------------------------------
	public void set_constraint_4() throws IloException{
		IloLinearNumExpr left;
		for (Sensor s : g.sensors){
			left = cplex.linearNumExpr();
			for (Position j : g.positions){
				if (g.Ph.get(j).get(s)-threshold >= eps){
					left.addTerm(g.Ph.get(j).get(s), t.get(j));	
				}
			}
			cplex.addGe(left, s.getCost(), "c4_s" + s.getName());
		}
	}
	//----------------------------------------------------------------------------------------------------------------------------------
	public void setConstraints() throws IloException {
		this.set_constraint_1();
		this.set_constraint_2();
		this.set_constraint_3();
		this.set_constraint_4();
	}
	//----------------------------------------------------------------------------------------------------------------------------------
	public void set_constraint_solution(int sol) throws IloException{
		System.out.println(" Adding constraint");
		IloLinearNumExpr left = cplex.linearNumExpr();
		int count = 0;
		for (Position j : g.positions) {
        		double tj = Math.abs(cplex.getValue(t.get(j)));
			if (tj > eps) {
				System.out.println("\t position\":(" + j.getX() + "," + j.getY() + "," + j.getH() + ")");
				left.addTerm(1,y.get(j));
				count++;
			}
        	}
        	cplex.addLe(left,count - 1, "c_sol_"+sol);
	}
	//----------------------------------------------------------------------------------------------------------------------------------
	// Print results in a file
	// Get value of objective function, resolution time, # of deployed drones, data about altitudes, ...
	public void printResults(String file, long time) throws IOException, IloException {
		FileWriter output = new FileWriter(file);
        	BufferedWriter wout = new BufferedWriter(output);
        	wout.write("LP RESULTS :\n Obj = "+a+"*lambda1 + "+(1 - a)+"* lambda2= "+cplex.getObjValue()+" (lambda1 = "+cplex.getValue(lambda1)+") (lambda2 = "+cplex.getValue(lambda2)+")  Resol time = "+time+" ms\n\n");
        	int task_id = 0;
        	for (Position j : g.positions) {
        		double tj = Math.abs(cplex.getValue(t.get(j)));
				if (tj > eps) {
					wout.write("{\"position\":(" + j.getX() + "," + j.getY() + "," + j.getH() + "), \"time\": " + tj + ",\"sensors\":[");	
					// wout.write("{\"position\":" +j.getName()+ ", \"time\": " + tj + ",\"sensors\":[");				
					boolean comma = false;
					for (Sensor i : g.sensors) {
						if (g.Ph.get(j).get(i) > threshold) {
							if(comma)wout.write(",");
							wout.write(i.getName());
							comma = true;
						} 
					}
					wout.write("],\"power\":[");
					comma = false;
					for (Sensor i : g.sensors) {
						if (g.Ph.get(j).get(i) > threshold) {
							if(comma)wout.write(",");
							wout.write("" + g.Ph.get(j).get(i)*tj);
							comma = true;
						} 
					}
					wout.write("]}\n");
				}
        	}
   //      	wout.write("\nWeird\n");
   //      	for (Position j : g.positions) {
   //      		double yj = Math.abs(cplex.getValue(y.get(j)));
   //      		double tj = Math.abs(cplex.getValue(t.get(j)));
			// if (yj == 0.0 && tj > eps) {
			// 	wout.write(j.getName() + "\t"+ j.getX() + "," + j.getY() + "," + j.getH() +"\n");				
			// }
   //      	}
	        wout.close();
		output.close();
	}
}
