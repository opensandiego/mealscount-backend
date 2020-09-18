# Strategy based on NYC Mayors Office of Data Analytics  "Free Lunch for All"
# https://moda-nyc.github.io/Project-Library/projects/free_lunch_for_all/
from .base import BaseCEPStrategy,CEPGroup
import multiprocessing as mp
import pandas as pd
import numpy as np
import time
from random import randint,sample,random,seed

SCHOOL_YEAR = 180
MULTIPLIER = 1.6
T_MIN = 0.40 * MULTIPLIER

class NYCMODASimulatedAnnealingCEPStrategy(BaseCEPStrategy):
    '''NYC MODA Simulated Annealing  '''
    name = "SimulatedAnnealing"

    def create_groups(self,district):
        self.debug = self.params.get("step_debug",False)
        # Use a seed to get consistent results
        seed( int(self.params.get("seed", 42 )))


        if self.params.get("original",False):
            self.do_nycmoda(district)
        elif len(district.schools) > 10: # less than 10 we do exhaustive
            self.groups = self.simplified(
                district,
                clear_groups = self.params.get("clear_groups",False),
                consolidate_groups = self.params.get("regroup",False),
                fresh_starts = int(self.params.get("fresh_starts",10)),
                iterations = int(self.params.get("iterations", 150)),
                ngroups = self.params.get("ngroups",None) and int(self.params.get("ngroups",None)) or None,
                evaluate_by = self.params.get("evaluate_by","reimbursement"),
            )
            # prune 0 school groups since we don't need to report them
            self.groups = [g for g in self.groups if len(g.schools) > 0]
        else:
            self.groups = [ CEPGroup(district,"OneGroup",[ s for s in district.schools ]) ]

        return self.groups

    def simplified( self,
                    district,
                    clear_groups=False,
                    consolidate_groups=False,
                    iterations = 1000,
                    fresh_starts = 1,
                    ngroups = None,
                    evaluate_by = "reimbursement",
                    ):
        '''Attempt at streamlining algorithm by skipping pandas'''
        if len(district.schools) <= 3: return None  # safeguard some assumptions

        TFactor = self.params.get("tfactor",100000)
        use_annealing = int(self.params.get("annealing",0))
        deltaT = float(self.params.get("delta_t",0.1))

        def random_start(district,ngroups=None):
            if not ngroups:
                ng = randint(2,len(district.schools)-1)
            else:
                ng = randint(2,ngroups)
            groups = [CEPGroup(district,"Group %i" % i,[]) for i in range(ng)]
            for s in district.schools:
                groups[randint(0,ng-1)].schools.append(s)
            for g in groups: g.calculate() 

            # prune empty groups. assignment is random
            groups = [g for g in groups if len(g.schools) > 0]
            return groups

        def step(groups,T):
            # Get 2 random groups
            if len(groups) <= 2:
                return
            
            g1,g2 = sample(groups,2)
            if len(g1.schools) == 0 and len(groups) == 2:
                #print("Cannot evaluate")
                return

            while len(g1.schools) == 0:
                g1,g2 = sample(groups,2)

            # track our starting reimbursement total of both groups
            start_r = round(g1.est_reimbursement() + g2.est_reimbursement())
            start_c = round(g1.covered_students + g2.covered_students)
            start_s = (g1.cep_eligible and 1 or 0) +  (g2.cep_eligible and 1 or 0)
            start_f = ( g1.free_rate == 1.0 and 1 or 0) + ( g2.free_rate == 1.0 and 1 or 0 )
   
            # remove random school from g1, add to g2, and recalculate
            s = g1.schools.pop(randint(0,len(g1.schools)-1))
            g2.schools.append(s)
            g1.calculate()
            g2.calculate()

            passing = False # Whether or not we persist this change
            # This depends on what we are optimizing for
            # TODO maybe assign this as a function to speed up?

            step_r = round(g1.est_reimbursement() + g2.est_reimbursement())

            # The original NYCMODA does this as a raw change in reimbursement
            # but this really produces worse results since our values are much smaller
            # (not NYC and daily not Annual for total). I try to compensate by normalizing
            # to starting reimbursement, but this still produces worse results.. 
            # TODO figure out what probability function and parameters work to utilize simualted annealing
            # https://en.wikipedia.org/wiki/Simulated_annealing
            step_temp = (start_r > 0 and (step_r - start_r)/start_r or -0.01) * TFactor

            if evaluate_by == "reimbursement":
                # our new reimbursement
                passing = step_r > start_r

            elif evaluate_by == "coverage":
                step_c = round(g1.covered_students + g2.covered_students)
                passing = step_c > start_c
            elif evaluate_by == "schools":
                step_s = (g1.cep_eligible and 1 or 0) +  (g2.cep_eligible and 1 or 0)
                if start_s < step_s:
                    passing = True
                elif start_s == step_s and step_r > start_r:
                    passing = True
            elif evaluate_by == "schools_free": 
                # max schools at 100% free and highest reimbursement (ask by SCUSD)
                step_f = ( g1.free_rate == 1.0 and 1 or 0) + ( g2.free_rate == 1.0 and 1 or 0 )
                if start_f < step_f:
                    passing = True
                elif start_f == step_f and step_r > start_r:
                    passing = True
                
            # undo if we have gone down, and return False
            # given that the different in change in reimbursement wildly varies amongst districts
            if not passing or (use_annealing and random() < np.exp( step_temp/T)):
                s = g2.schools.pop()
                g1.schools.append(s)
                g1.calculate()
                g2.calculate()
                return False
            else:
                pass
                #print("up +%0.2f" % (step_r - start_r) )

            # Return true if we had a saved changed
            return True

        def regroup(groups):
            reduced = {} 
            # Consolidate by isp to 1%
            for g in groups:
                r_isp = round(g.isp,2)
                reduced.setdefault( r_isp, [] )

        # TODO allow self.params.get('cores',1) to trigger multiprocessing
        # Although if we do that here, do we need to re-seed random?
        overall = 0
        best_grouping = None
        for i in range(fresh_starts):
            groups = random_start(district,ngroups)

            if self.debug:
                for g in groups:
                    print("%s: %s" % (g.name,",".join([s.code for s in g.schools]))) 

            for T in np.arange(1,0,-deltaT):
                for i in range(iterations):
                    if self.debug:
                        print("%i\t$%0.0f" % (i,sum([g.est_reimbursement() for g in groups])))
                        print("\t"," ".join( [ '*'*len(g.schools) for g in groups]))
                    changed = step(groups,T) 
                    if changed == None:
                        break # If we have hit a point where we can no longer shuffle, stop our iterations short
                    if changed and clear_groups:
                        groups = [g for g in groups if len(g.schools) > 0]
                    if self.debug:
                        print("\t"," ".join( [ '*'*len(g.schools) for g in groups]), changed and "Keep" or "Discard")
                        print("\t => $%0.0f" % (sum([g.est_reimbursement() for g in groups])))
            latest = sum([g.est_reimbursement() for g in groups])
            if latest >= overall:
                overall = latest
                best_grouping = groups

        return best_grouping 

    def do_nycmoda(self,district):
        cep = self.dataframe_from_district(district)

        # run and output
        print("Running on ",cep)
        reimb, cep = self.simulated_annealing(
            cep, 
            Tmax=1,
            deltaT=.01, 
            n_runs = int(self.params.get("runs",1000)), 
            ngroups = int(self.params.get("groups",10)),
            regroup = self.params.get("regroup",False),
        )

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
                        ngroupstart=1,ngroups=10, Tmax=1, deltaT=0.1, n_runs=1000, regroup=True):
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
            for i in range(n_runs):
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

        if regroup:
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