import math
import random
import parameters

from entity import Entity, Individual, Group

# Step 1 - set time to zero and initialise the population.
time = 0
nextPrint = 0

# Initial population.
while len(Group.population) < parameters.initialEntityN:
    founder1 = Individual(parameters.initialPhenotype)
    founder2 = Individual(parameters.initialPhenotype)
    founder3 = Individual(parameters.initialPhenotype)
    founder4 = Individual(parameters.initialPhenotype)
    founder5 = Individual(parameters.initialPhenotype)
    grp = Group([founder1, founder2, founder3, founder4, founder5])

if parameters.algorithm == "direct": # run the Direct Method algorithm.
    
    while time < parameters.tfinal:
            
        # Step 2 - calculate birth and death rates and sample the time to the next event using an exponential distribution.        
        sumRates = 0
        for entity in Entity.population:
            sumRates += entity.n * (entity.calcBirthRate() + entity.calcDeathRate())

        time += -math.log(random.random()) / sumRates # exponentially distributed random number.
        
        # Step 3 - determine and execute the next event using probabilities birthRate / sumRates and deathRate / sumRates, respectively.    
        randomEvent = random.random() * sumRates
        sumRatesAgain = 0
        for entity in Entity.population:
            sumRatesAgain += entity.n * entity.birthRate # not that we don't recalculate the birth rate this time.
            if sumRatesAgain >= randomEvent:
                entity.birthEvent() # execute entity birth and update the population.
                # print("individual birth")
                break 
            sumRatesAgain += entity.n * entity.deathRate # not that we don't recalculate the death rate this time.
            if sumRatesAgain >= randomEvent:
                entity.deathEvent() # execute entity death and update the population.
                # print("individual death")
                break
    
        # Print the outputs.
        if(time >= nextPrint):
            nextPrint += parameters.printInterval
            print("Time:", round(time, 3))
            print("E ent:", Entity.N)
            print("N ind:", round(Individual.N))
            print("M grp:", round(Group.N))

            print("Z ind tot:", round(Individual.Z, 4))
            print("Z grp tot:", round(Group.Z, 4))
            print("Z bar ind:", round(Individual.Z / Individual.N, 4))
            print("Z bar grp:", round(Group.Z  / Group.N, 4))
            print()

            # for group in Group.population:                           
            #     print("Ni:", round(group.individualN, 2))
            #     print("Zi tot:", round(group.individualZ, 2))
            #     print("Zi bar:", round(group.z, 2))
            #     print()    
            print(end = "\n\n")

else: # run the Allen & Dytham (2009) algorithm.

    c = 0
    cb = 0
    cd = 0
    event = True

    for entity in Entity.population: # calculate the initial birth and death rates.
        entity.calcPhenotype()
        entity.calcBirthRate()
        entity.calcDeathRate()

    while time < parameters.tfinal:

        if event == True:
            
            # Step 2 - choose maximum rate constants.
            for entity in Entity.population: 
                if entity.birthRate > cb:
                    cb = entity.birthRate
                if entity.deathRate > cd:
                    cd = entity.deathRate           
            
            event = False
        
        elif event == False:
            
            # Step 3 - sample the time to the next event using an exponential distribution.
            time += -math.log(random.random()) / ((cb + cd) * Entity.N) # exponentially distributed random number.

            # Step 4 & 5 - determine and execute the next event using probabilities birthRate / cb and deathRate / cd, respectively.            
            randomEvent = ""
            if random.random() < cb / (cb + cd):
                randomEvent = "birth"
            else: 
                randomEvent = "death"

            randomEntity = random.random() * Entity.N
            randomEntitySum = 0
            for entity in Entity.population:
                randomEntitySum += entity.n
                if randomEntitySum > randomEntity:
                    # entity.calcPhenotype()
                    if randomEvent == "birth":
                        if random.random() < entity.calcBirthRate() / cb:
                            entity.birthEvent() # execute entity birth and update the population.
                            event = True
                            break             
                    elif randomEvent == "death":
                        if random.random() < entity.calcDeathRate() / cd:
                            entity.deathEvent() # execute entity death and update the population.
                            event = True
                            break 
              
            # Print the outputs.
            if(time >= nextPrint):
                nextPrint += parameters.printInterval
                print("Time:", round(time, 3))
                print("E ent:", Entity.N)
                print("N ind:", round(Individual.N))
                print("M grp:", round(Group.N))

                print("Z ind tot:", round(Individual.Z, 4))
                print("Z grp tot:", round(Group.Z, 4))
                print("Z bar ind:", round(Individual.Z / Individual.N, 4))
                print("Z bar grp:", round(Group.Z  / Group.N, 4))
                print()

                # for group in Group.population:                           
                #     print("Ni:", round(group.individualN, 2))
                #     print("Zi tot:", round(group.individualZ, 2))
                #     print("Zi bar:", round(group.z, 2))
                #     print()    
                # print(end = "\n\n")
