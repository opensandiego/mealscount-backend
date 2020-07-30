from ortools.linear_solver import pywraplp
import pandas as pd
from typing import Any, Dict, Tuple

# Package imports
from .base import BaseCEPStrategy, CEPDistrict, CEPGroup

pd.options.mode.chained_assignment = None


class _LPOptimizer:
    """Runs a greedy linear programming optimizer to group schools together within a district.
    
    Parameters
    ----------
    target_isp : float
        Target group ISP.
        
    minimum_isp : float
        Minimum group ISP.

    free_breakfast : float
        Free breakfast rate.
        
    paid_breakfast : float
        Paid breakfast rate.
        
    free_lunch : float
        Free lunch rate.
        
    paid_lunch : float
        Paid lunch rate.
    """
    def __init__(self, 
                 *,
                 target_isp: float, 
                 minimum_isp: float,
                 free_breakfast: float,
                 paid_breakfast: float,
                 free_lunch: float,
                 paid_lunch: float) -> None:
        self.target_isp     = target_isp
        self.minimum_isp    = minimum_isp
        self.free_breakfast = free_breakfast
        self.paid_breakfast = paid_breakfast
        self.free_lunch     = free_lunch
        self.paid_lunch     = paid_lunch
    
    def _create_data_model(self, 
                           *,
                           df: pd.DataFrame, 
                           bin_size: int) -> Dict[str, Any]:
        """Creates data model for optimizer.
        
        Parameters
        ----------
        df : pandas DataFrame
            Input data.
            
        bin_size : int
            Maximum number of items that can go into a bin at each run.
        
        Returns
        -------
        dict
            Key/value pairs containing data elements for optimizer and the results.
        """
        n    = df.shape[0]
        data = {}
        
        # Package data
        data['num_items']      = n
        data['items']          = list(range(n))
        data['bins']           = [0]
        data['bin_capacities'] = [bin_size]
        data['weights']        = [1] * n
        data['values']         = [1] * n
        data['school_name']    = df['school_name'].tolist()
        data['total_enrolled'] = df['total_enrolled'].tolist()
        data['total_eligible'] = df['total_eligible'].tolist()
        data['isp']            = df['isp'].tolist()
        
        return data

    def _build_solver(self, 
                      *,
                      df: pd.DataFrame, 
                      bin_size: int) -> Tuple[Dict[str, Any], Dict[str, Any], Any, Any]:
        """Build solver.
        
        Parameters
        ----------
        df : pandas DataFrame.
            Input data.
            
        bin_size : int
            Size of bins.
        
        Returns
        -------
        data : dict
            Data model.
        
        x : dict
            Variables for solver.
            
        solver : pywraplp.Solver
            Instantiated linear solver.
            
        objective : pywraplp.Solver.Objective
            Instantiated objective function.
        """
        # Define data model
        data = self._create_data_model(df=df, bin_size=bin_size)
        
        # Solver and variables
        solver = pywraplp.Solver('multiple_knapsack_mip', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        x      = {}
        for i in data['items']:
            x[(i, 0)] = solver.IntVar(0, 1, f"x_{i}_0")
                        
        # 1. ISP constraint lower bound: Group ISP >= target_isp
        solver.Add(
            sum(data['total_eligible'][i] * x[i, 0] for i in data['items']) >= 
            sum(data['total_enrolled'][i] * x[i, 0] for i in data['items']) * self.minimum_isp
            )
        
        # 2. ISP constraint upper bound: Group ISP <= target_isp
        solver.Add(
            sum(data['total_eligible'][i] * x[i, 0] for i in data['items']) <= 
            sum(data['total_enrolled'][i] * x[i, 0] for i in data['items']) * self.target_isp
            )
        
        # 3. The amount packed in each bin cannot exceed its capacity.
        solver.Add(
            sum(x[(i, 0)] * data['weights'][i] for i in data['items']) <= data['bin_capacities'][0]
            )
        
        # Set objective and solve
        objective = solver.Objective()
        for i in data['items']:
            objective.SetCoefficient(x[(i, 0)], data['isp'][i])
        objective.SetMaximization()
        
        return data, x, solver, objective

    def _calculate_reimbursement(self, 
                                 *,
                                 df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate reimbursement based on optimized groupings.
        
        Parameters
        ----------
        df : pandas DataFrame 
            Input data with groups.
        
        Returns
        -------
        dict
            Key/value pairs containing groupings and reimbursements.
        """
        # Calculate group ISP
        group_isp = df\
                     .groupby('group')\
                     .apply(lambda x: sum(x['total_eligible']) / sum(x['total_enrolled']))\
                     .reset_index()\
                     .rename({0: 'group_isp'}, axis='columns')
        df        = df.merge(group_isp, on='group', how='inner')
        
        # CEP calculations
        df_cep        = df.groupby(['group', 'group_isp'], as_index=False).sum()
        df_cep['isp'] = df_cep['group_isp'].apply(lambda x: min(1, x * 1.6))
        
        # CEP breakfast
        df_cep['yearly_breakfast_ct']     = df_cep['daily_breakfast_served'] * 180
        df_cep['reimbursement_breakfast'] = df_cep['yearly_breakfast_ct'] * \
                                             (self.free_breakfast * df_cep['isp'] + 
                                              self.paid_breakfast * (1 - df_cep['isp']))
        # CEP lunch
        df_cep['yearly_lunch_ct']     = df_cep['daily_lunch_served'] * 180
        df_cep['reimbursement_lunch'] = df_cep['yearly_lunch_ct'] * \
                                         (self.free_lunch * df_cep['isp'] + 
                                          self.paid_lunch * (1 - df_cep['isp']))
        
        # Total CEP reimbursement
        df_cep['reimbursement_total'] = df_cep['reimbursement_breakfast'] + df_cep['reimbursement_lunch']
        
        # Groupings with ISP < minimum ISP, reimbursement is set to 0
        mask                   = df_cep['group_isp'] < self.minimum_isp
        cols                   = ['reimbursement_breakfast', 'reimbursement_lunch', 'reimbursement_total']
        df_cep.loc[mask, cols] = 0.0

        # Join back results to original df
        df = df.merge(df_cep['group'], on='group')

        return {
            'df'            : df[['school_name', 'school_code', 'group', 'group_isp']],
            'reimbursement' : df_cep['reimbursement_total'].sum(),
        }

    def _run_configuration(self, 
                           *, 
                           df: pd.DataFrame,
                           bin_size: int,
                           ) -> Dict[str, Any]:
        """Run optimization for bin size.
        
        Parameters
        ----------
        df : pandas DataFrame
            Input data.
            
        bin_size : int
            Maximum number of items that can go into a bin at each run.
        
        Returns
        -------
        dict
            Key/value pairs containing groupings and reimbursements.
        """
        results     = []
        df          = df.copy()
        group_id    = 1
        
        r = 1
        while True:
            data, x, solver, objective = \
                self._build_solver(df=df, bin_size=bin_size)
            
            # Run solver and parse solution
            status   = solver.Solve()            
            solution = status == pywraplp.Solver.OPTIMAL
            if solution:
                # No grouping found, stop optimization
                if objective.Value() == 0:
                    break
                else:
                    # Keep solution
                    idx_bin           = [i for i in data['items'] if x[i, 0].solution_value() > 0]
                    df_group          = df.iloc[idx_bin]
                    df_group['group'] = group_id
                    results.append(df_group)
                    group_id += 1
                        
                    # Remove these rows from dataframe before next round of optimization
                    if idx_bin:
                        df = df.drop(idx_bin, axis='rows').reset_index(drop=True)
                
                    # Data check
                    if df.shape[0] <= 1:
                        break
                    
                r += 1
            
            else:
                break

        # Package up solution
        solution = None
        if results:
            solution = self._calculate_reimbursement(df=pd.concat(results, axis=0))
        
        return solution

    def solve(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Run iterative optimization.
        
        Parameters
        ----------
        df : pandas DataFrame
            Input data.
        
        Returns
        -------
        dict
            Key/value pairs with best solution from optimization.
        """
        n = df.shape[0]
        
        # Run a fixed number of bin sizes ~ 100 bin sizes if possible
        bin_sizes = sorted(
            list(set([int(2 + x * (n - 2)/(100 - 1)) for x in range(100)]))
            )
        
        if n > 1000:
            bin_sizes = list(filter(lambda x: x > 20, bin_sizes))

        # Initialize best results
        best = {
            'reimbursement' : -1e20,
            'df'            : None,
            'bin_size'      : None
        }
        
        # Run configuration based on bin size
        for j, bin_size in enumerate(bin_sizes, 1):
            solution = self._run_configuration(df=df, bin_size=bin_size)
            if solution is not None:
                reimbursement = solution['reimbursement']
                if reimbursement > best['reimbursement']:
                    best['reimbursement'] = float(reimbursement)
                    best['df']            = solution['df']
                    best['bin_size']      = int(bin_size)
        
        return best


class GreedyLPStrategy(BaseCEPStrategy):
    """Greedy linear programming optimizer to group schools together within a district.
    """
    name = "GreedyLP"

    def create_groups(self, district: CEPDistrict) -> None:
        """Runs optimizer to find school groupings within a school district.
        
        Parameters
        ----------
        district : CEPDistrict
            CEP District of schools.
        
        Returns
        -------
        None
        """
        # Prepare data structures
        df    = pd.DataFrame(list(map(lambda x: x.as_dict(), district.schools)))
        rates = district.fed_reimbursement_rates
        
        # Drop schools with duplicate school codes
        df = df.iloc[df['school_code'].drop_duplicates().index]\
               .reset_index(drop=True)
        
        # Run solver        
        solution = _LPOptimizer(target_isp=0.625,
                                minimum_isp=0.400,
                                free_breakfast=rates['free_bfast'],
                                paid_breakfast=rates['paid_bfast'],
                                free_lunch=rates['free_lunch'],
                                paid_lunch=rates['paid_lunch']).solve(df=df)
        df_group = solution['df']
        
        # If no solution found, just fall back to Singleton-Group
        # Optimizer failed most likely due to small sample size (n <= 10) or school ISPs too low to
        # satisfy mathematical constraints
        if df_group is None:
            self.groups = [CEPGroup(district, "Singleton-Group", district.schools)]
            return

        # Pack groupings into CEP data structure
        self.groups = []
        available   = district.schools.copy()
        for group_id in solution['df']['group'].unique():
            # Get codes of current grouped schools
            group_codes = df_group[df_group['group'] == group_id]['school_code'].tolist()
            
            # Package schools together
            selected = []
            for code in group_codes:
                school = next(filter(lambda x: x.code == code, district.schools), None)
                if school is not None:
                    selected.append(school)
                    available.pop(available.index(school))
            
            # Create CEPGroup group
            self.groups.append(
                CEPGroup(district, group_name=f"Group-{group_id}", schools=selected)
            )
        
        # If any schools leftover, then place in a single CEPGroup
        if len(available):
            self.groups.append(
                CEPGroup(district, group_name=f"Not Selected", schools=available)
            )
            