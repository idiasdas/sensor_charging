

import java.util.*;

public class Drone {
	private String name;
	private Map<Position, Double> posTime; // each position with associate time
	
	public Drone(String n) {
		name = n;
		posTime = new HashMap<Position, Double>();
	}
	
	public String getName() {
		return name;
	}
	
	public Map<Position, Double> getPos() {
		return posTime;
	}
	
	public void addPosition(Position p, double t) throws Exception {
		if (!posTime.containsKey(p))
			posTime.put(p, t);
		else
			throw new Exception("Position already set for drone "+name);
	}
	
	public String toString() {
		return name + " with associated positions "+posTime;
	}
}
