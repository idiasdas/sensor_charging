public class Sensor implements Comparable<Sensor>{
	private double xcoord;
	private double ycoord;
	private String name;
	private double cost;	// Associated cost : priority or energy needs

	public Sensor(){}
	
	public Sensor(double x, double y, String n){
		xcoord = x;
		ycoord = y;
		name = n;
		cost = 1.0;
	}
	
	public Sensor(double x, double y, String n, double c){
		xcoord = x;
		ycoord = y;
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

	public void setName(String n) {
		name = n;
	}
	
	public void setCost(double c) {
		cost = c;
	}
	
	public String toString(){
		return name +" ("+ xcoord +","+ ycoord +") cost = "+cost;
	}
	
	public int compareTo(Sensor s) {
		return (int) Math.round(Math.signum(s.cost-cost));
	}

	@Override
	protected Object clone() throws CloneNotSupportedException {
		// TODO Auto-generated method stub
		return new Sensor(xcoord, ycoord, name, cost);
	}
	
	
}
