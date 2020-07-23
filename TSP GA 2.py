#TSP GA Implementation

import numpy, random, operator

noCities = 10 #including starting city
popSize = 10 #no of solutions/individuals
eliteNo = 5 #elitism, the number of individuals who don't go through the random selection process
mutationRate = 0.01 #mutation rate, chance of mutated member of population every gen
generations = 500 #500 iterations then terminate
popLeft = popSize - eliteNo #non-elite population

if popLeft % 2 != 0:
   popLeft = popLeft - 1

#class City to hold the properties of each city
class City:
    
    #creates city properties when object is created
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #getDistance() method, to be called through cityName.getDistance(otherCity)
    def getDistance(self, other):
        #use Pythagorean theorem to calculate distance
        distance = numpy.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
        return distance
    
    #use __repr__ method to format when City object is called with print()
    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
        
#class route to hold the properties of each route#
class Route:
    
    #creates route properties when object is created
    def __init__(self, route):
        self.route = route
        self.fitness = 0.0
        self.distance = 0
        
    #function to get total distance of a route
    def fitnessFunction(self):
        for x in range(0, len(self.route)):
            if x + 1 < len(self.route):
                self.distance += self.route[x].getDistance(self.route[x+1])
            else: 
                self.distance = self.route[x].getDistance(self.route[0])
        return self.distance
    
    #function to invert distance, and record that as fitness, smaller distance = larger fitness
    def getFitness(self):
        self.fitness = 1/float(self.distance)
        return self.fitness
    
    #use __repr__ method to format when Route object is called with print()
    def __repr__(self):
        return "Path: "  + str(self.route) + "\n Distance: " + str(self.distance) + "\n Fitness: " + str(self.fitness)

#function to create cityList, can be changed later to accomadate user input for city
def genCityList(noCities):
    cityList = []
    for x in range(0, noCities):
        cityList.append(City(x=int(random.random()*200), y=int(random.random()*200)))
    return cityList

#function to generate an individual/route
def genRoute(cityList):
    route = Route(random.sample(cityList, len(cityList)))
    return route

#function to generate initial population
def genPop(popSize, cityList):
    population = []
    for x in range(0, popSize):
        population.append(genRoute(cityList))
    return population

#function to sort the routes
def sortRoutes(population):
    fitnessScore = {}
    for x in range(0, len(population)):
        #population[x].fitnessFunction()
        fitnessScore[x] = population[x].getFitness()
    #returns fitnessScore as list of tuples sorted in descending order by the 1st element
    return sorted(fitnessScore.items(), key = operator.itemgetter(1), reverse = True)

#selection function, don't randomly select until the eliteNo'th element
def selection(routeSorted, eliteNo, popLeft):
    results = []
    addElement = []
    #loop to create elitism
    for x in range(0, eliteNo):
        results.append(routeSorted[x])
    del routeSorted[:eliteNo]
    addElement = selectionRandom(routeSorted, popLeft)
    #adds the randomly selected routes from addElement to the results list
    results.extend(addElement)
    #returns list of results
    return results

#weigh non-elite population and select who goes through based on random weighted chance
def selectionRandom(routeSorted, popLeft):
    weight = []
    choice = []
    #when val() called it will return the 1st element of the tuple
    val = operator.itemgetter(1)
    total = 0
    #use loop to get total
    for x in range(0, len(routeSorted)):
        total = total + val(routeSorted[x])
    #use loop to get weight from total
    for x in range(0, len(routeSorted)):
        weight.append(val(routeSorted[x])//total)
    #only half of routeSorted will be selected and returned, // is int division operator
    choice = random.choices(population = routeSorted, weights = weight, k = popLeft//2)
    return choice

#create mating pool 
def matingPool(results, population):
    matPool = []
    #when index() called it will return the 0st element of the tuple
    index = operator.itemgetter(0)
    for x in range(0, len(population)):
        #get the 0th element from the tuple and use it to call population to get route path
        a = index(population[x])
        matPool.append(results[a].route)
    #return the list matPool, containing the path of all the selected routes
    return matPool

#create offspring
def breed(parent1, parent2):
    childGenes = [] #offspring's route path
    childP1 = [] #part 1 of child's genes/path
    childP2 = [] #part 2 of child's genes/path
    #note: may need to change parent1 to parent1.route
    #find two points in the path sequence to splice
    point1 = int(random.random()*len(parent1))
    point2 = int(random.random()*len(parent1))
    #find whether point1, or point2 is smaller, make that the start gene
    startGene = min(point1, point2)
    #find whether point1, or point2 is larger, make that the end gene
    endGene = max(point1, point2)
    #create for loop, between start and end, which will create part 1 of the child's genes
    for x in range(startGene, endGene):
        #append xth element of parent1 to childP1
        childP1.append(parent1[x])
    #childP2 is an array of items, that uses the order of cities from parent2 if the city is not in childP1
    childP2 = [item for item in parent2 if item not in childP1]
    #splice the genes together to make offspring
    childGenes = childP1 + childP2
    return childGenes

#algorithm to match mates
def breedPopulation(matPool, eliteNo, popSize):
    children = []
    #how many offspring can be made
    length = popSize - len(matPool)
    #pool is a list of random routes from matPool
    pool = random.sample(matPool, len(matPool))
    #elitism - add on the elite solutions from earlier to new population
    for x in range(0, eliteNo):
        children.append(matPool[x])
    #create offspring
    for x in range(0, length):
        child = breed(pool[x], pool[len(matPool) - x - 1])
        children.append(child)
    return children

#mutate function to take a route, and randomly choose whether or not to mutate it
def mutate(individual, mutationRate):
    #loop len(individual) times
    for x in range(len(individual)):
        #gen random num, if less than mutationRate mutate route
        if(random.random() < mutationRate):
            #swapWith picks random index in route
            swapWith = int(random.random()*len(individual))
            city1 = individual[x]
            city2 = individual[swapWith]
            #the two selected cities swap place
            individual[x] = city2
            individual[swapWith] = city1
    #return route
    return individual

#mutatePopulation() to create new pop
def mutatePopulation(pop, mutationRate):
    mutatedPop = []
    #loop for no. elements in population
    for x in range(0, len(pop)):
        #get routes and assign them to mutatedPop
        mutatedInd = mutate(pop[x], mutationRate)
        mutatedPop.append(mutatedInd)
    #return list mutatedPop
    return mutatedPop

#next generation to repeat every generation after first
def nextGeneration(currentGen, eliteSize, mutationRate, popSize, popLeft):
    #get popRanked through calling sortRoutes with currentGen
    popRanked = sortRoutes(currentGen)
    #get selectionResults through calling selection() with popRanked
    selectionResults = selection(popRanked, eliteNo, popLeft)
    #get matPool by calling matingPool
    matPool = matingPool(currentGen, selectionResults)
    #get children through calling breedPopulation()
    children = breedPopulation(matPool, eliteNo, popSize)
    #get nextGeneration through calling mutatePopulation
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def geneticAlgorithm(cityList, popSize, eliteNo, mutationRate, generations, popLeft):
    val = operator.itemgetter(1)
    index = operator.itemgetter(0)
    pop = genPop(popSize, cityList)
    print("initial distance: " + str(1/val(sortRoutes(pop)[0])))
    for x in range(0, generations):
        pop = nextGeneration(pop, eliteNo, mutationRate, popSize, popLeft)
    print("final distance: " + str(1/val(sortRoutes(pop)[0])))
    bestRouteIndex = index(sortRoutes(pop)[0])
    bestRoute = pop[bestRouteIndex]
    return bestRoute

#run program
cityList = genCityList(noCities)
geneticAlgorithm(cityList, popSize, eliteNo, mutationRate, generations, popLeft)

"""
Test to see if mutate() and mutatePopulation() work:
    a = genCityList(noCities)
    b = genPop(popSize, a)
    c = sortRoutes(b)
    d = selection(c, eliteNo, popLeft)
    e = matingPool(d, b)
    f = breedPopulation(e, eliteNo, popSize)
    g = mutatePopulation(f, mutationRate)
    print(g)

    I think it works.
    
Test to see if breed() and breedPopulation() work:
    a = genCityList(noCities)
    b = genPop(popSize, a)
    c = sortRoutes(b)
    d = selection(c, eliteNo, popLeft)
    e = matingPool(d, b)
    f = breedPopulation(e, eliteNo, popSize)
    print(f)
    
    I think it workds, may need later testing
    
Test to see if matingPool() outputs path of all selected routes:
    a = genCityList(noCities)
    b = genPop(popSize, a)
    c = sortRoutes(b)
    d = selection(c, eliteNo, popLeft)
    e = matingPool(d, b)
    print(e)

    It works. I think. May need later testing

Test to see if selection and selectionRandom work:
    a = genCityList(noCities)
    b = genPop(popSize, a)
    c = sortRoutes(b)
    d = selection(c, eliteNo, popLeft)
    print(len(d))
    
    It works.

Test to see if initial population can be generated and then sorted based on fitness
    a = genCityList(noCities)
    b = genPop(popSize, a)
    c = sortRoutes(b)
    print(c)

    It works.

Test to check if initial population can be generated:
    a = genCityList(noCities)
    b = genPop(popSize, a)
    print(b)

    It works.

Test to check if Route can be generated from cityList:
    a = genCityList(noCities)
    b = genRoute(a)
    print(b)
    
    It works.

Test for genCityList():
    a = genCityList(noCities)
    print(a)

    It works.

"""
