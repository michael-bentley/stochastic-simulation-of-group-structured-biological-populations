import random
import math
import parameters

class Entity:
    population = []
    N = 0

class Individual:
    
    population = [] # population list. 
    N = 0 # population size.
    Z = 0 # total phenotype.

    def __init__(self, phenotype):        

        # Update individual
        self.n = 1 # set individual abundance to 1.
        self.z = phenotype # set individual phenotype to input.
        self.group = None # this is set in the group constructor.
        self.birthRate = 0
        self.deathRate = 0
        Individual.population.append(self) # append Individual to global population.        
        Individual.N += self.n # increment population size by Individual abundance.        
        Individual.Z += self.z # increment population phenotype by Individual phenotype.

        # Update group
        # all takes place within group constructor when individual is added to a group.

        # Update entity
        Entity.population.append(self) # append Individual to global population.
        Entity.N += self.n # increment population size by Individual abundance.        

    def calcPhenotype(self):                  
        return self.z
    
    def calcBirthRate(self):          
        self.birthRate = 1
        return self.birthRate
    
    def calcDeathRate(self):                
        self.deathRate = self.group.individualN / parameters.individualCarryingCapacity
        return self.deathRate

    def birthEvent(self):                
        if random.random() < 0.1:            
            phenotype = self.z
            if random.random() < 0.5:
                phenotype += 0.01
                if phenotype > 1:
                    phenotype = 1
            else:
                phenotype -= 0.01
                if phenotype < 0:
                    phenotype = 0

            # Update individual and entity (takes place within individual constructor)
            descendant = Individual(phenotype)    

            # Update group
            Group.Z -= self.group.z
            descendant.group = self.group
            descendant.group.individuals.append(descendant)
            descendant.group.individualN += 1        
            descendant.group.individualZ += descendant.z
            descendant.group.z = descendant.group.individualZ / descendant.group.individualN
            Group.Z += self.group.z
            
        else:
            # Update individual
            self.n += 1
            Individual.N += 1            
            Individual.Z += self.z  

            # Update group
            Group.Z -= self.group.z
            self.group.individualN += 1        
            self.group.individualZ += self.z 
            self.group.z = self.group.individualZ / self.group.individualN
            Group.Z += self.group.z

            # Update entity
            Entity.N += 1        

    def deathEvent(self):

        # Update individual
        self.n -= 1
        Individual.N -= 1        
        Individual.Z -= self.z
        if self.n == 0:        
            Individual.population.remove(self) # remove the object from the population list.          

        # Update group
        Group.Z -= self.group.z
        self.group.individualN -= 1
        self.group.individualZ -= self.z            
        if self.group.individualN > 0:            
            self.group.z = self.group.individualZ / self.group.individualN        
        Group.Z += self.group.z       
        
        if self.n == 0:
            self.group.individuals.remove(self)  
            if len(self.group.individuals) == 0:
                self.group.deathEvent()

        # Update entity
        Entity.N -= 1
        if self.n == 0:   
            Entity.population.remove(self) # remove the object from the population list.        

class Group:
    
    population = [] # population list. 
    N = 0 # population size.
    Z = 0 # total phenotype.

    def __init__(self, founders):

        # Update individual 
        for individual in founders: 
            individual.group = self          

        # Update group
        self.founders = founders # store the founder individuals.
        self.individuals = founders.copy() # the individuals list holds all the individuals within the group.
        self.n = 1 # set group abundance to 1.                
        self.birthRate = 0
        self.deathRate = 0
        self.individualN = 0
        self.individualZ = 0
        for individual in self.individuals: 
            self.individualN += individual.n
            self.individualZ += individual.n * individual.z
        self.z = self.individualZ / self.individualN # set group phenotype to average phenotype of founders.                      
        Group.population.append(self) # append Group to global population.        
        Group.N += self.n # increment population size by Group abundance.        
        Group.Z += self.z # increment population phenotype by Group phenotype.
        
        # Update entity
        Entity.population.append(self) # append group to entity population.
        Entity.N += self.n # increment entity population size by group abundance.           

    def calcPhenotype(self):
        Group.Z -= self.z
        self.individualN = 0
        self.individualZ = 0
        for individual in self.individuals:             
            self.individualN += individual.n
            self.individualZ += individual.n * individual.z
        self.z = self.individualZ / self.individualN # set group phenotype to average phenotype of founders.  
        Group.Z += self.z
        return self.z

    def calcBirthRate(self):
        self.birthRate = 0     
        return self.birthRate
    
    def calcDeathRate(self):                      
        self.deathRate = 0
        return self.deathRate

    def birthEvent(self):        
        randomIndividual = random.random() * self.individualN
        randomIndividualSum = 0
        for individual in self.individuals:
            randomIndividualSum += individual.n
            if randomIndividualSum > randomIndividual:
                founder = Individual(individual.z)
                grp = Group([founder])   

    def deathEvent(self):

        # Update individual
        if len(self.individuals) > 0:
            for individual in self.individuals:
                Individual.N -= individual.n       
                Individual.Z -= individual.n * individual.z
                Individual.population.remove(individual) # remove the object from the population list.                    

        # Update group
        self.n -= 1
        Group.N -= 1        
        Group.Z -= self.z
        Group.population.remove(self)
                
        # Update entity
        if len(self.individuals) > 0:
            for individual in self.individuals:
                Entity.N -= 1
                Entity.population.remove(individual) # remove the object from the population list.  
        Entity.N -= 1
        Entity.population.remove(self)