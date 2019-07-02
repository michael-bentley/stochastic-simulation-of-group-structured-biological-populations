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

        # Update self
        self.n = 1 # set individual abundance to 1.
        self.z = phenotype # set individual phenotype to input.
        self.group = None # this is set in the group constructor.
        self.birthRate = 0
        self.deathRate = 0

        # Update global individual
        Individual.population.append(self) # append Individual to global population.        
        Individual.N += self.n # increment population size by Individual abundance.        
        Individual.Z += self.z # increment population phenotype by Individual phenotype.

        # Update global entity
        Entity.population.append(self) # append Individual to global population.
        Entity.N += self.n # increment population size by Individual abundance.        

    def calcPhenotype(self):                  
        return self.z
    
    def calcBirthRate(self):          
        R = parameters.Rtot / Individual.N
        if R > 1:
            R = 1      
        self.birthRate = R * (1 - self.z)
        return self.birthRate
    
    def calcDeathRate(self):                
        R = parameters.Rtot / Individual.N
        if R > 1:
            R = 1
        self.deathRate = 1
        if R > 0:
            lmbda = parameters.K / (R * self.z) - parameters.K
            self.deathRate = parameters.mu0 + (1 - parameters.mu0) * (1 - math.exp(-lmbda))        
        return self.deathRate

    def birthEvent(self):        
        if random.random() < 0.01:            
            phenotype = self.z
            if random.random() < 0.5:
                phenotype += 0.01
                if phenotype > 1:
                    phenotype = 1
            else:
                phenotype -= 0.01
                if phenotype < 0:
                    phenotype = 0

            # Update self and global (takes place within individual constructor)
            descendant = Individual(phenotype)    

            # Update group
            descendant.group = self.group
            descendant.group.individuals.append(descendant)
            descendant.group.individualN += 1        
            descendant.group.individualZ += descendant.z
            descendant.group.calcPhenotype()
            
        else:
            # Update self
            self.n += 1

            # Update group
            self.group.individualN += 1        
            self.group.individualZ += self.z
            self.group.calcPhenotype()

            # Update global individual
            Individual.N += 1            
            Individual.Z += self.z  

            # Update global entity
            Entity.N += 1

    def deathEvent(self):

        # Update self
        self.n -= 1

        # Update group
        self.group.individualN -= 1        
        self.group.individualZ -= self.z        

        # Update global individual
        Individual.N -= 1        
        Individual.Z -= self.z

        # Update global entity
        Entity.N -= 1
        
        if self.n == 0:

            # Update self
            self.n = 0
            self.z = 0
            self.birthRate = 0
            self.deathRate = 0

            # Update group
            self.group.individuals.remove(self)            

            if self.group.individualN == 0:
                self.group.deathEvent()

            self.group = None

            # Update global individual
            Individual.population.remove(self) # remove the object from the population list.          

            # Update global entity            
            Entity.population.remove(self) # remove the object from the population list.        

class Group:
    
    population = [] # population list. 
    N = 0 # population size.
    Z = 0 # total phenotype.

    def __init__(self, founders):
        self.founders = founders # store the founder individuals.
        self.individuals = founders # the collective holds all the individuals within the group.
        self.n = 1 # set group abundance to 1.                
        self.birthRate = 0
        self.deathRate = 0
        self.individualN = 0
        self.individualZ = 0

        self.individualN = 0
        self.individualZ = 0
        for individual in self.individuals: 
            individual.group = self          
            self.individualN += individual.n
            self.individualZ += individual.n * individual.z
        
        self.z = self.individualZ / self.individualN # set group phenotype to average phenotype of founders.                      

        Group.population.append(self) # append Group to global population.        
        Group.N += self.n # increment population size by Group abundance.        
        Group.Z += self.z # increment population phenotype by Group phenotype.

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
        return self.birthRate
    
    def calcDeathRate(self):                      
        return self.deathRate

    def birthEvent(self):        
        pass   

    def deathEvent(self):

        # Update self
        self.n -= 1
                
        # Update individuals in group
        if len(self.individuals) > 0:
            for individual in self.individuals:
                
                # Update individual
                individual.n = 0
                individual.z = 0
                individual.birthRate = 0
                individual.deathRate = 0
                individual.group.remove(individual)

                # Update global individual
                Individual.N -= individual.n       
                Individual.Z -= individual.n * individual.z
                Individual.population.remove(individual) # remove the object from the population list.    

                # Update global entity
                Entity.N -= 1
                Entity.population.remove(individual) # remove the object from the population list.  

        # Update global group
        Group.N -= 1        
        Group.Z -= self.z
        Group.population.remove(self)

        # Update global entity
        Entity.N -= 1
        Entity.population.remove(self)