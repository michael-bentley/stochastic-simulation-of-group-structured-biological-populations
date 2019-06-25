import random
import math
import parameters

class Entity:
    
    population = [] # population list. 
    N = 0 # population size.
    Z = 0 # total phenotype.

    def __init__(self, phenotype):
        Entity.population.append(self) # append entity to global population.        
        self.n = 1 # set entity abundance to 1.
        Entity.N += self.n # increment population size by entity abundance.        
        self.z = phenotype # set entity phenotype to input.
        Entity.Z += self.z # increment population phenotype by entity phenotype.
        self.birthRate = 0
        self.deathRate = 0

    def calcBirthRate(self):          
        R = parameters.Rtot / Entity.N
        if R > 1:
            R = 1      
        self.birthRate = R * (1 - self.z)
        return self.birthRate
    
    def calcDeathRate(self):                
        R = parameters.Rtot / Entity.N
        if R > 1:
            R = 1
        self.deathRate = 1
        if R > 0:
            lmbda = parameters.K / (R * self.z) - parameters.K
            self.deathRate = parameters.mu0 + (1 - parameters.mu0) * (1 - math.exp(-lmbda))        
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
            descendant = Entity(phenotype)
            descendant.calcBirthRate()
            descendant.calcDeathRate()
        else:
            # descendant = Entity(self.z)
            # descendant.calcBirthRate()
            # descendant.calcDeathRate()
            self.n += 1
            Entity.N += 1            
            Entity.Z += self.z            

    def deathEvent(self):
        self.n -= 1
        if self.n == 0:
            Entity.population.remove(self) # remove the object from the population list.          
        Entity.N -= 1        
        Entity.Z -= self.z
        