import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import ilog.concert.IloException;
import ilog.cplex.IloCplex.UnknownObjectException;


public class OERPmainNEW {
	static final double eps = 1.0e-7;
	static final double threshold = 0.000063095734448;
	
	public static void printResults(OERPmin m) throws UnknownObjectException, IloException {
		for (Drone n : m.g.drones) {
			System.out.println("Drone "+n.getName()+" : alpha = "+m.cplex.getValue(m.x.get(n)));
			
			for (Position j : m.g.positions) {
				System.out.println("\t Position "+j.getName()+" beta = "+m.cplex.getValue(m.y.get(n).get(j))+", t = "+m.cplex.getValue(m.t.get(n).get(j)));
			}
		}
	}
	
	public static void main(String[] args) throws IOException, IloException {
		// INPUT values for topology
		double x=50, y=50; // Size of area
		Double[] h = {1.0, 2.0, 3.0, 4.0, 5.0}; // Possible altitudes
		double tau = 3600.0;
		
		String work_dir = "/user/idiasdas/home/dev/sensor_charging/milp/output_simplified/";
		int time_limit = 1200;
		int[] sensors = {5,10,15,20,30,40,50};
		int[] positions = {5,6,7};
		int[] drones = {3};
		int[] lambda2 = {1};
		double[] alpha = {0.01};
		
		experiment(sensors, positions, drones, lambda2, alpha,x,y,h,tau, work_dir, time_limit);
		// experiment_how_many(sensors, positions, drones, lambda2, alpha,x,y,h,tau, work_dir, time_limit);
	}

	public static void experiment(int[] sensors,int[] positions, int[] drones, int[] lambda2, double[] alpha, double x, double y, Double[] h, double tau,String work_dir, int time_limit) throws IOException, IloException{
		int count_dropped = 0;
		for (int i: sensors) {
			for (int n : drones) {
				for (int p : positions) {
					for(int l: lambda2){
						count_dropped = 0;
						for (int j=0; j<100; j++) {
							Topology g = new Topology(x, y, h, i, p, n, tau);
							for (double a : alpha) {
								// INITIALIZE INSTANCE
								OERPmin_nodrone m = new OERPmin_nodrone(g, a, time_limit,l);// I changed here
								
								long LPsolvingTime = System.currentTimeMillis();
								if (m.cplex.solve()) {
									System.out.println("OPA RESOLVEU");
									LPsolvingTime = System.currentTimeMillis() - LPsolvingTime;
									if(LPsolvingTime/1000 < time_limit ) {
										String resFile = work_dir + "s"+i+"_p"+p+"/"+j+".txt";
										Files.createDirectories(Paths.get(work_dir + "s"+i+"_p"+p+"/"));
										m.printResults(resFile, LPsolvingTime);

										FileWriter output = new FileWriter(work_dir + "ctrl_file.txt");
										BufferedWriter wout = new BufferedWriter(output);
										wout.write("Last Parameters Successfully Run:\n");
										// wout.write("d = " + n + "\n");
										wout.write("s = " + i + "\n");
										wout.write("p = " + p + "\n");
										wout.write("i = " + j + "\n");
										wout.close();
										output.close();
									}
									else {
										System.out.println("Dropped");
										count_dropped++;
										j--;
									}
									m.cplex.clearModel();
								}
							}
						}
						Files.createDirectories(Paths.get(work_dir + "s"+i+"_p"+p+"/"));
						FileWriter output = new FileWriter(work_dir + "s"+i+"_p"+p+"/dropped.txt");
						BufferedWriter wout = new BufferedWriter(output);
						wout.write("Amount of experiments that exceeded the time limit:\n");
						wout.write(count_dropped + "\n");
						wout.write("Time limit:\n");
						wout.write(time_limit + "\n");
						wout.close();
						output.close();
					}
				}
			}
		}
	}

	public static void experiment_how_many(int[] sensors,int[] positions, int[] drones, int[] lambda2, double[] alpha, double x, double y, Double[] h, double tau,String work_dir, int time_limit) throws IOException, IloException{
		int count_dropped = 0;
		for (int i: sensors) {
			for (int n : drones) {
				for (int p : positions) {
					for(int l: lambda2){
						count_dropped = 0;
						for (int j=0; j<20; j++) {
							Topology g = new Topology(x, y, h, i, p, n, tau);
							for (double a : alpha) {
								// INITIALIZE INSTANCE
								OERPmin_nodrone m = new OERPmin_nodrone(g, a, time_limit,l);// I changed here
								Boolean next_sol = true;
								int sol = 0;
								double obj = 0;
								while(next_sol){
									// if(sol == 500){
									// 	System.out.println(" 500 solutions ==> EXITING");
									// 	System.exit(1);
									// }
									long LPsolvingTime = System.currentTimeMillis();
									Boolean solved = false;
									try{
										solved = m.cplex.solve();
									} catch (Exception e){
										System.out.println("No Solution!!!");
										next_sol = false;
										m.cplex.clearModel();
									}
									if(solved){
										System.out.println(" Solved!!!");
										LPsolvingTime = System.currentTimeMillis() - LPsolvingTime;
										if(LPsolvingTime/1000 < time_limit ) {
											String resFile = work_dir + "s"+i+"_p"+p+"_lm/"+j+"_sol"+sol+".txt";
											Files.createDirectories(Paths.get(work_dir + "s"+i+"_p"+p+"_lm/"));
											m.printResults(resFile, LPsolvingTime);
											// m.cplex.exportModel(work_dir + "s"+i+"_p"+p+"_lm/model_"+j+"_sol"+sol+".lp");

											if(sol == 0){
												obj = m.cplex.getObjValue();
											}
											else if (m.cplex.getObjValue() - obj > 0.1) {
												System.out.println(" Next sol False");
												next_sol = false;
												m.cplex.clearModel();
											}


											FileWriter output = new FileWriter(work_dir + "ctrl_file.txt");
											BufferedWriter wout = new BufferedWriter(output);
											wout.write("Last Parameters Successfully Run:\n");
											// wout.write("d = " + n + "\n");
											wout.write("s = " + i + "\n");
											wout.write("p = " + p + "\n");
											wout.write("i = " + j + "\n");
											wout.write("sol = " + sol + "\n");
											wout.close();
											output.close();

											if(next_sol == true){
												System.out.println(" Constraint time");
												m.set_constraint_solution(sol);
											}
											sol++;
										}
										else {
											System.out.println("Dropped");
											count_dropped++;
											j--;
										}
									} else {
										System.out.println("Not solved!!!");
										next_sol = false;
										m.cplex.clearModel();
									}
									
									// System.out.println(" Chegou aqui");
								}
							}
						}
						Files.createDirectories(Paths.get(work_dir + "s"+i+"_p"+p+"_lm/"));
						FileWriter output = new FileWriter(work_dir + "s"+i+"_p"+p+"_lm/dropped.txt");
						BufferedWriter wout = new BufferedWriter(output);
						wout.write("Amount of experiments that exceeded the time limit:\n");
						wout.write(count_dropped + "\n");
						wout.write("Time limit:\n");
						wout.write(time_limit + "\n");
						wout.close();
						output.close();
					}
				}
			}
		}
	}
}
