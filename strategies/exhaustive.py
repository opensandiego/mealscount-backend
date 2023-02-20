from .base import BaseCEPStrategy,CEPGroup
from itertools import combinations, chain

class ExhaustiveCEPStrategy(BaseCEPStrategy):
    ''' Grouping strategy is to compute every possible partition

    * This follows with https://en.wikipedia.org/wiki/Partition_of_a_set
    * We limit this to districts with 10 Schools or less

      '''
    name="Exhaustive"
    exposed_options = [
        #('max_count','The largest number of schools',int,10),
        #('evaluate_by','',str,'reimbursement'),
    ]
    def create_groups(self,district):
        # some debugging/optimization required

        # check district size, if over 10 don't calculates partitions
        # bell number of 10 = 115,975 (15 ~ 1.4 bil;  20 ~ 51.7 tril)
        # if over assign groups like OneToOne (this way it can run on all districts without taking a year)
        schools = district.schools
        # Beware, raising this much above 11 makes your RAM go fast 
        max_count = int(self.params.get("max_count",10))
        if len(schools) > max_count:
            self.groups = [
                CEPGroup(district, school.name, [school])
                for school in schools
            ]
        elif len(schools) == 0:
            self.groups = []
        else:
            def partition(collection):
                '''gives the all possible partitions as nested lists'''
                # function straight from stock overflow- seems to work well (search Set partitions in python)
                if len(collection) == 1:
                    yield [collection]
                    return

                first = collection[0]
                for smaller in partition(collection[1:]):
                    # insert `first` in each of the subpartition's subsets
                    for n, subset in enumerate(smaller):
                        yield smaller[:n] + [[first] + subset] + smaller[n + 1:]
                    # put `first` in its own subset
                    yield [[first]] + smaller


            def powerset(iterable):
                ''' gives all possible combinations for group sizes 1 to all groups'''
                s = list(iterable)
                return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))

            # generate all CEPgroup objects for all possible groups
            possible_groups = {}
            for i, g in enumerate(powerset(schools)):
                possible_groups[g] = CEPGroup(district, i, list(g))

            best_grouping = []
            # generate all partions
            d_powerset = [i for i in partition(schools)]
            #print("Powerset for %i contains %i" % (len(schools),len(d_powerset)))

            evaluate_by = self.params.get("evaluate_by","reimbursement")
            best_option = [0,0]

            for x in partition(schools):
                est_reimbursement = sum([ 
                        possible_groups[tuple(group)].est_reimbursement() 
                        for group in x])
                # Just straight reimbursement comparison
                if evaluate_by == "reimbursement":
                    if est_reimbursement > best_option[0]:
                        best_grouping = [ possible_groups[tuple(group)] for group in x ]
                        best_option[0] = est_reimbursement
                # Highest number of covered students, and if equal, higher reimbursement
                elif evaluate_by == "coverage":
                    covered_students = sum([ 
                        possible_groups[tuple(group)].covered_students 
                        for group in x])
                    if covered_students > best_option[0]:
                        best_grouping = [ possible_groups[tuple(group)] for group in x ]
                        best_option = (covered_students,est_reimbursement)
                    elif covered_students == best_option[0]:
                        # If meals are the same, but reimbursement is higher, lets do this new option
                        if est_reimbursement > best_option[1]:
                            best_grouping = [ possible_groups[tuple(group)] for group in x ]
                            best_option = (covered_students,est_reimbursement)
                # highest number of included schools, and if equal, higher reimbursement
                elif evaluate_by == "schools":
                    schools = sum([    len(possible_groups[tuple(group)].schools) 
                                        for group in x 
                                        if possible_groups[tuple(group)].cep_eligible ])
                    if schools > best_option[0]:
                        best_grouping = [ possible_groups[tuple(group)] for group in x ]
                        best_option = (schools,est_reimbursement)
                    elif schools == best_option[0]:
                        # If meals are the same, but reimbursement is higher, lets do this new option
                        if est_reimbursement > best_option[1]:
                            best_grouping = [ possible_groups[tuple(group)] for group in x ]
                            best_option = (schools,est_reimbursement)

            self.groups = best_grouping

