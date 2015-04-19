# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """    

#
# PROBLEM 1
#

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        if type(maxBirthProb) != float or type(clearProb) != float:
            raise ValueError('maxBirthProb and clearProb should be a float')
        elif maxBirthProb < 0 or maxBirthProb > 1 or clearProb < 0 or clearProb > 1:
            raise ValueError('maxBirthProbs and clearProbs value should be between 0 and 1')
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        
    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        if random.random() <= self.clearProb:
            return True
        else:
            return False
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() <= (self.maxBirthProb * (1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else: 
            raise NoChildException()

class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):
        """
        Gets the current total virus population. 

        returns: The total virus population (an integer)
        """
        return len(self.viruses)   

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: the total virus population at the end of the update (an
        integer)
        """
        #decision for every virus instances, and deleting the unlucky ones
        mutableViruses = self.viruses.copy()
        deleteViruses = []
        for vir in mutableViruses:
            if vir.doesClear():
                self.viruses.remove(vir)
        #calculating population density
        popDensity = (len(self.viruses) / self.maxPop)
        mutableViruses = self.viruses.copy()
        for vir in mutableViruses:
            try:
                self.viruses.append(vir.reproduce(popDensity))
            except NoChildException:
                pass
        return self.getTotalPop()


#
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    virusPopOverTime = []
    startingVirusPopulation = []
    for i in range(100):
        startingVirusPopulation.append(SimpleVirus(0.1, 0.05))
    badLuckBrian = SimplePatient(startingVirusPopulation, 1000)
    for j in range(300):
        virusPopOverTime.append(badLuckBrian.update())
    pylab.plot(virusPopOverTime)
    pylab.title('Change of total virus population over time')
    pylab.xlabel('Time')
    pylab.ylabel('Number of viruses')
    pylab.show()

    
#
# PROBLEM 3
#

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """    
    
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        
        """
        if type(maxBirthProb) == float and 0 < maxBirthProb < 1 and (type(clearProb) == float) and 0 < clearProb < 1:
            self.maxBirthProb = maxBirthProb
            self.clearProb = clearProb
        else:
            raise ValueError('maxBirthProbs and clearProbs are float and their values should be between 0 and 1')
        if type(resistances) == dict:
            self.resistances = resistances
        else:
            raise ValueError('resistances should be a dictionary')
        if type(mutProb) == float and 0 < mutProb < 1:
            self.mutProb = mutProb
        
    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.resistances.keys() and self.resistances[drug] == True:
            return True
        else:
            return False
        
    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        #list of drugs the virus has resistance to
        rsa = []
        for drug in self.resistances.keys():
            if self.resistances[drug] == True:
                rsa.append(drug)
        #check for resistance fro currently used drugs
        if len(activeDrugs) != 0:
            chance = len(set(rsa) & set(activeDrugs))
        else:
            chance = 1
        #check if we should replicate
        if random.random() < self.maxBirthProb * (1- popDensity):
            secChance = True
        else:
            secChance = False
        #replication
        if secChance and chance != 0:
            resistances = {}
            for drug in self.resistances.keys():
                if random.random() < (1 - self.mutProb):
                    resistances[drug] = self.resistances[drug]
                else:
                    resistances[drug] = not self.resistances[drug]
            return ResistantVirus(self.maxBirthProb, self.clearProb, resistances, self.mutProb)
        else:
            raise NoChildException()
            
class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []
        
    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugs
        
    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        thePop = 0
        for virus in self.viruses:
            resForSmg = False
            for drug in drugResist:
                if virus.getResistance(drug):
                    resForSmg = True
            if resForSmg:
                thePop += 1
        return thePop

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly
          
        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        #decision for every virus instances, and deleting the unlucky ones
        mutableViruses = self.viruses[:]
        for vir in mutableViruses:
            if vir.doesClear():
                self.viruses.remove(vir)
        #calculating population density
        popDensity = (len(self.viruses) / self.maxPop)
        mutableViruses = self.viruses[:]
        for vir in mutableViruses:
            try:
                self.viruses.append(vir.reproduce(popDensity, self.getPrescriptions()))
            except NoChildException:
                pass
        return self.getTotalPop()

#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    resPopOvertime = []
    virusPopOverTime = []
    startingVirusPopulation = []
    for i in range(100):
        startingVirusPopulation.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))
    badLuckBrian = Patient(startingVirusPopulation, 1000)

    for j in range(150):
        virusPopOverTime.append(badLuckBrian.update())
        resPopOvertime.append(badLuckBrian.getResistPop(['guttagonol']))
    badLuckBrian.addPrescription('guttagonol')
    for j in range(150):
        virusPopOverTime.append(badLuckBrian.update())
        resPopOvertime.append(badLuckBrian.getResistPop(['guttagonol']))
        
    pylab.plot(virusPopOverTime, label = 'Total')
    pylab.plot(resPopOvertime, color = 'g', label = 'Resistant viruses')
    pylab.legend()
    pylab.title('Change of total advanced virus population over time')
    pylab.xlabel('Time')
    pylab.ylabel('Number of viruses')
    pylab.show()


#
# PROBLEM 5
#
        
def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    tbh = []
    delays = [0, 75, 150, 300]
    #do the test for each dealy
    for test in range(len(delays)):
        avg = []
        #repeat each test for 100 times, to get the average sometime in the future
        for reh in range(200):
            #initiate viruses
            startingVirusPopulation = []
            for i in range(100):
                startingVirusPopulation.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))
            #initate patient
            badLuckBrian = Patient(startingVirusPopulation, 1000)
            virpop = 0
            #run the simulation without treatment
            for i in range(delays[test]):
                virpop = badLuckBrian.update()
            #initiate treatment
            badLuckBrian.addPrescription('guttagonol')
            #run the simulation with treatment
            for j in range(150):
                virpop = badLuckBrian.update()
            avg.append(virpop)
        #create the histogram
        pylab.figure()
        pylab.hist(avg)
        hititle = '200 patients, drug administered with ' + str(delays[test]) + 'cycles delay'
        pylab.title(hititle)
        pylab.xlabel('Total virus populations')
        pylab.ylabel('Number of patients')
    #draw the histogram
    pylab.show()

#
# PROBLEM 6
#

def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    befAdDrug = [300, 150, 75, 0]
    for i in range(len(befAdDrug)):
        avg = []
        for k in range(30):
            #initiate startin virus population
            startingVirusPopulation = []
            for l in range(100):
                startingVirusPopulation.append(ResistantVirus(0.1, 0.05, {'guttagonol':False, 'grimpex':False}, 0.005))
            #initiate patient
            badLuckBrian = Patient(startingVirusPopulation, 1000)
            virpop = 0
            #run the simulation for 150 time step
            for j in range(150):
                    virpop = badLuckBrian.update()
            #administer guttagonol for the patient
            badLuckBrian.addPrescription('guttagonol')
            #delay
            for j in range(befAdDrug[i]):
                virpop = badLuckBrian.update()
            #administer the second drug (grimpex)
            badLuckBrian.addPrescription('grimpex')
            #run the simulation for additional 150 steps
            for j in range(150):
                    virpop = badLuckBrian.update()
            avg.append(virpop)
         #create the histogram
        pylab.figure()
        pylab.hist(avg)
        hititle = 'Delay: '+ str(befAdDrug[i])
        pylab.title(hititle)
        pylab.xlabel('Total virus populations')
        pylab.ylabel('Number of patients')
    #draw the histogram
    pylab.show()

problem6()