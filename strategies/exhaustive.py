from .base import BaseCEPStrategy,CEPGroup

class ExaustiveCEPStrategy(BaseCEPStrategy):
    ''' Grouping strategy is to compute every possible partition

    * This follows with https://en.wikipedia.org/wiki/Partition_of_a_set
    * We first calculate the Bell Number, as we don't want to break your computer
    https://en.wikipedia.org/wiki/Bell_number  

      '''
    name="Exhaustive"
    def create_groups(self,district):
        # some debugging/optimization required

        # check district size, if over 10 don't calculates partitions
        # bell number of 10 = 115,975 (15 ~ 1.4 bil;  20 = 51.7 tril)
        # if over assign groups like OneToOne (this way it can run on all districts without taking a year)
        if len(district.schools) > 10:
            self.groups = [
                CEPGroup(school.district,school.name,[school])
                for school in district.schools
            ]
        else:
            def partition(collection):
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

            best_grouping = []
            best_covered = 0
            # generate all partions
            for x in partition(district.schools):
                # save grouping with highest num of covered students
                grouping = []
                students_covered = 0
                for i, group in enumerate(x):
                    grouping.append(CEPGroup(district, i, group))
                    students_covered += grouping[i].covered_students
                if students_covered > best_covered:
                    best_grouping = grouping
                    best_covered = students_covered
            self.groups = best_grouping

