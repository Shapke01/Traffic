# Traffic Signalling
The project aim is to find an optimal schedule of traffic lights - based on Hash Code 2021 (Online Qualifications)

https://codingcompetitions.withgoogle.com/hashcode/archive

## General information
In our first version (simple.py), we generate a random initial
solution. Then, in a loop, we generate another random solution
and compare it to the initial one. The best solution found is
returned. A random solution has a random non-zero ( and
bounded) value assigned to each of the streets for all
intersections. The order of incoming streets is also random.

The second version (complex.py) implements Simulated
Annealing. This sometimes is a very effective method, which
doesn’t require a great number of evaluations, as opposed to
genetic programming, for example. The main parts are the loop
with time stopping criterion and a function generating a random neighbor.

### Three .py files:
* traffic.py - contains definitions and implementations of
classes (Intersection, Street, Car and TrafficProblem) as
well as a function for initializing the TrafficProblem
instance with the values from stdin
* simple.py - contains 
* complex.py - contains the more advanced version
## Launch
On Windows 11 we run scripts with (CMD):
```cmd
type e.txt | python simple.py > solution.txt 
```
(an example for e.txt, sample.py and redirection of stdout to solution.txt)

## Authors
Kacper Dobek, Stanisław Hapke

