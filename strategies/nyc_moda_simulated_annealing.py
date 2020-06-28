# Strategy based on NYC Mayors Office of Data Analytics  "Free Lunch for All"
# https://moda-nyc.github.io/Project-Library/projects/free_lunch_for_all/
from .base import BaseCEPStrategy,CEPGroup
import multiprocessing as mp
import pandas as pd
import numpy as np
import time

SCHOOL_YEAR = 180
MULTIPLIER = 1.6
T_MIN = 0.40 * MULTIPLIER

class NYCMODASimulatedAnnealingCEPStrategy(BaseCEPStrategy):
    '''NYC MODA Simulated Annealing  '''
    name = "SimulatedAnnealing"

    def create_groups(self,district):
        cep = self.dataframe_from_district(district)

        # run and output
        print("Running on ",cep)
        reimb, cep = self.simulated_annealing(cep, Tmax=1,deltaT=.01)
        self.setThreshold(cep)

        # The "thresholds" are the groups
        self.groups = []
        for g in cep.groupby('threshold'):
            self.groups.append(CEPGroup(
                district,
                "threshold %s" % g[0],
                [ s for s in district.schools if s.code in g[1]["School"].to_numpy()]
            ))

    def dataframe_from_district(self,district):

        freeLunch = district.fed_reimbursement_rates['free_lunch']
        paidLunch = district.fed_reimbursement_rates['paid_lunch']
        freeBreakfast = district.fed_reimbursement_rates['free_bfast']
        paidBreakfast = district.fed_reimbursement_rates['paid_bfast']

        deltaLunchRate = freeLunch - paidLunch
        deltaBreakfastRate = freeBreakfast - paidBreakfast 
        
        cep = pd.DataFrame([
            {
                "School":s.code, 
                "Enrollment":s.total_enrolled, 
                "Identified": s.total_eligible, 
                "Breakfast": s.bfast_served * SCHOOL_YEAR, 
                "Lunch": s.lunch_served * SCHOOL_YEAR,
            }
            for s in district.schools
        ])

        cep.reset_index(inplace=True)

        cep['meal'] = deltaLunchRate*cep['Lunch'] + deltaBreakfastRate*cep['Breakfast']
        cep['paidMeal'] = paidLunch*cep['Lunch'] + paidBreakfast*cep['Breakfast']
        cep['mealPerStudent'] = cep['meal']/cep['Enrollment']
        cep['baseThreshold'] = cep['Identified']/cep['Enrollment']*MULTIPLIER
        cep['group'] = 0
        cep.head()

        return cep

    # reimbursements over the base, this is the part that's dependant on groupings
    def calcReimburse(self,cep,cost=0):
        ''' calculates and returns the total reimbursments (above base) for schools in a particlar grouping 
        Parameters:
        cep: dataframe where each row is a school. cep columns include: Identified, Enrollment, meal, group
        cost: cost = 0 (default) no cost to dropping schools from the program
              cost = 1 sets a high penalty for letting a group go below the min threshold'''

        group_cep = cep.groupby('group')
        df = pd.DataFrame(index= group_cep.indices) #each row represents a group

        df['threshold'] =  (group_cep['Identified'].sum()  / group_cep['Enrollment'].sum()) * MULTIPLIER
        df['meal']      =  group_cep['meal'].sum()

        # enforcing threshold rules:
        df['applied_threshold'] = df['threshold']
        df.loc[df['applied_threshold']  > 1, 'applied_threshold'] = 1
        df.loc[df['applied_threshold']  < T_MIN,'applied_threshold'] = 0 - cost*10**6

        df['reimbursed'] = df['applied_threshold'] * df['meal']

        return df.reimbursed.sum()

    def setThreshold(self,cep):
        ''' calculates the threshold for each school based on its group
            cep columns: Enrollment, Identified'''
        for i in set(cep.group):
            df = cep[cep.group==i]
            cep.loc[cep.group == i,'threshold'] = df['Identified'].sum() / float(df['Enrollment'].sum()) * MULTIPLIER
        return 0

    # Direct from the MODA Jupyter Notebook 
    def simulated_annealing(self,cep, randomstart=True, seed=None,
                        ngroupstart=1,ngroups=10, Tmax=1, deltaT=0.1):
        '''simulated annealing procedure - finding optimal grouping
        cep: schools dataframe
        randomstart: if False start with groups already set in group column, otherwise
                     if True (default) start by randomly assigning groups 
        seed: seed for random generator
        ngroupstart: integer number of groups in the random start
        ngroups: number of groups
        Tmax: max value for "temperature"
        deltaT: change in "temperature" at each step

        returns a list of reimbursements at each step and the dataframe with the final groupings
        '''

        startTime = time.time()
        print("Starting")
        cep.reset_index(drop=True,inplace=True) 
        rows=cep.shape[0]

        # start by grouping schools randomly
        if randomstart:
            np.random.seed(seed)
            cep.loc[:,'group'] = pd.Series(np.random.randint(0,ngroupstart,size=rows),
                                           index=cep.index)

        # store the results
        old = self.calcReimburse(cep)
        results=[old]

        # mc loop
        for T in np.arange(Tmax,0,-deltaT):
            for i in range(1000):
                df = cep.copy()

                # choose a random school and move it to a different random group
                df.loc[np.random.randint(0,rows),'group'] = np.random.randint(0,ngroups)

                # calculate the reimbursement
                new = self.calcReimburse(df,cost=1)
                step = new - old                                                                           

                #keep move if reimbursement increases
                if (step > 0):
                    old=new
                    cep.loc[:,'group'] = df.group
                    results.append(new)

                #maybe keep move if reimbursement decreases, depending on how much
                elif (np.random.uniform() < np.exp(step/T)):
                    old=new
                    cep.loc[:,'group'] = df.group
                    results.append(new)

        cep = self.regroup(cep) #combining groups close by
        final = self.calcReimburse(cep)
        results.append(final)

        print("Final Reimbursement",final)
        print("%0.2f minutes" % ((time.time()-startTime)/60.0) )
        return results,cep

    def regroup(self,cep):
        '''if cep has multiple thresholds within one percent of each other, this 
        combines them'''
        self.setThreshold(cep)
        tlist = cep.groupby(cep.threshold.apply(lambda x: round(x,2))).groups.keys()
        for i,t in enumerate(tlist):
            cep.loc[cep.threshold.apply(lambda x:round(x,2))==t,'group']=i
        self.setThreshold(cep)
        return cep

    def sa_ensemble(self,cep,trials=10,randomstart=True,ngroupstart=1,ngroups=10,Tmax=1,deltaT=.1):
        '''run simulated annealing a number of times (trials) and choose the best 
        (highest reimbursement) as the final'''
        pool = mp.Pool(processes=10) # parrallel over 4 cores
        results = [pool.apply_async(self.simulated_annealing,
                                    args=(cep,)) for x in range(trials)]
        results = [p.get() for p in results]
        print(results)

        reimb_ensemble = [results[i][0][-1] for i in range(trials)]
        cep_ensemble = [results[i][1] for i in range(trials)]

        max_reimb = max(reimb_ensemble)
        max_index = reimb_ensemble.index(max_reimb)

        return cep_ensemble[max_index]