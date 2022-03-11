# Stanisław Hapke 148285 Kacper Dobek 148247 CO 21/22 winter semester


import sys
import random
import copy


class Intersection:
    def __init__(self):
        self.incoming_streets = []  # a list of incoming street names

    def add_incoming_street(self, street):
        self.incoming_streets.append(street)

    def __str__(self):
        text = "Intersection"
        for street in self.incoming_streets:
            text += ", "
            text += str(street)
        return text

    def __repr__(self):
        return str(self)


class Street:
    def __init__(self, inter, name, time):
        self.intersection = inter
        self.name = name
        self.time = time
        self.queueLength = 0
        self.cycleTime = None  # a sum of times of the intersection cycle
        self.cycleInfo = None  # a tuple with green starting time and duration

    def __str__(self):
        return f'Street({self.intersection},{self.name},{self.time},{self.queueLength},{self.cycleTime})'

    def __repr__(self):
        return str(self)


class Car:
    def __init__(self, plan, index):
        self.plan = plan
        self.position = 0  # = street duration - car progress
        self.index = index  # waiting queue car index on the street

    def __str__(self):
        text = "Car "
        text += str(self.position) + " " + str(self.index)
        for car in self.plan:
            text += ", "
            text += str(car)
        return text

    def __repr__(self):
        return str(self)


class TrafficProblem:
    def __init__(self, intersections, streets, waiting_cars, simulation_duration, bonus):
        self.intersections = intersections
        self.streets = streets
        self.simulation_duration = simulation_duration
        self.bonus = bonus
        # initial state of waiting cars (the beginning of simulation)
        self.waiting_cars = waiting_cars

    def getSchedule(self, solution) -> None:
        for intersection in solution:
            cycleTime = sum(streetName[1] for streetName in intersection)
            counter = 0
            for streetName in intersection:
                self.streets[streetName[0]].cycleTime = cycleTime
                durationGreen = streetName[1]
                self.streets[streetName[0]].cycleInfo = (
                    counter, counter + durationGreen)
                counter += durationGreen

    def generate_uniform_solution(self):
        solution = []
        for i, inter in enumerate(self.intersections):
            solution.append([])
            incoming_streets = inter.incoming_streets
            random.shuffle(incoming_streets)
            for street_name in inter.incoming_streets:
                solution[-1].append((street_name, 1))
        return solution

    def generate_random_solution(self):
        solution = []
        for i, inter in enumerate(self.intersections):
            solution.append([])
            incoming_streets = inter.incoming_streets
            random.shuffle(incoming_streets)
            for street_name in incoming_streets:
                time = random.randint(1, 5)
                solution[-1].append((street_name, time))
        return solution

    def carToNextIntersection(self, car):
        car.plan.pop(0)
        newStreet = car.plan[0]
        # car is now on the next street
        car.position = self.streets[newStreet].time - 1

    def evaluate(self, solution) -> int:
        score = 0
        waiting_cars = copy.deepcopy(self.waiting_cars)
        driving_cars = set()
        self.getSchedule(solution)
        streets = copy.deepcopy(self.streets)

        for second in range(self.simulation_duration):
            temp_cars = set()
            for car in driving_cars:
                if car.position == 0:  # car arrived at the end of the street
                    if len(car.plan) == 1:  # car finishes the plan
                        score += self.bonus + self.simulation_duration - second
                    else:  # car is moved to another street of its plan
                        car.index = streets[car.plan[0]].queueLength
                        streets[car.plan[0]].queueLength += 1
                        waiting_cars.add(car)
                    temp_cars.add(car)
                car.position -= 1
            driving_cars = driving_cars - temp_cars
            temp_cars.clear()

            for car in waiting_cars:
                street = streets[car.plan[0]]
                if street.cycleTime == 0:
                    continue
                if street.cycleInfo[0] <= second % street.cycleTime < street.cycleInfo[1]:
                    car.index -= 1
                    if car.index == -1:  # the car can enter the intersection
                        streets[car.plan[0]].queueLength -= 1
                        self.carToNextIntersection(car)
                        temp_cars.add(car)
            driving_cars = driving_cars.union(temp_cars)
            waiting_cars = waiting_cars - temp_cars
        return score

    def solution_print(self, solution):
        intersection_counter = 0
        for intersection in solution:
            if (len(intersection) == 0):
                continue
            intersection_counter += 1
        sys.stdout.write(str(intersection_counter) + "\n")
        for i, intersection in enumerate(solution):
            if (len(intersection) == 0):
                continue
            sys.stdout.write(str(i)+"\n")
            sys.stdout.write(str(len(intersection))+"\n")
            for street, tim in intersection:
                sys.stdout.write(street+" "+str(tim)+"\n")

# TrafficProblem instance initialization


def initialize():
    D, I, S, V, F = map(int, sys.stdin.readline().split())
    allStreets = dict()
    plannedStreets = dict()
    Intersections = []
    waiting_cars = set()

    for i in range(I):
        Intersections.append(Intersection())

    for s in range(S):
        beg, end, name, time = sys.stdin.readline().split()
        new_street = Street((int(beg), int(end)), name, int(time))
        allStreets[name] = new_street

    for c in range(V):
        car_data = list(sys.stdin.readline().split())
        plan = car_data[1:]
        for street in plan:
            if street not in plannedStreets:
                plannedStreets[street] = allStreets[street]
                Intersections[allStreets[street].intersection[1]
                              ].add_incoming_street(street)
        firstStreet = plan[0]
        index = plannedStreets[firstStreet].queueLength
        plannedStreets[firstStreet].queueLength += 1
        waiting_cars.add(Car(plan, index))
    tf = TrafficProblem(Intersections, plannedStreets,
                        waiting_cars, D, F)
    return tf
