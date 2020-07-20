#TSP GA Implementation

import numpy, random, sys, string, operator

noCities = 25 #including starting city
popSize = 100 #no of solutions/individuals
eliteNo = 20 #elitism, the number of individuals who don't go through the random selection process
mutationRate = 0.01
generations = 500

#function to create cityList based on noCities
def genCityList(noCities):
    cityList = []
    if noCities < 27:
        cityList.append(City(x=int(random.random()*200), y=int(random.random()*200)))
    else:
        sys.exit("too many cities")
    return cityList

#class City to hold the properties of each city
class City:
    
    #creates city properties when object is created
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #getDistance() method, to be called through cityName.getDistance(otherCity)
    def getDistance(self, other):
        #use Pythagorean theorem to calculate distance
        distance = numpy.sqrt(float((self.x-other.x)^2) + float((self.y-other.y)^2))
        return distance
    
#class route to hold the properties of each route#
class Route:
    
    #creates route properties when object is created
    def __init__(self, route):
        self.route = route
        self.fitness = 0.0
        
    #function to get fitness of a route
    def fitnessFunction(self):
        fitness = 0
        for x in range(0, len(self.route)):
            if x + 1 < len(self.route):
                fitness += self.route[x].getDistance(self.route[x+1])
            else: 
                fitness += self.route[x].getDistance(self.route[0])
        self.fitness = fitness #self.fitness is the total route distance
        #invert fitness value so the shortest distances have the highest value
        invertFitness = 1/float(self.fitness)
        return invertFitness
    
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
        fitnessScore[x] = population[x].fitnessFunction()
    #return fitnessScore as list, sorted in descending order, on the second digit(first element)
    return sorted(fitnessScore.items(), key = operator.itemgetter(1), reverse = True)

#selection function
def selection(routeSorted, eliteNo, popSize):
    results = []
    addElement = []
    for x in range(0, eliteNo):
        results.append(routeSorted[x])
    del routeSorted[:eliteNo]
    popLeft = popSize - eliteNo
    if popLeft % 2 != 0:
        popLeft = popLeft - 1
    addElement = selectionRandom(routeSorted, popLeft)
    results.extend(addElement)
    return results

#weigh rest of population and select who goes through based on random weighted chance
def selectionRandom(routeSorted, popLeft):
    weight = []
    choice = []
    total = 0
    for x in range(0, len(routeSorted)):
        total += routeSorted[x][0]
    for x in range(0, len(routeSorted)):
        weight[x] = routeSorted[x]/float(total)
    choice = random.choices(population = routeSorted, weights = weight, k = popLeft/2)
    return choice

#create mating pool 
def matingPool(population, results):
    matPool = []
    for x in range(0, len(results)):
        matPool[x] = results[x].route
    return matPool
    
#create offspring
def breed(parent1, parent2):
    childGenes = [] #route used to make offspring
    childP1 = [] #part 1 of child's genes
    childP2 = [] #part 2 of child's genes
    #note: may need to change parent1 to parent1.route
    #find a section to splice
    g1 = int(random.random()*len(parent1))
    g2 = int(random.random()*len(parent1))
    startGene = min(g1, g2)
    endGene = max(g1, g2)
    for x in range(startGene, endGene):
        childP1.append(parent1[x])
    childP2 = [item for item in parent2 if item not in parent1]
    childGenes = childP1 + childP2
    return childGenes

#algorithm to match mates
def breedPopulation(matPool, eliteNo, popSize):
    children = []
    length = popSize - len(matPool)
    pool = random.sample(matPool, len(matPool))
    #elitism - add on the elite solutions from earlier
    for x in range(0, eliteNo):
        children.append(matPool[x])
    for x in range(0, length):
        child = breed(pool[x], pool[len(matPool) - x - 1])
        children.append(child)
    return children

def mutate(individual, mutationRate):
    for x in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random()*len(individual))
            city1 = individual[x]
            city2 = individual[swapWith]
            individual[x] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    for x in range(0, len(population)):
        mutatedInd = mutate[population[x], mutationRate]
        mutatedPop.append(mutatedInd)
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate, popSize):
    popRanked = sortRoutes(currentGen)
    selectionResults = selection(popRanked, eliteNo, popSize)
    matingPool(currentGen, selectionResults)
    children = breedPopulation(matingPool, eliteNo, popSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def geneticAlgorithm(population, popSize, eliteNo, mutationRate, generations, cityList):
    pop = genPop(popSize, cityList)
    print("initial distance: " + str(1/sortRoutes(pop)[0][1]))
    for x in range(0, generations):
        pop = nextGeneration(pop, eliteNo, mutationRate, popSize)
    print("final distance: " + str(1/sortRoutes(pop)[0][1]))
    bestRouteIndex = sortRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute

cityList = genCityList(noCities)

cityChart = []
cityChart.append(City(x=int(random.random()*200), y=int(random.random()*200)))

geneticAlgorithm(cityChart, popSize, eliteNo, mutationRate, generations, cityList)