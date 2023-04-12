

public class Position implements Comparable<Position>{
	private double xcoord;
	private double ycoord;
	private double hcoord;	// Altitude
	private String name;
	private double cost; // harvested capacity
	
	public Position() {
	}
	
	public Position(double x, double y, double h, String n) {
		xcoord = x;
		ycoord = y;
		hcoord = h;
		name = n;
	}

	public Position(double x, double y, double h, String n, double c) {
		xcoord = x;
		ycoord = y;
		hcoord = h;
		name = n;
		cost = c;
	}

	public double getX(){
		return xcoord;
	}
	
	public double getY(){
		return ycoord;
	}
	
	public String getName() {
		return name;
	}
	
	public double getCost() {
		return cost;
	}
	
	public double getH() {
		return hcoord;
	}

	public void setName(String n) {
		name = n;
	}
	
	public void setCost(double c) {
		cost = c;
	}
	
	
	public double getDistance(Sensor i) {
		return Math.sqrt(Math.pow(getX()-i.getX(), 2.0)+Math.pow(getY()-i.getY(), 2.0)+Math.pow(getH(), 2.0));
	}
	
	public double getDistance(Position i) {
		return Math.sqrt(Math.pow(getX()-i.getX(), 2.0)+Math.pow(getY()-i.getY(), 2.0)+Math.pow(getH()-i.getH(), 2.0));
	}
	
	public String toString(){
		return name +" ("+ xcoord +","+ ycoord +","+ hcoord +") cost = "+cost;
	}	
	
	public int compareTo(Position p) {
		return (int) Math.round(Math.signum(p.cost-cost));
	}
	
}
