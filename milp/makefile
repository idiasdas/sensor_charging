method = cg
output_dir = "/home/idiasdas/project/output/"
traces_path  = /home/idiasdas/project/traces/

CLASSPATH = -classpath .:/home/dcoudert/CPLEX_Studio1210/cplex/lib/cplex.jar 

JFLAGS = -g \
	$(CLASSPATH)
JVMFLAGS = -Djava.library.path=/home/dcoudert/CPLEX_Studio1210/cplex/bin/x86-64_linux \
	-Xmx20000m
JC = javac
JVM = java
.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

CLASSES = \
	Sensor.java \
	Position.java \
	Drone.java \
	Topology.java \
	OERPmin.java \
	OERPmin_nodrone.java\
	OERPmainNEW.java

MAIN = OERPmainNEW

default: classes

classes: $(CLASSES:.java=.class)

run: classes
	$(JVM) $(CLASSPATH) $(JVMFLAGS)  $(MAIN)

clean:
	$(RM) *.class